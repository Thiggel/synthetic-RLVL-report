from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PREPRINT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "tables"
OUT = PREPRINT / "figures"

LOGIC = "#2E5AA8"
NL = "#2A9D8F"
LOGIC_LIGHT = "#86A5E5"
NL_LIGHT = "#7BC8B8"
GRAY = "#555555"
RED = "#B85042"
GOLD = "#C28E2C"


def pct(x):
    return 100.0 * np.asarray(x, dtype=float)


def clean_axes(ax, ylabel="Accuracy (%)", ylim=(0, 105)):
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=240, bbox_inches="tight")
    plt.close(fig)


def main_correctness():
    df = pd.read_csv(TABLES / "main_olmo7b_summary.csv")
    df = df[df["template"].isin(["logic", "nl_exact"])].copy()
    labels = {"logic": "Formal logic", "nl_exact": "Natural language"}
    colors = {"logic": LOGIC, "nl_exact": NL}

    fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.1), sharey=True)
    for ax, metric, title in [
        (axes[0], "ood_correct@16", "Long-depth band"),
        (axes[1], "depth50_correct@16", "Depth-50 endpoint"),
    ]:
        for template in ["logic", "nl_exact"]:
            sub = df[df["template"] == template].sort_values("train_max")
            ax.plot(
                sub["train_max"],
                pct(sub[metric]),
                marker="o",
                linewidth=2.2,
                color=colors[template],
                label=labels[template],
            )
            ax.fill_between(
                sub["train_max"],
                pct(sub[metric] - sub[f"{metric}_std"]),
                pct(sub[metric] + sub[f"{metric}_std"]),
                color=colors[template],
                alpha=0.17,
                linewidth=0,
            )
        ax.set_title(title)
        ax.set_xlabel("Maximum training depth")
        clean_axes(ax)
    axes[0].legend(frameon=False, loc="lower right")
    save(fig, "main_correctness")


def attribute_correctness():
    df = pd.read_csv(TABLES / "active_paired_partial_by_seed.csv")
    df = df[df["family"].eq("hard_attribute_fresh")].copy()
    df["template"] = df["template"].replace({"nl_exact": "nl"})
    g = (
        df.groupby(["template", "train_max"])[["ood_correct@16", "depth50_correct@16"]]
        .agg(["mean", "std"])
        .reset_index()
    )
    g.columns = ["_".join(c).strip("_") for c in g.columns]

    fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.1), sharey=True)
    for ax, metric, title in [
        (axes[0], "ood_correct@16", "Hard-depth band"),
        (axes[1], "depth50_correct@16", "Depth-50 endpoint"),
    ]:
        for template, color, label in [("logic", LOGIC, "Formal logic"), ("nl", NL, "Natural language")]:
            sub = g[g["template"].eq(template)].sort_values("train_max")
            ax.plot(
                sub["train_max"],
                pct(sub[f"{metric}_mean"]),
                marker="o",
                linewidth=2.2,
                color=color,
                label=label,
            )
            ax.fill_between(
                sub["train_max"],
                pct(sub[f"{metric}_mean"] - sub[f"{metric}_std"]),
                pct(sub[f"{metric}_mean"] + sub[f"{metric}_std"]),
                color=color,
                alpha=0.17,
                linewidth=0,
            )
        ax.set_title(title)
        ax.set_xlabel("Maximum training depth")
        clean_axes(ax)
    axes[0].legend(frameon=False, loc="lower right")
    save(fig, "attribute_correctness")


def shortcut_robustness():
    df = pd.read_csv(TABLES / "shortcut_rate_ablation_by_seed.csv")
    df["rate"] = df["shortcut_rate"].str.replace("p", ".", regex=False).astype(float)
    g = (
        df.groupby(["template", "rate"])[["depth50_correct@16"]]
        .agg(["mean", "std"])
        .reset_index()
    )
    g.columns = ["_".join(c).strip("_") for c in g.columns]

    fig, ax = plt.subplots(figsize=(4.7, 3.15))
    for template, color, label in [("logic", LOGIC, "Formal logic"), ("nl_exact", NL, "Natural language")]:
        sub = g[g["template"].eq(template)].sort_values("rate")
        ax.plot(
            pct(sub["rate"]),
            pct(sub["depth50_correct@16_mean"]),
            marker="o",
            linewidth=2.4,
            color=color,
            label=label,
        )
        ax.fill_between(
            pct(sub["rate"]),
            pct(sub["depth50_correct@16_mean"] - sub["depth50_correct@16_std"]),
            pct(sub["depth50_correct@16_mean"] + sub["depth50_correct@16_std"]),
            color=color,
            alpha=0.18,
            linewidth=0,
        )
    ax.set_xlabel("Shortcut-marker rate in training (%)")
    ax.set_title("Depth 50 correctness under shortcut distractors")
    clean_axes(ax)
    ax.legend(frameon=False, loc="lower left")
    save(fig, "shortcut_robustness")


