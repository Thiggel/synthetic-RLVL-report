from pathlib import Path
import textwrap

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


def generation_excerpt(samples, label_fragment, max_chars=92):
    row = samples[samples["label"].str.contains(label_fragment, regex=False)].iloc[0]
    generation = " ".join(str(row["generation"]).split())
    if len(generation) > max_chars:
        generation = generation[:max_chars].rstrip() + " ..."
    answer = str(row["answer"])
    if answer.startswith("<") or len(answer) > 24:
        answer = "missing"
    return (
        f"gold={row['gold']} | answer={answer} | valid={int(row['valid'])}\n"
        f"{generation}"
    )


def overview_claim():
    main = pd.read_csv(TABLES / "main_olmo7b_summary.csv")
    attr = pd.read_csv(TABLES / "active_paired_partial_by_seed.csv")
    trace = pd.read_csv(TABLES / "trace_control_ablation_by_seed.csv")
    samples = pd.read_csv(TABLES / "sample_generation_snippets.csv")

    logic = main[(main["template"].eq("logic")) & (main["train_max"].eq(25))].iloc[0]
    nl = main[(main["template"].eq("nl_exact")) & (main["train_max"].eq(25))].iloc[0]
    attr25 = attr[(attr["family"].eq("hard_attribute_fresh")) & (attr["train_max"].eq(25))]
    attr_logic = attr25[attr25["template"].eq("logic")]
    attr_nl = attr25[attr25["template"].eq("nl_exact")]
    invalid = trace[trace["template"].eq("invalid_logic")]

    fig = plt.figure(figsize=(8.4, 5.55))
    gs = fig.add_gridspec(
        2,
        2,
        height_ratios=[0.95, 1.05],
        width_ratios=[1.02, 0.98],
        wspace=0.42,
        hspace=0.58,
    )
    ax_design = fig.add_subplot(gs[0, 0])
    ax_gap = fig.add_subplot(gs[0, 1])
    ax_valid = fig.add_subplot(gs[1, 0])
    ax_examples = fig.add_subplot(gs[1, 1])

    # A. Design.
    ax_design.axis("off")
    ax_design.set_title("A. Same proof, different trace language", loc="left", fontweight="bold")
    boxes = [
        (0.04, 0.38, 0.32, 0.34, "same prompt\nsame answer\nsame latent\nproof", "#F5F7FB"),
        (0.58, 0.62, 0.38, 0.20, "compact formal\ntrace", "#E8EFFB"),
        (0.58, 0.25, 0.38, 0.20, "controlled natural\nlanguage trace", "#E7F5F1"),
    ]
    for x, y, w, h, txt, color in boxes:
        ax_design.add_patch(
            plt.Rectangle((x, y), w, h, facecolor=color, edgecolor="#777777", linewidth=0.8)
        )
        ax_design.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=8.4)
    ax_design.annotate("", xy=(0.58, 0.72), xytext=(0.36, 0.57), arrowprops=dict(arrowstyle="->", lw=1.25, color=GRAY))
    ax_design.annotate("", xy=(0.58, 0.35), xytext=(0.36, 0.52), arrowprops=dict(arrowstyle="->", lw=1.25, color=GRAY))
    ax_design.text(0.04, 0.12, "Only the trace substrate changes.", fontsize=8.6, color=GRAY)
    ax_design.set_xlim(0, 1)
    ax_design.set_ylim(0, 1)

    # B. Main depth-50 answer gap.
    width = 0.26
    bp_center = 0.0
    attr_center = 1.05
    ax_gap.bar(bp_center - width / 2, pct(logic["depth50_correct@16"]), width, yerr=pct(logic["depth50_correct@16_std"]), color=LOGIC, label="Formal", capsize=3)
    ax_gap.bar(bp_center + width / 2, pct(nl["depth50_correct@16"]), width, yerr=pct(nl["depth50_correct@16_std"]), color=NL, label="Natural", capsize=3)
    for offset, values, color in [
        (-width / 2, attr_logic["depth50_correct@16"], LOGIC),
        (width / 2, attr_nl["depth50_correct@16"], NL),
    ]:
        xs = np.full(len(values), attr_center + offset)
        ax_gap.scatter(xs, pct(values), s=31, color=color, edgecolor="white", linewidth=0.7, zorder=3)
        ax_gap.hlines(pct(values.mean()), attr_center + offset - 0.10, attr_center + offset + 0.10, color=color, linewidth=2.5)
    ax_gap.set_xticks([bp_center, attr_center])
    ax_gap.set_xticklabels(["BranchProof\nmean $\\pm$ sd", "AttrCon\nseed dots"])
    ax_gap.set_title("B. Formal traces win at depth 50", loc="left", fontweight="bold")
    clean_axes(ax_gap)
    ax_gap.legend(frameon=False, loc="upper right", fontsize=8)
    ax_gap.text(bp_center, 95, f"+{100*(logic['depth50_correct@16']-nl['depth50_correct@16']):.1f}", ha="center", fontsize=8, color=GRAY)

    # C. Faithfulness caveat.
    labels = ["Compact\nformal", "Invalid\nformal"]
    corr = [logic["depth50_correct@16"], invalid["depth50_correct@16"].mean()]
    corr_std = [logic["depth50_correct@16_std"], invalid["depth50_correct@16"].std()]
    joint = [logic["depth50_joint@16"], invalid["depth50_formal_joint@16"].mean()]
    joint_std = [logic["depth50_joint@16_std"], invalid["depth50_formal_joint@16"].std()]
    x = np.arange(len(labels))
    ax_valid.bar(x - width / 2, pct(corr), width, yerr=pct(corr_std), color=LOGIC, label="Correct answer", capsize=3)
    ax_valid.bar(x + width / 2, pct(joint), width, yerr=pct(joint_std), color=RED, label="Correct + valid proof", capsize=3)
    ax_valid.set_xticks(x)
    ax_valid.set_xticklabels(labels)
    ax_valid.set_title("C. Correct answers need not be valid proofs", loc="left", fontweight="bold")
    clean_axes(ax_valid, ylabel="pass@16 rate (%)")
    ax_valid.legend(frameon=False, loc="upper right", fontsize=8)

    # D. Representative sample excerpts.
    ax_examples.axis("off")
    ax_examples.set_title("D. Samples expose success and truncation", loc="left", fontweight="bold")
    snippets = [
        ("Formal depth-50 success", generation_excerpt(samples, "OLMo-7B logic train1..25 depth-50"), LOGIC),
        ("Natural depth-50 failure", generation_excerpt(samples, "OLMo-7B NL train1..25 depth-50"), NL),
    ]
    y = 0.86
    for title, body, color in snippets:
        ax_examples.text(0.02, y, title, color=color, fontsize=9, fontweight="bold", va="top")
        wrapped = "\n".join(textwrap.wrap(body, width=39, break_long_words=False))
        ax_examples.text(0.04, y - 0.10, wrapped, fontsize=8.2, family="monospace", va="top")
        y -= 0.39
    ax_examples.text(0.02, 0.03, "Excerpts come from sample_generation_snippets.csv. Metrics use 16 samples per prompt.", fontsize=7.4, color=GRAY)

    fig.suptitle(
        "Formal traces improve extrapolative answers, but proof validity remains a separate target",
        fontsize=10.5,
        fontweight="bold",
        y=1.02,
    )
    fig.subplots_adjust(left=0.07, right=0.98, bottom=0.08, top=0.90, wspace=0.42, hspace=0.60)
    save(fig, "overview_claim", tight_kwargs=False)


