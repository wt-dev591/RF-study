#!/usr/bin/env python3
"""Generate an LC scaling chart for a 5th-order Chebyshev LPF."""

import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "matplotlib"))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "logs" / "image-8.png"
SVG_OUTPUT_PATH = OUTPUT_PATH.with_suffix(".svg")

FC_HZ = 3.8e9
R0_OHM = 50.0
OMEGA_C = 2.0 * np.pi * FC_HZ
G_VALUES = [3.4817, 0.7618, 4.5381, 0.7618, 3.4817]


def setup_japanese_font():
    candidates = ["IPAexGothic", "IPAPGothic", "IPAGothic", "Droid Sans Fallback"]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            plt.rcParams["font.family"] = candidate
            break


def draw_capacitor(ax, x, y_top, y_bottom, label, value=None):
    y_mid = (y_top + y_bottom) / 2
    ax.plot([x, x], [y_top, y_mid + 0.18], color="black", lw=1.8)
    ax.plot([x - 0.34, x + 0.34], [y_mid + 0.18, y_mid + 0.18], color="black", lw=1.8)
    ax.plot([x - 0.34, x + 0.34], [y_mid - 0.18, y_mid - 0.18], color="black", lw=1.8)
    ax.plot([x, x], [y_mid - 0.18, y_bottom + 0.35], color="black", lw=1.8)
    draw_ground(ax, x, y_bottom + 0.35)
    ax.text(x - 0.52, y_mid + 0.02, label, fontsize=15, ha="right", va="center")
    if value is not None:
        ax.text(x, y_bottom - 0.32, value, fontsize=13, ha="center", va="top")


def draw_inductor(ax, x0, x1, y, label, value=None):
    lead = 0.28
    ax.plot([x0, x0 + lead], [y, y], color="black", lw=1.8)
    ax.plot([x1 - lead, x1], [y, y], color="black", lw=1.8)
    coil_x = np.linspace(x0 + lead, x1 - lead, 160)
    coil_y = y + 0.22 * np.sin(np.linspace(0, 6 * np.pi, len(coil_x)))
    ax.plot(coil_x, coil_y, color="black", lw=1.8)
    ax.text((x0 + x1) / 2, y + 0.72, label, fontsize=15, ha="center")
    if value is not None:
        ax.text((x0 + x1) / 2, y + 0.34, value, fontsize=13, ha="center", va="bottom")


def draw_ground(ax, x, y):
    ax.plot([x - 0.32, x + 0.32], [y, y], color="black", lw=1.6)
    ax.plot([x - 0.23, x + 0.23], [y - 0.18, y - 0.18], color="black", lw=1.6)
    ax.plot([x - 0.13, x + 0.13], [y - 0.36, y - 0.36], color="black", lw=1.6)


def draw_lpf(ax, y, normalized=True):
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.8, 5)
    ax.axis("off")

    node_x = [0.8, 1.8, 4.15, 6.5, 8.55, 9.45]
    ax.plot([node_x[0], node_x[-1]], [y, y], color="black", lw=1.8)
    ax.scatter([node_x[0], node_x[-1]], [y, y], s=60, facecolors="white", edgecolors="black", zorder=4)

    if normalized:
        draw_capacitor(ax, node_x[1], y, y - 1.45, "g1")
        draw_inductor(ax, node_x[1], node_x[2], y, "g2")
        draw_capacitor(ax, node_x[2], y, y - 1.45, "g3")
        draw_inductor(ax, node_x[2], node_x[3], y, "g4")
        draw_capacitor(ax, node_x[3], y, y - 1.45, "g5")
        ax.text(8.7, y - 0.65, "5次", fontsize=15)
    else:
        draw_capacitor(ax, node_x[1], y, y - 1.55, "C1", "2.92 pF")
        draw_inductor(ax, node_x[1], node_x[2], y, "L2", "1.60 nH")
        draw_capacitor(ax, node_x[2], y, y - 1.55, "C3", "3.80 pF")
        draw_inductor(ax, node_x[2], node_x[3], y, "L4", "1.60 nH")
        draw_capacitor(ax, node_x[3], y, y - 1.55, "C5", "2.92 pF")
        ax.text(8.7, y - 0.65, "50 Ω", fontsize=14)


