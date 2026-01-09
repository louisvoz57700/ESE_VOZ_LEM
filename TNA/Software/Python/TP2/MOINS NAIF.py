import scipy.io
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==========================================
# 0. CONFIGURATION
# ==========================================
chemin = "/Users/louisvoz/Desktop/Annee 2025-2026/S9/TNA/TP/TNA-TP/playback_44100.mat"


L = 160  # Upsampling
M = 147  # Downsampling
Fs_in = 44100

# Paramètres du filtre (Kaiser)
numtaps = 600
beta = 8.0

# === PARAMÈTRES D'AFFICHAGE ===
VIEW_DURATION_S = 10  # Vue globale sur 10 secondes
ZOOM_OFFSET_MS = 2000  # Zoom technique à 2 secondes
ZOOM_WIDTH_MS = 10  # Fenêtre de 10ms

# Calculs théoriques
Fs_up = Fs_in * L
Fs_out = Fs_up / M
wc_norm = 1.0 / L


# ==========================================
# FONCTION D'AFFICHAGE INTELLIGENTE
# ==========================================
def plot_diapo(sig, Fs, title, step_num, color='tab:blue', full_view=False, zoom_freq_max=None):
    N = len(sig)
    if N == 0: return

    t = np.arange(N) / Fs

    # FFT Optimisée
    fft_N = min(N, 2 ** 19)
    freqs = np.fft.rfftfreq(fft_N, d=1 / Fs)
    spect = np.fft.rfft(sig[:fft_N])
    mag_db = 20 * np.log10(np.abs(spect) + 1e-12)

    # --- CALCUL DYNAMIQUE DES LIMITES ---
    # Pour éviter que le spectre soit coupé
    peak_db = np.max(mag_db)
    ylim_top = peak_db + 10  # Un peu de marge au-dessus
    ylim_bottom = peak_db - 130  # On affiche 130dB de dynamique

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    plt.suptitle(f'DIAPO {step_num}: {title}', fontsize=14, fontweight='bold', color='darkblue')

    # --- 1. TEMPOREL ---
    if full_view:
        # VUE GLOBALE
        ax1.plot(t, sig, color=color, linewidth=0.5)
        ax1.set_title(f'Temporel - VUE GLOBALE ({VIEW_DURATION_S} secondes)', fontsize=10, fontweight='bold')
        ax1.set_xlim(0, VIEW_DURATION_S)
        ax1.set_xlabel('Temps (secondes)')

        rect = patches.Rectangle((ZOOM_OFFSET_MS / 1000, min(sig)), ZOOM_WIDTH_MS / 1000, max(sig) - min(sig),
                                 linewidth=1.5, edgecolor='r', facecolor='none')
        ax1.add_patch(rect)
        ax1.text(ZOOM_OFFSET_MS / 1000, max(sig), " Zone de Zoom (2s)", color='red', fontsize=9, fontweight='bold')
    else:
        # VUE ZOOMÉE
        idx_start = int((ZOOM_OFFSET_MS / 1000) * Fs)
        idx_end = idx_start + int((ZOOM_WIDTH_MS / 1000) * Fs)
        if idx_start >= N: idx_start = N - 100
        if idx_end > N: idx_end = N
        t_slice = t[idx_start:idx_end] * 1000
        sig_slice = sig[idx_start:idx_end]

        ax1.plot(t_slice, sig_slice, '.-', color=color, linewidth=1, markersize=4)
        ax1.set_title(f'Temporel - ZOOM TECHNIQUE ({ZOOM_OFFSET_MS}ms)', fontsize=10, fontweight='bold')
        ax1.set_xlim(ZOOM_OFFSET_MS, ZOOM_OFFSET_MS + ZOOM_WIDTH_MS)
        ax1.set_xlabel('Temps (ms)')

    ax1.set_ylabel('Amplitude')
    ax1.grid(True, alpha=0.4)
    props = dict(boxstyle='round', facecolor='white', alpha=0.9)
    ax1.text(0.98, 0.95, f"Fs = {Fs / 1000:.3f} kHz", transform=ax1.transAxes, ha='right', va='top', bbox=props,
             fontsize=9)

    # --- 2. FRÉQUENTIEL ---
    ax2.plot(freqs, mag_db, color=color, linewidth=0.8)
    ax2.set_title('Spectre en Fréquence (FFT)', fontsize=10, fontweight='bold')
    ax2.set_xlabel('Fréquence (Hz)')
    ax2.set_ylabel('Amplitude (dB)')
    ax2.grid(True, alpha=0.4)

    # Application des limites dynamiques
    ax2.set_ylim(ylim_bottom, ylim_top)

    if zoom_freq_max:
        ax2.set_xlim(0, zoom_freq_max)
    elif Fs > 100000:
        ax2.set_xlim(0, 100000)
        ax2.text(0.5, 0.9, "Zoom bande utile (0-100 kHz)", transform=ax2.transAxes,
                 ha='center', color='red', fontsize=9, bbox=props)
    else:
        ax2.set_xlim(0, Fs / 2)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()


