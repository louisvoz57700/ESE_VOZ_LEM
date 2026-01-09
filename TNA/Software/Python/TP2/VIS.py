import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.fft import fft, fftfreq

# --- Chargement du fichier ---
path = "/Users/louisvoz/Desktop/Annee 2025-2026/S9/TNA/TP/TNA-TP/playback_44100.mat"
data = loadmat(path)
audio = data["w441"].flatten()

# --- Paramètres ---
fs = 44100
N = len(audio)

# --- FFT ---
Y = fft(audio)
freqs = fftfreq(N, 1/fs)
Y_mag = np.abs(Y)

# Fréquences positives
pos = freqs >= 0

# --- FIGURE ---
plt.figure(figsize=(14, 10))

# 1) TEMPOREL
plt.subplot(3, 1, 1)
plt.plot(audio[:2000000])
plt.title("Signal PDM – Domaine temporel (zoom)")
plt.xlabel("Échantillons")
plt.ylabel("Amplitude")
plt.grid(True)

# 2) ZOOM 0–25 kHz
plt.subplot(3, 1, 2)
plt.plot(freqs[pos], 20*np.log10(Y_mag[pos] + 1e-12))
plt.title("Spectre (zoom 0–25 kHz)")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude (dB)")
plt.xlim(0, 25000)
plt.grid(True)

# 3) SPECTRE COMPLET
plt.subplot(3, 1, 3)
plt.plot(freqs[pos], 20*np.log10(Y_mag[pos] + 1e-12))
plt.title("Spectre complet du signal PDM")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude (dB)")
plt.xlim(0, fs/2)
plt.grid(True)

plt.tight_layout()
plt.show()