"""Build homework/gh3_gomart/experiment_answers.csv for Task 4 (team 10).

Step 1  Read the answers that group members collected on paper or in the shared survey sheet.
        - tuan-anh and minh-nguyet (and any other collector except quang-minh, thao and simulated): the rows
          already in the CSV (not changed).
        - quang-minh: typed as fractions of the reference value (1/5 means 20), see QUANG_MINH below.
        - thao: typed as numbers with a decimal comma (16,67), see THAO below.
        - hwinh: three respondents of the team leader, to be added to TYPED when the answers are typed.
Step 2  Add placeholder respondents for the people we could not collect in time. They are simulated
        from the errors of the collected respondents, and they are labelled everywhere:
        respondent code `sim-R01` ... and collector `simulated`.

Run from the root of the repository:  python scripts/build_experiment_answers.py
"""
import re
from fractions import Fraction
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "homework" / "gh3_gomart" / "experiment_answers.csv"
TEAM_NUMBER = 10
N_TOTAL = 19                      # respondents in the hand-in table: collected + simulated
SEED = 2026                       # fixed, so that the simulated rows are the same every time

PANELS = {"bars": "ABCDE", "pie": "ABCDE", "bubbles": "ABCDE"}


def true_values(team_number=TEAM_NUMBER):
    """Same draw as make_stimuli() in the notebook: the true values of the three panels."""
    rng = np.random.default_rng(1000 + team_number)
    truth = {}
    for kind in PANELS:
        v = np.round(rng.uniform(10, 90, 5))
        v[rng.integers(5)] = 100
        truth[kind] = dict(zip("ABCDE", v.astype(int).tolist()))
    return truth


TRUTH = true_values()
ITEMS = {k: [L for L in "ABCDE" if TRUTH[k][L] != 100] for k in PANELS}      # the four unmarked items

# ---------------------------------------------------------------------------------------------
# Quang Minh: tabs "People 1", "People 2", "People 3". The answer is a fraction of the marked value.
# Typed exactly as in the sheet, in the order of ITEMS (bars: A B D E, pie: A B C E, bubbles: B C D E).
# Two entries needed a decision (see the notes in README.md):
#   People 2, bubbles B: the sheet says "8", which cannot be a fraction, so we read it as 8 (of 100).
#   People 3, bars: the sheet says "C = 7/8" but C is the marked bar, so we read it as D.
# ---------------------------------------------------------------------------------------------
QUANG_MINH = {
    "R01": {"bars": ["1/5", "1/2", "2/5", "7/10"], "pie": ["1/3", "7/10", "1/5", "1/4"],
            "bubbles": ["3/10", "9/10", "3/5", "4/5"]},
    "R02": {"bars": ["1/6", "1/2", "7/8", "5/6"], "pie": ["1/3", "2/3", "1/5", "1/4"],
            "bubbles": ["8%", "1", "3/4", "5/6"]},
    "R03": {"bars": ["1/6", "1/2", "7/8", "3/4"], "pie": ["1/3", "1/2", "1/8", "1/4"],
            "bubbles": ["3/10", "1/8", "4/5", "9/10"]},
}

# Thao: tab "Thao". Numbers on the 0 to 100 scale with a decimal comma. The text in brackets in the sheet
# says how the respondent got the number (for example "3/4B"); we keep only the number. Thao surveyed six
# people. In her second table, columns 4 to 6 repeat column 3 to the last digit. We keep all six, and the
# notebook also shows the results without the repeats.
THAO = {
    "R01": {"bars": ["10", "50", "90", "80"], "pie": ["50", "60", "20", "30"], "bubbles": ["10", "100", "90", "95"]},
    "R02": {"bars": ["16,666", "50", "86", "75"], "pie": ["50,25", "66,67", "17", "33"],
            "bubbles": ["20", "100", "75", "80"]},
    "R03": {"bars": ["16,67", "50", "83,33", "75"], "pie": ["50", "66,67", "25", "33"],
            "bubbles": ["20", "100", "66,67", "75"]},
}
for code in ("R04", "R05", "R06"):
    THAO[code] = THAO["R03"]


