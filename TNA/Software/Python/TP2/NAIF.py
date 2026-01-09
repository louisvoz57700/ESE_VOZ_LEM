import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.signal import resample_poly
from scipy.fft import fft, fftfreq

# =========================================================
# Upsampling / Downsampling 44.1 kHz -> 48 kHz
# =========================================================
def upsample_dsp(x):
    """
    Conversion 44.1 kHz -> 48 kHz
    44100 * 160 / 147 = 48000
    """
    return resample_poly(x, up=160, down=147)

# =========================================================
# FFT utilitaire
# =========================================================
def compute_fft(signal, fs):
    N = len(signal)
    Y = fft(signal)
    freqs = fftfreq(N, d=1/fs)
    Y_mag = np.abs(Y) / N
    return freqs[:N//2], Y_mag[:N//2]


path = "/Users/louisvoz/Desktop/Annee 2025-2026/S9/TNA/TP/TNA-TP/playback_44100.mat"
data = loadmat(path)

audio = data["w441"].flatten()
fs_in = 44100
fs_out = 48000

y_up_down = upsample_dsp(audio)

N_plot = 2000000

print(len(audio))
print(len(y_up_down))
print()
plt.figure(figsize=(12,8))

# ---- Temps : audio original ----
plt.subplot(2, 2, 1)
plt.plot(audio[:N_plot])
plt.title("Audio original (44.1 kHz) - Temps")
plt.xlabel("n")
plt.ylabel("Amplitude")
plt.grid()

# ---- Temps : audio converti ----
plt.subplot(2, 2, 2)
plt.plot(y_up_down[:N_plot])
plt.title("Audio converti (48 kHz) - Temps")
plt.xlabel("n")
plt.ylabel("Amplitude")
plt.grid()

# ---- Fréquence : audio original ----
freqs_in, mag_in = compute_fft(audio, fs_in)
plt.subplot(2, 2, 3)
plt.plot(freqs_in, 20*np.log10(mag_in + 1e-12))
plt.title("Spectre audio original")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude (dB)")
plt.grid()

# ---- Fréquence : audio converti ----
freqs_out, mag_out = compute_fft(y_up_down, fs_out)
plt.subplot(2, 2, 4)
plt.plot(freqs_out, 20*np.log10(mag_out + 1e-12))
plt.title("Spectre audio converti")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude (dB)")
plt.grid()

plt.tight_layout()
plt.show()