"""Dice module for the battle simulator.

Contains the ``Dice`` class, which models an n-sided die (n >= 2).
INF201 Deliverable 3, NMBU 2026.
"""

import random


class Dice:
    """An n-sided die that can be rolled to produce a random integer from 1 to n."""

    def __init__(self, sides: int = 6) -> None:
        """
        Initialise the Dice.

        Args:
            sides (int): Number of sides on the die, must be at least 2 (default = 6).

        Raises:
            TypeError: If ``sides`` is not an integer.
            ValueError: If ``sides`` is smaller than 2.
        """
        if not isinstance(sides, int) or isinstance(sides, bool):
            raise TypeError(f"sides must be an int, got {type(sides).__name__}")
        if sides < 2:
            raise ValueError(f"A dice must have at least 2 sides, got {sides}")
        self._sides = sides  # private: the number of sides cannot change after creation

    @property
    def sides(self) -> int:
        """Read-only number of sides on the die."""
        return self._sides

    def roll(self) -> int:
        """Roll the die and return a random integer between 1 and ``sides`` (inclusive)."""
        return random.randint(1, self.sides)

    def __call__(self) -> int:
        """Make the die callable, so ``d20()`` is the same as ``d20.roll()``."""
        return self.roll()

    def __repr__(self) -> str:
        """Representation of the die, e.g. ``Dice(sides=6)``."""
        return f"Dice(sides={self.sides})"
