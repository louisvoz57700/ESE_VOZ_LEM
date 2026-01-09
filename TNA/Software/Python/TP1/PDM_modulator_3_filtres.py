import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.signal import firwin, lfilter, kaiserord
from scipy.fft import fft, fftfreq


import time

start = time.perf_counter()
# --- Chargement du fichier PDM ---
path = "/Users/louisvoz/Desktop/Annee 2025-2026/S9/TNA/TP/TNA-TP/pdm_in.mat"
data = loadmat(path)
audio = data["in"].flatten()


def fir_linear_phase_multistage(pdm_signal, fs_pdm, fs_out=48000, n_bits=20, Asb=60):
    signal = pdm_signal
    fs = fs_pdm
    # ================== ÉTAPE 1 : décimation x8 ==================
    D1 = 8
    fpb1 = fs / (2 * D1) * 0.8
    fsb1 = fs / (2 * D1)

    N1, beta1 = kaiserord(Asb, (fsb1 - fpb1) / (fs / 2))
    print("N1, beta1 = ", N1, beta1)
    fir1 = firwin(N1, fpb1, window=('kaiser', beta1), fs=fs)

    signal = lfilter(fir1, 1.0, signal)[::D1]
    fs /= D1
    # ================== ÉTAPE 2 : décimation x8 ==================
    D2 = 8
    fpb2 = fs / (2 * D2) * 0.8
    fsb2 = fs / (2 * D2)

    N2, beta2 = kaiserord(Asb, (fsb2 - fpb2) / (fs / 2))
    print("N2, beta2 = ", N2, beta2)
    fir2 = firwin(N2, fpb2, window=('kaiser', beta2), fs=fs)

    signal = lfilter(fir2, 1.0, signal)[::D2]
    fs /= D2
    # ================== ÉTAPE 3 : décimation x2 ==================
    D3 = 2
    fpb3 = fs_out * 0.45
    fsb3 = fs_out * 0.5

    N3, beta3 = kaiserord(Asb, (fsb3 - fpb3) / (fs / 2))
    print("N3, beta3 = ", N3, beta3)
    fir3 = firwin(N3, fpb3, window=('kaiser', beta3), fs=fs)

    signal = lfilter(fir3, 1.0, signal)[::D3]
    fs /= D3
    # ================== Quantification ==================
    signal /= np.max(np.abs(signal))
    pcm_int = np.round(signal * (2**(n_bits - 1) - 1)).astype(np.int32)

    return pcm_int


# --- Paramètres ---
fs_pdm = 6144000  # fréquence du PDM
fs_out = 48000  # sortie PCM

# --- Démodulation ---
pcm_signal = fir_linear_phase_multistage(audio, fs_pdm, fs_out, n_bits=20)

# --- FFT pour analyse ---
N = len(pcm_signal)
Y = fft(pcm_signal)
Y_mag = np.abs(Y)[:N // 2]
Y_phase = np.angle(Y)[:N // 2]
freqs = fftfreq(N, 1 / fs_out)[:N // 2]


end = time.perf_counter()

print(f"Temps de calcul : {(end - start)*1000:.2f} ms")


# ================== CALCUL DU SNR ==================

# Limites fréquentielles
f_signal_max = 20000  # 20 kHz
f_nyquist = fs_out / 2

# Masques fréquentiels
signal_band = (freqs > 0) & (freqs <= f_signal_max)
noise_band = (freqs > f_signal_max) & (freqs <= f_nyquist)

# Puissances (spectrales)
signal_power = np.sum(Y_mag[signal_band]**2)
noise_power = np.sum(Y_mag[noise_band]**2)

# SNR en dB
SNR = 10 * np.log10(signal_power / noise_power)

print(f"SNR (0–20 kHz) : {SNR:.2f} dB")
# --- Tracé ---
plt.figure(figsize=(14, 10))

# Signal temporel
plt.subplot(3, 1, 1)
plt.plot(pcm_signal[:len(pcm_signal)])
plt.title("Signal PCM – Domaine temporel (zoom)")
plt.xlabel("Échantillons")
plt.ylabel("Amplitude")
plt.grid(True)

# Spectre amplitude
plt.subplot(3, 1, 2)
plt.semilogx(freqs, 20 * np.log10(Y_mag + 1e-12))
plt.title("Spectre PCM – Amplitude (log)")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude (dB)")
plt.grid(True, which='both', linestyle='--')

# Phase
plt.subplot(3, 1, 3)
plt.plot(freqs, np.unwrap(Y_phase) * 180 / np.pi)
plt.title("Phase du signal PCM")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Phase (°)")
plt.grid(True, which='both', linestyle='--')

plt.tight_layout()
plt.show()