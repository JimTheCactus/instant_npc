"""
Creates an NPC using the random tables from the DMG and returns a dict structure with their
parameters, including basic stats.
"""

import logging
import random

logger=logging.getLogger(__name__)

from dice import roll

from .races import DEFAULT_RACES
from .stats import STATS

def roll_attribute():
    attr_roll = roll("4d6s")
    total=sum(attr_roll[1:])
    return {
        "kept":attr_roll[1:],
        "dropped": attr_roll[0],
        "total": total
    }

def get_attributes(low_stat, high_stat, modifiers: dict={}):
    attr_rolls = []
    for _ in range(6):
        attr_rolls.append(roll_attribute())
    sorted_attrs = sorted(attr_rolls, key=lambda x: x['total'])

    stat_list = list(STATS.values())

    attributes={
        high_stat: sorted_attrs[5],
        low_stat: sorted_attrs[0]
    }

    stat_list.remove(low_stat)
    stat_list.remove(high_stat)

    random.shuffle(stat_list)

    count = 1
    for stat in stat_list:
        attributes[stat] = sorted_attrs[count]
        count += 1

    return attributes

def make_npc(races=DEFAULT_RACES):
    npc={}
    logger.info("Rolling for race...")
    race_roll=roll("1d100")
    for threshold, race, race_routine in races:
        if threshold >= int(race_roll):
            npc['race']={"name": race, "dice_rolled":race_roll}
            racial_routine = race_routine
            break
    logger.info("Rolling for stats...")
    high_stat=roll("1d6")
    low_stat=roll("1d6")
    while int(high_stat) == int(low_stat):
        logger.info("Rerolling low stat due to a collision with the high stat...")
        low_stat=roll("1d6")

    npc['high_stat'] = {"name": STATS[int(high_stat)], "dice_rolled": high_stat}
    npc['low_stat'] = {"name": STATS[int(low_stat)], "dice_rolled": low_stat}

    npc['attributes'] = get_attributes(STATS[int(low_stat)], STATS[int(high_stat)])

    # Do the race specific stuff
    if not racial_routine is None:
        npc = racial_routine(npc)

    return npc

