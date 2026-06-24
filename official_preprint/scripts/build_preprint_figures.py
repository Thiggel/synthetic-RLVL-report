from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PREPRINT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "tables"
OUT = PREPRINT / "figures"

LOGIC = "#4477AA"
NL = "#228833"
LOGIC_LIGHT = "#88AADD"
NL_LIGHT = "#66CC99"
GRAY = "#555555"
LIGHT_GRAY = "#B7B7B7"
RED = "#CC6677"
GOLD = "#C28E2C"
MARKERS = {"logic": "o", "nl_exact": "s", "nl": "s"}
SEED_JITTER = {3407: -0.12, 3408: 0.0, 3409: 0.12}


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


def seed_jitter(seed, width=1.0):
    return SEED_JITTER.get(int(seed), 0.0) * width


def label_last_point(ax, x, y, text, color, dx=0.45):
    ax.text(x + dx, y, text, color=color, va="center", ha="left", fontsize=8)


def draw_seed_line(ax, df, x_col, y_col, template, color, label, marker, jitter_width=1.0, label_dx=0.45):
    sub = df[df["template"].eq(template)].copy()
    grouped = sub.groupby(x_col)[y_col].mean().reset_index().sort_values(x_col)
    ax.plot(
        grouped[x_col],
        pct(grouped[y_col]),
        color=color,
        marker=marker,
        linewidth=2.1,
        markersize=5.5,
        label=label,
    )
    for _, row in sub.iterrows():
        ax.scatter(
            row[x_col] + seed_jitter(row["seed"], jitter_width),
            pct(row[y_col]),
            marker=marker,
            s=24,
            color=color,
            alpha=0.34,
            linewidth=0,
            zorder=2,
        )
    label_last_point(ax, grouped[x_col].iloc[-1], pct(grouped[y_col].iloc[-1]), label, color, dx=label_dx)


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
    ax_gap.set_title("B. Formal gap is large, but task-dependent", loc="left", fontweight="bold")
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
    df = endpoint_rows_from_main()
    labels = {"logic": "Formal logic", "nl_exact": "Natural language"}
    colors = {"logic": LOGIC, "nl_exact": NL}
    markers = {"logic": "o", "nl_exact": "s"}

    fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.1), sharey=True)
    for ax, metric, title in [
        (axes[0], "ood_correct@16", "Formal traces extrapolate farther"),
        (axes[1], "depth50_correct@16", "The endpoint gap opens late"),
    ]:
        for template in ["logic", "nl_exact"]:
            draw_seed_line(ax, df, "train_max", metric, template, colors[template], labels[template], markers[template])
        ax.set_title(title)
        ax.set_xlabel("Maximum training depth")
        clean_axes(ax)
        ax.set_xlim(3.5, 28.5)
    axes[0].legend(frameon=False, loc="lower right", fontsize=8)
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
            draw_seed_line(ax, df, "train_max", metric, template, color, label, MARKERS[template])
        ax.set_title(title)
        ax.set_xlabel("Maximum training depth")
        clean_axes(ax)
        ax.set_xlim(3.5, 28.5)
    axes[0].legend(frameon=False, loc="lower right", fontsize=8)
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
        draw_seed_line(ax, df, "rate", "depth50_correct@16", template, color, label, MARKERS[template], jitter_width=0.08, label_dx=0.03)
    ax.set_xlabel("Shortcut-marker rate in training (%)")
    ax.set_title("Formal traces resist shortcut shift")
    clean_axes(ax)
    ax.set_xticks([0, 0.3, 0.5, 0.8])
    ax.set_xticklabels(["0", "30", "50", "80"])
    ax.set_xlim(-0.08, 1.18)
    ax.legend(frameon=False, loc="lower left", fontsize=8)
    save(fig, "shortcut_robustness")


