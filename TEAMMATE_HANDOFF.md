# Handoff: INF201 Deliverable 3 (due 13 Nov 2026)

## Already done

- **Code:** `dice.py`, `items.py`, `character.py` (`Character`, `Warrior`, `Mage`), `battle.py`. Covers Tasks 1-5.
- **Tests:** `test_game.py`, 44 pytest tests, all passing.
- **Notebook:** `deliverable_03_battle_simulator.ipynb`, already run with no errors. It presents every class,
  runs 5 example battles (with and without weapons), simulates each match-up 10 000 times and discusses the results.
- **PDF:** `deliverable_03_battle_simulator.pdf` (19 pages). Has to be exported again once names and link are added.
- **Other files:** `requirements.txt`, `README.md`, `.gitignore`, and `GENAI_USE.md` (a draft with two
  sections left for us to fill in).

## Still to do

- [ ] **Names and GitHub link:** replace the placeholders in the first cell of the notebook. Then export the
      PDF again (see below).
- [ ] **GitHub repo:** create it and push everything. `.gitignore` already leaves out `.venv/`. Commits from
      both of us if possible, since the log shows who committed.
- [ ] **Git log:** after the last commit, run
      `git log --graph --pretty=format:"%h - %an, %ar : %s" > git_log.txt`
- [ ] **GENAI_USE.md:** both of us read it and fill in the two bracketed sections (what we checked or changed,
      and our reflection).
- [ ] **Video:** about 5 minutes, and both of us must be in it. Each person records their own part, then we
      edit them together (see the plan below).
- [ ] **Submit (one person):** the files in the table at the bottom, plus the GitHub link and the video.

## How to run it

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
jupyter notebook
```

The notebook uses `random.seed(201)`, so **Kernel → Restart & Run All** gives the same numbers every time,
and they match the discussion text.

## How to export the PDF again

1. In Jupyter: **File → Save and Export Notebook As → HTML**.
2. Open the HTML file in a browser, press **Ctrl+P**, choose **Save as PDF**, and save it as
   `deliverable_03_battle_simulator.pdf`.

## Video plan (~5 min, two parts)

Free ways to record and edit: Windows 11 has **Clipchamp** (screen + webcam recording and editing) and the
Xbox Game Bar (**Win+Alt+R**). On Mac: **Cmd+Shift+5**. A phone recording works too.

### Part 1, about 2.5 min: overview and Tasks 1-3

1. **Intro:** what the project is, and the file structure (one module per class).
2. **Task 1, encapsulation:** in the original code `attack()` changed the target's `_hp` directly, which is bad
   form. Now `attack()` calls `target.take_damage()`, so each object only changes its own HP. `hp` and
   `is_alive` are read-only properties. Show the notebook cell where setting `hp` raises `AttributeError`.
   `heal()` never goes above `hp_max`.
3. **Task 2, Dice:** `roll()` uses `random.randint`. `__repr__` gives `Dice(sides=6)`. `__call__` makes `d20()`
   work. Fewer than 2 sides raises an error. Show the fairness histogram.
4. **Task 3, Weapon:** composition, meaning a character *has a* weapon and the weapon *has a* die. A weapon
   replaces the base damage, so a d4 dagger (mean 2.5) is worse than bare hands (10).

### Part 2, about 2.5 min: Tasks 4-5 and results

1. **Task 4, inheritance:** `Warrior` overrides `take_damage()` so armor reduces each hit, and calls
   `super()`. `Mage` overrides `attack()`: a spell costs 10 mana and deals double damage, otherwise it does a
   normal attack and gets 5 mana back. Show the cell with 9 mage attacks (3 spells, then weapon, weapon,
   spell, ...).
2. **Task 5, Battle:** `play_round()` (hero first, enemy only if still alive) and `simulate_battle()` (a `while`
   loop until someone dies). `max_rounds` makes a battle nobody can win end in a draw. Show Battle 3
   (Warrior + Greatsword vs Mage + Staff).
3. **Results table:**
   - Attacking first is a big advantage: identical mages give the hero 95 % wins.
   - A weapon is not always better than bare hands.
   - Armor 5 makes the d6 staff almost useless.
   - Possible fix: decide who starts with a dice roll.
4. **GenAI:** one sentence on how we used it (see `GENAI_USE.md`).

## What to upload

| What | File |
|---|---|
| Python scripts | `dice.py`, `items.py`, `character.py`, `battle.py`, `test_game.py` |
| Notebook and its PDF | `deliverable_03_battle_simulator.ipynb`, `deliverable_03_battle_simulator.pdf` |
| Git log and GitHub link | `git_log.txt`, plus the link in the notebook or the submission text |
| GenAI discussion | `GENAI_USE.md` |
| Video | the file or a link to it |

The GitHub repo must also contain `requirements.txt`. Do not upload `.venv/`.
