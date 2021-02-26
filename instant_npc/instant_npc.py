"""
Creates an NPC using the random tables from the DMG and returns a dict structure with their
parameters, including basic stats.
"""

import logging

logger=logging.getLogger(__name__)

from dice import roll 

DEFAULT_RACES=[
    (40, "human"),
    (60, "half-elf"),
    (80, "half-orc"),
    (90, "halfling"),
    (96, "elf"),
    (98, "dwarf"),
    (99, "tiefling"),
    (100, "gnome")
    ]

STATS = {
    1: "STR",
    2: "DEX",
    3: "CON",
    4: "INT",
    5: "WIS",
    6: "CHA"
}

def make_npc(races=DEFAULT_RACES):
    npc={}
    logger.info("Rolling for race...")
    race_roll=roll("1d100")
    for threshold, race in races:
        if threshold >= int(race_roll):
            npc['race']={"name": race, "dice_rolled":race_roll}
            break
    logger.info("Rolling for stats...")
    high_stat=roll("1d6")
    low_stat=roll("1d6")
    while int(high_stat) == int(low_stat):
        logger.info("Rerolling low stat due to a collision with the high stat...")
        low_stat=roll("1d6")

    npc['high_stat'] = {"name": STATS[int(high_stat)], "dice_rolled": high_stat}
    npc['low_stat'] = {"name": STATS[int(low_stat)], "dice_rolled": low_stat}

    return npc

