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


def label_last_point(ax, x, y, text, color, dx=0.45, dy=0.0):
    ax.text(x + dx, y + dy, text, color=color, va="center", ha="left", fontsize=8)


def draw_seed_line(
    ax,
    df,
    x_col,
    y_col,
    template,
    color,
    label,
    marker,
    jitter_width=1.0,
    label_dx=0.45,
    group_col="template",
    linestyle="-",
    linewidth=2.1,
    alpha=1.0,
    label_dy=0.0,
):
    sub = df[df[group_col].eq(template)].copy()
    grouped = sub.groupby(x_col)[y_col].mean().reset_index().sort_values(x_col)
    ax.plot(
        grouped[x_col],
        pct(grouped[y_col]),
        color=color,
        marker=marker,
        linewidth=linewidth,
        markersize=5.5,
        label=label,
        linestyle=linestyle,
        alpha=alpha,
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
    if label_dx is not None:
        label_last_point(
            ax,
            grouped[x_col].iloc[-1],
            pct(grouped[y_col].iloc[-1]),
            label,
            color,
            dx=label_dx,
            dy=label_dy,
        )


def connected_category_plot(ax, rows, line_color="#444444", seed_width=0.16):
    """Draw a compact connected-point plot for categorical comparisons."""
    x = np.arange(len(rows))
    means = [np.mean(values) for _, values, _, _ in rows]
    ax.plot(x, pct(means), color=line_color, linewidth=1.45, alpha=0.75, zorder=1)
    for xi, (_, values, color, marker) in zip(x, rows):
        ax.plot(
            [xi],
            [pct(np.mean(values))],
            marker=marker,
            markersize=6.8,
            color=color,
            linestyle="None",
            zorder=4,
        )
        if len(values) > 1:
            offsets = np.linspace(-seed_width / 2, seed_width / 2, len(values))
            for offset, value in zip(offsets, values):
                ax.scatter(
                    xi + offset,
                    pct(value),
                    marker=marker,
                    s=21,
                    facecolor="white",
                    edgecolor=color,
                    linewidth=0.9,
                    alpha=0.9,
                    zorder=3,
                )
    ax.set_xticks(x)
    ax.set_xticklabels([label for label, _, _, _ in rows])


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
    branch = endpoint_rows_from_main()
    attr = pd.read_csv(TABLES / "active_paired_partial_by_seed.csv")
    trace = pd.read_csv(TABLES / "trace_control_ablation_by_seed.csv")
    samples = pd.read_csv(TABLES / "sample_generation_snippets.csv")

    branch25 = branch[branch["train_max"].eq(25)]
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
    task_x = np.array([0.0, 1.0])
    task_labels = ["BranchProof\ndepth 50", "AttrCon\ndepth 50"]
    for template, attr_sub, color, marker, label in [
        ("logic", attr_logic, LOGIC, "o", "Formal"),
        ("nl_exact", attr_nl, NL, "s", "Natural"),
    ]:
        branch_sub = branch25[branch25["template"].eq(template)]
        means = [branch_sub["depth50_correct@16"].mean(), attr_sub["depth50_correct@16"].mean()]
        ax_gap.plot(task_x, pct(means), color=color, marker=marker, linewidth=2.1, markersize=5.8, label=label)
        for xi, values in zip(task_x, [branch_sub["depth50_correct@16"], attr_sub["depth50_correct@16"]]):
            offsets = np.linspace(-0.035, 0.035, len(values))
            for offset, value in zip(offsets, values):
                ax_gap.scatter(
                    xi + offset,
                    pct(value),
                    marker=marker,
                    s=22,
                    facecolor="white",
                    edgecolor=color,
                    linewidth=0.9,
                    alpha=0.9,
                    zorder=3,
                )
    bp_gap = (
        branch25[branch25["template"].eq("logic")]["depth50_correct@16"].mean()
        - branch25[branch25["template"].eq("nl_exact")]["depth50_correct@16"].mean()
    )
    ax_gap.text(0.0, 94, f"+{100 * bp_gap:.1f}", ha="center", fontsize=8, color=GRAY)
    ax_gap.set_xticks(task_x)
    ax_gap.set_xticklabels(task_labels)
    ax_gap.set_title("B. Depth-50 gap is large, but task-dependent", loc="left", fontweight="bold")
    clean_axes(ax_gap)
    ax_gap.legend(frameon=False, loc="upper right", fontsize=8)
    ax_gap.set_xlim(-0.25, 1.25)

    # C. Faithfulness caveat.
    labels = ["Compact\nformal", "Invalid\nformal"]
    compact = branch25[branch25["template"].eq("logic")]
    corr_values = [compact["depth50_correct@16"].to_numpy(), invalid["depth50_correct@16"].to_numpy()]
    joint_values = [compact["depth50_joint@16"].to_numpy(), invalid["depth50_formal_joint@16"].to_numpy()]
    corr = [values.mean() for values in corr_values]
    joint = [values.mean() for values in joint_values]
    x = np.arange(len(labels))
    ax_valid.plot(x, pct(corr), color=LOGIC, marker="o", linewidth=2.1, markersize=5.8, label="Correct answer")
    ax_valid.plot(x, pct(joint), color=RED, marker="D", linewidth=2.1, markersize=5.4, label="Correct + valid proof")
    for xi, values in zip(x, corr_values):
        for offset, value in zip(np.linspace(-0.035, 0.035, len(values)), values):
            ax_valid.scatter(xi + offset, pct(value), marker="o", s=21, facecolor="white", edgecolor=LOGIC, linewidth=0.9, zorder=3)
    for xi, values in zip(x, joint_values):
        for offset, value in zip(np.linspace(-0.035, 0.035, len(values)), values):
            ax_valid.scatter(xi + offset, pct(value), marker="D", s=21, facecolor="white", edgecolor=RED, linewidth=0.9, zorder=3)
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
    save(fig, "shortcut_robustness")


def syntax_controls():
    rows = []
    main = endpoint_rows_from_main()
    same_token = pd.read_csv(TABLES / "same_target_token_budget_by_seed.csv")
    compact = main[(main["template"].eq("logic")) & (main["train_max"].eq(25))]
    natural = main[(main["template"].eq("nl_exact")) & (main["train_max"].eq(25))]
    rows.append(("Compact\nformal", compact["ood_correct@16"].to_numpy(), LOGIC, "o"))
    rows.append(("Same-token\nformal", same_token[same_token["template"].eq("logic")]["ood_correct@16"].to_numpy(), LOGIC_LIGHT, "^"))
    for path, label, color, marker in [
        ("logic_wordified_eval_by_seed.csv", "Wordified\nformal", LOGIC_LIGHT, "D"),
        ("logic_symbol_padded_eval_by_seed.csv", "Symbol\npadded", LOGIC_LIGHT, "^"),
    ]:
        df = pd.read_csv(TABLES / path)
        rows.append((label, df["ood_correct@16"].to_numpy(), color, marker))
    rows.append(("Natural\nlanguage", natural["ood_correct@16"].to_numpy(), NL, "s"))
    rows.append(("Same-token\nnatural", same_token[same_token["template"].eq("nl_exact")]["ood_correct@16"].to_numpy(), NL_LIGHT, "v"))
    trace = pd.read_csv(TABLES / "trace_control_ablation_by_seed.csv")
    for template, label, color, marker in [
        ("rule_annotated_nl", "Rule labels\nin NL", NL_LIGHT, "P"),
        ("pseudocode", "Pseudocode", LIGHT_GRAY, "X"),
    ]:
        sub = trace[trace["template"].eq(template)]
        rows.append((label, sub["ood_correct@16"].to_numpy(), color, marker))

    fig, ax = plt.subplots(figsize=(7.9, 3.2))
    connected_category_plot(ax, rows)
    ax.axhline(pct(compact["ood_correct@16"].mean()), color=LOGIC, linewidth=1.0, linestyle=":", alpha=0.55)
    ax.axhline(pct(natural["ood_correct@16"].mean()), color=NL, linewidth=1.0, linestyle=":", alpha=0.55)
    ax.set_title("Most controls fall below the compact formal baseline")
    clean_axes(ax)
    ax.set_xlim(-0.4, len(rows) - 0.6)
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
    fig, ax = plt.subplots(figsize=(5.1, 3.1))
    corr = [np.mean(r[1]) for r in rows]
    joint = [np.mean(r[2]) for r in rows]
    ax.plot(x, pct(corr), marker="o", markersize=5.8, linewidth=2.1, color=LOGIC, label="Correct answer")
    ax.plot(x, pct(joint), marker="D", markersize=5.3, linewidth=2.1, color=RED, label="Correct + valid proof")
    for xi, (_, corr_values, joint_values) in zip(x, rows):
        for offset, value in zip(np.linspace(-0.05, 0.05, len(corr_values)), corr_values):
            ax.scatter(xi + offset, pct(value), marker="o", s=21, facecolor="white", edgecolor=LOGIC, linewidth=0.9, zorder=3)
        for offset, value in zip(np.linspace(-0.05, 0.05, len(joint_values)), joint_values):
            ax.scatter(xi + offset, pct(value), marker="D", s=21, facecolor="white", edgecolor=RED, linewidth=0.9, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Invalid traces keep answers but lose validity")
    clean_axes(ax, ylabel="pass@16 rate (%)")
    ax.legend(frameon=False, loc="upper right")
    save(fig, "trace_integrity")


def hybrids():
    main = endpoint_rows_from_main()
    hybrid = pd.read_csv(TABLES / "hybrid_order_ablation_by_seed.csv")
    fig, ax = plt.subplots(figsize=(4.9, 3.15))
    draw_seed_line(ax, main, "train_max", "depth50_correct@16", "logic", LOGIC, "Formal only", "o", label_dx=0.55, linestyle="--", linewidth=1.8, alpha=0.85)
    draw_seed_line(ax, main, "train_max", "depth50_correct@16", "nl_exact", NL, "Natural only", "s", label_dx=0.55, linestyle="--", linewidth=1.8, alpha=0.85, label_dy=-1.5)
    draw_seed_line(ax, hybrid, "train_max", "depth50_correct@16", "formal_think", LOGIC_LIGHT, "Formal then NL", "^", label_dx=0.55, group_col="mode", label_dy=2.0)
    draw_seed_line(ax, hybrid, "train_max", "depth50_correct@16", "think_formal", NL_LIGHT, "NL then formal", "D", label_dx=0.55, group_col="mode", label_dy=-2.0)
    ax.set_xlabel("Maximum training depth")
    ax.set_title("Hybrids trail formal-only extrapolation")
    clean_axes(ax)
    ax.set_xlim(3.5, 34.0)
    save(fig, "hybrid_order")


def conditioned_dual():
    main = endpoint_rows_from_main()
    dual = pd.read_csv(TABLES / "conditioned_dual_50k_by_seed.csv")
    fig, ax = plt.subplots(figsize=(4.9, 3.15))
    draw_seed_line(ax, main, "train_max", "depth50_correct@16", "logic", LOGIC, "Formal only", "o", label_dx=0.55, linestyle="--", linewidth=1.8, alpha=0.85)
    draw_seed_line(ax, main, "train_max", "depth50_correct@16", "nl_exact", NL, "Natural only", "s", label_dx=0.55, linestyle="--", linewidth=1.8, alpha=0.85, label_dy=-4.0)
    draw_seed_line(ax, dual, "train_max", "depth50_correct@16", "conditioned_logic", LOGIC_LIGHT, "Dual, formal prompt", "^", label_dx=0.55, group_col="eval_template", label_dy=2.0)
    draw_seed_line(ax, dual, "train_max", "depth50_correct@16", "conditioned_nl", NL_LIGHT, "Dual, NL prompt", "D", label_dx=0.55, group_col="eval_template", label_dy=5.0)
    ax.set_xlabel("Maximum training depth")
    ax.set_title("Dual training still trails formal-only")
    clean_axes(ax)
    ax.set_xlim(3.5, 34.0)
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