def syntax_controls():
    rows = []
    main = endpoint_rows_from_main()
    for template, label, color, marker in [("logic", "Compact\nformal", LOGIC, "o"), ("nl_exact", "Natural\nlanguage", NL, "s")]:
        sub = main[(main["template"].eq(template)) & (main["train_max"].eq(25))]
        rows.append((label, sub["ood_correct@16"].to_numpy(), color, marker))
    for path, label, color, marker in [
        ("logic_wordified_eval_by_seed.csv", "Wordified\nformal", LOGIC_LIGHT, "D"),
        ("logic_symbol_padded_eval_by_seed.csv", "Symbol\npadded", LOGIC_LIGHT, "^"),
    ]:
        df = pd.read_csv(TABLES / path)
        rows.append((label, df["ood_correct@16"].to_numpy(), color, marker))
    trace = pd.read_csv(TABLES / "trace_control_ablation_by_seed.csv")
    for template, label, color, marker in [
        ("pseudocode", "Pseudocode", LIGHT_GRAY, "v"),
        ("rule_annotated_nl", "Rule labels\nin NL", NL_LIGHT, "P"),
    ]:
        sub = trace[trace["template"].eq(template)]
        rows.append((label, sub["ood_correct@16"].to_numpy(), color, marker))

    labels = [r[0] for r in rows]
    means = [np.mean(r[1]) for r in rows]
    colors = [r[2] for r in rows]
    markers = [r[3] for r in rows]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    ax.bar(x, pct(means), color=colors, edgecolor="white", alpha=0.84)
    for xi, (_, values, color, marker) in zip(x, rows):
        for j, value in enumerate(values):
            ax.scatter(xi + [-0.10, 0.0, 0.10][j % 3], pct(value), marker=marker, s=28, color="#222222", alpha=0.75, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Compact formal syntax is the hard-to-match condition")
    clean_axes(ax)
    save(fig, "syntax_controls")


def trace_integrity():
    rows = []
    main = endpoint_rows_from_main()
    logic = main[(main["template"].eq("logic")) & (main["train_max"].eq(25))]
    rows.append(("Compact\nformal", logic["ood_correct@16"].to_numpy(), logic["ood_joint@16"].to_numpy()))
    trace = pd.read_csv(TABLES / "trace_control_ablation_by_seed.csv")
    for template, label in [("invalid_logic", "Invalid\nlogic"), ("shuffled_logic", "Shuffled\nlogic")]:
        sub = trace[trace["template"].eq(template)]
        rows.append((label, sub["ood_correct@16"].to_numpy(), sub["ood_formal_joint@16"].to_numpy()))
    labels = [r[0] for r in rows]
    x = np.arange(len(labels))
    width = 0.36
    fig, ax = plt.subplots(figsize=(5.1, 3.1))
    corr = [np.mean(r[1]) for r in rows]
    joint = [np.mean(r[2]) for r in rows]
    ax.bar(x - width / 2, pct(corr), width, label="Correct answer", color=LOGIC, alpha=0.88)
    ax.bar(x + width / 2, pct(joint), width, label="Correct + valid proof", color=RED, alpha=0.88)
    for xi, (_, corr_values, joint_values) in zip(x, rows):
        for j, value in enumerate(corr_values):
            ax.scatter(xi - width / 2 + [-0.05, 0.0, 0.05][j % 3], pct(value), marker="o", s=22, color="#222222", alpha=0.72, zorder=3)
        for j, value in enumerate(joint_values):
            ax.scatter(xi + width / 2 + [-0.05, 0.0, 0.05][j % 3], pct(value), marker="D", s=22, color="#222222", alpha=0.72, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Invalid traces keep answers but lose validity")
    clean_axes(ax, ylabel="pass@16 rate (%)")
    ax.legend(frameon=False, loc="upper right")
    save(fig, "trace_integrity")


def hybrids():
    main = endpoint_rows_from_main()
    hybrid = pd.read_csv(TABLES / "hybrid_order_ablation_by_seed.csv")
    rows = [
        ("Formal\nonly", main[(main["template"].eq("logic")) & (main["train_max"].eq(25))]["depth50_correct@16"].to_numpy(), LOGIC, "o"),
        ("Natural\nonly", main[(main["template"].eq("nl_exact")) & (main["train_max"].eq(25))]["depth50_correct@16"].to_numpy(), NL, "s"),
        ("Formal\nthen NL", hybrid[(hybrid["mode"].eq("formal_think")) & (hybrid["train_max"].eq(25))]["depth50_correct@16"].to_numpy(), LOGIC_LIGHT, "^"),
        ("NL then\nformal", hybrid[(hybrid["mode"].eq("think_formal")) & (hybrid["train_max"].eq(25))]["depth50_correct@16"].to_numpy(), NL_LIGHT, "D"),
    ]
    fig, ax = plt.subplots(figsize=(4.6, 3.15))
    x = np.arange(len(rows))
    ax.bar(x, pct([np.mean(r[1]) for r in rows]), color=[r[2] for r in rows], edgecolor="white", alpha=0.86)
    for xi, (_, values, _, marker) in zip(x, rows):
        for j, value in enumerate(values):
            ax.scatter(xi + [-0.10, 0.0, 0.10][j % 3], pct(value), marker=marker, s=30, color="#222222", alpha=0.75, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels([r[0] for r in rows])
    ax.set_title("Hybrid traces do not beat formal only")
    clean_axes(ax)
    save(fig, "hybrid_order")


def conditioned_dual():
    main = endpoint_rows_from_main()
    dual = pd.read_csv(TABLES / "conditioned_dual_50k_by_seed.csv")
    rows = []
    for template, label, color, marker in [("logic", "Formal\nonly", LOGIC, "o"), ("nl_exact", "Natural\nonly", NL, "s")]:
        sub = main[(main["template"].eq(template)) & (main["train_max"].eq(25))]
        rows.append((label, sub["depth50_correct@16"].to_numpy(), color, marker))
    for template, label, color, marker in [("conditioned_logic", "Dual,\nformal", LOGIC_LIGHT, "^"), ("conditioned_nl", "Dual,\nNL", NL_LIGHT, "D")]:
        sub = dual[(dual["eval_template"].eq(template)) & (dual["train_max"].eq(25))]
        rows.append((label, sub["depth50_correct@16"].to_numpy(), color, marker))

    labels = [r[0] for r in rows]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(4.6, 3.15))
    ax.bar(x, pct([np.mean(r[1]) for r in rows]), color=[r[2] for r in rows], edgecolor="white", alpha=0.86)
    for xi, (_, values, _, marker) in zip(x, rows):
        for j, value in enumerate(values):
            ax.scatter(xi + [-0.10, 0.0, 0.10][j % 3], pct(value), marker=marker, s=30, color="#222222", alpha=0.75, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Dual training still trails formal only")
    clean_axes(ax)
    save(fig, "conditioned_dual")


def architecture():
    df = pd.read_csv(TABLES / "architecture_ablation_summary.csv")
    df = df[df["model"].isin(["OLMo-7B", "Qwen-2.5-1.5B", "Qwen-2.5-7B", "Gemma-3-4B"])]
    df = df[df["train_max"].eq(25)]
    models = ["OLMo-7B", "Qwen-2.5-1.5B", "Qwen-2.5-7B", "Gemma-3-4B"]
    x = np.arange(len(models))
    fig, ax = plt.subplots(figsize=(7.2, 3.15))
    for offset, template, label, color, marker in [(-0.12, "logic", "Formal logic", LOGIC, "o"), (0.12, "nl_exact", "Natural language", NL, "s")]:
        sub = df[df["template"].eq(template)].set_index("model").reindex(models)
        y = pct(sub["depth50_correct@16"])
        yerr = pct(sub["depth50_correct@16_std"])
        ax.errorbar(x + offset, y, yerr=yerr, fmt=marker, markersize=6, color=color, elinewidth=1.4, capsize=3, label=label)
        ax.plot(x + offset, y, color=color, linewidth=1.2, alpha=0.45)
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=15, ha="right")
    ax.set_title("The formal direction repeats across families")
    clean_axes(ax, ylim=(0, 115))
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
