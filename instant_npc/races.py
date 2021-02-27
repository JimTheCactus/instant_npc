from dice import roll
from .stats import STATS

def format_feet(inches: int):
    return f"{inches // 12}' {inches % 12}\"",

def add_racial_modifier(npc: dict, stat: str, modifier: int):
    npc['attributes'][stat]['racial_modifier'] = modifier
    npc['attributes'][stat]['total'] += modifier

def add_height_and_weight(npc: dict, base_height: int, height_dice: str,
                          base_weight:int, weight_dice: str) -> dict:
    height_roll = roll(height_dice)
    inches = int(height_roll) + base_height
    npc['height'] = {
        "total": inches,
        "feet": format_feet(inches),
        "roll": height_roll
    }
    weight_roll = roll(weight_dice)
    npc['weight'] = {
        "total": base_weight + int(height_roll) * int(weight_roll),
        "roll": weight_roll
    }
    return npc

def be_human(npc: dict) -> dict:
    for stat in STATS.values():
        add_racial_modifier(npc, stat, 1)

    add_height_and_weight(npc, 56, "2d10", 110, "2d4")
    npc.setdefault('languages', []).append(["Common", "Bonus Language"])
    return npc

def be_halfelf(npc: dict) -> dict:
    add_racial_modifier(npc, "CHA", 2)

    add_height_and_weight(npc, 57, "2d8", 110, "2d4")
    npc.setdefault('abilities', []).append("Darkvision")
    npc['abilities'].append("Fey Ancestry")
    npc['abilities'].append("Skill Versatility")
    npc.setdefault('languages', []).append(["Common", "Elvish", "Bonus Language"])
    npc.setdefault('notes', []).append("Skill Versatility: gain proficiency in two Skills")
    return npc


DEFAULT_RACES=[
    (40, "human", be_human),
    (60, "half-elf", be_halfelf),
    (80, "half-orc", None),
    (90, "halfling", None),
    (96, "elf", None),
    (98, "dwarf", None),
    (99, "tiefling", None),
    (100, "gnome", None)
    ]