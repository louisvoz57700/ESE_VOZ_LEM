import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.signal import firwin
from numpy.fft import fft, ifft, fftshift


def executer_tp_tna(N_val):
    # =========================================================
    # 1️⃣ Chargement des données
    # =========================================================
    path = "/Users/louisvoz/Desktop/Annee 2025-2026/S9/TNA/TP/TNA-TP/pcm_48k.mat"
    try:
        data = loadmat(path)
        audio_full = data["pcm_48"].flatten()
        audio = audio_full[0:20000]
    except Exception as e:
        print(f"Erreur de chargement : {e}")
        # Signal de secours si le fichier n'est pas trouvé
        t = np.linspace(0, 0.5, 20000)
        audio = np.sin(2 * np.pi * 440 * t) + 0.5 * np.random.randn(20000)

    # =========================================================
    # 2️⃣ Paramètres du traitement
    # =========================================================
    N = N_val  # Taille de bloc (Fenêtre)
    R = N // 2  # Recouvrement 50% (Condition COLA pour Hanning)
    numtaps = 61  # Longueur du filtre FIR
    cutoff = 0.1  # Fréquence de coupure normalisée

    # Taille FFT : doit être >= N + numtaps - 1 pour éviter l'aliasing temporel
    n_fft = 2 ** int(np.ceil(np.log2(N + numtaps - 1)))

    # Préparation du filtre et de la fenêtre
    fir_coeff = firwin(numtaps, cutoff)
    H = fft(fir_coeff, n_fft)
    window = np.hanning(N)

    # =========================================================
    # 3️⃣ Traitement Overlap-Add (Domaine Fréquentiel)
    # =========================================================
    # On prévoit un buffer de sortie assez large pour la queue de la IFFT
    reconstructed = np.zeros(len(audio) + n_fft)
    norm_sum = np.zeros(len(audio) + n_fft)
    starts = range(0, len(audio) - N + 1, R)

    demo_block = {}  # Pour stocker les étapes d'un bloc précis (ex: le 10ème)

    for i, start in enumerate(starts):
        # a) Extraction et Fenêtrage
        block_raw = audio[start:start + N]
        block_win = block_raw * window

        # b) Filtrage par FFT (Convolution Rapide)
        X = fft(block_win, n_fft)
        Y = X * H

        # c) Retour au temps (IFFT)
        block_filt = np.real(ifft(Y))

        # d) Accumulation (OLA)
        reconstructed[start:start + n_fft] += block_filt
        norm_sum[start:start + N] += window

        # Sauvegarde pour la visualisation
        if i == 10:
            demo_block = {'raw': block_raw, 'win': block_win, 'X': X, 'Y': Y, 'out': block_filt}

    # Tronquer et normaliser
    reconstructed = reconstructed[:len(audio)]
    norm_sum = norm_sum[:len(audio)]
    # Division par la somme des fenêtres pour retrouver l'amplitude correcte
    reconstructed_final = reconstructed / (norm_sum + 1e-12)

    # =========================================================
    # 4️⃣ Calcul de l'erreur avec compensation du retard
    # =========================================================
    retard = (numtaps - 1) // 2
    audio_sync = audio[:-retard]
    reconstructed_sync = reconstructed_final[retard:]
    erreur_signal = audio_sync - reconstructed_sync

    # =========================================================
    # 5️⃣ Visualisation Complète
    # =========================================================
    plt.figure(figsize=(15, 18))

    # --- Graphique 1 : COLA ---
    plt.subplot(5, 1, 1)
    vue_cola = 4000
    for s in list(starts)[:25]:
        w_plot = np.zeros(vue_cola)
        if s < vue_cola - N:
            w_plot[s:s + N] = window
            plt.plot(w_plot, alpha=0.3, linestyle='--')
    plt.plot(norm_sum[:vue_cola], color='black', lw=2, label="Somme des fenêtres")
    plt.title(f"Étape 1 : Reconstruction de l'unité (Somme COLA) avec N = {N}")
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.2)

    # --- Graphique 2 : Fenêtrage ---
    plt.subplot(5, 1, 2)
    plt.plot(demo_block['raw'], label="Signal Brut du bloc", alpha=0.4)
    plt.plot(demo_block['win'], label="Signal Fenêtré (Hanning)", lw=2, color='orange')
    plt.title(f"Étape 2 : Fenêtrage du bloc (Analyse temporelle)")
    plt.legend()

    # --- Graphique 3 : Domaine Fréquentiel ---
    plt.subplot(5, 1, 3)
    f_axis = fftshift(np.fft.fftfreq(n_fft))
    plt.plot(f_axis, 20 * np.log10(np.abs(fftshift(demo_block['X'])) + 1e-6), label="Spectre Entrée")
    plt.plot(f_axis, 20 * np.log10(np.abs(fftshift(demo_block['Y'])) + 1e-6), label="Spectre Filtré (X * H)",
             color='red')
    plt.title(f"Étape 3 : Filtrage Fréquentiel (FFT Taille {n_fft})")
    plt.ylabel("Magnitude (dB)")
    plt.legend()

    # --- Graphique 4 : Comparaison Temporelle ---
    plt.subplot(5, 1, 4)
    plt.plot(audio_sync[:2000], label="Original (Recalé)", alpha=0.6, color='gray')
    plt.plot(reconstructed_final[:2000], label="Filtré (IFFT + OLA)", color='red', linestyle='--')
    plt.title("Étape 4 : Résultat de la reconstruction (Zoom)")
    plt.legend()

    # --- Graphique 5 : Analyse de l'erreur (Échelle Logarithmique) ---
    plt.subplot(5, 1, 5)

    # Calcul de la valeur absolue de l'erreur (pour éviter les log de nombres négatifs)
    erreur_abs = np.abs(erreur_signal[:2000])

    # Ajout d'un "epsilon" très petit (1e-10) pour éviter log(0)
    plt.semilogy(erreur_abs, color='green', lw=1, label="|Erreur| (Log)")

    mse = np.mean(erreur_signal ** 2)
    plt.title(f"Étape 5 : Analyse de l'erreur (MSE: {mse:.2e}) - Échelle Log")
    plt.ylabel("Magnitude (Log)")
    plt.xlabel("Nombre d'échantillons")
    plt.grid(True, which="both", ls="-", alpha=0.2)  # Grille plus fine pour le log
    plt.legend()

    plt.tight_layout()
    plt.show()


# --- Appel de la fonction ---
# Tu peux tester ici : 128, 256, 512, 1024, etc.
executer_tp_tna(N_val=2048)