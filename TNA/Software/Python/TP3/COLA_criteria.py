import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin
from numpy.fft import fft, ifft, fftshift

# --- Configuration identique ---
nb_points_audio = 20000  # Réduit pour la lisibilité des graphes
N = 512
R = N // 2
numtaps = 61
n_fft = 1024  # Taille FFT élargie pour éviter l'aliasing temporel
cutoff = 0.1

# Signal et Filtre
t = np.linspace(0, 1, nb_points_audio)
audio = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 300 * t)  # 50Hz (utile) + 300Hz (à couper)
fir_coeff = firwin(numtaps, cutoff)
H = fft(fir_coeff, n_fft)
window = np.hanning(N)

# --- Traitement ---
reconstructed = np.zeros(len(audio) + n_fft)
norm_sum = np.zeros(len(audio) + n_fft)
starts = range(0, len(audio) - N + 1, R)

# On garde un bloc spécifique pour l'analyse visuelle (ex: le 2ème bloc)
index_demo = 1
demo_data = {}

for i, start in enumerate(starts):
    block_raw = audio[start:start + N]
    block_win = block_raw * window

    X = fft(block_win, n_fft)
    Y = X * H
    block_filt = np.real(ifft(Y))

    # Stockage pour démo
    if i == index_demo:
        demo_data = {'raw': block_raw, 'win': block_win, 'spec_X': X, 'spec_Y': Y, 'out': block_filt}

    reconstructed[start:start + n_fft] += block_filt
    norm_sum[start:start + N] += window

# --- Visualisation ---
plt.figure(figsize=(14, 12))

# 1. Visualisation COLA (Somme des fenêtres)
plt.subplot(4, 1, 1)
for i, start in enumerate(starts):
    w_plot = np.zeros(len(audio))
    w_plot[start:start + N] = window
    plt.plot(w_plot, alpha=0.3, linestyle='--')
plt.plot(norm_sum[:len(audio)], color='black', lw=2, label="Somme (COLA)")
plt.title("Étape 1 : Fenêtrage et reconstruction de l'unité (COLA)")
plt.legend(loc='upper right')

# 2. Zoom sur un bloc : Temps -> Fréquence
plt.subplot(4, 1, 2)
plt.plot(demo_data['raw'], label="Signal Brut", alpha=0.5)
plt.plot(demo_data['win'], label="Signal Fenêtré", lw=2)
plt.title("Étape 2 : Préparation du bloc (Fenêtrage)")
plt.legend()

# 3. Spectre (Module)
plt.subplot(4, 1, 3)
freqs = np.fft.fftfreq(n_fft)
plt.plot(fftshift(freqs), 20 * np.log10(np.abs(fftshift(demo_data['spec_X'])) + 1e-6), label="|X(f)| (Entrée)")
plt.plot(fftshift(freqs), 20 * np.log10(np.abs(fftshift(demo_data['spec_Y'])) + 1e-6), label="|Y(f)| (Filtré)")
plt.title("Étape 3 : Filtrage dans le domaine fréquentiel (Multiplication X * H)")
plt.ylabel("dB")
plt.legend()

# 4. Retour au temps
plt.subplot(4, 1, 4)
plt.plot(demo_data['out'], color='red', label="Sortie IFFT (n_fft points)")
plt.title("Étape 4 : Retour au temps (IFFT) - Notez l'étalement du bloc dû au filtre")
plt.legend()

plt.tight_layout()
plt.show()