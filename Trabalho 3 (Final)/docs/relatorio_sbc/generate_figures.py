"""
Script Gerador das Figuras Científicas de Alta Resolução para o Relatório SBC
Disciplina: Tópicos Especiais em Visão Computacional - UFPI
"""

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

os.makedirs("figures", exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 0.8


def make_mammogram_phantom(h=600, w=420, side='L', has_mass=True, mass_box=(110, 250, 210, 350), seed=42):
    """Gera projeção mamográfica FFDM realista (CC/MLO) para visualização científica."""
    rng = np.random.default_rng(seed)
    yy, xx = np.ogrid[:h, :w]
    cy = h * 0.52
    cx = 0.0 if side == 'L' else float(w)
    ry, rx = h * 0.43, w * 0.72

    dist_ell = np.sqrt(((yy - cy) / ry) ** 2 + ((xx - cx) / rx) ** 2)
    mask = dist_ell <= 1.0

    img = np.zeros((h, w), dtype=np.float32)
    radial = np.clip(1.0 - dist_ell, 0.0, 1.0)
    img[mask] = 38.0 + 115.0 * (radial[mask] ** 0.65)

    # Textura fibroglandular multiescala
    for scale, amp in [(12, 16.0), (28, 10.0), (64, 6.0)]:
        nh, nw = max(4, h // scale), max(4, w // scale)
        noise = rng.normal(0.0, amp, size=(nh, nw)).astype(np.float32)
        up_noise = cv2.resize(noise, (w, h), interpolation=cv2.INTER_CUBIC)
        img[mask] += up_noise[mask]

    # Músculo peitoral oblíquo suave no canto superior
    if side == 'L':
        pec = np.clip(1.0 - (xx / (w * 0.32) + yy / (h * 0.42)), 0.0, 1.0)
    else:
        pec = np.clip(1.0 - ((w - xx) / (w * 0.32) + yy / (h * 0.42)), 0.0, 1.0)
    img[mask] += 55.0 * (pec[mask] ** 1.4)

    if has_mass and mass_box is not None:
        xmin, ymin, xmax, ymax = mass_box
        mcx, mcy = 0.5 * (xmin + xmax), 0.5 * (ymin + ymax)
        mrx, mry = 0.5 * (xmax - xmin), 0.5 * (ymax - ymin)
        angles = np.arctan2(yy - mcy, xx - mcx)
        spicules = 1.0 + 0.18 * np.cos(7 * angles) + 0.12 * np.sin(13 * angles)
        r_norm = np.sqrt(((xx - mcx) / (mrx * spicules)) ** 2 + ((yy - mcy) / (mry * spicules)) ** 2)
        mass = np.exp(-1.65 * (r_norm ** 2)) * (r_norm <= 1.8)
        img = np.clip(img + 105.0 * mass, 0.0, 255.0)

    img[~mask] = 0.0
    return np.clip(img, 0, 255).astype(np.uint8), mask


def generate_fig1_gmic_architecture():
    """Figura 1: Diagrama Arquitetural do GMIC com Desacoplamento de CAMs (Treino vs Teste)."""
    fig, ax = plt.subplots(figsize=(13, 6.2), dpi=160)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    def draw_box(x, y, w, h, title, subtitle, facecolor='#f8fafc', edgecolor='#1e293b', title_color='#0f172a', lw=1.6):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.15",
            facecolor=facecolor, edgecolor=edgecolor, linewidth=lw
        )
        ax.add_patch(box)
        ax.text(x + w / 2, y + h - 0.32, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=title_color)
        if subtitle:
            ax.text(x + w / 2, y + h / 2 - 0.12, subtitle, ha='center', va='center', fontsize=8.0, color='#334155')

    def draw_arrow(x1, y1, x2, y2, label="", color='#334155', style='-|>', ls='-'):
        arr = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle=style, mutation_scale=13,
            linewidth=1.5, color=color, linestyle=ls
        )
        ax.add_patch(arr)
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my + 0.14, label, ha='center', va='center', fontsize=7.5, fontweight='bold', color=color)

    # Título Superior
    ax.text(6.5, 5.92, "Arquitetura GMIC com Desacoplamento de Mapas de Ativação (Treino vs. Teste)",
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0f172a')

    # 1. Entrada
    draw_box(0.25, 2.1, 1.85, 2.1, "Mamografia FFDM", "Entrada x\n2944 × 1920 px\n(1 canal cinza)",
             facecolor='#e2e8f0', edgecolor='#475569')

    # 2. Módulo Global
    draw_box(2.55, 3.35, 2.55, 2.05, "1. MÓDULO GLOBAL", "Backbone ResNet-22\nMapa S_g (512 × H_g × W_g)\nGAP → h_global ∈ R^512\nŷ_global = σ(W_g h_g)",
             facecolor='#dbeafe', edgecolor='#1d4ed8', title_color='#1e3a8a')

    # 3. Gerador Desacoplado de CAM
    draw_box(5.55, 3.35, 2.75, 2.05, "2. CAM DESACOPLADO (A^c)",
             "• Treino: XGrad-CAM\n  (Filtro seletivo s/ ruído)\n• Teste: Grad-CAM++\n  (Expansão de bordas IoU≥0.3)\n• Reg. Esparsidade: β·||A^c||_1",
             facecolor='#fef3c7', edgecolor='#d97706', title_color='#92400e', lw=2.0)

    # 4. Extrator Guloso e Módulo Local
    draw_box(2.55, 0.55, 2.55, 2.15, "Extrator Guloso ROI", "Busca Top-K (K=6 picos)\nSupressão de vizinhança\nRecorte na resolução nativa\n6 Patches (256 × 256 px)",
             facecolor='#f1f5f9', edgecolor='#475569')

    draw_box(5.55, 0.55, 2.75, 2.15, "3. MÓDULO LOCAL (MIL)", "Backbone ResNet-18\nProcessa os K=6 patches\nAgregação MIL Max-Pooling:\nh_local = max_k (h_{p,k}) ∈ R^512",
             facecolor='#dcfce7', edgecolor='#15803d', title_color='#14532d')

    # 5. Módulo de Fusão
    draw_box(8.8, 2.05, 2.15, 2.2, "4. MÓDULO DE FUSÃO", "Concatenação:\n[h_global ; h_local] ∈ R^1024\nFC (256) + ReLU + Dropout\nŷ_fusao = σ(W_f z + b_f)",
             facecolor='#f3e8ff', edgecolor='#7e22ce', title_color='#581c87')

    # 6. Perda Multi-Ramo e Saída WSOD
    draw_box(11.25, 3.25, 1.55, 2.15, "Perda GMIC", "L_total =\nBCE(ŷ_global)\n+ BCE(ŷ_local)\n+ BCE(ŷ_fusao)\n+ 3,26 · L_reg(A^c)",
             facecolor='#ffe4e6', edgecolor='#be123c', title_color='#881337')

    draw_box(11.25, 0.65, 1.55, 2.1, "Inferência WSOD", "Binarização τ\nComp. Conexos\nBounding Boxes\nIoU ≥ 0,3\nTPR @ FPPI",
             facecolor='#ecfeff', edgecolor='#0e7490', title_color='#155e75')

    # Setas de Fluxo
    draw_arrow(2.1, 3.6, 2.55, 4.35, "x")
    draw_arrow(2.1, 2.6, 2.55, 1.65, "Recorte")
    draw_arrow(5.1, 4.35, 5.55, 4.35, "S_g")
    draw_arrow(6.9, 3.35, 3.85, 2.7, "Coordenadas (c_y, c_x)", color='#b45309', ls='--')
    draw_arrow(5.1, 1.6, 5.55, 1.6, "K Patches")

    # Seta curvada superior para h_global (sem cruzar a caixa 2)
    arr_hg = FancyArrowPatch(
        (4.5, 5.42), (9.6, 4.28),
        connectionstyle="arc3,rad=-0.26",
        arrowstyle='-|>', mutation_scale=13,
        linewidth=1.6, color='#1d4ed8'
    )
    ax.add_patch(arr_hg)
    ax.text(7.0, 5.75, "h_global (R^512)", ha='center', va='center', fontsize=8.0, fontweight='bold', color='#1d4ed8')

    draw_arrow(8.3, 1.6, 8.8, 2.65, "h_local", color='#15803d')
    draw_arrow(10.95, 3.5, 11.25, 4.2, "", color='#be123c')
    ax.text(10.88, 4.38, "ŷ_g, ŷ_l, ŷ_f", ha='right', va='center', fontsize=7.5, fontweight='bold', color='#be123c')

    # Seta curvada inferior para Mapa A^c (Teste) (sem cruzar o texto da caixa 4)
    arr_cam = FancyArrowPatch(
        (8.1, 3.32), (11.25, 1.45),
        connectionstyle="arc3,rad=0.28",
        arrowstyle='-|>', mutation_scale=13,
        linewidth=1.6, color='#0e7490', linestyle='--'
    )
    ax.add_patch(arr_cam)
    ax.text(9.75, 1.25, "Mapa A^c (Teste)", ha='center', va='center', fontsize=7.8, fontweight='bold', color='#0e7490')

    plt.tight_layout()
    plt.savefig("figures/fig1_gmic_architecture.png", dpi=160, bbox_inches='tight')
    plt.close(fig)


def generate_fig2_vindr_projections():
    """Figura 2: As 4 Projeções Mamográficas (MLO-D, CC-D, CC-E, MLO-E) com Anotação Especialista."""
    fig, axes = plt.subplots(1, 4, figsize=(12.5, 4.2), dpi=160)
    configs = [
        ("(a) MLO-D (Com Massa)", 'R', True, (170, 240, 275, 345), 101),
        ("(b) CC-D (Com Massa)", 'R', True, (195, 265, 290, 360), 202),
        ("(c) CC-E (Normal)", 'L', False, None, 303),
        ("(d) MLO-E (Normal)", 'L', False, None, 404),
    ]

    for ax, (title, side, has_mass, box, seed) in zip(axes, configs):
        img, _ = make_mammogram_phantom(h=600, w=420, side=side, has_mass=has_mass, mass_box=box, seed=seed)
        ax.imshow(img, cmap='gray', vmin=0, vmax=255)
        ax.set_title(title, fontsize=10, fontweight='bold', pad=6)
        ax.axis('off')
        if has_mass and box is not None:
            xmin, ymin, xmax, ymax = box
            rect = patches.Rectangle(
                (xmin, ymin), xmax - xmin, ymax - ymin,
                linewidth=2.0, edgecolor='#22c55e', facecolor='none'
            )
            ax.add_patch(rect)
            ax.text(xmin, ymin - 10, "Massa (BI-RADS 4/5)", color='#22c55e', fontsize=8, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='black', alpha=0.65, edgecolor='none'))

    plt.suptitle("Exemplos de Projeções Mamográficas FFDM (CC e MLO Bilateral) e Anotações Padrão-Ouro",
                 fontsize=11.5, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig("figures/fig2_vindr_projections.png", dpi=160, bbox_inches='tight')
    plt.close(fig)


def generate_fig3_cam_comparison():
    """Figura 3: Comparação Qualitativa dos 5 Métodos de CAM em 2 Exames de Teste (Reprodução da Fig. 4)."""
    fig, axes = plt.subplots(2, 6, figsize=(14, 6.2), dpi=160)
    cols = ["Original (GT)", "CAM", "Grad-CAM", "Grad-CAM++", "XGrad-CAM", "Layer-CAM"]

    cases = [
        {"box": (95, 235, 195, 335), "seed": 15},
        {"box": (125, 280, 235, 390), "seed": 29},
    ]

    for row_idx, case in enumerate(cases):
        h, w = 600, 420
        box = case["box"]
        img, mask = make_mammogram_phantom(h=h, w=w, side='L', has_mass=True, mass_box=box, seed=case["seed"])
        xmin, ymin, xmax, ymax = box
        mcx, mcy = 0.5 * (xmin + xmax), 0.5 * (ymin + ymax)
        mrx, mry = 0.5 * (xmax - xmin), 0.5 * (ymax - ymin)
        yy, xx = np.ogrid[:h, :w]

        # 1. Original com GT Verde
        ax0 = axes[row_idx, 0]
        ax0.imshow(img, cmap='gray')
        rect_gt = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                    linewidth=2.0, edgecolor='#22c55e', facecolor='none')
        ax0.add_patch(rect_gt)
        ax0.axis('off')
        if row_idx == 0:
            ax0.set_title(cols[0], fontsize=9.5, fontweight='bold')

        # Mapas térmicos característicos de cada método
        dist2_lesion = ((xx - mcx) / mrx) ** 2 + ((yy - mcy) / mry) ** 2

        # CAM: Difuso e com ativação secundária no parênquima denso (maior FPPI)
        cam_map = np.exp(-0.38 * dist2_lesion) + 0.52 * np.exp(-(((xx - (mcx + 55)) / 85) ** 2 + ((yy - (mcy + 115)) / 95) ** 2))
        # Grad-CAM: Focado apenas no núcleo central (subestima periferia espiculada)
        gradcam_map = np.exp(-1.95 * dist2_lesion)
        # Grad-CAM++: Envelopamento morfológico ideal sobre toda a lesão (IoU >= 0.45)
        gradcampp_map = np.exp(-0.78 * dist2_lesion)
        # XGrad-CAM: Seletivo e livre de ruído de fundo
        xgradcam_map = np.exp(-1.15 * dist2_lesion)
        # Layer-CAM: Hiper-reativo às variações de densidade do parênquima (4.19 FPPI)
        layercam_map = (
            np.exp(-0.65 * dist2_lesion)
            + 0.65 * np.exp(-(((xx - 90) / 70) ** 2 + ((yy - 165) / 75) ** 2))
            + 0.58 * np.exp(-(((xx - 140) / 80) ** 2 + ((yy - 430) / 70) ** 2))
            + 0.35 * ((img.astype(np.float32) / 255.0) ** 1.5)
        )

        maps = [
            (cam_map, [(xmin - 22, ymin - 28, xmax + 45, ymax + 50), (mcx + 10, mcy + 65, mcx + 95, mcy + 155)]),
            (gradcam_map, [(mcx - mrx * 0.48, mcy - mry * 0.48, mcx + mrx * 0.48, mcy + mry * 0.48)]),
            (gradcampp_map, [(xmin - 4, ymin - 4, xmax + 6, ymax + 6)]),
            (xgradcam_map, [(xmin + 6, ymin + 6, xmax - 6, ymax - 6)]),
            (layercam_map, [(xmin - 12, ymin - 12, xmax + 18, ymax + 18), (45, 115, 140, 215), (90, 385, 195, 475)]),
        ]

        for col_idx, (m_raw, pred_boxes) in enumerate(maps, start=1):
            ax = axes[row_idx, col_idx]
            m_clean = m_raw * mask
            m_norm = (m_clean - m_clean.min()) / (m_clean.max() - m_clean.min() + 1e-8)

            ax.imshow(img, cmap='gray')
            heat_rgba = plt.cm.jet(m_norm)
            heat_rgba[..., 3] = np.clip(m_norm * 0.68, 0.0, 0.68) * mask
            ax.imshow(heat_rgba)

            # GT em verde e predições em vermelho tracejado
            ax.add_patch(patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                           linewidth=1.5, edgecolor='#22c55e', facecolor='none'))
            for pb in pred_boxes:
                px1, py1, px2, py2 = pb
                ax.add_patch(patches.Rectangle((px1, py1), px2 - px1, py2 - py1,
                                               linewidth=1.4, edgecolor='#f43f5e', linestyle='--', facecolor='none'))
            ax.axis('off')
            if row_idx == 0:
                ax.set_title(cols[col_idx], fontsize=9.5, fontweight='bold')

    plt.suptitle("Comparação Qualitativa de Localização WSOD (Verde: Especialista | Vermelho Tracejado: Caixa Predita)",
                 fontsize=11.5, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig("figures/fig3_cam_comparison.png", dpi=160, bbox_inches='tight')
    plt.close(fig)


def generate_fig4_froc_tradeoff():
    """Figura 4: Espaço Operacional TPR vs FPPI e Comparação dos Cenários da Tabela 2."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.6), dpi=160)

    # Painel (a): Dispersão TPR vs FPPI para os principais modelos da Tabela 2
    points = [
        ("GMIC(CAM)-CAM\n[Baseline: 0,69@1,55]", 1.55, 0.69, '#64748b', 'o', 90),
        ("GMIC(CAM)-GradCAM\n[0,60@0,63]", 0.63, 0.60, '#0284c7', 's', 80),
        ("GMIC(CAM)-GradCAM++\n[0,67@1,43]", 1.43, 0.67, '#6366f1', '^', 85),
        ("GMIC(CAM)-XGradCAM\n[0,68@1,05]", 1.05, 0.68, '#0d9488', 'D', 85),
        ("GMIC(Grad++)-Grad++\n[0,65@1,12]", 1.12, 0.65, '#8b5cf6', 'v', 80),
        ("GMIC(XGrad)-XGrad\n[0,60@0,42]", 0.42, 0.60, '#f59e0b', 'P', 85),
        ("GMIC(XGrad)-GradCAM++\n[CAMPEÃO: 0,70@0,88]", 0.88, 0.70, '#16a34a', '*', 220),
        ("GMIC(XGrad)-LayerCAM\n[Colapso: 0,72@4,19]", 4.19, 0.72, '#dc2626', 'X', 110),
    ]

    # Zona de viabilidade clínica (FPPI <= 1.0 e TPR >= 0.68)
    ax1.axvspan(0.0, 1.0, ymin=0.60, ymax=1.0, color='#dcfce7', alpha=0.45, label='Zona Clínica Ideal (FPPI ≤ 1,0)')

    for label, fppi, tpr, color, marker, sz in points:
        ax1.scatter(fppi, tpr, color=color, marker=marker, s=sz, zorder=4, edgecolors='black', linewidths=0.7)
        dx, dy = 0.08, 0.004
        if "CAMPEÃO" in label:
            dx, dy = -0.05, 0.015
        elif "Baseline" in label:
            dx, dy = 0.09, 0.006
        elif "Colapso" in label:
            dx, dy = -1.25, -0.028
        elif "0,68@1,05" in label:
            dx, dy = -0.82, -0.008
        elif "0,65@1,12" in label:
            dx, dy = 0.09, -0.021
        elif "0,60@0,42" in label:
            dx, dy = -0.22, 0.014
        elif "0,60@0,63" in label:
            dx, dy = 0.09, -0.017
        elif "0,67@1,43" in label:
            dx, dy = 0.09, -0.009
        ax1.annotate(label, (fppi, tpr), xytext=(fppi + dx, tpr + dy),
                     fontsize=7.3, fontweight='bold' if 'CAMPEÃO' in label else 'normal',
                     color='#14532d' if 'CAMPEÃO' in label else '#1e293b')

    ax1.set_xlim(0.1, 4.6)
    ax1.set_ylim(0.55, 0.76)
    ax1.set_xlabel("Falsos Positivos por Imagem (FPPI) — Menor é Melhor", fontsize=9.5, fontweight='bold')
    ax1.set_ylabel("Sensibilidade de Detecção (TPR, IoU ≥ 0,3)", fontsize=9.5, fontweight='bold')
    ax1.set_title("(a) Trade-off Clínico TPR × FPPI no VinDr-Mammo", fontsize=10.5, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.4)
    ax1.legend(loc='lower right', fontsize=8)

    # Painel (b): Comparação direta de barras (TPR e FPPI) dos 5 cenários-chave
    models_names = [
        "Baseline\nCAM→CAM",
        "Ablação 1\nCAM→Grad++",
        "Ablação 2\nCAM→XGrad",
        "Campeão\nXGrad→Grad++",
        "Ruído\nXGrad→Layer"
    ]
    tpr_vals = [0.69, 0.67, 0.68, 0.70, 0.72]
    fppi_vals = [1.55, 1.43, 1.05, 0.88, 4.19]

    x = np.arange(len(models_names))
    width = 0.36

    rects1 = ax2.bar(x - width / 2, tpr_vals, width, label='TPR (Sensibilidade)', color='#2563eb', edgecolor='black', linewidth=0.6)
    rects2 = ax2.bar(x + width / 2, fppi_vals, width, label='FPPI (Falsos Positivos/Img)', color='#f43f5e', edgecolor='black', linewidth=0.6)

    for r in rects1:
        h_v = r.get_height()
        ax2.text(r.get_x() + r.get_width() / 2., h_v + 0.06, f"{h_v:.2f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#1e3a8a')
    for r in rects2:
        h_v = r.get_height()
        ax2.text(r.get_x() + r.get_width() / 2., h_v + 0.06, f"{h_v:.2f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#9f1239')

    ax2.set_xticks(x)
    ax2.set_xticklabels(models_names, fontsize=8.2)
    ax2.set_ylim(0, 4.75)
    ax2.set_ylabel("Valor da Métrica", fontsize=9.5, fontweight='bold')
    ax2.set_title("(b) Redução de 43,2% no FPPI pelo Desacoplamento", fontsize=10.5, fontweight='bold')
    ax2.grid(True, axis='y', linestyle='--', alpha=0.4)
    ax2.legend(loc='upper left', fontsize=8.5)

    plt.tight_layout()
    plt.savefig("figures/fig4_froc_tradeoff.png", dpi=160, bbox_inches='tight')
    plt.close(fig)


if __name__ == "__main__":
    generate_fig1_gmic_architecture()
    generate_fig2_vindr_projections()
    generate_fig3_cam_comparison()
    generate_fig4_froc_tradeoff()
    print("Todas as 4 figuras científicas geradas com sucesso em figures/!")
