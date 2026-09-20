# -*- coding: utf-8 -*-
"""
=============================================================================
Segmentação por Clustering K-Means em Imagens Coloridas (Espaço CIE L*a*b*)
UFPI - Tópicos Especiais em Visão Computacional | Prof. José Denes Lima Araújo
Grupo 4 - Técnicas de Segmentação Baseada em Região (Seção 10.5 - Gonzalez & Woods, 4ª Edição)
Integrante 3: O Analista Experimental (Slide 10 do Seminário)
=============================================================================
"""

import os
import urllib.request
import cv2
import numpy as np
import matplotlib.pyplot as plt

def executar_kmeans(imagem_rgb, k, usar_lab=True, tentativas=10, max_iter=100, eps=0.2):
    """
    Executa o algoritmo K-Means no espaço de atributos das cores.
    """
    if usar_lab:
        img_espaco = cv2.cvtColor(imagem_rgb, cv2.COLOR_RGB2LAB)
    else:
        img_espaco = imagem_rgb.copy()
        
    H, W, C = img_espaco.shape
    amostras = img_espaco.reshape((-1, 3)).astype(np.float32)
    criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter, eps)
    
    compactness, rotulos, centroides = cv2.kmeans(
        amostras, k, None, criterio, tentativas, cv2.KMEANS_RANDOM_CENTERS
    )
    
    centroides = np.uint8(centroides)
    imagem_quantizada = centroides[rotulos.flatten()].reshape((H, W, C))
    mapa_rotulos = rotulos.reshape((H, W))
    
    if usar_lab:
        imagem_quantizada_rgb = cv2.cvtColor(imagem_quantizada, cv2.COLOR_LAB2RGB)
    else:
        imagem_quantizada_rgb = imagem_quantizada
        
    return imagem_quantizada_rgb, mapa_rotulos, compactness, centroides

def main():
    print("=" * 70)
    print("CLUSTERING K-MEANS EM IMAGENS COLORIDAS NO ESPAÇO CIE L*A*B*")
    print("=" * 70)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    imagens_dir = os.path.join(base_dir, "imagens")
    resultados_dir = os.path.join(base_dir, "resultados")
    os.makedirs(imagens_dir, exist_ok=True)
    os.makedirs(resultados_dir, exist_ok=True)

    img_path = os.path.join(imagens_dir, "cena_colorida.jpg")
    if not os.path.exists(img_path):
        url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/butterfly.jpg"
        print(f"Baixando imagem canônica de teste de: {url}")
        urllib.request.urlretrieve(url, img_path)

    # 1. Carregamento
    img_bgr = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    print(f"-> Cena colorida: {img_rgb.shape[1]}x{img_rgb.shape[0]} px, {img_rgb.shape[2]} canais.")

    # 2. Experimentos com K = 2, 3, 5
    k_valores = [2, 3, 5]
    resultados = {}

    fig, ax = plt.subplots(1, 4, figsize=(18, 5))
    ax[0].imshow(img_rgb)
    ax[0].set_title("Cena Original", fontweight='bold')
    ax[0].axis("off")

    for idx, k in enumerate(k_valores, 1):
        seg_rgb, lbl_img, J, cents = executar_kmeans(img_rgb, k, usar_lab=True)
        resultados[k] = (seg_rgb, lbl_img, J, cents)
        print(f"-> K = {k}: Inércia intra-cluster J = {J:.2e}")
        
        ax[idx].imshow(seg_rgb)
        ax[idx].set_title(f"K = {k}\n(Inércia J = {J:.2e})", fontweight='bold')
        ax[idx].axis("off")

    plt.tight_layout()
    out_k = os.path.join(resultados_dir, "kmeans_comparativo_k.png")
    plt.savefig(out_k, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"-> Gráfico comparativo de K salvo em: {out_k}")

    # 3. Análise Detalhada dos 3 Clusters de K = 3
    seg_k3, lbl_k3, _, cents_k3 = resultados[3]
    total_px = lbl_k3.size

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    print("\n-> Distribuição de pixels em K = 3:")
    for c in range(3):
        mask = (lbl_k3 == c)
        pct = (np.sum(mask) / total_px) * 100
        print(f"   Cluster {c+1}: {np.sum(mask)} px ({pct:.1f}% da área total)")
        
        recorte = np.zeros_like(img_rgb)
        recorte[mask] = img_rgb[mask]
        
        axes[0, c].imshow(mask, cmap="gray")
        axes[0, c].set_title(f"Máscara Binária - Grupo {c+1}\n({pct:.1f}% dos pixels)", fontweight='bold')
        axes[0, c].axis("off")
        
        axes[1, c].imshow(recorte)
        axes[1, c].set_title(f"Recorte Isolado da Cena\n(Grupo {c+1})", fontweight='bold')
        axes[1, c].axis("off")

    plt.tight_layout()
    out_masc = os.path.join(resultados_dir, "kmeans_mascaras_k3.png")
    plt.savefig(out_masc, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"-> Máscaras de K = 3 salvas em: {out_masc}")
    print("=" * 70)

if __name__ == "__main__":
    main()
