#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Slot Stats Visualizer (+ combined images + curved HR graph)
- Loads a Stake/Carrot-style stats_summary.json
- Loads a per-mode Excel with Win Ranges / Hit Rates / RTP Allocation
- Produces:
  * Bar charts: RTP, M2M, Std, Prob Nil, Prob < Bet  (by mode)
  * Per-mode line charts: Hit Rate vs Win Range midpoint, RTP Allocation vs Win Range midpoint
  * CSV export of cleaned per-mode distributions
  * combined_overview.png (all cross-mode charts in one image)
  * {mode}_combined.png (per-mode 1x2 image)
  * NEW: {mode}_hr_curve.png (continuous per-spin probability vs payout)
  * NEW: combined_hr_curves.png (overlay of all modes)
"""

import argparse
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ---------- helpers ----------

def parse_win_range(s: str):
    if not isinstance(s, str):
        return (None, None)
    m = re.match(r"\(([^,]+),\s*([^)]+)\)", s.strip())
    if not m:
        return (None, None)
    try:
        lo = float(str(m.group(1)).strip())
        hi = float(str(m.group(2)).strip())
        return lo, hi
    except Exception:
        return (None, None)


def clean_mode_sheet(df: pd.DataFrame) -> pd.DataFrame:
    # find "Win Ranges" column (handles variants like "Win Ranges.1")
    win_cols = [c for c in df.columns if str(c).strip().startswith("Win Ranges")]
    if not win_cols:
        return pd.DataFrame()
    win_col = win_cols[0]

    # keep only rows whose Win Ranges look like "(a, b)"
    mask = df[win_col].astype(str).str.match(r"\(.*?,\s*.*?\)")
    keep_cols = [win_col]
    for c in ["Hit Rates", "RTP Allocation", "freegame", "basegame", "SIM COUNTS"]:
        if c in df.columns:
            keep_cols.append(c)
    df2 = df.loc[mask, keep_cols].copy()

    # numeric coercion
    for c in keep_cols:
        if c != win_col:
            df2[c] = pd.to_numeric(df2[c], errors="coerce")

    # parse ranges → lo/hi/mid
    lo_hi = df2[win_col].apply(parse_win_range)
    df2["lo"] = lo_hi.apply(lambda t: t[0])
    df2["hi"] = lo_hi.apply(lambda t: t[1])
    df2["mid"] = (df2["lo"] + df2["hi"]) / 2.0

    df2 = df2.sort_values("mid").reset_index(drop=True)
    df2.rename(columns={win_col: "Win Ranges"}, inplace=True)
    return df2


def save_bar(series, title, ylabel, out_path):
    ax = series.plot(kind="bar")
    ax.set_title(title)
    ax.set_xlabel("Mode")
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def save_xy(x, y, title, xlabel, ylabel, out_path, marker="o"):
    plt.figure()
    plt.plot(x, y, marker=marker)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def render_bar_on_axis(ax, series, title, ylabel):
    series.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Mode")
    ax.set_ylabel(ylabel)


def render_xy_on_axis(ax, x, y, title, xlabel, ylabel, marker="o"):
    ax.plot(x, y, marker=marker)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def save_hr_curve(mode_name: str,
                  df_clean: pd.DataFrame,
                  max_win: float,
                  out_path: Path,
                  num_points: int = 2000):
    """
    Build a smooth curve of per-spin probability vs payout (0..max_win).
    'Hit Rates' are interpreted as '1 in N' => per-spin probability p = 1 / N.
    Lower HR (e.g. 5) => taller curve (p=0.2), satisfying the user's requirement.
    """
    if df_clean.empty or "Hit Rates" not in df_clean.columns or "mid" not in df_clean.columns:
        return False

    # Extract valid (midpoint, hr) where hr > 0
    mids = df_clean["mid"].to_numpy()
    hrs = df_clean["Hit Rates"].to_numpy()

    # filter
    valid = np.isfinite(mids) & np.isfinite(hrs) & (hrs > 0)
    mids = mids[valid]
    hrs = hrs[valid]
    if mids.size < 2:
        return False

    # per-spin probability for that bin (at its midpoint)
    probs = 1.0 / hrs

    # ensure ascending x for interpolation
    order = np.argsort(mids)
    mids = mids[order]
    probs = probs[order]

    # build uniform x grid 0..max_win
    if not np.isfinite(max_win) or max_win <= 0:
        max_win = max(1.0, float(np.nanmax(mids)))
    x_grid = np.linspace(0.0, max_win, num_points)

    # Linear interpolation; for x outside data, clamp to edges
    y_grid = np.interp(x_grid, mids, probs, left=probs[0], right=probs[-1])

    # Plot
    plt.figure(figsize=(10, 4))
    plt.plot(x_grid, y_grid)
    plt.title(f"{mode_name}: Per-Spin Probability vs Payout (smoothed)")
    plt.xlabel("Payout (x bet)")
    plt.ylabel("Per-spin probability (1 / Hit Rate)")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return True

def save_hr_curve_advanced(mode_name: str,
                           df_clean: pd.DataFrame,
                           max_win: float,
                           out_dir: Path,
                           num_points: int = 2000,
                           logy: bool = True,
                           min_payout: float | None = None):
    """
    Builds multiple useful views:
      1) prob vs payout (optionally log-y)
      2) prob vs payout excluding payouts < min_payout (if provided)
      3) RTP density = payout * prob vs payout
      4) Survival S(x) = P(payout >= x)
    Returns dict of output paths.
    """
    outs = {}

    if df_clean.empty or "Hit Rates" not in df_clean.columns or "mid" not in df_clean.columns:
        return outs

    mids = df_clean["mid"].to_numpy()
    hrs  = df_clean["Hit Rates"].to_numpy()

    valid = np.isfinite(mids) & np.isfinite(hrs) & (hrs > 0)
    mids = mids[valid]
    hrs  = hrs[valid]
    if mids.size < 2:
        return outs

    probs = 1.0 / hrs

    order = np.argsort(mids)
    mids  = mids[order]
    probs = probs[order]

    if not np.isfinite(max_win) or max_win is None or max_win <= 0:
        max_win = max(1.0, float(np.nanmax(mids)))

    x_grid = np.linspace(0.0, max_win, num_points)
    y_grid = np.interp(x_grid, mids, probs, left=probs[0], right=probs[-1])

    # 1) Probability curve (optionally log-y)
    plt.figure(figsize=(10, 4))
    plt.plot(x_grid, y_grid)
    if logy:
        plt.yscale("log")
    plt.title(f"{mode_name}: Per-Spin Probability vs Payout")
    plt.xlabel("Payout (x bet)")
    plt.ylabel("Per-spin probability (1 / Hit Rate)")
    p1 = out_dir / f"{mode_name}_hr_curve_prob{'_logy' if logy else ''}.png"
    plt.tight_layout(); plt.savefig(p1); plt.close()
    outs["prob_curve"] = str(p1)

    # 2) Thresholded probability curve (exclude tiny payouts)
    if min_payout is not None and min_payout > 0:
        mask = x_grid >= float(min_payout)
        if mask.sum() > 2:
            plt.figure(figsize=(10, 4))
            plt.plot(x_grid[mask], y_grid[mask])
            if logy:
                plt.yscale("log")
            plt.title(f"{mode_name}: Probability vs Payout (≥ {min_payout}x)")
            plt.xlabel("Payout (x bet)")
            plt.ylabel("Per-spin probability (1 / Hit Rate)")
            p2 = out_dir / f"{mode_name}_hr_curve_prob_ge_{int(min_payout)}x{'_logy' if logy else ''}.png"
            plt.tight_layout(); plt.savefig(p2); plt.close()
            outs["prob_curve_threshold"] = str(p2)

    # 3) RTP density curve: payout * probability
    rtp_density = x_grid * y_grid
    plt.figure(figsize=(10, 4))
    plt.plot(x_grid, rtp_density)
    plt.title(f"{mode_name}: RTP Density (payout × probability)")
    plt.xlabel("Payout (x bet)")
    plt.ylabel("Expected contribution per payout")
    p3 = out_dir / f"{mode_name}_hr_curve_rtp_density.png"
    plt.tight_layout(); plt.savefig(p3); plt.close()
    outs["rtp_density"] = str(p3)

    # 4) Survival function S(x) = P(payout ≥ x)
    # Approximate from the discretized curve by treating y_grid as density per payout unit
    # (good enough for eyeballing tail heaviness)
    dx = x_grid[1] - x_grid[0]
    # normalize to turn y into a proper density over x (avoid dividing by zero)
    total = np.trapz(y_grid, x_grid)
    y_pdf = (y_grid / total) if total > 0 else y_grid
    surv = np.flip(np.cumsum(np.flip(y_pdf))) * dx  # integrate from right to left
    plt.figure(figsize=(10, 4))
    plt.plot(x_grid, surv)
    plt.yscale("log")  # survival is best on log-y
    plt.title(f"{mode_name}: Survival S(x) = P(payout ≥ x)")
    plt.xlabel("Payout (x bet)")
    plt.ylabel("Probability (log scale)")
    p4 = out_dir / f"{mode_name}_hr_curve_survival.png"
    plt.tight_layout(); plt.savefig(p4); plt.close()
    outs["survival"] = str(p4)

    return outs

# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(description="Visualize Stake/Carrot slot statistics.")
    ap.add_argument("--json", required=True, help="Path to stats_summary.json")
    ap.add_argument("--excel", required=True, help="Path to *_full_statistics.xlsx")
    ap.add_argument("--out", default="slot_stats_figs", help="Output directory for images/CSV")
    ap.add_argument("--show", default="0", help="Set to '1' to show charts interactively (blocks)")
    ap.add_argument("--curve-points", type=int, default=2000, help="Resolution of HR curve (x samples)")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- Load JSON summary ---
    with open(args.json, "r") as f:
        stats = json.load(f)

    rows = []
    for mode, payload in stats.items():
        row = {"mode": mode}
        row.update(payload)
        rows.append(row)
    modes_df = pd.DataFrame(rows).set_index("mode")

    # --- Individual bar charts across modes ---
    chart_specs = [
        ("rtp", "RTP by Mode", "RTP (return per 1.0 bet)", "rtp_by_mode.png"),
        ("m2m", "Mean-to-Median Ratio (Volatility) by Mode", "M2M (higher = more volatile)", "m2m_by_mode.png"),
        ("std", "Payout Standard Deviation by Mode", "Std Dev (multiplier units)", "std_by_mode.png"),
        ("prob_nil", "Probability of Zero-Win Spin by Mode", "Probability", "prob_nil_by_mode.png"),
        ("prob_less_bet", "Probability Payout < Bet by Mode", "Probability", "prob_less_bet_by_mode.png"),
    ]
    for col, title, ylabel, fname in chart_specs:
        if col in modes_df.columns:
            save_bar(modes_df[col], title, ylabel, out_dir / fname)

    # --- Combined overview image with all cross-mode bar charts ---
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 12))
    axes = axes.flatten()
    slots = [
        ("rtp", "RTP by Mode", "RTP"),
        ("m2m", "Mean-to-Median by Mode", "M2M"),
        ("std", "Std Dev by Mode", "Std Dev"),
        ("prob_nil", "Nil Probability by Mode", "Probability"),
        ("prob_less_bet", "Payout < Bet by Mode", "Probability"),
    ]
    idx = 0
    for col, title, ylabel in slots:
        if col in modes_df.columns:
            render_bar_on_axis(axes[idx], modes_df[col], title, ylabel)
            idx += 1
    if idx < len(axes):
        ax = axes[idx]
        ax.axis("off")
        ax.text(
            0.02, 0.98,
            "Overview:\n• Bars share the same mode index\n• M2M + Std Dev ≈ volatility\n• Nil & <Bet show dryness",
            va="top", ha="left", fontsize=10
        )
    plt.tight_layout()
    plt.savefig(out_dir / "combined_overview.png")
    plt.close(fig)

    # --- Load per-mode Excel + per-mode charts + HR curves ---
    xls = pd.ExcelFile(args.excel)
    export_rows = []
    # For a combined overlay of curves
    overlay_curves = []  # list of (mode_name, x_grid, y_grid_image_path)

    for sheet in xls.sheet_names:
        raw = pd.read_excel(xls, sheet_name=sheet)
        cleaned = clean_mode_sheet(raw)
        if cleaned.empty:
            continue

        tmp = cleaned.copy()
        tmp.insert(0, "mode", sheet)
        export_rows.append(tmp)

        # Individual per-mode plots
        if "Hit Rates" in cleaned.columns:
            save_xy(
                cleaned["mid"],
                cleaned["Hit Rates"],
                f"{sheet}: Hit Rate by Win Multiplier (midpoint)",
                "Win multiplier (range midpoint)",
                "Hit rate (1 in N)",
                out_dir / f"{sheet}_hit_rate_by_range.png",
            )
        if "RTP Allocation" in cleaned.columns:
            save_xy(
                cleaned["mid"],
                cleaned["RTP Allocation"],
                f"{sheet}: RTP Allocation by Win Multiplier (midpoint)",
                "Win multiplier (range midpoint)",
                "RTP allocation (share)",
                out_dir / f"{sheet}_rtp_alloc_by_range.png",
            )

        # Combined per-mode 1x2 image
        cols_have = [
            "Hit Rates" in cleaned.columns,
            "RTP Allocation" in cleaned.columns
        ]
        if any(cols_have):
            fig2, axs2 = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
            if "Hit Rates" in cleaned.columns:
                render_xy_on_axis(
                    axs2[0], cleaned["mid"], cleaned["Hit Rates"],
                    f"{sheet}: Hit Rate vs Multiplier", "Multiplier (mid)", "Hit rate (1 in N)"
                )
            else:
                axs2[0].axis("off")
            if "RTP Allocation" in cleaned.columns:
                render_xy_on_axis(
                    axs2[1], cleaned["mid"], cleaned["RTP Allocation"],
                    f"{sheet}: RTP Allocation vs Multiplier", "Multiplier (mid)", "RTP share"
                )
            else:
                axs2[1].axis("off")
            plt.tight_layout()
            plt.savefig(out_dir / f"{sheet}_combined.png")
            plt.close(fig2)

        # NEW: Per-mode HR curve (payout vs per-spin probability)
        max_win = None
        if sheet in modes_df.index and "max_win" in modes_df.columns:
            max_win = float(modes_df.loc[sheet, "max_win"])
        min_plot_payout = 1.0  # tweak: hide sub-1× spike in the thresholded view
        curve_ok = save_hr_curve_advanced(
            sheet, cleaned, max_win, out_dir,
            num_points=args.curve_points,
            logy=True,
            min_payout=min_plot_payout
        )
        # record for overlay if we can reconstruct the grid easily
        if curve_ok:
            # Recompute grid quickly to overlay without reloading image
            mids = cleaned["mid"].to_numpy()
            hrs = cleaned["Hit Rates"].to_numpy()
            valid = np.isfinite(mids) & np.isfinite(hrs) & (hrs > 0)
            mids = mids[valid]
            hrs = hrs[valid]
            order = np.argsort(mids)
            mids = mids[order]
            probs = (1.0 / hrs[order])
            if not np.isfinite(max_win) or max_win is None or max_win <= 0:
                max_win = max(1.0, float(np.nanmax(mids)))
            x_grid = np.linspace(0.0, max_win, args.curve_points)
            y_grid = np.interp(x_grid, mids, probs, left=probs[0], right=probs[-1])
            overlay_curves.append((sheet, x_grid, y_grid))

    # Export combined CSV
    if export_rows:
        combined = pd.concat(export_rows, ignore_index=True)
        (out_dir.parent / "win_range_distributions_combined.csv").write_text(
            combined.to_csv(index=False)
        )

    # NEW: Combined overlay of all modes' HR curves
    if overlay_curves:
        # Align curves to a common x-grid up to the global max
        global_max = max([c[1][-1] for c in overlay_curves])
        x_common = np.linspace(0.0, global_max, args.curve_points)
        plt.figure(figsize=(12, 5))
        for mode_name, x_g, y_g in overlay_curves:
            # Resample each curve to x_common
            y_common = np.interp(x_common, x_g, y_g, left=y_g[0], right=y_g[-1])
            plt.plot(x_common, y_common, label=mode_name)
        plt.title("Per-Spin Probability vs Payout (all modes)")
        plt.xlabel("Payout (x bet)")
        plt.ylabel("Per-spin probability (1 / Hit Rate)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(out_dir / "combined_hr_curves.png")
        plt.close()

    if args.show.strip() == "1":
        plt.show()


if __name__ == "__main__":
    main()
