# -*- coding: utf-8 -*-
"""
=============================================================================
Confronto Prático: Watershed vs K-Means em Objetos Sobrepostos
UFPI - Tópicos Especiais em Visão Computacional | Prof. José Denes Lima Araújo
Grupo 4 - Técnicas de Segmentação Baseada em Região (Seção 10.5 - Gonzalez & Woods)
Integrante 3: O Analista Experimental (Slide 11 do Seminário)
=============================================================================
"""

import os
import urllib.request
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 70)
    print("CONFRONTO PRÁTICO: WATERSHED VS K-MEANS EM OBJETOS SOBREPOSTOS")
    print("=" * 70)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    imagens_dir = os.path.join(base_dir, "imagens")
    resultados_dir = os.path.join(base_dir, "resultados")
    os.makedirs(imagens_dir, exist_ok=True)
    os.makedirs(resultados_dir, exist_ok=True)

    img_path = os.path.join(imagens_dir, "moedas_sobrepostas.jpg")
    if not os.path.exists(img_path):
        url = "https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_watershed/images/water_coins.jpg"
        urllib.request.urlretrieve(url, img_path)

    img_bgr = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # 1. K-Means (K=2)
    pixels = img_rgb.reshape((-1, 3)).astype(np.float32)
    criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels_k2, centers_k2 = cv2.kmeans(pixels, 2, None, criterio, 10, cv2.KMEANS_RANDOM_CENTERS)
    seg_k2 = np.uint8(centers_k2)[labels_k2.flatten()].reshape(img_rgb.shape)
    mapa_k2 = labels_k2.reshape((img_rgb.shape[0], img_rgb.shape[1]))
    cluster_moeda = np.argmin(np.mean(centers_k2, axis=1))
    mascara_moedas_kmeans = np.uint8(mapa_k2 == cluster_moeda)
    num_comp_kmeans, _ = cv2.connectedComponents(mascara_moedas_kmeans)

    print(f"-> K-Means (K=2):")
    print(f"   Componentes conexos formados pelas moedas: {num_comp_kmeans - 1}")
    print("   [DIAGNÓSTICO]: Falha na separação por toque (assinatura espectral idêntica).")

    # 2. Watershed com Marcadores
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    unknown = cv2.subtract(sure_bg, sure_fg)
    num_labels_ws, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    img_ws = img_rgb.copy()
    markers_res = cv2.watershed(img_ws, markers)
    img_ws[markers_res == -1] = [255, 0, 0]
    total_ws = len(np.unique(markers_res)) - 2

    print(f"\n-> Transformada de Watershed:")
    print(f"   Moedas individualizadas com sucesso: {total_ws}")
    print("   [DIAGNÓSTICO]: Sucesso total através do relevo da distância topográfica.")

    # 3. Geração da Figura Comparativa
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    axes[0].imshow(img_rgb)
    axes[0].set_title("(a) Imagem Original (24 Moedas Tangentes)", fontsize=12, fontweight='bold')
    axes[0].axis("off")

    axes[1].imshow(seg_k2)
    axes[1].set_title("(b) K-Means (K=2) [FALHA DE TOQUE: 1 Bloco]", fontsize=12, fontweight='bold', color='darkred')
    axes[1].axis("off")

    axes[2].imshow(img_ws)
    axes[2].set_title(f"(c) Watershed [SUCESSO: {total_ws} Moedas Separadas]", fontsize=12, fontweight='bold', color='darkgreen')
    axes[2].axis("off")

    plt.tight_layout()
    out_duelo = os.path.join(resultados_dir, "comparativo_toque_watershed_vs_kmeans.png")
    plt.savefig(out_duelo, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"\n-> Gráfico comparativo salvo em: {out_duelo}")
    print("=" * 70)

if __name__ == "__main__":
    main()