def syntax_controls():
    rows = []
    main = pd.read_csv(TABLES / "main_olmo7b_summary.csv")
    for template, label in [("logic", "Logic"), ("nl_exact", "NL")]:
        sub = main[(main["template"].eq(template)) & (main["train_max"].eq(25))].iloc[0]
        rows.append((label, sub["ood_correct@16"], sub["ood_correct@16_std"], LOGIC if template == "logic" else NL))
    for path, label, color in [
        ("logic_wordified_eval_by_seed.csv", "Wordified\nlogic", LOGIC_LIGHT),
        ("logic_symbol_padded_eval_by_seed.csv", "Symbol-\npadded", LOGIC_LIGHT),
    ]:
        df = pd.read_csv(TABLES / path)
        rows.append((label, df["ood_correct@16"].mean(), df["ood_correct@16"].std(), color))
    trace = pd.read_csv(TABLES / "trace_control_ablation_by_seed.csv")
    for template, label, color in [
        ("pseudocode", "Pseudo-\ncode", GRAY),
        ("rule_annotated_nl", "Rule-\nannotated NL", NL_LIGHT),
        ("terse_nl", "Terse\nNL", NL_LIGHT),
    ]:
        sub = trace[trace["template"].eq(template)]
        rows.append((label, sub["ood_correct@16"].mean(), sub["ood_correct@16"].std(), color))

    labels, means, stds, colors = zip(*rows)
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    ax.bar(x, pct(means), yerr=pct(stds), color=colors, edgecolor="white", capsize=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Surface syntax controls at maximum training depth")
    clean_axes(ax)
    save(fig, "syntax_controls")


def trace_integrity():
    rows = []
    main = pd.read_csv(TABLES / "main_olmo7b_summary.csv")
    logic = main[(main["template"].eq("logic")) & (main["train_max"].eq(25))].iloc[0]
    rows.append(("Valid\nlogic", logic["ood_correct@16"], logic["ood_correct@16_std"], logic["ood_joint@16"], logic["ood_joint@16_std"]))
    trace = pd.read_csv(TABLES / "trace_control_ablation_by_seed.csv")
    for template, label in [("invalid_logic", "Invalid\nlogic"), ("shuffled_logic", "Shuffled\nlogic")]:
        sub = trace[trace["template"].eq(template)]
        rows.append(
            (
                label,
                sub["ood_correct@16"].mean(),
                sub["ood_correct@16"].std(),
                sub["ood_formal_joint@16"].mean(),
                sub["ood_formal_joint@16"].std(),
            )
        )
    labels = [r[0] for r in rows]
    x = np.arange(len(labels))
    width = 0.36
    fig, ax = plt.subplots(figsize=(5.1, 3.1))
    ax.bar(x - width / 2, pct([r[1] for r in rows]), width, yerr=pct([r[2] for r in rows]), label="Correct", color=LOGIC, capsize=3)
    ax.bar(x + width / 2, pct([r[3] for r in rows]), width, yerr=pct([r[4] for r in rows]), label="Correct + valid", color=RED, capsize=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Correctness is not the same as proof validity")
    clean_axes(ax)
    ax.legend(frameon=False, loc="upper right")
    save(fig, "trace_integrity")


def hybrids():
    main = pd.read_csv(TABLES / "main_olmo7b_summary.csv")
    hybrid = pd.read_csv(TABLES / "hybrid_order_ablation_by_seed.csv")
    hg = (
        hybrid.groupby(["mode", "train_max"])[["ood_correct@16", "depth50_correct@16"]]
        .agg(["mean", "std"])
        .reset_index()
    )
    hg.columns = ["_".join(c).strip("_") for c in hg.columns]

    fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.1), sharey=True)
    for ax, metric, title in [
        (axes[0], "ood_correct@16", "Long-depth band"),
        (axes[1], "depth50_correct@16", "Depth-50 endpoint"),
    ]:
        for template, color, label in [("logic", LOGIC, "Logic only"), ("nl_exact", NL, "NL only")]:
            sub = main[main["template"].eq(template)].sort_values("train_max")
            ax.plot(sub["train_max"], pct(sub[metric]), linestyle="--", marker="o", linewidth=1.9, color=color, label=label)
            ax.fill_between(sub["train_max"], pct(sub[metric] - sub[f"{metric}_std"]), pct(sub[metric] + sub[f"{metric}_std"]), color=color, alpha=0.10, linewidth=0)
        for mode, color, label in [("formal_think", LOGIC, "Formal first hybrid"), ("think_formal", NL, "NL first hybrid")]:
            sub = hg[hg["mode"].eq(mode)].sort_values("train_max")
            ax.plot(sub["train_max"], pct(sub[f"{metric}_mean"]), marker="s", linewidth=2.2, color=color, label=label)
            ax.fill_between(sub["train_max"], pct(sub[f"{metric}_mean"] - sub[f"{metric}_std"]), pct(sub[f"{metric}_mean"] + sub[f"{metric}_std"]), color=color, alpha=0.16, linewidth=0)
        ax.set_title(title)
        ax.set_xlabel("Maximum training depth")
        clean_axes(ax)
    axes[0].legend(frameon=False, fontsize=8, loc="lower right")
    save(fig, "hybrid_order")


