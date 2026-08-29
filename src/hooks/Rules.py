from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import is_option_enabled
from BaseClasses import MultiWorld, CollectionState

import re
from enum import StrEnum
from typing import Literal, Self
import logging

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
    Levels.WEIRDER_SCIENCE,
    Levels.LOOSE_SCREWS,
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
    Levels.WEIRDER_SCIENCE,
    Levels.LOOSE_SCREWS,
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
# Note that for locations in the same level, this doesn't account for backtracking at the moment.
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
        Weapons.FREEZER: ['Freezer Ammo Above Trigger Scenery Secret'],
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

# Tuples of level and an arbitrary number, splitting the level into region groups
# based on whether TNT can be brought there from within itself or an earlier
# part of the level
IN_LEVEL_TNT_RULES: dict[tuple[Levels, int], list[str] | bool] = {
    # Funky Grooveathon #0: The entire level
    (Levels.FUNKY_GROOVEATHON, 0): ['TNT Ammo Above Vine Near Start'],
    # Beach Bunny Bingo #0: The entire level
    (Levels.BEACH_BUNNY_BINGO, 0): True,
    # Voltage Village #0: Jazz's path until the paths meet
    (Levels.VOLTAGE_VILLAGE, 0): True,
    # Voltage Village #1: Spaz's path until the paths meet
    (Levels.VOLTAGE_VILLAGE, 1): False,
    # Voltage Village #2: The rest of the level
    (Levels.VOLTAGE_VILLAGE, 2): True,
    # Bad Pitt #0: From start to after the first wildcard blocks
    (Levels.BAD_PITT, 0): False,
    # Bad Pitt #1: From start to after the first wildcard blocks
    (Levels.BAD_PITT, 1): True
}


def hasMovementUnlock(multiworld: MultiWorld, state: CollectionState, player: int, unlockItem: str):
    if not is_option_enabled(multiworld, player, 'basic_movement_in_pool'):
        return True

    return state.has(unlockItem, player)


def canDoubleJump(multiworld: MultiWorld, state: CollectionState, player: int):
    if not state.has('Spaz Unlock', player):
        return False

    return hasMovementUnlock(multiworld, state, player, 'Double Jump Unlock')


def canCopter(multiworld: MultiWorld, state: CollectionState, player: int):
    if not state.has('Jazz Unlock', player) and not state.has('Lori Unlock', player):
        return False

    return hasMovementUnlock(multiworld, state, player, 'Copter Ears Unlock')


def canUppercut(multiworld: MultiWorld, state: CollectionState, player: int):
    if not state.has('Jazz Unlock', player):
        return False

    return hasMovementUnlock(multiworld, state, player, 'Uppercut Unlock')


def canSidekick(multiworld: MultiWorld, state: CollectionState, player: int):
    if not state.has('Spaz Unlock', player) and not state.has('Lori Unlock', player):
        return False

    return hasMovementUnlock(multiworld, state, player, 'Sidekick Unlock')


def canButtstomp(multiworld: MultiWorld, state: CollectionState, player: int):
    return hasMovementUnlock(multiworld, state, player, 'Buttstomp Unlock')


def canGrabVines(multiworld: MultiWorld, state: CollectionState, player: int):
    return hasMovementUnlock(multiworld, state, player, 'Vine Traversal')


def canGrabHooks(multiworld: MultiWorld, state: CollectionState, player: int):
    return hasMovementUnlock(multiworld, state, player, 'Hook Traversal')


def canSwim(multiworld: MultiWorld, state: CollectionState, player: int):
    return hasMovementUnlock(multiworld, state, player, 'Swimming Unlock')


def canDestroyWildcardBlocks(multiworld: MultiWorld, state: CollectionState, player: int):
    if not is_option_enabled(multiworld, player, 'block_destruction_in_pool'):
        return True
    
    return state.has('Wildcard Destructible Scenery', player)


def canDestroyWeaponBlocks(multiworld: MultiWorld, state: CollectionState, player: int, weapon: str):
    if not weapon in Weapons:
        logging.error(f'canDestroyWeaponBlocks: invalid weapon {weapon}')
        return False

    if not state.has(f'{weapon} Permit', player):
        return False
    
    if not is_option_enabled(multiworld, player, 'block_destruction_in_pool'):
        return True
    
    return state.has(f'{weapon} Destructible Scenery', player)


