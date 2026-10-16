"""Recreate compact figures from regression results transcribed in the report.

The raw Nielsen and SafeGraph inputs and original estimation code are not included.
This script visualizes reported table values; it does not re-estimate the models.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "reported_results.csv"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA)

# First-stage strength reported in the project tables.
first = df[df.section.eq("first_stage")].copy()
fig, ax = plt.subplots(figsize=(8.2, 4.6))
colors = ["#17807E" if x >= 10 else "#D18B32" for x in first.first_stage_f_stat]
bars = ax.bar(first.event, first.first_stage_f_stat, color=colors, width=.68)
ax.axhline(10, color="#687381", linestyle="--", linewidth=1.2, label="Reference line: F = 10")
ax.set_ylabel("Reported first-stage F-statistic")
ax.set_title("Local team participation predicted event ratings unevenly")
ax.set_ylim(0, max(first.first_stage_f_stat) * 1.18)
ax.tick_params(axis="x", rotation=12)
ax.legend(frameon=False, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)
for bar, value in zip(bars, first.first_stage_f_stat):
    ax.text(bar.get_x() + bar.get_width()/2, value + 4, f"{value:g}", ha="center", va="bottom", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "first_stage_strength.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# Same transformed outcome, contrasting 1-day and 7-day windows.
second = df[df.section.eq("second_stage") & df.outcome.isin([
    "Log(1 + next-day footprint)", "Log(1 + 7-day footprint)"
])].copy()
order = ["Super Bowl", "NBA Finals", "Stanley Cup Finals", "World Series"]
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.5), sharey=False)
for ax, outcome, title in zip(
    axes,
    ["Log(1 + next-day footprint)", "Log(1 + 7-day footprint)"],
    ["Next day", "Seven day window"],
):
    part = second[second.outcome.eq(outcome)].set_index("event").loc[order]
    y = range(len(order))
    ci = 1.96 * part.std_error.to_numpy()
    ax.errorbar(part.estimate, y, xerr=ci, fmt="o", color="#176B87", ecolor="#6F8791",
                capsize=3, markersize=6, linewidth=1.4)
    ax.axvline(0, color="#9AA4AD", linewidth=1, linestyle="--")
    ax.set_yticks(list(y), order)
    ax.invert_yaxis()
    ax.set_title(title)
    ax.set_xlabel("Coefficient (95% CI)")
    ax.spines[["top", "right"]].set_visible(False)
fig.suptitle("Reported IV estimates for log(1 + dealership footprint)", y=1.02, fontsize=13)
fig.tight_layout()
fig.savefig(OUT / "reported_iv_estimates.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print(f"Wrote figures to {OUT}")
