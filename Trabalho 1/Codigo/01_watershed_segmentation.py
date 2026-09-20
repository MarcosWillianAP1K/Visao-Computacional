# -*- coding: utf-8 -*-
"""
=============================================================================
Segmentação por Transformada de Watershed Baseada em Marcadores
UFPI - Tópicos Especiais em Visão Computacional | Prof. José Denes Lima Araújo
Grupo 4 - Técnicas de Segmentação Baseada em Região (Seção 10.5 - Gonzalez & Woods)
Integrante 3: O Analista Experimental (Slide 9 do Seminário)
=============================================================================
"""

import os
import urllib.request
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 70)
    print("TRANSFORMADA DE WATERSHED BASEADA EM MARCADORES E DISTÂNCIA EUCLIDIANA")
    print("=" * 70)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    imagens_dir = os.path.join(base_dir, "imagens")
    resultados_dir = os.path.join(base_dir, "resultados")
    os.makedirs(imagens_dir, exist_ok=True)
    os.makedirs(resultados_dir, exist_ok=True)

    img_path = os.path.join(imagens_dir, "moedas_sobrepostas.jpg")
    if not os.path.exists(img_path):
        url = "https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_watershed/images/water_coins.jpg"
        print(f"Baixando imagem canônica de moedas de: {url}")
        urllib.request.urlretrieve(url, img_path)

    # 1. Carregamento e Conversões de Espaço de Cor
    img_bgr = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    print(f"-> Imagem carregada: {img_rgb.shape[1]}x{img_rgb.shape[0]} px, {img_rgb.shape[2]} canais.")

    # 2. Limiarização de Otsu e Abertura Morfológica
    # Em moedas escuras sobre fundo claro, usamos THRESH_BINARY_INV
    otsu_thresh, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    print(f"-> Limiar ótimo de Otsu: {otsu_thresh:.1f}")

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Avaliação do Otsu isolado
    num_otsu_labels, _ = cv2.connectedComponents(opening)
    print(f"-> Componentes conexos detectados pelo Otsu puro: {num_otsu_labels - 1}")
    if (num_otsu_labels - 1) == 1:
        print("   [ALERTA]: O método baseado em intensidade falhou, unindo todas as moedas em 1 massa única!")

    # 3. Delimitação do Fundo Seguro (Sure Background)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # 4. Transformada de Distância Euclidiana Exata (L2)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    max_dist = dist_transform.max()
    print(f"-> Distância euclidiana máxima ao fundo: {max_dist:.2f} pixels")

    # 5. Delimitação do Primeiro Plano Seguro (Sure Foreground / Sementes)
    thresh_dist = 0.7 * max_dist
    _, sure_fg = cv2.threshold(dist_transform, thresh_dist, 255, 0)
    sure_fg = np.uint8(sure_fg)

    # 6. Região Desconhecida (Zona de Disputa e Fronteira)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # 7. Rotulação Conexa dos Marcadores
    num_labels, markers = cv2.connectedComponents(sure_fg)
    total_moedas = num_labels - 1
    print(f"-> Sementes internas (marcadores das moedas): {total_moedas} moedas identificadas.")

    # Offset nos rótulos: Fundo = 1, Objetos = 2..N+1, Desconhecido = 0
    markers = markers + 1
    markers[unknown == 255] = 0

    # 8. Execução da Transformada de Watershed
    img_watershed = img_rgb.copy()
    markers_result = cv2.watershed(img_watershed, markers)

    # Barragens morfológicas recebem -1
    img_watershed[markers_result == -1] = [255, 0, 0]
    num_barragens = np.sum(markers_result == -1)
    print(f"-> Barragens morfológicas construídas: {num_barragens} pixels de fronteira fechada.")

    # 9. Metrologia e Contagem Individual
    coin_labels = [lbl for lbl in np.unique(markers_result) if lbl > 1]
    img_metrologia = img_rgb.copy()
    areas = []

    for i, lbl in enumerate(coin_labels, 1):
        mask = np.uint8(markers_result == lbl)
        areas.append(np.sum(mask))
        M = cv2.moments(mask)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.putText(img_metrologia, str(i), (cX - 8, cY + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 0), 2)

    img_metrologia[markers_result == -1] = [255, 0, 0]
    print(f"-> Sucesso total: {len(coin_labels)} moedas contadas individualmente.")
    print(f"-> Área média: {np.mean(areas):.1f} px² (Desvio padrão: {np.std(areas):.1f} px²)")

    # 10. Salvamento do Painel Multipainel
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title("(a) Imagem Original com Moedas Tangentes", fontweight='bold')
    axes[0, 0].axis("off")

    axes[0, 1].imshow(opening, cmap="gray")
    axes[0, 1].set_title("(b) Otsu + Abertura (Falha de Toque)", fontweight='bold')
    axes[0, 1].axis("off")

    im_dist_plot = axes[0, 2].imshow(dist_transform, cmap="viridis")
    axes[0, 2].set_title("(c) Transformada de Distância Euclidiana", fontweight='bold')
    axes[0, 2].axis("off")
    plt.colorbar(im_dist_plot, ax=axes[0, 2], fraction=0.046, pad=0.04)

    axes[1, 0].imshow(sure_fg, cmap="gray")
    axes[1, 0].set_title("(d) Primeiro Plano Seguro (Sementes)", fontweight='bold')
    axes[1, 0].axis("off")

    axes[1, 1].imshow(unknown, cmap="gray")
    axes[1, 1].set_title("(e) Região Desconhecida", fontweight='bold')
    axes[1, 1].axis("off")

    axes[1, 2].imshow(img_metrologia)
    axes[1, 2].set_title(f"(f) Watershed Final ({len(coin_labels)} Moedas Separadas)", fontweight='bold')
    axes[1, 2].axis("off")

    plt.tight_layout()
    out_path = os.path.join(resultados_dir, "watershed_pipeline_completo.png")
    plt.savefig(out_path, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"-> Gráfico salvo em: {out_path}")
    print("=" * 70)

if __name__ == "__main__":
    main()