def canUseSpecialMoveByDirection(multiworld: MultiWorld, state: CollectionState, player: int, directions: str = ''):
    direction_set = set(['above', 'below', 'sides'])
    if directions and len(directions) > 0:
        direction_set = set(directions.split('/'))

    if 'above' in direction_set:
        if canButtstomp(multiworld, state, player):
            return True
    
    if 'below' in direction_set:
        if canUppercut(multiworld, state, player):
            return True
        
    if 'sides' in direction_set:
        if canSidekick(multiworld, state, player):
            return True
        
    return False


def canDestroySpecialMoveBlockOrTriggerCrate(multiworld: MultiWorld, state: CollectionState, player: int, level: str, directions: str = ''):
    level_subdivision_index = 0
    if level.find('@') > 0:
        level, level_subdivision_index = level.split('@', 2)
        level_subdivision_index = int(level_subdivision_index)

    if canUseSpecialMoveByDirection(multiworld, state, player, directions):
        return True

    if state.has('TNT Permit', player):
        if hasWeaponAccess(state, player, level, Weapons.TNT):
            return True

        try:
            if (level, level_subdivision_index) in IN_LEVEL_TNT_RULES:
                in_level_rule = IN_LEVEL_TNT_RULES[(Levels(level), level_subdivision_index)]
                if isinstance(in_level_rule, list):
                    for location in in_level_rule:
                        if CanReachRegion(state, player, f'{level} - {location}'):
                            return True
                elif in_level_rule is True:
                    return True
        except ValueError:
            pass
    
    return False


def canDestroySpecialMoveBlocks(multiworld: MultiWorld, state: CollectionState, player: int, level: str, directions: str = ''):
    if is_option_enabled(multiworld, player, 'block_destruction_in_pool') and not state.has('Special Move Destructible Scenery', player):
        return False

    return canDestroySpecialMoveBlockOrTriggerCrate(multiworld, state, player, level, directions)


def canDestroyTriggerCrates(multiworld: MultiWorld, state: CollectionState, player: int, level: str, directions: str = ''):
    # Trigger crates could be an additional unlockable in the future. But, as is, this is just a passthrough to the common parts.
    return canDestroySpecialMoveBlockOrTriggerCrate(multiworld, state, player, level, directions)


def canDestroySpeedBlocks(multiworld: MultiWorld, state: CollectionState, player: int):
    if not is_option_enabled(multiworld, player, 'block_destruction_in_pool'):
        return True
    
    return state.has('Speed Destructible Scenery', player)


def CanReachRegion(state: CollectionState, player: int, location: str) -> bool:
    """Can the player reach the given region?"""
    if state.can_reach_region(location, player):
        return True
    return False


def hasContinuousLevelAccess(state: CollectionState, player: int, from_level: str, to_level: str) -> bool:
    from ..Rules import CanReachLocation

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


type StartPositionCharacterName = Literal['Jazz', 'Spaz']


class CoinPathNode:
    region: str | None = None
    amount: int = 0

    def __init__(self, amount, region = None) -> None:
        self.amount = amount
        self.region = region
        pass


class CoinPathGroup:
    name: str
    character: StartPositionCharacterName | None
    branches: list['CoinPathGroup | None']
    sequence: list['CoinPathNode | CoinPathGroup']
    min_mode: bool

    minimum_coins_from_branches = 0
    minimum_coins_from_sequence = 0
    minimum_coins = 0

    def __init__(self, name: str, character: StartPositionCharacterName | None = None, min_mode: bool = False) -> None:
        logging.debug(f'')
        logging.debug(f'CoinPathGroup: init {name}')

        self.name = name
        self.character = character
        self.min_mode = min_mode
        self.sequence = []
        self.branches = []

    def branch(self, subpath: 'CoinPathGroup') -> Self:
        self.branches.append(subpath)
        
        if self.min_mode:
            self.minimum_coins_from_branches = min([branch.minimum_coins for branch in self.branches if branch is not None])
        else:
            self.minimum_coins_from_branches = max([branch.minimum_coins for branch in self.branches if branch is not None])

        self._update_minimum_coins()
        return self
    
    def seq(self, sequence: list['CoinPathNode | CoinPathGroup']) -> Self:
        self.sequence = sequence

        self.minimum_coins_from_sequence = 0
        for step in sequence:
            if isinstance(step, CoinPathGroup):
                self.minimum_coins_from_sequence += step.minimum_coins
            elif step.region is None:
                self.minimum_coins_from_sequence += step.amount

        self._update_minimum_coins()
        return self

    def _update_minimum_coins(self):        
        logging.debug(f'CoinPathGroup._update_minimum_coins: {self.name} - branch {self.minimum_coins_from_branches} seq {self.minimum_coins_from_sequence}')
        self.minimum_coins = self.minimum_coins_from_branches + self.minimum_coins_from_sequence

