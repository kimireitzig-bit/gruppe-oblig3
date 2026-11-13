"""Character module for the battle simulator.

Contains the ``Character`` base class and its two specialisations, ``Warrior`` and
``Mage``. Builds on ``game_simulator_v1.py`` from lecture 08.
INF201 Deliverable 3, NMBU 2026.
"""

from items import Weapon


def _check_int(value, name: str, minimum: int = 0) -> None:
    """Raise TypeError/ValueError unless ``value`` is an int that is at least ``minimum``."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}, got {value}")


class Character:
    """Represents a character in the RPG."""

    def __init__(
        self, name: str, hp_max: int = 100, damage: int = 10, weapon: Weapon | None = None
    ) -> None:
        """
        Initialise the Character.

        Args:
            name (str): The name of the character.
            hp_max (int): Max hit points, must be at least 1 (default = 100).
            damage (int): Base damage dealt when attacking without a weapon (default = 10).
            weapon (Weapon | None): Optional equipped weapon (default = None).
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be a str, got {type(name).__name__}")
        _check_int(hp_max, "hp_max", minimum=1)
        _check_int(damage, "damage", minimum=0)

        self.name = name
        self._hp_max = hp_max
        self._hp = hp_max  # private: only changed through take_damage() and heal()
        self._damage = damage
        self.weapon = weapon  # goes through the property setter below, which validates it

    # ----- Properties --------------------------------------------------------------

    @property
    def hp(self) -> int:
        """Public read-only property to inspect HP without allowing direct, unsafe edits."""
        return self._hp

    @property
    def hp_max(self) -> int:
        """Read-only max HP (read-only so HP can never end up above the max)."""
        return self._hp_max

    @property
    def damage(self) -> int:
        """Read-only base damage, used when the character has no weapon equipped."""
        return self._damage

    @property
    def is_alive(self) -> bool:
        """Read-only: True if the character has more than 0 HP, False otherwise."""
        return self._hp > 0

    @property
    def weapon(self) -> Weapon | None:
        """The equipped weapon, or None if the character fights with bare hands."""
        return self._weapon

    @weapon.setter
    def weapon(self, new_weapon: Weapon | None) -> None:
        """Equip a new weapon (or None to unequip), checking that it really is a Weapon."""
        if new_weapon is not None and not isinstance(new_weapon, Weapon):
            raise TypeError(f"weapon must be a Weapon or None, got {type(new_weapon).__name__}")
        self._weapon = new_weapon

    @property
    def status(self) -> str:
        """Short status string used in battle logs, e.g. ``'84/100 HP'``."""
        return f"{self.hp}/{self.hp_max} HP"

    # ----- Health ------------------------------------------------------------------

    def take_damage(self, amount: int) -> int:
        """
        Reduce the character's *own* HP by ``amount``, never going below 0.

        Args:
            amount (int): Incoming damage, must be a non-negative int.

        Returns:
            int: The HP actually lost (can be less than ``amount`` if HP hits 0).
        """
        _check_int(amount, "amount", minimum=0)
        hp_before = self._hp
        self._hp = max(self._hp - amount, 0)
        return hp_before - self._hp

    def heal(self, amount: int) -> int:
        """
        Increase the character's HP by ``amount``, never going above ``hp_max``.

        A dead character (0 HP) cannot be healed.

        Args:
            amount (int): HP to restore, must be a non-negative int.

        Returns:
            int: The HP actually restored.
        """
        _check_int(amount, "amount", minimum=0)
        if not self.is_alive:
            return 0
        hp_before = self._hp
        self._hp = min(self._hp + amount, self._hp_max)
        return self._hp - hp_before

    # ----- Combat ------------------------------------------------------------------

    def _check_target(self, target: "Character") -> None:
        """Raise an error if ``target`` is not a valid character to attack."""
        if not isinstance(target, Character):
            raise TypeError(f"target must be a Character, got {type(target).__name__}")
        if target is self:
            raise ValueError("A character cannot attack itself")

    def _roll_attack_damage(self) -> int:
        """Damage of a normal attack: roll the weapon if one is equipped, else base damage."""
        if self.weapon is not None:
            return self.weapon.roll_damage()
        return self.damage

    def attack(self, target: "Character") -> int:
        """
        Attack the target character.

        The target's own ``take_damage()`` method is called, so this character never
        modifies the target's private ``_hp`` directly. Dead characters cannot attack.

        Args:
            target (Character): The character being attacked.

        Returns:
            int: The damage actually dealt to the target.
        """
        self._check_target(target)
        if not self.is_alive:
            return 0
        return target.take_damage(self._roll_attack_damage())

    def next_attack_description(self) -> str:
        """Describe what the next attack will be, used in battle logs."""
        if self.weapon is not None:
            return f"{self.weapon}"
        return f"bare hands ({self.damage} dmg)"

    # ----- Text representations -----------------------------------------------------

    def introduce(self) -> None:
        """Print a line that introduces the character."""
        print(f"Hi, my name is {self.name}! I am a {type(self).__name__.lower()}.")

    def _repr_fields(self) -> list[str]:
        """Fields shown in ``__repr__``. Subclasses extend this list."""
        return [
            f"name={self.name!r}",
            f"hp={self.hp}",
            f"hp_max={self.hp_max}",
            f"damage={self.damage}",
            f"weapon={self.weapon!r}",
        ]

    def _str_fields(self) -> list[str]:
        """Parts shown in ``__str__``. Subclasses extend this list."""
        weapon = str(self.weapon) if self.weapon is not None else "none"
        return [f"{self.hp}/{self.hp_max} HP", f"base damage {self.damage}", f"weapon: {weapon}"]

    def __repr__(self) -> str:
        """Representation of character object."""
        return f"{type(self).__name__}({', '.join(self._repr_fields())})"

    def __str__(self) -> str:
        """String representation of character object."""
        return f"{type(self).__name__} {self.name}: {', '.join(self._str_fields())}"