def conditioned_dual():
    main = pd.read_csv(TABLES / "main_olmo7b_summary.csv")
    dual = pd.read_csv(TABLES / "conditioned_dual_50k_by_seed.csv")
    rows = []
    for template, label, color in [("logic", "Logic\nonly", LOGIC), ("nl_exact", "NL\nonly", NL)]:
        sub = main[(main["template"].eq(template)) & (main["train_max"].eq(25))].iloc[0]
        rows.append((label, sub["ood_correct@16"], sub["ood_correct@16_std"], sub["depth50_correct@16"], sub["depth50_correct@16_std"], color))
    for template, label, color in [("conditioned_logic", "Dual,\nlogic prompt", LOGIC_LIGHT), ("conditioned_nl", "Dual,\nNL prompt", NL_LIGHT)]:
        sub = dual[(dual["eval_template"].eq(template)) & (dual["train_max"].eq(25))]
        rows.append((label, sub["ood_correct@16"].mean(), sub["ood_correct@16"].std(), sub["depth50_correct@16"].mean(), sub["depth50_correct@16"].std(), color))

    labels = [r[0] for r in rows]
    x = np.arange(len(labels))
    width = 0.36
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    ax.bar(x - width / 2, pct([r[1] for r in rows]), width, yerr=pct([r[2] for r in rows]), label="Long-depth", color=[r[5] for r in rows], alpha=0.95, capsize=3)
    ax.bar(x + width / 2, pct([r[3] for r in rows]), width, yerr=pct([r[4] for r in rows]), label="Depth 50", color=[r[5] for r in rows], alpha=0.55, capsize=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Conditioned dual training does not recover each single modality")
    clean_axes(ax)
    ax.legend(frameon=False, loc="upper right")
    save(fig, "conditioned_dual")


def architecture():
    df = pd.read_csv(TABLES / "architecture_ablation_summary.csv")
    df = df[df["model"].isin(["OLMo-7B", "Qwen-2.5-1.5B", "Qwen-2.5-7B", "Gemma-3-4B"])]
    df = df[df["train_max"].eq(25)]
    models = ["OLMo-7B", "Qwen-2.5-1.5B", "Qwen-2.5-7B", "Gemma-3-4B"]
    x = np.arange(len(models))
    width = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 3.15))
    for offset, template, label, color in [(-width / 2, "logic", "Formal logic", LOGIC), (width / 2, "nl_exact", "Natural language", NL)]:
        sub = df[df["template"].eq(template)].set_index("model").reindex(models)
        ax.bar(x + offset, pct(sub["depth50_correct@16"]), width, yerr=pct(sub["depth50_correct@16_std"]), label=label, color=color, capsize=3)
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=15, ha="right")
    ax.set_title("Depth 50 correctness across model families")
    clean_axes(ax)
    ax.legend(frameon=False, loc="upper right")
    save(fig, "architecture_depth50")


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
    main_correctness()
    attribute_correctness()
    shortcut_robustness()
    syntax_controls()
    trace_integrity()
    hybrids()
    conditioned_dual()
    architecture()


if __name__ == "__main__":
    main()