CN = CoinPathNode
CG = CoinPathGroup

COIN_ACCESS_BY_LEVEL_LOOKUP: dict[Levels, CoinPathGroup] = {
    Levels.RABBIT_IN_TRAINING: CG(Levels.RABBIT_IN_TRAINING).seq([
        # M3    silver: (165, 49)
        CN(1)
    ]),
    Levels.DUNGEON_DILEMMA: CG(Levels.DUNGEON_DILEMMA).seq([
        # M1    silver: (31, 15) (33, 15) (72, 2) (72, 3)
        CN(4),
        # M2    silver: (36, 18) (36, 19) (37, 18) (37, 19)
        CN(4), 
        # M4    gold:   (156, 38) (156, 39)       
        CN(10),
        # A4    silver: (176, 41) (177, 41) (178, 41) (179, 41) (180, 41) (186, 38) (186, 37) (186, 36)
        CN(8, 'Gem Chute Next to Bonus Warp')
    ]),
    Levels.KNIGHT_CAP: CG(Levels.KNIGHT_CAP).seq([
        CG('Start position branch', min_mode=True).branch(
            CG('Jazz branch', 'Jazz').seq([
                # J1     gold:   (112, 8) (112, 9) (189, 9)
                CN(15),
                # A2     gold:   (163, 6)
                CN(5, 'Jazz Only Gold Coin Secret'),
                # J3     gold:   (20, 23) (56, 31) (56, 32)
                CN(15)
            ])
        ).branch(
            CG('Spaz branch', 'Spaz').seq([
                # A4     silver: (10, 44) (11, 44) (10, 45) (11, 45)
                CN(4, 'Spaz Only Four Silver Coins Behind Trigger Scenery Secret'),
                # S1     silver: (67, 54) (68, 54) (67, 55) (68, 55)
                CN(4),
                # A5     silver: (7, 61) (7, 62) (8, 61) (8, 62)
                CN(4, 'Spaz Only Four Silver Coins in Secluded Room Secret'),
                # A6     gold:   (77, 62) (78, 62)
                CN(10, 'Spaz Only Two Gold Coins Secret'),
                # A8     gold:   (77, 62) (78, 62)
                CN(5, 'Spaz Only Gold Coin Secret'),
            ])
        ),
        CG('Shared path').seq([
            # M2     silver: (139, 34) (140, 34) (139, 35) (140, 35)
            CN(4),
            # A9     gold:   (139, 45)
            CN(5)
        ])
    ]),
    Levels.TOSSED_SALAD: CG(Levels.TOSSED_SALAD).seq([
        CG('Start position branch', min_mode=True).branch(
            CG('Jazz branch', 'Jazz').seq([
                # A2    silver: (152, 18) (153, 17) (153, 18) (153, 19) (154, 18)
                CN(5, 'Five Silver Coins Above Trigger Scenery Blocks Secret')
            ])
        ).branch(
            CG('Spaz branch', 'Spaz').seq([
                CG('Spaz branch directions').branch(
                    CG('Into Jazz branch').seq([
                        # A2     silver: (152, 18) (153, 17) (153, 18) (153, 19) (154, 18)
                        CN(5, 'Five Silver Coins Above Trigger Scenery Blocks Secret')
                    ])
                ).branch(
                    CG('To the end of Spaz branch').seq([
                        # S1     silver: (182, 2) (183, 2) (182, 3) (183, 3) (202, 7) (203, 7) (204, 7) (202, 8) (203, 8) (204, 8)
                        CN(10)
                    ])
                )
            ])
        ),
        CG('Shared path').seq([
            # A3     gold:   (222, 36)
            CN(5, 'East Gold Coin Area'),
            # M3     silver: (118, 61) (119, 61) (121, 61) (122, 61) (118, 62) (119, 62) (121, 62) (122, 62)
            CN(8),
            # A4     gold:   (168, 30)
            CN(5, 'Under Jazz Section Bridge'),
            # A5     silver: (104, 41) (104, 42)
            CN(2, 'Two Silver Coins After Second Save Point Secret'),
        ])
    ]),
    Levels.CARROT_JUICE: CG(Levels.CARROT_JUICE).seq([
        CG('Branch at start of level').branch(
            CG('Left path (M1)').seq([
                # A4     gold:   (112, 57)
                CN(5)
            ])
        ).branch(
            CG('Right path (M6)').seq([])
        ),
        # A5     silver: (49, 3) (50, 2) (50, 3) (50, 4) (51, 3)
        CN(5, 'Five Silver Coins Behind Blocks Secret'),
        # A6     silver: (88, 1) (89, 1) (88, 2) (89, 2) (88, 3) (89, 3)
        CN(6, 'Six Silver Coins Above Bubble Shield Secret'),
        # A8     gold:   (134, 13)
        CN(5, 'Gold Coin And Bouncer Ammo Warp Secret'),
        # A10    gold:   (175, 4)
        CN(5, 'Gold Coin Warp Secret')
    ]),
    Levels.WEIRDER_SCIENCE: CG(Levels.WEIRDER_SCIENCE).seq([
        CG('Start position branch', min_mode=True).branch(
            CG('Jazz branch', 'Jazz').seq([
                # J0     silver: (2, 10)
                CN(1),
                # A1     silver: (43, 10) (44, 9) (44, 10) (44, 11) (45, 10)
                CN(5, 'Jazz Super Gem and Five Silver Coins Above Trigger Scenery Secret'),
                # A2     gold:   (73, 9)
                CN(5, 'Jazz Gold Coin Secret')
            ])
        ).branch(
            CG('Spaz branch', 'Spaz').seq([
                # A3     gold:   (1, 37)
                CN(5, 'Spaz Gold Coin Below Start Secret'),
                # A4     silver: (29, 30) (30, 30) (29, 31) (30, 31) (29, 32) (30, 32)
                CN(6, 'Spaz Silver Coins Warp Secret'),
                # A5     silver: (37, 42)
                CN(1, 'Spaz Silver Coins Behind Blocks Secret'),
                # S1     silver: (36, 42) (36, 43) (36, 44) (36, 45)
                CN(4)
            ])
        ),
        CG('Shared path').seq([
            # A7     gold:   (122, 32)
            CN(5, 'Gold Coin and Super Gem Above Frozen Spring Secret'),
            # A9     gold:   (139, 55)
            CN(5, 'Gold Coin Among Breakable Blocks Secret'),
            # A10    gold:   (168, 43) (169, 43)
            CN(10, 'Two Gold Coins Above Trigger Scenery Secret'),
            # A11    silver: (161, 21) (162, 21) (161, 22) (162, 22)
            CN(4, 'Silver Coins Behind Buttstomp Blocks Secret'),
            # M5     gold:   (183, 11) (184, 11)
            CN(10),
            # M8     silver: (225, 3) (225, 4) (225, 5) (225, 6) (225, 7)
            CN(5),
            # M9     silver: (245, 18) (245, 19)
            CN(2)
        ])
    ]),
    Levels.LOOSE_SCREWS: CG(Levels.LOOSE_SCREWS).seq([
        # M0     gold:   (45, 40)
        #        silver: (0, 53) (1, 53) (0, 54) (1, 54) (22, 39) (23, 39)
        CN(11),
        # A2     gold:   (105, 43)
        CN(5, 'Gold Coin Behind Vine and Buttstomp Block Secret'),
        # A3     silver: (13, 16) (14, 16) (15, 16)
        CN(3, 'Silver Coins Behind Destructible Wall and Springs Secret'),
        # A5     silver: (112, 20) (113, 20) (114, 20) (112, 21) (113, 21) (114, 21)
        CN(6, 'Airboard Backtrack Silver Coins Behind Blocks Secret'),
        # M6     gold:   (149, 1)
        CN(5),
        # A6     gold:   (191, 23) (191, 24)
        CN(10, 'Gold Coins Above Second Save Point Secret')
    ]),
    Levels.VICTORIAN_SECRET: CG(Levels.VICTORIAN_SECRET).seq([]),
    Levels.COLONIAL_CHAOS: CG(Levels.COLONIAL_CHAOS).seq([]),
    Levels.PURPLE_HAZE_MAZE: CG(Levels.PURPLE_HAZE_MAZE).seq([]),
    Levels.FUNKY_GROOVEATHON: CG(Levels.FUNKY_GROOVEATHON).seq([]),
    Levels.BEACH_BUNNY_BINGO: CG(Levels.BEACH_BUNNY_BINGO).seq([]),
    Levels.MARINATED_RABBIT: CG(Levels.MARINATED_RABBIT).seq([]),
    Levels.A_DIAMONDUS_FOREVER: CG(Levels.A_DIAMONDUS_FOREVER).seq([]),
    Levels.FOURTEEN_CARROT: CG(Levels.FOURTEEN_CARROT).seq([]),
    Levels.ELECTRIC_BOOGALOO: CG(Levels.ELECTRIC_BOOGALOO).seq([]),
    Levels.VOLTAGE_VILLAGE: CG(Levels.VOLTAGE_VILLAGE).seq([]),
    Levels.MEDIEVAL_KINEVAL: CG(Levels.MEDIEVAL_KINEVAL).seq([]),
    Levels.HARE_SCARE: CG(Levels.HARE_SCARE).seq([]),
    Levels.GARGOYLES_LAIR: CG(Levels.GARGOYLES_LAIR).seq([]),
    Levels.THRILLER_GORILLA: CG(Levels.THRILLER_GORILLA).seq([]),
    Levels.JUNGLE_JUMP: CG(Levels.JUNGLE_JUMP).seq([]),
    Levels.A_COLD_DAY_IN_HECK: CG(Levels.A_COLD_DAY_IN_HECK).seq([]),
    Levels.RABBIT_ROAST: CG(Levels.RABBIT_ROAST).seq([]),
    Levels.BURNIN_BISCUITS: CG(Levels.BURNIN_BISCUITS).seq([]),
    Levels.BAD_PITT: CG(Levels.BAD_PITT).seq([]),
}

