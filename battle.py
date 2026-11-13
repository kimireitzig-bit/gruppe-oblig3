"""Battle module for the battle simulator.

Contains the ``Battle`` class, which runs turn-based combat between two characters.
INF201 Deliverable 3, NMBU 2026.
"""

from character import Character


class Battle:
    """Turn-based combat between a hero and an enemy, fought until one of them dies."""

    def __init__(
        self, hero: Character, enemy: Character, verbose: bool = True, max_rounds: int = 1000
    ) -> None:
        """
        Initialise the Battle.

        Args:
            hero (Character): The character that attacks first in every round.
            enemy (Character): The character that attacks second.
            verbose (bool): If True, print a log of every attack (default = True).
            max_rounds (int): Safety limit. If neither character can hurt the other
                (e.g. armor higher than all damage), the battle ends in a draw after this
                many rounds instead of looping forever (default = 1000).
        """
        for role, character in (("hero", hero), ("enemy", enemy)):
            if not isinstance(character, Character):
                raise TypeError(f"{role} must be a Character, got {type(character).__name__}")
        if hero is enemy:
            raise ValueError("hero and enemy must be two different characters")
        if not isinstance(max_rounds, int) or isinstance(max_rounds, bool) or max_rounds < 1:
            raise ValueError(f"max_rounds must be a positive int, got {max_rounds!r}")

        self._hero = hero
        self._enemy = enemy
        self.verbose = verbose
        self.max_rounds = max_rounds
        self._rounds_played = 0

    @property
    def hero(self) -> Character:
        """The character that attacks first (read-only)."""
        return self._hero

    @property
    def enemy(self) -> Character:
        """The character that attacks second (read-only)."""
        return self._enemy

    @property
    def rounds_played(self) -> int:
        """Number of rounds played so far (read-only)."""
        return self._rounds_played

    @property
    def is_over(self) -> bool:
        """True when at least one of the characters is no longer alive."""
        return not (self.hero.is_alive and self.enemy.is_alive)

    @property
    def winner(self) -> Character | None:
        """The surviving character, or None if the battle is not decided."""
        if self.hero.is_alive and not self.enemy.is_alive:
            return self.hero
        if self.enemy.is_alive and not self.hero.is_alive:
            return self.enemy
        return None

    def _log(self, message: str) -> None:
        """Print ``message`` only if the battle is verbose."""
        if self.verbose:
            print(message)

    def _attack(self, attacker: Character, defender: Character) -> None:
        """Let ``attacker`` attack ``defender`` and log what happened."""
        description = attacker.next_attack_description()
        dealt = attacker.attack(defender)
        self._log(
            f"  {attacker.name} attacks {defender.name} with {description} "
            f"and deals {dealt} damage."
        )

    def play_round(self) -> None:
        """
        Play one round: the hero attacks the enemy, and if the enemy is still alive,
        the enemy attacks the hero.

        Raises:
            RuntimeError: If the battle is already over.
        """
        if self.is_over:
            raise RuntimeError("The battle is already over")
        self._rounds_played += 1
        self._log(f"Round {self.rounds_played}")

        self._attack(self.hero, self.enemy)
        if self.enemy.is_alive:
            self._attack(self.enemy, self.hero)

        self._log(
            f"  -> {self.hero.name}: {self.hero.status} | {self.enemy.name}: {self.enemy.status}"
        )

    def simulate_battle(self) -> Character | None:
        """
        Play rounds until one character is no longer alive.

        Returns:
            Character | None: The winner, or None if the battle hit ``max_rounds``
            without a winner (a draw).
        """
        self._log(f"=== {self.hero.name} vs {self.enemy.name} ===")
        self._log(f"Hero:  {self.hero}")
        self._log(f"Enemy: {self.enemy}")

        while self.hero.is_alive and self.enemy.is_alive:
            if self.rounds_played >= self.max_rounds:
                self._log(f"No winner after {self.max_rounds} rounds - it's a draw!")
                return None
            self.play_round()

        winner = self.winner
        if winner is not None:
            self._log(
                f"*** {winner.name} wins after {self.rounds_played} rounds "
                f"with {winner.hp}/{winner.hp_max} HP left! ***"
            )
        return winner
