# Data Visualization: Group Homework 3

My group keeps its work for Group Homework 3 of the Data Visualization course in this repository. In this homework, my group audits the six charts of the GoMart Operations Report 2025, redesigns them, tests the redesigns for every reader, and runs a perception experiment with real people. GoMart is a made-up online grocery service, and all of its data is simulated.

Team name: Team 10, after the team number on the LMS list. The file for the hand-in is saved as `GH3_Team10.ipynb`.

## Members and branches

Each member works on their own branch.

| Member | Branch |
|---|---|
| Nguyễn Hoàng Minh (leader) | `hwinh` |
| Phạm Quang Minh | `quang-minh` |
| Phạm Tuấn Anh | `tuan-anh` |
| Trần Nhã Đoan | `nha-doan` |
| Nguyễn Minh Nguyệt | `minh-nguyet` |
| Trần Nguyễn Thanh Thảo | `thao` |

## How my group works together

A member never pushes to `dev` or `main` directly. A member pushes to their own branch and then opens a pull request into `dev`. The leader reads the pull request and merges it. When my group is ready to hand in the work, the leader opens a pull request from `dev` into `main`.

GitHub enforces these rules for us:

- The `main` branch accepts pull requests only from `dev`, and only the repository owner can merge them. Nobody can push to `main` directly, and the owner cannot either.
- The `dev` branch accepts changes only through pull requests. Every member can open one, and only the repository owner can merge it.
- A pull request into `main` from any other branch fails the check named `chi-nhan-tu-dev`. A pull request into `main` that a member opens is also closed automatically.
- Nobody can delete a member branch.

### Steps for a member

First, download the repository and switch to your own branch. The example below uses the branch `thao`.

```bash
git clone https://github.com/hwinhwork-dot/DataViz_Day03_Group.git
cd DataViz_Day03_Group
git checkout thao
```

Before you start working, pull the newest work from `dev`.

```bash
git pull origin dev
```

When you finish a piece of work, save it and push it to your own branch.

```bash
git add .
git commit -m "Short description of the change"
git push origin thao
```

Last, open GitHub, go to Pull requests, and choose New pull request. Set the base branch to `dev` and the compare branch to your own branch.

## What my group hands in

| File | Task |
|---|---|
| `homework/gh3_gomart/GH3_TeamName.ipynb` | Tasks 0 to 6, with the memo at the top. It starts from `homework03_starter.ipynb`. |
| `homework/gh3_gomart/experiment_answers.csv` | Task 4: one row per estimate, with the columns `respondent, encoding, item, true, judged, collector`. It holds 19 respondents: the collected ones and the simulated ones (see below). |
| `homework/gh3_gomart/evidence/` | Task 4: photos of the paper sheets or the form export with time stamps. Task 0: the photo of the hand sketch. |
| `homework/gh3_gomart/charts/` | Task 2: the six redesigned charts as PNG files, so that the lecturer can check them without running the notebook. Task 0: the original Figure 5 of the NSO report and my group's redesign. The last cell of Task 2 saves all of them except the original screenshot. Task 5: `task5_one_page.png`, which the cell of Task 5 saves. |

We do not hand in the GoMart files.

## The data of Task 4

`experiment_answers.csv` has one row per estimate and 12 estimates for each respondent. It holds 19 respondents: the respondents that my group collected and the simulated respondents that fill the table up to 19.

**Collected respondents.** They come from the members of my group, and the column `collector` shows who collected each one. The first two collectors typed numbers into the CSV. The others typed their answers in the shared survey sheet, and `scripts/build_experiment_answers.py` turns them into rows. The script multiplies a fraction of the marked value by 100 (3/4 becomes 75) and reads a number with a decimal comma as a decimal point. The notebook lists the three decisions about odd answers in section 4.2.

**Simulated respondents.** They have the codes `sim-R01` and so on and the collector `simulated`. For every item the script takes the answer of a randomly chosen collected respondent, changes it by about 5% and rounds it. These rows have no sheet in `evidence/` and add no new information. The notebook shows every result of Task 4 with and without them, and its interpretation relies on the collected respondents.

The script keeps every row of the CSV that is not simulated and rebuilds the rest. To replace simulated respondents with real ones, add the real rows to the CSV under the collector's own name and run the script again: it only simulates the respondents that are still missing up to 19 (`N_TOTAL`). Run it from the root of the repository:

```bash
python scripts/build_experiment_answers.py
```

## Folders

```
.
├── homework/
│   └── gh3_gomart/   the hand-in set: the notebook, experiment_answers.csv, evidence/ and charts/
├── scripts/          build_experiment_answers.py, which builds experiment_answers.csv
├── data/
│   ├── raw/          the five GoMart files from the LMS, which we never edit
│   └── bad_charts/   the six charts of the intern report as PNG files, for the audit
└── requirements.txt  The Python packages that we use
```

The five GoMart files are `gomart_orders_2025_clean.csv`, `gomart_districts.csv`, `gomart_targets_2025.csv`, `gomart_bad_report.pdf` and `gomart_bad_report.py`. The Setup cell of the starter reads the CSV files from the folder of the notebook, so inside the repository it has to point to `data/raw/`.

We keep `data/raw/` and `data/bad_charts/` in the repository so that every member works with the same files. They are not part of the hand-in, so we do not upload them to the LMS.

## Setup

The commands below create a virtual environment and install the packages.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```
