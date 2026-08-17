#!/usr/bin/env python3
"""Compare low-pass filter frequency responses."""

import argparse
import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "matplotlib"))

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


FILTER_ORDER = 5
CUTOFF_HZ = 4.0e9
PASSBAND_RIPPLE_DB = 0.5
STOPBAND_ATTENUATION_DB = 40
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "logs" / "filter_response_comparison.png"


def analog_lpf_response(b, a, frequency_hz):
    """Return magnitude [dB] and group delay [ns] for an analog filter."""
    angular_frequency = 2.0 * np.pi * frequency_hz
    _, h = signal.freqs(b, a, worN=angular_frequency)

    magnitude_db = 20.0 * np.log10(np.maximum(np.abs(h), 1e-12))
    phase = np.unwrap(np.angle(h))
    group_delay_s = -np.gradient(phase, angular_frequency)

    return magnitude_db, group_delay_s * 1e9


def design_filters():
    cutoff_rad_s = 2.0 * np.pi * CUTOFF_HZ

    return {
        "Butterworth": signal.butter(
            FILTER_ORDER, cutoff_rad_s, btype="low", analog=True, output="ba"
        ),
        "Chebyshev I": signal.cheby1(
            FILTER_ORDER,
            PASSBAND_RIPPLE_DB,
            cutoff_rad_s,
            btype="low",
            analog=True,
            output="ba",
        ),
        "Elliptic": signal.ellip(
            FILTER_ORDER,
            PASSBAND_RIPPLE_DB,
            STOPBAND_ATTENUATION_DB,
            cutoff_rad_s,
            btype="low",
            analog=True,
            output="ba",
        ),
        "Bessel": signal.bessel(
            FILTER_ORDER,
            cutoff_rad_s,
            btype="low",
            analog=True,
            norm="mag",
            output="ba",
        ),
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Plot frequency responses for elliptic, Chebyshev, Bessel, and Butterworth LPFs."
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show the plot window after saving the image.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    frequency_hz = np.linspace(0.01e9, 10.0e9, 4000)
    filters = design_filters()

    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.grid": True,
            "grid.alpha": 0.35,
            "figure.figsize": (10, 7),
        }
    )

    fig, (ax_gain, ax_delay) = plt.subplots(2, 1, sharex=True, constrained_layout=True)

    for name, (b, a) in filters.items():
        magnitude_db, group_delay_ns = analog_lpf_response(b, a, frequency_hz)
        ax_gain.plot(frequency_hz / 1e9, magnitude_db, label=name, linewidth=1.8)
        ax_delay.plot(frequency_hz / 1e9, group_delay_ns, label=name, linewidth=1.8)

    ax_gain.axvline(CUTOFF_HZ / 1e9, color="black", linestyle="--", linewidth=1.0)
    ax_gain.set_title(
        f"{FILTER_ORDER}th-order Analog Low-pass Filter Comparison "
        f"(fc = {CUTOFF_HZ / 1e9:.1f} GHz)"
    )
    ax_gain.set_ylabel("Magnitude [dB]")
    ax_gain.set_ylim(-80, 3)
    ax_gain.legend(loc="lower left")

    ax_delay.axvline(CUTOFF_HZ / 1e9, color="black", linestyle="--", linewidth=1.0)
    ax_delay.set_xlabel("Frequency [GHz]")
    ax_delay.set_ylabel("Group delay [ns]")
    ax_delay.set_ylim(bottom=0)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=200)
    print(f"Saved: {OUTPUT_PATH}")

    if args.show:
        plt.show()


if __name__ == "__main__":
    main()
