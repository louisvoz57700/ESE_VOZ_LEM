# ============================================================
# TP TNA – SRC MULTI-ÉTAGES PROPRE (x160 / ÷147)
# ============================================================
import sounddevice as sd
import numpy as np
import scipy.io
import scipy.signal
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ============================================================
# 0. CONFIGURATION
# ============================================================
chemin = "/Users/louisvoz/Desktop/Annee 2025-2026/S9/TNA/TP/TNA-TP/playback_44100.mat"

Fs_in = 44100
VIEW_DURATION_S = 10
ZOOM_OFFSET_MS = 2000
ZOOM_WIDTH_MS = 100

# Bande audio à préserver
AUDIO_BAND_HZ = 20000

# SRC global
L_total = 160
M_total = 147

# Étages SRC (produit = 160 / 147)
stages = [
    {"L": 5, "M": 7},
    {"L": 8, "M": 7},
    {"L": 4, "M": 3},
]

# Filtres
numtaps = 200
beta = 8.0

# ============================================================
# 1. FONCTION D’AFFICHAGE
# ============================================================
def plot_diapo(sig, Fs, title, step,
               color='tab:blue', full_view=False, zoom_freq_max=None):

    if len(sig) == 0:
        return

    N = len(sig)
    t = np.arange(N) / Fs

    fft_N = min(N, 2**19)
    f = np.fft.rfftfreq(fft_N, 1/Fs)
    S = np.fft.rfft(sig[:fft_N])
    mag = 20*np.log10(np.abs(S) + 1e-12)

    peak = np.max(mag)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    plt.suptitle(f"DIAPO {step} – {title}", fontweight='bold')

    # ----- TEMPOREL -----
    if full_view:
        ax1.plot(t, sig, linewidth=0.5, color=color)
        ax1.set_xlim(0, VIEW_DURATION_S)

        rect = patches.Rectangle(
            (ZOOM_OFFSET_MS/1000, np.min(sig)),
            ZOOM_WIDTH_MS/1000,
            np.max(sig)-np.min(sig),
            edgecolor='r', facecolor='none', linewidth=1.2
        )
        ax1.add_patch(rect)
    else:
        i0 = int(ZOOM_OFFSET_MS/1000 * Fs)
        i1 = i0 + int(ZOOM_WIDTH_MS/1000 * Fs)
        ax1.plot(t[i0:i1]*1000, sig[i0:i1], '.-', color=color)

    ax1.set_ylabel("Amplitude")
    ax1.grid(True)

    # ----- FRÉQUENTIEL -----
    ax2.plot(f, mag, color=color)
    ax2.set_ylim(peak-130, peak+10)
    ax2.set_ylabel("Amplitude (dB)")
    ax2.set_xlabel("Fréquence (Hz)")
    ax2.grid(True)

    if zoom_freq_max:
        ax2.set_xlim(0, zoom_freq_max)
    else:
        ax2.set_xlim(0, Fs/2)

    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.show()


# ============================================================
# 2. CHARGEMENT DU SIGNAL
# ============================================================
print("Chargement du signal...")

samples = int(Fs_in * VIEW_DURATION_S)
try:
    mat = scipy.io.loadmat(chemin)
    key = next(k for k in mat if not k.startswith("_"))
    signal_in = mat[key].squeeze()[:samples]
except:
    print("⚠️ Signal synthétique")
    t = np.arange(samples)/Fs_in
    signal_in = (
        0.6*np.sin(2*np.pi*440*t)
      + 0.3*np.sin(2*np.pi*8000*t)
    )

plot_diapo(signal_in, Fs_in, "Signal original – global", 1, full_view=True)
plot_diapo(signal_in, Fs_in, "Signal original – zoom", 2)

# ============================================================
# 3. SRC MULTI-ÉTAGES (PROPRE)
# ============================================================
print("SRC multi-étages...")

sig = signal_in
Fs = Fs_in
sd.play(sig, Fs)

for i, st in enumerate(stages, start=1):
    L = st["L"]
    M = st["M"]

    print(f"Étage {i} : ×{L} / ÷{M}")

    # ---- UPSAMPLING ----
    up = np.zeros(len(sig)*L)
    up[::L] = sig
    Fs_up = Fs * L

    plot_diapo(up, Fs_up, f"Étage {i} – Upsampling ×{L}",
               10+i*3, 'tab:orange', zoom_freq_max=100000)

    # ---- FILTRE FIR KAISER (CUTOFF CORRECT) ----
    #cutoff = 24000
    cutoff = min(
        AUDIO_BAND_HZ,
        Fs_up / (2*M)
    )

    taps = scipy.signal.firwin(
        numtaps,
        cutoff=cutoff,
        window=('kaiser', beta),
        fs=Fs_up
    )

    filt = scipy.signal.lfilter(taps * L, 1.0, up)

    plot_diapo(filt, Fs_up, f"Étage {i} – Filtrage FIR",
               11+i*3, 'tab:green', zoom_freq_max=100000)

    # ---- DOWNSAMPLING ----
    sig = filt[::M]
    Fs = Fs_up / M

    plot_diapo(sig, Fs, f"Étage {i} – Downsampling ÷{M}",
               12+i*3, 'tab:red')

# ============================================================
# 4. SIGNAL FINAL
# ============================================================
sig_out = sig
Fs_out = Fs

print("SRC terminé")
print("Fs sortie :", Fs_out)
print("Ratio réel :", Fs_out / Fs_in)

# ============================================================
# 5. VALIDATION
# ============================================================
plt.figure(figsize=(10, 8))
plt.suptitle("Validation finale", fontweight='bold')

# ----- TEMPOREL -----
plt.subplot(2, 1, 1)
t_in = np.arange(len(signal_in))/Fs_in
t_out = np.arange(len(sig_out))/Fs_out

m_in = (t_in >= ZOOM_OFFSET_MS/1000) & (t_in <= (ZOOM_OFFSET_MS+ZOOM_WIDTH_MS)/1000)
m_out = (t_out >= ZOOM_OFFSET_MS/1000) & (t_out <= (ZOOM_OFFSET_MS+ZOOM_WIDTH_MS)/1000)

plt.plot(t_in[m_in]*1000, signal_in[m_in], label="Entrée")
plt.plot(t_out[m_out]*1000, sig_out[m_out], '--', label="Sortie")
plt.legend()
plt.grid(True)

# ----- FRÉQUENTIEL -----
plt.subplot(2, 1, 2)
f_in = np.fft.rfftfreq(len(signal_in), 1/Fs_in)
f_out = np.fft.rfftfreq(len(sig_out), 1/Fs_out)

plt.plot(f_in, 20*np.log10(np.abs(np.fft.rfft(signal_in))+1e-12), label="Entrée")
plt.plot(f_out, 20*np.log10(np.abs(np.fft.rfft(sig_out))+1e-12), '--', label="Sortie")

plt.xlim(0, 24000)
plt.xlabel("Fréquence (Hz)")
plt.ylabel("dB")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print("Script OK ✔")


# Lecture
sd.play(sig_out, Fs_out)

# Attend la fin de la lecture
sd.wait()