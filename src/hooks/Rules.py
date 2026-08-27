from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value
from BaseClasses import MultiWorld, CollectionState

import re
from enum import StrEnum

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

class Levels(StrEnum):
    RABBIT_IN_TRAINING = 'Rabbit in Training'
    DUNGEON_DILEMMA = 'Dungeon Dilemma'
    KNIGHT_CAP = 'Knight Cap'
    TOSSED_SALAD = 'Tossed Salad'
    CARROT_JUICE = 'Carrot Juice'
    WEIRDER_SCIENCE = 'Weirder Science'
    LOOSE_SCREWS = 'Loose Screws'
    VICTORIAN_SECRET = 'Victorian Secret'
    COLONIAL_CHAOS = 'Colonial Chaos'
    PURPLE_HAZE_MAZE = 'Purple Haze Maze'
    FUNKY_GROOVEATHON = 'Funky Grooveathon'
    BEACH_BUNNY_BINGO = 'Beach Bunny Bingo'
    MARINATED_RABBIT = 'Marinated Rabbit'
    A_DIAMONDUS_FOREVER = 'A Diamondus Forever'
    FOURTEEN_CARROT = 'Fourteen Carrot'
    ELECTRIC_BOOGALOO = 'Electric Boogaloo'
    VOLTAGE_VILLAGE = 'Voltage Village'
    MEDIEVAL_KINEVAL = 'Medieval Kineval'
    HARE_SCARE = 'Hare Scare'
    GARGOYLES_LAIR = 'Gargoyles Lair'
    THRILLER_GORILLA = 'Thriller Gorilla'
    JUNGLE_JUMP = 'Jungle Jump'
    A_COLD_DAY_IN_HECK = 'A Cold Day in Heck'
    RABBIT_ROAST = 'Rabbit Roast'
    BURNIN_BISCUITS = 'Burnin Biscuits'
    BAD_PITT = 'Bad Pitt'
    DARN_RATZ = 'Darn Ratz'
    RETRO_RABBIT = 'Retro Rabbit'
    FROG_STOMP = 'Frog Stomp'
    EASTER_BUNNY = 'Easter Bunny'
    SPRING_CHICKENS = 'Spring Chickens'
    SCRAMBLED_EGGS = 'Scrambled Eggs'
    GHOSTLY_ANTICS = 'Ghostly Antics'
    SKELETONS_TURF = 'Skeletons Turf'
    GRAVEYARD_SHIFT = 'Graveyard Shift'
    TURTLE_TOWN = 'Turtle Town'
    SUBURBIA_COMMANDO = 'Suburbia Commando'
    URBAN_BRAWL = 'Urban Brawl'
    SNOW_BUNNIES = 'Snow Bunnies'
    DASHING_THRU_THE_SNOW = 'Dashing thru the snow..'
    TINSEL_TOWN = 'Tinsel Town'
    
class Weapons(StrEnum):
    BOUNCER = 'Bouncer'
    FREEZER = 'Freezer'
    SEEKER = 'Seeker'
    RF = 'RF Missile'
    TOASTER = 'Toaster'
    TNT = 'TNT'
    PEPPER = 'Pepper Spray'
    ELECTRO = 'Electro Blaster'

