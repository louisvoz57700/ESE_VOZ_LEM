import numpy as np
from matplotlib import pyplot as plt
from scipy.io import loadmat
from scipy.signal import cheby1, lfilter, freqz
from numpy.fft import fft, fftfreq
import sounddevice as sd

# --- Fonctions ---
def crop_20bits_float(signal):
    levels = 2**20 - 1
    signal_clipped = np.clip(signal, -1, 1)
    signal_quant = np.round((signal_clipped + 1)/2 * levels)/levels*2 - 1
    return signal_quant

def low_pass_cheby1(data, cutoff_freq, fs, order=15, rp=1):
    nyq = 0.5 * fs
    normal_cutoff = cutoff_freq / nyq
    if not 0 < normal_cutoff < 1:
        normal_cutoff = 0.99
    b, a = cheby1(order, rp, normal_cutoff, btype='low')
    filtered = lfilter(b, a, data)
    return filtered, b, a

def compute_fft(signal, fs):
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1/fs)[:N//2]
    yf_mag = np.abs(yf[:N//2])
    yf_db = 20*np.log10(yf_mag + 1e-12)
    return xf, yf_mag, yf_db

def compute_snr(xf, yf_mag):
    signal_idx = xf <= 20000
    noise_idx = xf > 20000
    P_signal = np.sum(yf_mag[signal_idx]**2)
    P_noise = np.sum(yf_mag[noise_idx]**2)
    snr = 10 * np.log10(P_signal / P_noise)
    return snr

# --- Charger le signal PDM ---
path = "/Users/louisvoz/Desktop/Annee 2025-2026/S9/TNA/TP/TNA-TP/pdm_in.mat"
data = loadmat(path)
audio = data["in"].flatten()

# --- Paramètres ---
fs = 6144000                # fréquence d’échantillonnage d’origine
cutoff = 20000              # cutoff unique
order = 6

# --- Un seul filtrage ---
filtered, b, a = low_pass_cheby1(audio, cutoff, fs, order)

# --- Décimation simple (si nécessaire) ---
decim = 128
x = filtered[::decim]
fs_current = fs / decim

# --- Crop 20 bits ---
x_cropped = crop_20bits_float(x)

# --- FFT ---
xf_signal, yf_signal_mag, yf_signal_db = compute_fft(x_cropped, fs_current)

# --- Réponse du filtre ---
w_filter, h_filter = freqz(b, a, worN=4096, fs=fs)
h_filter_db = 20*np.log10(np.abs(h_filter)+1e-12)

# --- SNR ---
snr = compute_snr(xf_signal, yf_signal_mag)
print(f"SNR final : {snr:.2f} dB")

# --- Tracés ---
fig, axes = plt.subplots(3,1, figsize=(14,10))

axes[0].plot(x[:20000])
axes[0].set_title("Signal décimé")
axes[0].grid(True)

axes[1].semilogx(xf_signal, yf_signal_db)
axes[1].set_title("FFT du signal")
axes[1].grid(True, which='both')

axes[2].semilogx(w_filter, h_filter_db, color='red')
axes[2].set_title("Réponse du filtre")
axes[2].grid(True, which='both')

plt.tight_layout()
plt.show()

# --- Écoute ---
sd.play(x, samplerate=int(fs_current))
sd.wait()
sd.play(x_cropped, samplerate=int(fs_current))
sd.wait()