def canCollectEnoughCoins(state: CollectionState, player: int, level: str, cost: int) -> bool:
    coin_path: CoinPathGroup
    try:
        coin_path = COIN_ACCESS_BY_LEVEL_LOOKUP[Levels(level)]
    except ValueError:
        logging.error(f'canCollectEnoughCoins: no coin data found for level {level}')
        return False

    # short circuit if the case is trivial
    if coin_path.minimum_coins >= cost:
        logging.debug(f'canCollectEnoughCoins: trivial case (min: {coin_path.minimum_coins}, cost: {cost}, level: {level})')
        return True

    def recurse_coin_path_group(group: CoinPathGroup) -> int:
        logging.debug(f'canCollectEnoughCoins: recurse group ({group.name} branches: {len(group.branches)} sequence: {len(group.sequence)})')
        coins_collected = 0

        for branch in group.branches:
            if branch is None:
                continue

            if branch.character is not None:
                available = False
                if branch.character == 'Spaz':
                    available = available or state.has('Spaz Unlock', player)
                elif branch.character == 'Jazz':
                    available = available or state.has('Jazz Unlock', player) or state.has('Lori Unlock', player)

                if not available:
                    logging.debug(f'canCollectEnoughCoins: {branch.name} inaccessible, requires locked character {branch.character}')
                    continue

            logging.debug(f'canCollectEnoughCoins: recurse into branch {branch.name}')
            branch_coins_collected = recurse_coin_path_group(branch)
            logging.debug(f'canCollectEnoughCoins: update group coins collected from {coins_collected} to {max(coins_collected, branch_coins_collected)}')
            coins_collected = max(coins_collected, branch_coins_collected)

            if coins_collected >= cost:
                logging.debug(f'canCollectEnoughCoins: target reached, exiting recursion branch')
                return coins_collected

        for step in group.sequence:
            logging.debug(f'canCollectEnoughCoins: next sequence step')
            if isinstance(step, CoinPathGroup):
                logging.debug(f'canCollectEnoughCoins: recurse into step {step.name}')
                step_coins_collected = recurse_coin_path_group(step)
                logging.debug(f'canCollectEnoughCoins: update group coins collected from {coins_collected} to {coins_collected + step_coins_collected}')
                coins_collected += step_coins_collected
            else:
                if step.region is None or CanReachRegion(state, player, f'{level} - {step.region}'):
                    logging.debug(f'canCollectEnoughCoins: update group coins collected from {coins_collected} to {coins_collected + step.amount} (region {step.region or 'none'})')
                    coins_collected += step.amount
                else:
                    logging.debug(f'canCollectEnoughCoins: skip step (region {step.region} not reachable)')

            if coins_collected >= cost:
                logging.debug(f'canCollectEnoughCoins: target reached, exiting recursion branch')
                return coins_collected

        return coins_collected

    logging.debug(f'canCollectEnoughCoins: starting main recurse (min: {coin_path.minimum_coins}, cost: {cost}, level: {level})')
    coin_result = recurse_coin_path_group(coin_path)
    logging.debug(f'canCollectEnoughCoins: final result (collected: {coin_result}, cost: {cost}, level: {level})')

    return coin_result >= cost