LEVEL_ORDER_LOOKUP = [
    None,
    # Base game episodes
    Levels.RABBIT_IN_TRAINING,
    Levels.DUNGEON_DILEMMA,
    Levels.KNIGHT_CAP,
    Levels.TOSSED_SALAD,
    Levels.CARROT_JUICE,
    Levels.VICTORIAN_SECRET,
    Levels.COLONIAL_CHAOS,
    Levels.PURPLE_HAZE_MAZE,
    Levels.FUNKY_GROOVEATHON,
    Levels.BEACH_BUNNY_BINGO,
    Levels.MARINATED_RABBIT,
    Levels.A_DIAMONDUS_FOREVER,
    Levels.FOURTEEN_CARROT,
    Levels.ELECTRIC_BOOGALOO,
    Levels.VOLTAGE_VILLAGE,
    Levels.MEDIEVAL_KINEVAL,
    Levels.HARE_SCARE,
    Levels.THRILLER_GORILLA,
    Levels.JUNGLE_JUMP,
    Levels.A_COLD_DAY_IN_HECK,
    Levels.RABBIT_ROAST,
    Levels.BURNIN_BISCUITS,
    Levels.BAD_PITT,
    None,
    # Alternate lookup for Gargoyles Lair
    Levels.RABBIT_IN_TRAINING,
    Levels.DUNGEON_DILEMMA,
    Levels.KNIGHT_CAP,
    Levels.TOSSED_SALAD,
    Levels.CARROT_JUICE,
    Levels.VICTORIAN_SECRET,
    Levels.COLONIAL_CHAOS,
    Levels.PURPLE_HAZE_MAZE,
    Levels.FUNKY_GROOVEATHON,
    Levels.BEACH_BUNNY_BINGO,
    Levels.MARINATED_RABBIT,
    Levels.A_DIAMONDUS_FOREVER,
    Levels.FOURTEEN_CARROT,
    Levels.ELECTRIC_BOOGALOO,
    Levels.VOLTAGE_VILLAGE,
    Levels.MEDIEVAL_KINEVAL,
    Levels.GARGOYLES_LAIR,
    None,
    # Shareware Episode
    Levels.DARN_RATZ,
    Levels.RETRO_RABBIT,
    Levels.FROG_STOMP,
    None,
    # The Secret Files
    Levels.EASTER_BUNNY,
    Levels.SPRING_CHICKENS,
    Levels.SCRAMBLED_EGGS,
    Levels.GHOSTLY_ANTICS,
    Levels.SKELETONS_TURF,
    Levels.GRAVEYARD_SHIFT,
    Levels.TURTLE_TOWN,
    Levels.SUBURBIA_COMMANDO,
    Levels.URBAN_BRAWL,
    None,
    # Holiday Hare/Christmas Chronicles
    Levels.SNOW_BUNNIES,
    Levels.DASHING_THRU_THE_SNOW,
    Levels.TINSEL_TOWN,
    None
]

# For each level, which weapons are available and how.
# If the value is true, the weapon can be obtained if the main path can be followed to the end.
# Otherwise, the list specifies the regions that, if accessible, can all provide access to the weapon.
LEVEL_WEAPON_ACCESS_LOOKUP: dict[str, dict[Weapons, bool | list[str]]] = {
    Levels.RABBIT_IN_TRAINING: {},
    Levels.DUNGEON_DILEMMA: { 
        Weapons.BOUNCER: True 
    },
    Levels.KNIGHT_CAP: {
        Weapons.BOUNCER: True,
        Weapons.FREEZER: ['Jazz Main Area']
    },
    Levels.TOSSED_SALAD: {
        Weapons.TOASTER: True
    },
    Levels.CARROT_JUICE: {
        Weapons.BOUNCER: True,
        Weapons.TOASTER: True
    },
    Levels.WEIRDER_SCIENCE: {
        Weapons.BOUNCER: True,
        Weapons.TOASTER: True
    },
    Levels.LOOSE_SCREWS: {
        Weapons.BOUNCER: True,
        Weapons.TOASTER: True
    },
    Levels.VICTORIAN_SECRET: {
        Weapons.SEEKER: True
    },
    Levels.COLONIAL_CHAOS: {
        Weapons.FREEZER: True,
        Weapons.SEEKER: True
    },
    Levels.PURPLE_HAZE_MAZE: {
        Weapons.RF: True,
        Weapons.TOASTER: ['Toaster Ammo Crate Behind RF Blocks Secret']
    },
    Levels.FUNKY_GROOVEATHON: {
        Weapons.BOUNCER: True,
        Weapons.RF: True,
        Weapons.TOASTER: True,
        Weapons.TNT: ['TNT Ammo Above Vine Near Start']
    },
    Levels.BEACH_BUNNY_BINGO: {
        Weapons.BOUNCER: True,
        Weapons.TOASTER: ['Bonus Warp Area'],
        Weapons.TNT: True
    },
    Levels.MARINATED_RABBIT: {
        Weapons.SEEKER: True,
        Weapons.RF: ['Bonus Warp Area']
    },
    Levels.A_DIAMONDUS_FOREVER: {
        Weapons.BOUNCER: True,
        Weapons.FREEZER: True,
        Weapons.SEEKER: ['Spaz Start'],
        Weapons.TOASTER: True
    },
    Levels.FOURTEEN_CARROT: {
        Weapons.BOUNCER: ['Character Morph Power-Up Below Buttstomp Block Secret'],
        Weapons.FREEZER: True,
        Weapons.TOASTER: True,
        Weapons.PEPPER: True
    },
    Levels.ELECTRIC_BOOGALOO: {
        Weapons.BOUNCER: True,
        Weapons.FREEZER: [
            'Freezer Ammo Behind Bouncer Blocks Secret',
            'Freezer Ammo Behind Destructible Barrier Secret',
            'First Freezer Power Up Behind Sidekick Blocks Secret',
            'Second Freezer Power Up Behind Sidekick Blocks Secret'
        ]
    },
    Levels.VOLTAGE_VILLAGE: {
        Weapons.TOASTER: ['Spaz Only Toaster Ammo Above Main Path Secret', 'Bonus Warp Area'],
        Weapons.TNT: True
    },
    Levels.MEDIEVAL_KINEVAL: {
        Weapons.ELECTRO: True
    },
    Levels.HARE_SCARE: {
        Weapons.RF: True
    },
    Levels.GARGOYLES_LAIR: {
        Weapons.BOUNCER: True,
        Weapons.SEEKER: True,
        Weapons.RF: True,
        Weapons.TOASTER: True
    },
    Levels.THRILLER_GORILLA: {
        Weapons.TOASTER: True
    },
    Levels.JUNGLE_JUMP: {
        Weapons.FREEZER: True
    },
    Levels.A_COLD_DAY_IN_HECK: {
        Weapons.TOASTER: True
    },
    Levels.RABBIT_ROAST: {
        Weapons.FREEZER: True
    },
    Levels.BURNIN_BISCUITS: {
        Weapons.TOASTER: True,
        Weapons.PEPPER: True
    },
    Levels.BAD_PITT: {
        Weapons.TOASTER: True,
        Weapons.TNT: True
    }
}

