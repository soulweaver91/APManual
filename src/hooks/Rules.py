from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value
from BaseClasses import MultiWorld, CollectionState

import re

# # Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# # Define a function here, and you can use it in a requires string with {function_name()}.
# def overfishedAnywhere(world: World, state: CollectionState, player: int):
#     """Has the player collected all fish from any fishing log?"""
#     for cat, items in world.item_name_groups:
#         if cat.endswith("Fishing Log") and state.has_all(items, player):
#             return True
#     return False
# 
# # You can also pass an argument to your function, like {function_name(15)}
# # Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
# def anyClassLevel(state: CollectionState, player: int, level: str):
#     """Has the player reached the given level in any class?"""
#     for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
#         if state.count(item, player) >= int(level):
#             return True
#     return False

def canDoubleJump():
    return "|Spaz Unlock| and (|Double Jump Unlock| or {YamlDisabled(basic_movement_in_pool)})"

def canCopter():
    return "(|Jazz Unlock| or |Lori Unlock|) and (|Copter Ears Unlock| or {YamlDisabled(basic_movement_in_pool)})"

def canUppercut():
    return "|Jazz Unlock| and (|Uppercut Unlock| or {YamlDisabled(basic_movement_in_pool)})"

def canSidekick():
    return "(|Spaz Unlock| or |Lori Unlock|) and (|Sidekick Unlock| or {YamlDisabled(basic_movement_in_pool)})"

def canButtstomp():
    return "|Buttstomp Unlock| or {YamlDisabled(basic_movement_in_pool)}"

def canDestroyWildcardBlocks():
    return "|Wildcard Destructible Scenery| or {YamlDisabled(block_destruction_in_pool)}"

def canDestroyBouncerBlocks():
    return "(|Bouncer Destructible Scenery| or {YamlDisabled(block_destruction_in_pool)}) and |Bouncer Permit|"

def canDestroySeekerBlocks():
    return "(|Seeker Destructible Scenery| or {YamlDisabled(block_destruction_in_pool)}) and |Seeker Permit|"

def canDestroyRFMissileBlocks():
    return "(|RF Missile Destructible Scenery| or {YamlDisabled(block_destruction_in_pool)}) and |RF Missile Permit|"

def canDestroyToasterBlocks():
    return "(|Toaster Destructible Scenery| or {YamlDisabled(block_destruction_in_pool)}) and |Toaster Permit|"

def canDestroyTNTBlocks():
    return "(|TNT Destructible Scenery| or {YamlDisabled(block_destruction_in_pool)}) and |TNT Permit|"

def canDestroyButtstompBlocks():
    return "(|Special Move Destructible Scenery| or {YamlDisabled(block_destruction_in_pool)}) and (|Buttstomp Unlock| or {YamlDisabled(basic_movement_in_pool)})"

def canDestroySpeedBlocks():
    return "|Speed Destructible Scenery| or {YamlDisabled(block_destruction_in_pool)}"

def canGrabVines():
    return "|Vine Traversal| or {YamlDisabled(basic_movement_in_pool)}"

def canGrabHooks():
    return "|Hook Traversal| or {YamlDisabled(basic_movement_in_pool)}"

def canSwim():
    return "|Swimming Unlock| or {YamlDisabled(basic_movement_in_pool)}"

def CanReachRegion(state: CollectionState, player: int, location: str) -> bool:
    """Can the player reach the given region?"""
    if state.can_reach_region(location, player):
        return True
    return False
