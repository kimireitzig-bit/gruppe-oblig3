"""Tests for the battle simulator. Run with: python -m pytest"""

import pytest

from battle import Battle
from character import Character, Mage, Warrior
from dice import Dice
from items import Weapon


class FixedDice(Dice):
    """A Dice that always rolls the same value, so tests are predictable."""

    def __init__(self, value: int, sides: int = 20) -> None:
        super().__init__(sides)
        self.value = value

    def roll(self) -> int:
        return self.value


# ----- Dice -----------------------------------------------------------------------


def test_dice_default_has_six_sides():
    assert Dice().sides == 6


def test_dice_repr():
    assert repr(Dice(sides=20)) == "Dice(sides=20)"


@pytest.mark.parametrize("sides", [0, 1, -6])
def test_dice_needs_at_least_two_sides(sides):
    with pytest.raises(ValueError):
        Dice(sides)


@pytest.mark.parametrize("sides", [6.0, "6", True])
def test_dice_sides_must_be_int(sides):
    with pytest.raises(TypeError):
        Dice(sides)


def test_dice_rolls_cover_all_faces_and_stay_in_range():
    d4 = Dice(4)
    rolls = {d4.roll() for _ in range(1000)}
    assert rolls == {1, 2, 3, 4}


def test_dice_is_callable():
    d20 = Dice(sides=20)
    assert all(1 <= d20() <= 20 for _ in range(200))


def test_dice_sides_is_read_only():
    with pytest.raises(AttributeError):
        Dice().sides = 10


# ----- Weapon ---------------------------------------------------------------------


def test_weapon_rolls_its_dice():
    sword = Weapon("Sword", FixedDice(7))
    assert sword.roll_damage() == 7


def test_weapon_damage_in_range():
    dagger = Weapon("Dagger", Dice(4))
    assert all(1 <= dagger.roll_damage() <= 4 for _ in range(200))


def test_weapon_requires_dice():
    with pytest.raises(TypeError):
        Weapon("Stick", 6)


def test_weapon_repr():
    assert repr(Weapon("Dagger", Dice(4))) == "Weapon(name='Dagger', damage_dice=Dice(sides=4))"


# ----- Character ------------------------------------------------------------------


def test_take_damage_reduces_own_hp_and_stops_at_zero():
    c = Character("A", hp_max=20)
    assert c.take_damage(5) == 5
    assert c.hp == 15
    assert c.take_damage(100) == 15  # only 15 HP was left to lose
    assert c.hp == 0
    assert not c.is_alive


def test_take_damage_rejects_negative_amount():
    with pytest.raises(ValueError):
        Character("A").take_damage(-5)


def test_heal_stops_at_hp_max():
    c = Character("A", hp_max=50)
    c.take_damage(20)
    assert c.heal(5) == 5
    assert c.hp == 35
    assert c.heal(100) == 15
    assert c.hp == 50


def test_dead_character_cannot_be_healed():
    c = Character("A", hp_max=10)
    c.take_damage(10)
    assert c.heal(5) == 0
    assert c.hp == 0


def test_hp_and_is_alive_are_read_only():
    c = Character("A")
    with pytest.raises(AttributeError):
        c.hp = 1000
    with pytest.raises(AttributeError):
        c.is_alive = False


def test_attack_uses_targets_take_damage():
    class Spy(Character):
        def take_damage(self, amount):
            self.received = amount
            return super().take_damage(amount)

    target = Spy("Target")
    Character("Attacker", damage=12).attack(target)
    assert target.received == 12
    assert target.hp == 88


def test_attack_with_weapon_uses_weapon_damage():
    attacker = Character("A", damage=10, weapon=Weapon("Axe", FixedDice(17)))
    target = Character("B")
    assert attacker.attack(target) == 17
    assert target.hp == 83


def test_dead_character_cannot_attack():
    attacker = Character("A", hp_max=1)
    attacker.take_damage(1)
    target = Character("B")
    assert attacker.attack(target) == 0
    assert target.hp == 100


def test_character_cannot_attack_itself():
    c = Character("A")
    with pytest.raises(ValueError):
        c.attack(c)


def test_weapon_must_be_weapon():
    with pytest.raises(TypeError):
        Character("A", weapon="sword")


# ----- Warrior --------------------------------------------------------------------


def test_warrior_default_armor_is_five():
    assert Warrior("W").armor == 5


