from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[2]
PREPRINT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "tables"
OUT = PREPRINT / "figures"

LOGIC = "#4477AA"
NL = "#228833"
LOGIC_LIGHT = "#88AADD"
NL_LIGHT = "#66CC99"
GRAY = "#555555"


def pct(x):
    return 100.0 * np.asarray(x, dtype=float)


def clean_axes(ax, ylabel="pass@16 answer correctness (%)", ylim=(0, 105)):
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save(fig, name, tight_kwargs=None):
    OUT.mkdir(parents=True, exist_ok=True)
    if tight_kwargs is None:
        fig.tight_layout()
    elif tight_kwargs is False:
        pass
    else:
        fig.tight_layout(**tight_kwargs)
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def label_last_point(ax, x, y, text, color, dx=0.45, dy=0.0):
    ax.text(x + dx, y + dy, text, color=color, va="center", ha="left", fontsize=8)


def rounded_box(ax, xy, width, height, text, facecolor, edgecolor="#777777", fontsize=8.3):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=0.85,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
    )


def draw_seed_line(
    ax,
    df,
    x_col,
    y_col,
    template,
    color,
    label,
    label_dx=0.45,
    group_col="template",
    linestyle="-",
    linewidth=2.1,
    alpha=1.0,
    label_dy=0.0,
    band_alpha=0.16,
):
    sub = df[df[group_col].eq(template)].copy()
    grouped = (
        sub.groupby(x_col)[y_col]
        .agg(["mean", "std"])
        .reset_index()
        .sort_values(x_col)
        .fillna(0.0)
    )
    x = grouped[x_col].to_numpy(dtype=float)
    mean = pct(grouped["mean"])
    std = pct(grouped["std"])
    ax.plot(
        x,
        mean,
        color=color,
        linewidth=linewidth,
        label=label,
        linestyle=linestyle,
        alpha=alpha,
    )
    ax.fill_between(
        x,
        np.maximum(0, mean - std),
        np.minimum(100, mean + std),
        color=color,
        alpha=band_alpha,
        linewidth=0,
    )
    if label_dx is not None:
        label_last_point(
            ax,
            x[-1],
            mean[-1],
            label,
            color=color,
            dx=label_dx,
            dy=label_dy,
        )


def endpoint_rows_from_main():
    curves = pd.read_csv(TABLES / "main_olmo7b_depth_curves_k16.csv")
    rows = []
    for template in ["logic", "nl_exact"]:
        for train_max in sorted(curves[curves["template"].eq(template)]["train_max"].unique()):
            sub = curves[(curves["template"].eq(template)) & (curves["train_max"].eq(train_max))]
            for seed, seed_df in sub.groupby("seed"):
                long_depth = seed_df[seed_df["depth"].gt(train_max)]["correct"].mean()
                depth50 = seed_df[seed_df["depth"].eq(50)]["correct"].mean()
                rows.append(
                    {
                        "template": template,
                        "train_max": train_max,
                        "seed": seed,
                        "ood_correct@16": long_depth,
                        "depth50_correct@16": depth50,
                        "ood_joint@16": seed_df[seed_df["depth"].gt(train_max)]["joint"].mean(),
                        "depth50_joint@16": seed_df[seed_df["depth"].eq(50)]["joint"].mean(),
                    }
                )
    return pd.DataFrame(rows)