class Warrior(Character):
    """Defensive specialist: armor reduces all incoming damage."""

    def __init__(
        self,
        name: str,
        hp_max: int = 100,
        damage: int = 10,
        weapon: Weapon | None = None,
        armor: int = 5,
    ) -> None:
        """
        Initialise the Warrior.

        Args:
            name, hp_max, damage, weapon: See ``Character``.
            armor (int): Amount subtracted from every incoming hit (default = 5).
        """
        super().__init__(name, hp_max, damage, weapon)
        _check_int(armor, "armor", minimum=0)
        self._armor = armor

    @property
    def armor(self) -> int:
        """Read-only armor value."""
        return self._armor

    def take_damage(self, amount: int) -> int:
        """Reduce incoming damage by ``armor`` (not below 0) before applying it."""
        _check_int(amount, "amount", minimum=0)
        reduced = max(amount - self.armor, 0)
        return super().take_damage(reduced)

    def _repr_fields(self) -> list[str]:
        return super()._repr_fields() + [f"armor={self.armor}"]

    def _str_fields(self) -> list[str]:
        return super()._str_fields() + [f"armor {self.armor}"]


class Mage(Character):
    """Resource-based attacker: spends mana on spells that deal double damage."""

    SPELL_COST = 10  # mana spent on one spell
    MANA_REGEN = 5  # mana restored after a normal (non-spell) attack
    SPELL_MULTIPLIER = 2  # spells deal double base damage

    def __init__(
        self,
        name: str,
        hp_max: int = 100,
        damage: int = 10,
        weapon: Weapon | None = None,
        mana: int = 30,
        mana_max: int = 30,
    ) -> None:
        """
        Initialise the Mage.

        Args:
            name, hp_max, damage, weapon: See ``Character``.
            mana (int): Starting mana, between 0 and ``mana_max`` (default = 30).
            mana_max (int): Maximum mana (default = 30).
        """
        super().__init__(name, hp_max, damage, weapon)
        _check_int(mana_max, "mana_max", minimum=0)
        _check_int(mana, "mana", minimum=0)
        if mana > mana_max:
            raise ValueError(f"mana ({mana}) cannot be larger than mana_max ({mana_max})")
        self._mana_max = mana_max
        self._mana = mana

    @property
    def mana(self) -> int:
        """Read-only current mana."""
        return self._mana

    @property
    def mana_max(self) -> int:
        """Read-only max mana."""
        return self._mana_max

    @property
    def status(self) -> str:
        """Short status string including mana, e.g. ``'84/100 HP, 20/30 mana'``."""
        return f"{super().status}, {self.mana}/{self.mana_max} mana"

    def can_cast_spell(self) -> bool:
        """True if the mage has enough mana to cast a spell."""
        return self._mana >= self.SPELL_COST

    def attack(self, target: Character) -> int:
        """
        Attack the target, using a spell if there is enough mana.

        * At least ``SPELL_COST`` (10) mana: spend it on a spell dealing double base
          damage. The spell ignores any equipped weapon.
        * Otherwise: do a normal attack (with the weapon, if equipped) and restore
          ``MANA_REGEN`` (5) mana, without going above ``mana_max``.

        Returns:
            int: The damage actually dealt to the target.
        """
        self._check_target(target)
        if not self.is_alive:
            return 0
        if self.can_cast_spell():
            self._mana -= self.SPELL_COST
            return target.take_damage(self.SPELL_MULTIPLIER * self.damage)
        dealt = super().attack(target)
        self._mana = min(self._mana + self.MANA_REGEN, self._mana_max)
        return dealt

    def next_attack_description(self) -> str:
        if self.can_cast_spell():
            return f"a magic spell ({self.SPELL_MULTIPLIER * self.damage} dmg, {self.SPELL_COST} mana)"
        return super().next_attack_description()

    def _repr_fields(self) -> list[str]:
        return super()._repr_fields() + [f"mana={self.mana}", f"mana_max={self.mana_max}"]

    def _str_fields(self) -> list[str]:
        return super()._str_fields() + [f"{self.mana}/{self.mana_max} mana"]
