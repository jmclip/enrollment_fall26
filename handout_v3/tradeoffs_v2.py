"""Emotional/educational cost vs. yearly savings for budget options. Edit options.csv (cost_score is a
PLACEHOLDER until the group scores it) and rerun. Made with help from Claude (AI); please verify."""
from pathlib import Path
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from adjustText import adjust_text
import textwrap

HERE = Path(__file__).parent
df = pd.read_csv(Path("options_v2.csv"))
df["mid"] = (df.savings_low_m + df.savings_high_m) / 2
COLORS = {"Buildings": "#B34700", "Classes & staff": "#0060A8", "Administration": "#8A3B8F",
          "Revenue & partners": "#007A55"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 16})
fig, ax = plt.subplots(figsize=(12.5, 13.5))
XMAX, YMAX = 2.6, 10
ax.plot([0, XMAX], [0, YMAX], ls="--", color="#bdbdbd", lw=2, zorder=1)
ax.text(XMAX * 0.985, YMAX * 0.965, "equal trade-off", color="#8a8a8a", fontsize=13,
        ha="right", va="top", rotation=45, rotation_mode="anchor")
texts = []
for _, r in df.iterrows():
    label = textwrap.fill(r.label, 15)
    texts.append(ax.text(r.mid, r.cost_score, label, linespacing=1.0, color=COLORS[r.category], fontsize=16,
                         fontweight="bold", ha="center", va="center", zorder=3))
ax.set_xlim(0, XMAX); ax.set_ylim(0, YMAX); ax.set_aspect(XMAX / YMAX)
fig.canvas.draw()
adjust_text(texts, ax=ax, target_x=df["mid"].values, target_y=df["cost_score"].values,
            expand=(1.03, 1.15), only_move={"text": "y", "static": "y", "explode": "y", "pull": "y"},
            ensure_inside_axes=True, iter_lim=3000,
            arrowprops=dict(arrowstyle="-", color="#b0b0b0", lw=1, shrinkA=6, shrinkB=0))
ax.set_xlabel("Estimated yearly savings ($ millions, midpoint of range)", fontsize=18, labelpad=10)
ax.set_ylabel("Emotional / educational cost  (0 = low, 10 = high)", fontsize=18, labelpad=10)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:.1f}M" if v else "$0"))
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color("#999"); ax.spines["bottom"].set_color("#999")
ax.tick_params(colors="#444", labelsize=15)
ax.grid(color="#eeeeee", lw=1); ax.set_axisbelow(True)
handles = [plt.Line2D([], [], ls="", marker="s", ms=14, color=c, label=k) for k, c in COLORS.items()]
ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=15, ncol=4, bbox_to_anchor=(-0.01, 1.0),
          handletextpad=0.3, columnspacing=1.2)
plt.tight_layout(rect=(0, 0.02, 1, 1))
fig.savefig("img/options.png", dpi=150, bbox_inches="tight", pad_inches=0.3)