def test_warrior_armor_reduces_damage():
    w = Warrior("W", armor=5)
    assert w.take_damage(12) == 7
    assert w.hp == 93


def test_warrior_armor_never_heals():
    w = Warrior("W", armor=5)
    assert w.take_damage(3) == 0
    assert w.hp == 100


def test_warrior_is_a_character():
    assert isinstance(Warrior("W"), Character)


# ----- Mage -----------------------------------------------------------------------


def test_mage_default_mana():
    m = Mage("M")
    assert m.mana == 30
    assert m.mana_max == 30


def test_mage_spell_costs_mana_deals_double_damage_and_ignores_weapon():
    m = Mage("M", damage=10, weapon=Weapon("Staff", FixedDice(3)))
    target = Character("T")
    assert m.attack(target) == 20
    assert m.mana == 20
    assert target.hp == 80


def test_mage_without_mana_uses_weapon_and_regains_mana():
    m = Mage("M", damage=10, weapon=Weapon("Staff", FixedDice(3)), mana=9)
    target = Character("T")
    assert m.attack(target) == 3
    assert m.mana == 14


def test_mage_without_mana_or_weapon_uses_base_damage():
    m = Mage("M", damage=10, mana=0)
    target = Character("T")
    assert m.attack(target) == 10
    assert m.mana == 5


def test_mage_mana_never_exceeds_max():
    m = Mage("M", mana=8, mana_max=10)
    m.attack(Character("T"))
    assert m.mana == 10


def test_mage_attack_pattern():
    """30 mana -> 3 spells, then base, base, spell, ..."""
    m = Mage("M", damage=10)
    target = Character("T", hp_max=1000)
    dealt = [m.attack(target) for _ in range(9)]
    assert dealt == [20, 20, 20, 10, 10, 20, 10, 10, 20]


def test_mage_mana_cannot_start_above_max():
    with pytest.raises(ValueError):
        Mage("M", mana=40, mana_max=30)


def test_mage_spell_against_warrior_is_reduced_by_armor():
    w = Warrior("W", armor=5)
    Mage("M", damage=10).attack(w)
    assert w.hp == 85


# ----- Battle ---------------------------------------------------------------------


def test_play_round_hero_attacks_then_enemy():
    hero = Character("H", damage=10)
    enemy = Character("E", damage=7)
    battle = Battle(hero, enemy, verbose=False)
    battle.play_round()
    assert enemy.hp == 90
    assert hero.hp == 93
    assert battle.rounds_played == 1


def test_dead_enemy_does_not_strike_back():
    hero = Character("H", damage=50)
    enemy = Character("E", hp_max=50, damage=7)
    Battle(hero, enemy, verbose=False).play_round()
    assert not enemy.is_alive
    assert hero.hp == 100


def test_simulate_battle_runs_until_one_dies():
    hero = Character("H", damage=10)
    enemy = Character("E", damage=9)
    battle = Battle(hero, enemy, verbose=False)
    winner = battle.simulate_battle()
    assert winner is hero
    assert not enemy.is_alive
    assert battle.rounds_played == 10
    assert hero.hp == 100 - 9 * 9


def test_battle_with_random_weapons_always_ends_with_one_survivor():
    for _ in range(100):
        hero = Warrior("W", weapon=Weapon("Sword", Dice(8)))
        enemy = Mage("M", weapon=Weapon("Wand", Dice(6)))
        battle = Battle(hero, enemy, verbose=False)
        winner = battle.simulate_battle()
        assert winner in (hero, enemy)
        assert hero.is_alive != enemy.is_alive


def test_battle_where_nobody_can_win_is_a_draw():
    hero = Warrior("H", damage=3, armor=5)
    enemy = Warrior("E", damage=3, armor=5)
    battle = Battle(hero, enemy, verbose=False, max_rounds=50)
    assert battle.simulate_battle() is None
    assert battle.rounds_played == 50


def test_play_round_after_battle_is_over_raises():
    hero = Character("H", damage=200)
    enemy = Character("E")
    battle = Battle(hero, enemy, verbose=False)
    battle.simulate_battle()
    with pytest.raises(RuntimeError):
        battle.play_round()


def test_battle_requires_two_different_characters():
    c = Character("A")
    with pytest.raises(ValueError):
        Battle(c, c)
    with pytest.raises(TypeError):
        Battle(c, "enemy")
