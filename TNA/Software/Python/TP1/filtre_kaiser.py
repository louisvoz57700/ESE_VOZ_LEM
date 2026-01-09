import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, freqz, kaiserord

# ================== PARAMÈTRES ==================
fs_pdm = 6_144_000   # Hz
fpb = 20_000         # Hz (bande passante)
fsb = 24_000         # Hz (bande coupée)
Asb = 60             # dB atténuation stopband

# ================== DESIGN DU FILTRE ==================
transition_bw = fsb - fpb
N, beta = kaiserord(Asb, transition_bw / (fs_pdm / 2))

fir = firwin(
    N,
    cutoff=fpb,
    window=('kaiser', beta),
    fs=fs_pdm
)

print(f"Ordre FIR = {N}, beta Kaiser = {beta:.2f}")

# ================== RÉPONSE FRÉQUENTIELLE ==================
w, h = freqz(fir, worN=32768, fs=fs_pdm)
H_db = 20 * np.log10(np.abs(h) + 1e-12)
H_phase = np.unwrap(np.angle(h)) * 180 / np.pi

# ================== TRACÉS ==================
plt.figure(figsize=(14, 9))

# -------- AMPLITUDE --------
plt.subplot(2, 1, 1)
plt.semilogx(w, H_db, label="Réponse du filtre")

# Lignes verticales (fréquences)
plt.axvline(fpb, color='g', linestyle='--', linewidth=2, label=f"fpb = {fpb/1000:.1f} kHz")
plt.axvline(fsb, color='r', linestyle='--', linewidth=2, label=f"fsb = {fsb/1000:.1f} kHz")

# Lignes horizontales (niveaux dB)
plt.axhline(0, color='k', linestyle=':', linewidth=1)
plt.axhline(-Asb, color='purple', linestyle='--', linewidth=2,
            label=f"Asb = -{Asb} dB")

# Annotations texte
plt.text(fpb*1.05, -3, "Fin bande passante", color='g')
plt.text(fsb*1.05, -Asb+5, "Début bande coupée", color='r')
plt.text(w[-1]*0.7, -Asb-5, f"-{Asb} dB", color='purple')

plt.title("Réponse fréquentielle du filtre FIR passe-bas (fenêtre de Kaiser)")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude (dB)")
plt.grid(True, which='both', linestyle='--')
plt.legend()
plt.xlim(100, fs_pdm/2)
plt.ylim(-120, 5)

# -------- PHASE --------
plt.subplot(2, 1, 2)
plt.plot(w, H_phase)
plt.title("Phase du filtre FIR (linéaire)")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Phase (°)")
plt.grid(True, which='both', linestyle='--')

plt.tight_layout()
plt.show()