# ==========================================
# 1. CHARGEMENT
# ==========================================
print("Chargement...")
samples_target = int(Fs_in * VIEW_DURATION_S)
try:
    mat = scipy.io.loadmat(chemin)
    key = next(k for k in mat.keys() if not k.startswith('_'))
    signal_in = mat[key].squeeze()
    if len(signal_in) > samples_target:
        signal_in = signal_in[:samples_target]
except:
    print("⚠️ Mode Synthétique")
    t = np.arange(samples_target) / Fs_in
    env = np.minimum(t / 2, 1)
    signal_in = (0.5 * np.sin(2 * np.pi * 440 * t) + 0.3 * np.sin(2 * np.pi * 8000 * t)) * env

plot_diapo(signal_in, Fs_in, f"SIGNAL ORIGINAL (Vue {VIEW_DURATION_S} secondes)", 1, full_view=True)
plot_diapo(signal_in, Fs_in, f"SIGNAL ORIGINAL (Zoom à {ZOOM_OFFSET_MS}ms)", 2, full_view=False)

# ==========================================
# 2. CONCEPTION FILTRE (CORRIGÉ & COMPLET)
# ==========================================
print("Calcul comparatif des 5 filtres...")
fig, (ax_gain, ax_phase) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)
plt.suptitle('DIAPO 3: CHOIX DU FILTRE (Comparatif complet)', fontsize=14, fontweight='bold', color='darkblue')

w_range = np.linspace(0, wc_norm * 4, 5000)
freq_hz = w_range * (Fs_up / 2)
w_rad = w_range * np.pi

# --- 1. Butterworth (IIR) ---
b, a = scipy.signal.butter(8, wc_norm, btype='low')
w, h = scipy.signal.freqz(b, a, worN=w_rad)
ax_gain.plot(freq_hz, 20 * np.log10(abs(h)), '--', color='tab:blue', alpha=0.6, label='1. IIR Butterworth')
ax_phase.plot(freq_hz, np.unwrap(np.angle(h)), '--', color='tab:blue', alpha=0.6)

# --- 2. Chebyshev I (IIR) ---
b, a = scipy.signal.cheby1(8, 1.0, wc_norm, btype='low')
w, h = scipy.signal.freqz(b, a, worN=w_rad)
ax_gain.plot(freq_hz, 20 * np.log10(abs(h)), '-.', color='tab:orange', alpha=0.6, label='2. IIR Chebyshev I')
ax_phase.plot(freq_hz, np.unwrap(np.angle(h)), '-.', color='tab:orange', alpha=0.6)

# --- 3. Chebyshev II (IIR) ---
b, a = scipy.signal.cheby2(8, 60, wc_norm, btype='low')
w, h = scipy.signal.freqz(b, a, worN=w_rad)
ax_gain.plot(freq_hz, 20 * np.log10(abs(h)), ':', color='tab:brown', alpha=0.6, label='3. IIR Chebyshev II')
ax_phase.plot(freq_hz, np.unwrap(np.angle(h)), ':', color='tab:brown', alpha=0.6)

# --- 4. Equiripple (FIR) ---
try:
    bands = [0, wc_norm, wc_norm * 1.3, 0.5]
    taps_remez = scipy.signal.remez(numtaps, bands, [1, 0], fs=1.0)
    w, h = scipy.signal.freqz(taps_remez, 1.0, worN=w_rad)
    ax_gain.plot(freq_hz, 20 * np.log10(abs(h)), '-', color='tab:purple', alpha=0.5, linewidth=1,
                 label='4. FIR Equiripple')
    ax_phase.plot(freq_hz, np.unwrap(np.angle(h)), '-', color='tab:purple', alpha=0.5, linewidth=1)
except:
    pass

cutoff = min(
        20000,
        Fs_up / (2*M)
    )
# --- 5. Kaiser (FIR) - RETENU ---
taps_kaiser = scipy.signal.firwin(
    numtaps,
    cutoff=cutoff,               # 20 kHz
    window=('kaiser', beta),
    fs=Fs_up                    # fréquence d'échantillonnage en Hz
)
w, h_kaiser = scipy.signal.freqz(taps_kaiser, 1.0, worN=w_rad)
ax_gain.plot(freq_hz, 20 * np.log10(abs(h_kaiser)), 'r-', linewidth=2.5, label='5. FIR Kaiser (RETENU)')
ax_phase.plot(freq_hz, np.unwrap(np.angle(h_kaiser)), 'r-', linewidth=2.5)

