"""Items module for the battle simulator.

Contains items that characters can hold. Currently only the ``Weapon`` class,
which uses a ``Dice`` object to decide how much damage it deals.
INF201 Deliverable 3, NMBU 2026.
"""

from dice import Dice


class Weapon:
    """A weapon whose damage is decided by rolling its damage dice."""

    def __init__(self, name: str, damage_dice: Dice) -> None:
        """
        Initialise the Weapon.

        Args:
            name (str): The name of the weapon, e.g. "Longsword".
            damage_dice (Dice): The die rolled to decide the damage of one attack.

        Raises:
            TypeError: If ``name`` is not a string or ``damage_dice`` is not a Dice.
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be a str, got {type(name).__name__}")
        if not isinstance(damage_dice, Dice):
            raise TypeError(f"damage_dice must be a Dice, got {type(damage_dice).__name__}")
        self.name = name
        self.damage_dice = damage_dice  # composition: a Weapon *has a* Dice

    def roll_damage(self) -> int:
        """Roll the weapon's damage dice and return the damage for one attack."""
        return self.damage_dice.roll()

    def __repr__(self) -> str:
        """Representation of the weapon, e.g. ``Weapon(name='Dagger', damage_dice=Dice(sides=4))``."""
        return f"Weapon(name={self.name!r}, damage_dice={self.damage_dice!r})"

    def __str__(self) -> str:
        """Readable description of the weapon, e.g. ``Dagger (1d4)``."""
        return f"{self.name} (1d{self.damage_dice.sides})"