def hasContinuousLevelAccess(state: CollectionState, player: int, from_level: str, to_level: str) -> bool:
    from ..Rules import CanReachLocation
    import logging

    end_index = 0
    try:
        end_index = LEVEL_ORDER_LOOKUP.index(to_level)
    except ValueError:
        logging.error(f'hasContinuousLevelAccess: invalid target level {to_level}')
        return False

    cursor_index = end_index
    while cursor_index > 0:
        cursor_index = cursor_index - 1
        prev_level = LEVEL_ORDER_LOOKUP[cursor_index]

        if prev_level is None:
            logging.error(f'hasContinuousLevelAccess: no valid path from {from_level} to {to_level}')
            return False

        try:
            next_level_access = CanReachLocation(state, player, f'{prev_level} - Level Complete')

            if prev_level == from_level:
                return next_level_access
            elif not next_level_access:
                return False
        except ValueError:
            logging.error(f'hasContinuousLevelAccess: unexpected error when checking if level completion location for {prev_level} could be reached')
            return False

    return False

def hasWeaponAccess(state: CollectionState, player: int, level: str, weapon: str) -> bool:
    from ..Rules import CanReachLocation
    import logging

    if not weapon in Weapons:
        logging.error(f'hasWeaponAccess: invalid weapon {weapon}')
        return False

    end_index = None
    try:
        end_index = LEVEL_ORDER_LOOKUP.index(level)
    except ValueError:
        logging.error(f'hasWeaponAccess: invalid target level {level}')
        return False

    unconditional_last_level = None
    conditional_last_locations: list[tuple[str, str]] = []
            
    cursor_index = end_index
    while cursor_index > 0:
        cursor_index = cursor_index - 1
        prev_level = LEVEL_ORDER_LOOKUP[cursor_index]

        if prev_level is None:
            break

        if prev_level in LEVEL_WEAPON_ACCESS_LOOKUP.keys() and weapon in LEVEL_WEAPON_ACCESS_LOOKUP[prev_level].keys():
            if LEVEL_WEAPON_ACCESS_LOOKUP[prev_level][Weapons(weapon)] == True:
                unconditional_last_level = prev_level
                break
            else:
                for location in LEVEL_WEAPON_ACCESS_LOOKUP[weapon]:
                    conditional_last_locations.append((prev_level, location))

    if unconditional_last_level is not None:
        if hasContinuousLevelAccess(state, player, unconditional_last_level, level):
            logging.debug(f'hasWeaponAccess: can access unconditional weapon {weapon} location in {unconditional_last_level}')
            return True
        logging.debug(f'hasWeaponAccess: unconditional weapon {weapon} location in {unconditional_last_level} is inaccessible')
    else:
        logging.debug(f'hasWeaponAccess: no unconditional weapon {weapon} location available')

    for weapon_level, location in conditional_last_locations:
        if not hasContinuousLevelAccess(state, player, weapon_level, level):
            continue

        if CanReachLocation(state, player, f'{weapon_level} - {location}'):
            logging.debug(f'hasWeaponAccess: can access conditional weapon {weapon} location in {weapon_level} - {location}')
            return True
        logging.debug(f'hasWeaponAccess: conditional weapon {weapon} location in {weapon_level} - {location} is inaccessible')

    logging.debug(f'hasWeaponAccess: cannot access any weapon {weapon} locations from {level}')
    return False
    