def scaled_value(index, g):
    if index % 2 == 1:
        return g / (R0_OHM * OMEGA_C), "F"
    return R0_OHM * g / OMEGA_C, "H"


def engineering(value, unit):
    if unit == "F":
        return f"{value * 1e12:.2f} pF"
    return f"{value * 1e9:.2f} nH"


def scientific(value):
    return f"{value:.2E}"


def main():
    setup_japanese_font()
    plt.rcParams.update(
        {
            "font.size": 12,
            "figure.figsize": (14, 8),
            "axes.grid": False,
        }
    )

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(3, 2, height_ratios=[0.76, 1.0, 1.1], width_ratios=[1.08, 1.0])

    ax_title = fig.add_subplot(gs[0, 0])
    ax_title.axis("off")
    ax_title.text(0.0, 0.78, "L, C定数を求める", color="crimson", fontsize=27, weight="bold")
    ax_title.text(0.0, 0.20, "3 dBリップル・5次チェビシェフ型LPF", fontsize=18)

    ax_note = fig.add_subplot(gs[0, 1])
    ax_note.axis("off")
    ax_note.text(0.0, 0.78, r"$R=1\,\Omega,\ \omega_c=1$ で正規化された値", fontsize=18)
    ax_note.text(0.0, 0.30, "選択する行: N=5", fontsize=17, color="crimson", weight="bold")

    ax_norm = fig.add_subplot(gs[1, 0])
    draw_lpf(ax_norm, y=3.2, normalized=True)
    ax_norm.text(0.0, 4.55, "正規化プロトタイプ", fontsize=17, weight="bold")

    ax_scaled = fig.add_subplot(gs[2, 0])
    draw_lpf(ax_scaled, y=3.45, normalized=False)
    ax_scaled.text(0.0, 4.65, "50 Ω, 3.8 GHzへスケーリング後", fontsize=17, weight="bold")

    ax_formula = fig.add_subplot(gs[1, 1])
    ax_formula.axis("off")
    box = FancyBboxPatch(
        (0.02, 0.06),
        0.96,
        0.86,
        boxstyle="round,pad=0.03",
        facecolor="#f7f7f7",
        edgecolor="#bdbdbd",
        linewidth=1.2,
    )
    ax_formula.add_patch(box)
    ax_formula.text(0.07, 0.78, "スケーリング式", fontsize=18, weight="bold")
    ax_formula.text(
        0.10,
        0.52,
        rf"$\omega_c=2\pi f_c=2\pi({FC_HZ / 1e9:.1f}\,\mathrm{{GHz}})"
        rf"={OMEGA_C / 1e9:.3f}\times10^9$",
        fontsize=16,
    )
    ax_formula.text(0.10, 0.32, rf"$R_0={R0_OHM:.0f}\,\Omega$", fontsize=16)
    ax_formula.text(
        0.10,
        0.12,
        r"$L'_k=\dfrac{R_0 g_k}{\omega_c}$"
        "      "
        r"$C'_k=\dfrac{g_k}{R_0\omega_c}$",
        fontsize=18,
    )

    ax_table = fig.add_subplot(gs[2, 1])
    ax_table.axis("off")
    rows = []
    for index, g in enumerate(G_VALUES, start=1):
        value, unit = scaled_value(index, g)
        component = f"C{index}" if unit == "F" else f"L{index}"
        rows.append([f"g{index}", f"{g:.4f}", component, engineering(value, unit), scientific(value)])

    table = ax_table.table(
        cellText=rows,
        colLabels=["g", "係数", "C,L番号", "C,L値", "SI表記"],
        loc="center",
        cellLoc="center",
        colLoc="center",
        colWidths=[0.12, 0.18, 0.18, 0.22, 0.22],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    table.scale(1.0, 1.55)
    for (row, col), cell in table.get_celld().items():
        cell.set_linewidth(1.0)
        if row == 0:
            cell.set_facecolor("#e8f2d2")
            cell.set_text_props(weight="bold")

    ax_table.text(0.0, 0.95, "計算結果", fontsize=17, weight="bold", transform=ax_table.transAxes)

    fig.savefig(OUTPUT_PATH, dpi=200)
    fig.savefig(SVG_OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")
    print(f"Saved: {SVG_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