def overview_claim():
    branch = endpoint_rows_from_main()

    fig = plt.figure(figsize=(8.4, 3.15))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.12, 1.0], wspace=0.30)
    ax_design = fig.add_subplot(gs[0, 0])
    ax_curve = fig.add_subplot(gs[0, 1])

    ax_design.axis("off")
    ax_design.set_title("A. Paired trace intervention", loc="left", fontweight="bold")
    rounded_box(
        ax_design,
        (0.03, 0.46),
        0.23,
        0.26,
        "same input\nsame answer\nsame proof",
        "#F7F7F7",
        fontsize=8.1,
    )
    rounded_box(
        ax_design,
        (0.37, 0.65),
        0.27,
        0.18,
        "formal trace\nvalid proof",
        "#EAF1FB",
        edgecolor=LOGIC,
        fontsize=8.1,
    )
    rounded_box(
        ax_design,
        (0.37, 0.32),
        0.27,
        0.18,
        "NL trace\nprose proof",
        "#E9F6EF",
        edgecolor=NL,
        fontsize=8.1,
    )
    rounded_box(
        ax_design,
        (0.73, 0.46),
        0.24,
        0.26,
        "short-D SFT\n\nlong-D eval",
        "#F7F7F7",
        fontsize=8.0,
    )
    for y in [0.73, 0.41]:
        ax_design.annotate(
            "",
            xy=(0.37, y),
            xytext=(0.26, 0.59),
            arrowprops=dict(arrowstyle="->", lw=1.15, color=GRAY, shrinkA=4, shrinkB=4),
        )
        ax_design.annotate(
            "",
            xy=(0.73, 0.59),
            xytext=(0.64, y),
            arrowprops=dict(arrowstyle="->", lw=1.15, color=GRAY, shrinkA=4, shrinkB=4),
        )
    ax_design.text(0.37, 0.90, "intervention", fontsize=7.8, color=GRAY, ha="left")
    ax_design.text(0.73, 0.82, "extrapolation test", fontsize=7.8, color=GRAY, ha="left")
    ax_design.text(0.03, 0.18, "Only the supervised trace substrate changes.", fontsize=8.0, color=GRAY)
    ax_design.set_xlim(0, 1)
    ax_design.set_ylim(0, 1)

    for template, color, label in [
        ("logic", LOGIC, "Formal trace"),
        ("nl_exact", NL, "Natural language"),
    ]:
        draw_seed_line(
            ax_curve,
            branch,
            "train_max",
            "depth50_correct@16",
            template,
            color,
            label,
            label_dx=0.45,
            band_alpha=0.15,
        )
    bp_gap = (
        branch[(branch["template"].eq("logic")) & (branch["train_max"].eq(25))]["depth50_correct@16"].mean()
        - branch[(branch["template"].eq("nl_exact")) & (branch["train_max"].eq(25))]["depth50_correct@16"].mean()
    )
    ax_curve.text(23.6, 73.0, f"+{100 * bp_gap:.1f} pp", fontsize=8.2, color=GRAY)
    ax_curve.set_title("B. Formal traces extrapolate farther", loc="left", fontweight="bold")
    ax_curve.set_xlabel("Maximum training depth")
    clean_axes(ax_curve)
    ax_curve.set_xlim(3.5, 28.5)
    save(fig, "overview_claim")


def main_correctness():
    df = endpoint_rows_from_main()
    labels = {"logic": "Formal logic", "nl_exact": "Natural language"}
    colors = {"logic": LOGIC, "nl_exact": NL}

    fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.1), sharey=True)
    for ax, metric, title in [
        (axes[0], "ood_correct@16", "Formal traces extrapolate farther"),
        (axes[1], "depth50_correct@16", "The endpoint gap opens late"),
    ]:
        for template in ["logic", "nl_exact"]:
            draw_seed_line(ax, df, "train_max", metric, template, colors[template], labels[template])
        ax.set_title(title)
        ax.set_xlabel("Maximum training depth")
        clean_axes(ax)
        ax.set_xlim(3.5, 28.5)
    save(fig, "main_correctness")


def attribute_correctness():
    df = pd.read_csv(TABLES / "active_paired_partial_by_seed.csv")
    df = df[df["family"].eq("hard_attribute_fresh")].copy()
    df["template"] = df["template"].replace({"nl_exact": "nl"})

    fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.1), sharey=True)
    for ax, metric, title in [
        (axes[0], "ood_correct@16", "Constraint transfer is positive"),
        (axes[1], "depth50_correct@16", "Depth 50 remains high variance"),
    ]:
        for template, color, label in [("logic", LOGIC, "Formal logic"), ("nl", NL, "Natural language")]:
            draw_seed_line(ax, df, "train_max", metric, template, color, label)
        ax.set_title(title)
        ax.set_xlabel("Maximum training depth")
        clean_axes(ax)
        ax.set_xlim(3.5, 28.5)
    save(fig, "attribute_correctness")