def main_correctness():
    df = pd.read_csv(TABLES / "main_olmo7b_summary.csv")
    df = df[df["template"].isin(["logic", "nl_exact"])].copy()
    labels = {"logic": "Formal logic", "nl_exact": "Natural language"}
    colors = {"logic": LOGIC, "nl_exact": NL}

    fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.1), sharey=True)
    for ax, metric, title in [
        (axes[0], "ood_correct@16", "Long-depth band pass@16"),
        (axes[1], "depth50_correct@16", "Depth-50 endpoint pass@16"),
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
        (axes[0], "ood_correct@16", "Hard-depth band pass@16"),
        (axes[1], "depth50_correct@16", "Depth-50 endpoint pass@16"),
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
    ax.set_title("Depth-50 pass@16 after shortcut-rich training")
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
    ]:
        sub = trace[trace["template"].eq(template)]
        rows.append((label, sub["ood_correct@16"].mean(), sub["ood_correct@16"].std(), color))

    labels, means, stds, colors = zip(*rows)
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    ax.bar(x, pct(means), yerr=pct(stds), color=colors, edgecolor="white", capsize=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Long-depth pass@16 for syntax controls")
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
    clean_axes(ax, ylabel="pass@16 rate (%)")
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
        (axes[0], "ood_correct@16", "Long-depth band pass@16"),
        (axes[1], "depth50_correct@16", "Depth-50 endpoint pass@16"),
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
    ax.bar(x + width / 2, pct([r[3] for r in rows]), width, yerr=pct([r[4] for r in rows]), label="Depth-50", color=[r[5] for r in rows], alpha=0.55, capsize=3)
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
    ax.set_title("Depth-50 pass@16 across model families")
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
    overview_claim()
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