# --- Mise en page Gain ---
ax_gain.set_ylabel('Gain (dB)')
# Limites élargies pour voir jusqu'au fond du filtre Kaiser
ax_gain.set_ylim(-140, 10)
ax_gain.grid(True, which='both', alpha=0.3)
ax_gain.legend(loc='lower left', fontsize=9)
ax_gain.set_title('A. Réponse en Amplitude (Atténuation)', fontsize=10, fontweight='bold')
ax_gain.axvline(22050, color='k', alpha=0.3)

# --- Mise en page Phase ---
ax_phase.set_ylabel('Phase (Radians)')
ax_phase.set_xlabel('Fréquence (Hz)')
ax_phase.grid(True, which='both', alpha=0.3)
ax_phase.set_title('B. Réponse en Phase (Linéarité)', fontsize=10, fontweight='bold')
ax_phase.axvline(22050, color='k', alpha=0.3)

# Annotations pédagogiques
ax_phase.annotate('Phase Linéaire (FIR)\n= Droite = Retard constant',
                  xy=(15000, -50), xytext=(40000, -50),
                  arrowprops=dict(facecolor='red', shrink=0.05),
                  bbox=dict(boxstyle="round", fc="wheat", alpha=0.8))

plt.xlim(0, 60000)
plt.tight_layout()
plt.subplots_adjust(top=0.90)
plt.show()

# ==========================================
# 3. TRAITEMENT SRC
# ==========================================
print(f"Traitement SRC...")
# UPSAMPLING
sig_up = np.zeros(len(signal_in) * L)
sig_up[::L] = signal_in
plot_diapo(sig_up, Fs_up, f"UPSAMPLING x{L} (Zoom Zéros)", 4, 'tab:orange', full_view=False, zoom_freq_max=100000)

# FILTRAGE
final_filter = taps_kaiser * L
sig_filt = scipy.signal.lfilter(final_filter, 1.0, sig_up)
delay = 0 #int((numtaps - 1) / 2)
sig_filt = sig_filt[delay:]
plot_diapo(sig_filt, Fs_up, "INTERPOLATION (Signal lissé)", 5, 'tab:green', full_view=False, zoom_freq_max=100000)

# DOWNSAMPLING
sig_out = sig_filt[::M]
plot_diapo(sig_out, Fs_out, f"SORTIE FINALE (48 kHz)", 6, 'tab:red', full_view=False)
print(len(sig_out))
print(len(signal_in))
# ==========================================
# 4. VALIDATION
# ==========================================
print("Validation...")
plt.figure(figsize=(10, 8))
plt.suptitle(f'DIAPO 7: VALIDATION (Zone {ZOOM_OFFSET_MS}-{ZOOM_OFFSET_MS + ZOOM_WIDTH_MS} ms)', fontsize=14,
             fontweight='bold', color='darkblue')

# Temporel
plt.subplot(2, 1, 1)
t_in = np.arange(len(signal_in)) / Fs_in
t_out = np.arange(len(sig_out)) / Fs_out
mask_in = (t_in >= ZOOM_OFFSET_MS / 1000) & (t_in <= (ZOOM_OFFSET_MS + ZOOM_WIDTH_MS) / 1000)
mask_out = (t_out >= ZOOM_OFFSET_MS / 1000) & (t_out <= (ZOOM_OFFSET_MS + ZOOM_WIDTH_MS) / 1000)
plt.plot(t_in[mask_in] * 1000, signal_in[mask_in], 'b.-', label='Entrée (44.1k)', alpha=0.6, markersize=5)
plt.plot(t_out[mask_out] * 1000, sig_out[mask_out], 'r.--', label='Sortie (48k)', alpha=0.6, markersize=5)
plt.title(f'Temporel : Superposition Parfaite (Zoom {ZOOM_OFFSET_MS}ms)')
plt.xlabel('Temps (ms)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Fréquentiel
plt.subplot(2, 1, 2)
f_in = np.fft.rfftfreq(len(signal_in), d=1 / Fs_in)
db_in = 20 * np.log10(np.abs(np.fft.rfft(signal_in)) + 1e-12)
f_out = np.fft.rfftfreq(len(sig_out), d=1 / Fs_out)
db_out = 20 * np.log10(np.abs(np.fft.rfft(sig_out)) + 1e-12)
# Limites dynamiques aussi pour la validation
peak_val = max(np.max(db_in), np.max(db_out))
plt.plot(f_in, db_in, 'b', label='Entrée', linewidth=1, alpha=0.7)
plt.plot(f_out, db_out, 'r--', label='Sortie', linewidth=1, alpha=0.7)
plt.title('Fréquentiel : Spectre Global')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('dB')
plt.xlim(0, 24000)
plt.ylim(peak_val - 130, peak_val + 10)  # Dynamique auto
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

print("Script terminé.")