def shortcut_robustness():
    df = pd.read_csv(TABLES / "shortcut_rate_ablation_by_seed.csv")
    df["rate"] = df["shortcut_rate"].str.replace("p", ".", regex=False).astype(float)
    baseline = endpoint_rows_from_main()
    baseline = baseline[baseline["train_max"].eq(25)][["template", "seed", "depth50_correct@16"]].copy()
    baseline["rate"] = 0.0
    df = pd.concat([baseline, df[["template", "seed", "rate", "depth50_correct@16"]]], ignore_index=True)

    fig, ax = plt.subplots(figsize=(4.7, 3.15))
    for template, color, label in [("logic", LOGIC, "Formal logic"), ("nl_exact", NL, "Natural language")]:
        draw_seed_line(ax, df, "rate", "depth50_correct@16", template, color, label, label_dx=0.03)
    ax.set_xlabel("Shortcut-marker rate in training (%)")
    ax.set_title("Formal traces resist shortcut shift")
    clean_axes(ax)
    ax.set_xticks([0, 0.3, 0.5, 0.8])
    ax.set_xticklabels(["0", "30", "50", "80"])
    ax.set_xlim(-0.08, 1.18)
    save(fig, "shortcut_robustness")


def hybrids():
    main = endpoint_rows_from_main()
    hybrid = pd.read_csv(TABLES / "hybrid_order_ablation_by_seed.csv")
    fig, ax = plt.subplots(figsize=(4.9, 3.15))
    draw_seed_line(ax, main, "train_max", "depth50_correct@16", "logic", LOGIC, "Formal only", label_dx=0.55, linestyle="--", linewidth=1.8, alpha=0.85)
    draw_seed_line(ax, main, "train_max", "depth50_correct@16", "nl_exact", NL, "Natural only", label_dx=0.55, linestyle="--", linewidth=1.8, alpha=0.85, label_dy=-1.5)
    draw_seed_line(ax, hybrid, "train_max", "depth50_correct@16", "formal_think", LOGIC_LIGHT, "Formal then NL", label_dx=0.55, group_col="mode", label_dy=2.0)
    draw_seed_line(ax, hybrid, "train_max", "depth50_correct@16", "think_formal", NL_LIGHT, "NL then formal", label_dx=0.55, group_col="mode", label_dy=-2.0)
    ax.set_xlabel("Maximum training depth")
    ax.set_title("Hybrids trail formal-only extrapolation")
    clean_axes(ax)
    ax.set_xlim(3.5, 34.0)
    save(fig, "hybrid_order")


def conditioned_dual():
    main = endpoint_rows_from_main()
    dual = pd.read_csv(TABLES / "conditioned_dual_50k_by_seed.csv")
    fig, ax = plt.subplots(figsize=(4.9, 3.15))
    draw_seed_line(ax, main, "train_max", "depth50_correct@16", "logic", LOGIC, "Formal only", label_dx=0.55, linestyle="--", linewidth=1.8, alpha=0.85)
    draw_seed_line(ax, main, "train_max", "depth50_correct@16", "nl_exact", NL, "Natural only", label_dx=0.55, linestyle="--", linewidth=1.8, alpha=0.85, label_dy=-4.0)
    draw_seed_line(ax, dual, "train_max", "depth50_correct@16", "conditioned_logic", LOGIC_LIGHT, "Dual, formal prompt", label_dx=0.55, group_col="eval_template", label_dy=2.0)
    draw_seed_line(ax, dual, "train_max", "depth50_correct@16", "conditioned_nl", NL_LIGHT, "Dual, NL prompt", label_dx=0.55, group_col="eval_template", label_dy=5.0)
    ax.set_xlabel("Maximum training depth")
    ax.set_title("Dual training still trails formal-only")
    clean_axes(ax)
    ax.set_xlim(3.5, 34.0)
    save(fig, "conditioned_dual")


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    overview_claim()
    main_correctness()
    attribute_correctness()
    shortcut_robustness()
    hybrids()
    conditioned_dual()


if __name__ == "__main__":
    main()
