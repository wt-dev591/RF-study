#!/usr/bin/env python3
"""Generate a Chebyshev LPF order selection chart."""

import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "matplotlib"))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "logs" / "image-5.png"
SVG_OUTPUT_PATH = OUTPUT_PATH.with_suffix(".svg")

FC_HZ = 3.8e9
STOP_FREQ_HZ = 4.8e9
TARGET_ATTENUATION_DB = 20.0
SELECTED_ORDER = 5
RIPPLES_DB = (0.5, 3.0)


def setup_japanese_font():
    candidates = [
        "IPAexGothic",
        "IPAPGothic",
        "IPAGothic",
        "Droid Sans Fallback",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            plt.rcParams["font.family"] = candidate
            break


def chebyshev_attenuation_db(order, ripple_db, normalized_frequency):
    epsilon = np.sqrt(10.0 ** (ripple_db / 10.0) - 1.0)
    chebyshev_poly = np.cosh(order * np.arccosh(normalized_frequency))
    return 10.0 * np.log10(1.0 + (epsilon * chebyshev_poly) ** 2)


def required_order(ripple_db, normalized_frequency, attenuation_db):
    epsilon = np.sqrt(10.0 ** (ripple_db / 10.0) - 1.0)
    numerator = np.arccosh(np.sqrt(10.0 ** (attenuation_db / 10.0) - 1.0) / epsilon)
    denominator = np.arccosh(normalized_frequency)
    return int(np.ceil(numerator / denominator))


def draw_ladder(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    y = 3.2
    xs = [0.8, 2.0, 3.4, 5.0, 6.4, 8.0, 9.2]
    ax.plot([xs[0], xs[-1]], [y, y], color="black", lw=1.7)
    ax.scatter([xs[0], xs[-1]], [y, y], s=38, facecolors="white", edgecolors="black", zorder=3)

    for x, label in [(2.0, "g1"), (5.0, "g3"), (8.0, "g5")]:
        ax.plot([x, x], [y, 2.35], color="black", lw=1.5)
        ax.plot([x - 0.34, x + 0.34], [2.35, 2.35], color="black", lw=1.5)
        ax.plot([x - 0.34, x + 0.34], [2.08, 2.08], color="black", lw=1.5)
        ax.plot([x, x], [2.08, 1.55], color="black", lw=1.5)
        ax.plot([x - 0.28, x + 0.28], [1.55, 1.55], color="black", lw=1.5)
        ax.plot([x - 0.20, x + 0.20], [1.35, 1.35], color="black", lw=1.5)
        ax.plot([x - 0.12, x + 0.12], [1.15, 1.15], color="black", lw=1.5)
        ax.text(x - 0.72, 2.0, label, fontsize=15, ha="right", va="center")

    for x, label in [(3.4, "g2"), (6.4, "g4")]:
        coil_x = np.linspace(x - 0.45, x + 0.45, 120)
        coil_y = y + 0.18 * np.sin(np.linspace(0, 6 * np.pi, 120))
        ax.plot(coil_x, coil_y, color="black", lw=1.5)
        ax.text(x - 0.25, 4.0, label, fontsize=15)

    ax.text(8.8, 2.45, "5次", fontsize=15)


def main():
    setup_japanese_font()

    delta = STOP_FREQ_HZ / FC_HZ - 1.0
    normalized_frequency = 1.0 + delta
    x = np.logspace(-2, 0, 500)
    omega_ratio = 1.0 + x

    plt.rcParams.update(
        {
            "font.size": 12,
            "axes.grid": True,
            "grid.alpha": 0.32,
            "figure.figsize": (14, 8),
        }
    )

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2, 3, width_ratios=[1.18, 1.35, 1.35])
    ax_info = fig.add_subplot(gs[:, 0])
    ax_top = fig.add_subplot(gs[0, 1:])
    ax_bottom = fig.add_subplot(gs[1, 1:])

    ax_info.axis("off")
    ax_info.text(0.0, 0.96, "等リップル型LPF", color="crimson", fontsize=23, weight="bold")
    ax_info.text(0.0, 0.78, "今回作成するLPFの仕様", fontsize=15, weight="bold")
    ax_info.text(
        0.04,
        0.70,
        "\n".join(
            [
                f"・カットオフ周波数: {FC_HZ / 1e9:.1f} GHz",
                f"・減衰量: {TARGET_ATTENUATION_DB:.0f} dB以上 @ {STOP_FREQ_HZ / 1e9:.1f} GHz",
                "・最大リップル: 3 dB以下",
            ]
        ),
        fontsize=14,
        linespacing=1.65,
        va="top",
    )
    ax_info.text(0.0, 0.43, "横軸", fontsize=15, weight="bold")
    ax_info.text(
        0.04,
        0.33,
        rf"$\left|\frac{{\omega}}{{\omega_c}}\right|-1"
        rf"=\frac{{{STOP_FREQ_HZ / 1e9:.1f}}}{{{FC_HZ / 1e9:.1f}}}-1"
        rf"={delta:.3f}$",
        fontsize=17,
    )

    ladder_ax = ax_info.inset_axes([0.03, 0.02, 0.92, 0.24])
    draw_ladder(ladder_ax)

    for ax, ripple_db in [(ax_top, RIPPLES_DB[0]), (ax_bottom, RIPPLES_DB[1])]:
        for order in range(1, 11):
            attenuation = chebyshev_attenuation_db(order, ripple_db, omega_ratio)
            lw = 2.7 if order == SELECTED_ORDER else 1.1
            color = "tab:red" if order == SELECTED_ORDER else "0.25"
            alpha = 1.0 if order == SELECTED_ORDER else 0.72
            ax.semilogx(x, attenuation, color=color, lw=lw, alpha=alpha)
            label_x = 0.74
            label_y = chebyshev_attenuation_db(order, ripple_db, 1.0 + label_x)
            if label_y < 68:
                ax.text(label_x, label_y, f"n={order}", fontsize=9, color=color, va="center")

        actual_selected = chebyshev_attenuation_db(
            SELECTED_ORDER, ripple_db, normalized_frequency
        )
        n_required = required_order(ripple_db, normalized_frequency, TARGET_ATTENUATION_DB)

        ax.axvline(delta, color="tab:red", lw=1.8)
        ax.axhline(TARGET_ATTENUATION_DB, color="tab:red", lw=1.8)
        ax.scatter([delta], [TARGET_ATTENUATION_DB], color="tab:red", s=46, zorder=5)
        ax.scatter([delta], [actual_selected], color="tab:blue", s=46, zorder=5)
        ax.annotate(
            f"n={SELECTED_ORDER}: {actual_selected:.1f} dB",
            xy=(delta, actual_selected),
            xytext=(0.38, min(actual_selected + 12, 62)),
            arrowprops={"arrowstyle": "->", "color": "tab:blue", "lw": 1.4},
            color="tab:blue",
            fontsize=13,
        )
        ax.text(
            0.016,
            61,
            f"{ripple_db:g} dBリップル / 必要次数: {n_required}次以上",
            fontsize=16,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.8},
        )

        ax.set_xlim(0.01, 1.0)
        ax.set_ylim(0, 70)
        ax.set_ylabel("減衰量 [dB]")
        ax.grid(True, which="both")

    ax_top.set_title("チェビシェフI型LPFの次数選定", fontsize=20, pad=12)
    ax_bottom.set_xlabel(r"正規化周波数の偏差  $|\omega/\omega_c| - 1$")

    fig.savefig(OUTPUT_PATH, dpi=200)
    fig.savefig(SVG_OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")
    print(f"Saved: {SVG_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
