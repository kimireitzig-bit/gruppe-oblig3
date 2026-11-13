# Use of generative AI - Deliverable 3

> **Draft - edit before submitting.** This file was drafted by the AI tool itself. The parts in
> _italics with brackets_ must be filled in by us, and everything else should be checked so it
> matches what we actually did.

## Tool

- **Claude Code** (Anthropic, model Claude Opus 5.5), used through the Claude desktop app on
  13 November 2026.

## What we asked for

We gave Claude Code the assignment notebook (`deliverable_03-1.ipynb`) and the starting code
(`game_simulator_v1.py`) and asked for help completing the deliverable before the deadline.

## What the AI produced

- The modules `dice.py`, `items.py`, `character.py` and `battle.py` (Tasks 1-5), including input
  validation, read-only properties and docstrings.
- The tests in `test_game.py` (44 `pytest` tests, all passing).
- The notebook `deliverable_03_battle_simulator.ipynb`: the class presentations, the example
  battles, the 10 000-battle statistics and the first draft of the discussion of results.
- `README.md`, `requirements.txt`, the PDF export, and this draft.

Design choices the AI made that were not specified in the assignment, which we should be able to
explain:

- `take_damage()`, `heal()` and `attack()` return how much HP actually changed.
- A dead character cannot be healed and cannot attack.
- Negative damage/healing raises `ValueError`, so `take_damage(-50)` cannot secretly heal.
- `Battle` has a `max_rounds` limit (default 1000) so a battle where nobody can deal damage ends in
  a draw instead of an infinite loop.
- The interpretation of the `__call__` task: `d20()` does the same as `d20.roll()`.

## Summary of the chat log

1. **"Can you help me with this deliverable that is due today?"** Claude Code read the assignment notebook
   and `game_simulator_v1.py`, and created a new virtual environment. It then wrote the four modules and
   44 tests, ran the tests, and built and ran the notebook. It exported the notebook to PDF, checked the
   pages, and fixed two layout problems it found: code lines were cut off, and a placeholder disappeared.
   It also wrote `README.md`, `requirements.txt` and this draft.
2. **Git:** we said we would handle git and GitHub ourselves. Claude gave us the commands for `git init`,
   committing, pushing and making `git_log.txt`, and suggested that both of us make commits.
3. **"What do we deliver?"** Claude listed the hand-in requirements from the assignment and which file
   covers each one.
4. **"Is AI use allowed?"** Claude pointed out that the assignment asks for a discussion of GenAI use, so
   it is expected as long as it is disclosed, and told us to check the course's own GenAI rules. It then
   wrote `TEAMMATE_HANDOFF.md` (a to-do list and a two-part plan for the video), added this summary, and
   packed the files into a zip to share within the group.

## What we checked and changed ourselves

_[Fill in: e.g. which parts we read through line by line, which tests we ran, anything we changed,
rewrote or disagreed with, and anything we added ourselves.]_

## Reflection

_[Fill in: what worked well, what did not, what we learned about encapsulation, inheritance and
composition, and whether we understand the code well enough to explain it in the video.]_