def to_number(text, fraction_scale):
    """'7/8' -> 87.5, '1' -> 100 (fractions of the marked value); '16,67' -> 16.67 (already on the 0-100 scale)."""
    text = text.strip()
    if text.endswith("%"):                                    # an explicit percent: keep it as typed
        return float(text[:-1].replace(",", "."))
    if fraction_scale:
        return round(float(Fraction(text) * 100), 2)
    return round(float(text.replace(",", ".")), 2)


def rows_from_typed(table, collector, fraction_scale):
    rows = []
    for code, panels in table.items():
        for kind, answers in panels.items():
            assert len(answers) == len(ITEMS[kind]), (collector, code, kind)
            for item, text in zip(ITEMS[kind], answers):
                rows.append((f"{collector}-{code}", kind, item, TRUTH[kind][item],
                             to_number(text, fraction_scale), collector))
    return rows


COLUMNS = ["respondent", "encoding", "item", "true", "judged", "collector"]

# (collector, typed answers, are the answers fractions of the marked value?)
# To add the three respondents of the team leader: HWINH = {"R01": {"bars": [...], "pie": [...], "bubbles": [...]}, ...}
# and append ("hwinh", HWINH, False) to this list (True if they typed fractions).
TYPED = [("quang-minh", QUANG_MINH, True), ("thao", THAO, False)]


def collected_table():
    """Collected respondents: the rows already in the CSV, then the typed answers of the other collectors."""
    old = pd.read_csv(CSV)
    # every row that is not simulated and not rebuilt below stays as it is, so a new real respondent can be added to the CSV
    keep = old[~old["collector"].isin(["simulated"] + [who for who, _, _ in TYPED])]
    new = pd.DataFrame([row for who, table, fractions in TYPED for row in rows_from_typed(table, who, fractions)],
                       columns=COLUMNS)
    table = pd.concat([keep, new], ignore_index=True)
    # every `true` value must be the value on the printed sheet
    expected = table.apply(lambda r: TRUTH[r["encoding"]][r["item"]], axis=1)
    assert (table["true"] == expected).all(), "a true value differs from the stimulus sheet"
    return table


def simulate(collected, n_new, seed=SEED):
    """Placeholder respondents, built from the collected ones. For every item, a simulated respondent
    takes the answer of a randomly chosen collected respondent and changes it a little (about 5% on
    average), then rounds it the way people answer (to the nearest 5, sometimes to the nearest 1).
    The answers keep the pattern of the real ones, including the large misjudgements, but they add no
    new information about the world: they only fill the table."""
    rng = np.random.default_rng(seed)
    pool = collected.groupby(["encoding", "item"])["judged"].apply(list).to_dict()
    rows = []
    for i in range(n_new):
        code = f"sim-R{i + 1:02d}"
        for kind in PANELS:
            for item in ITEMS[kind]:
                base = rng.choice(pool[(kind, item)])
                raw = base * np.exp(rng.normal(0, 0.05))
                step = 5 if rng.random() < 0.7 else 1
                judged = int(np.clip(round(raw / step) * step, 1, 100))
                rows.append((code, kind, item, TRUTH[kind][item], judged, "simulated"))
    return pd.DataFrame(rows, columns=COLUMNS)


def main():
    collected = collected_table()
    n_collected = collected["respondent"].nunique()
    sim = simulate(collected, max(0, N_TOTAL - n_collected))
    table = pd.concat([collected, sim], ignore_index=True)
    table["judged"] = pd.Series([int(x) if float(x).is_integer() else float(x) for x in table["judged"]],
                                index=table.index, dtype=object)                       # write 20, not 20.0
    table.to_csv(CSV, index=False)
    print(f"{n_collected} collected + {sim['respondent'].nunique()} simulated = {table['respondent'].nunique()} respondents, "
          f"{len(table)} rows -> {CSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
