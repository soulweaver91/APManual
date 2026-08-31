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
        Weapons.TOASTER: True,
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
    },
    Levels.DARN_RATZ: {
        Weapons.BOUNCER: True
    },
    Levels.RETRO_RABBIT: {
        Weapons.FREEZER: True,
        Weapons.TOASTER: True
    },
    Levels.FROG_STOMP: {
        # no weapon specific ammo in this level, only ammo crates
    },
    Levels.EASTER_BUNNY: {
        Weapons.BOUNCER: True
    },
    Levels.SPRING_CHICKENS: {
        Weapons.TOASTER: True
    },
    Levels.SCRAMBLED_EGGS: {
        # no weapon specific ammo in this level
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


def levelFreeSelectEnabled(multiworld: MultiWorld, state: CollectionState, player: int):
    return is_option_enabled(multiworld, player, 'allow_levels_out_of_order') and is_option_enabled(multiworld, player, 'individual_level_unlock_keys')


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
    amount: int
    region: str | None

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

    minimum_coins_from_branches: int
    minimum_coins_from_sequence: int
    minimum_coins: int

    def __init__(self, name: str, character: StartPositionCharacterName | None = None, min_mode: bool = False) -> None:
        logging.debug(f'')
        logging.debug(f'CoinPathGroup: init {name}')

        self.name = name
        self.character = character
        self.min_mode = min_mode
        self.sequence = []
        self.branches = []
        
        self.minimum_coins_from_branches = 0
        self.minimum_coins_from_sequence = 0
        self.minimum_coins = 0

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
    Levels.VICTORIAN_SECRET: CG(Levels.VICTORIAN_SECRET).seq([
        # M0     gold:   (55, 39)
        #        silver: (104, 34) (105, 34) (104, 35) (105, 35)
        CN(9),
        # A1     silver: (9, 35) (10, 35) (9, 36) (10, 36)
        CN(4, 'Coins in Window Above Start Secret'),
        # M1     gold:   (111, 21)
        CN(5),
        # A3     gold:   (145, 12)
        CN(5, 'Gold Coin on the Roof Behind Blocks Secret'),
        # M2     silver: (216, 38) (217, 38) (216, 39) (217, 39)
        CN(4),
        # M3     gold:   (230, 61) (214, 60) (201, 62) (172, 57)
        CN(20),
        # M4     silver: (0, 16) (1, 16) (0, 17) (1, 17) (52, 15) (53, 15) (57, 15) (58, 15)
        CN(8)
    ]),
    Levels.COLONIAL_CHAOS: CG(Levels.COLONIAL_CHAOS).seq([
        # M0     gold:   (69, 33)
        CN(5),
        # A1     silver: (14, 30) (15, 30) (14, 31) (15, 31)
        CN(4, 'Silver Coins in Window Above Start'),
        # M1     gold:   (102, 31)
        #        silver: (118, 18) (119, 18) (118, 19) (119, 19) (153, 13) (154, 13) (153, 14) (154, 14)
        CN(13),
        # M2     silver: (147, 22) (148, 22) (147, 23) (148, 23)
        CN(4)
    ]),
    Levels.PURPLE_HAZE_MAZE: CG(Levels.PURPLE_HAZE_MAZE).seq([
        # A1     silver: (76, 51) (77, 51) (78, 51) (76, 52) (77, 52) (78, 52)
        CN(6, 'Six Silver Coins Behind RF Blocks Secret'),
        # A3     silver: (43, 21) (44, 21) (45, 21) (43, 22) (44, 22) (45, 22)
        CN(6, 'Six Silver Coins Behind Breakable Wall Before First Save Point')
    ]),
    Levels.FUNKY_GROOVEATHON: CG(Levels.FUNKY_GROOVEATHON).seq([
        # M0     silver: (98, 40) (99, 40) (100, 40) (98, 41) (99, 41)
        CN(5),
        # M2     gold:   (208, 44)
        CN(5),
        # A6     silver: (223, 54) (223, 55) (223, 56) (223, 57) (223, 58)
        CN(5, 'Five Silver Coins Behind Destructible Blocks Secret')
    ]),
    Levels.BEACH_BUNNY_BINGO: CG(Levels.BEACH_BUNNY_BINGO).seq([
        # M0     gold:   (146, 20)
        #        silver: (39, 27) (40, 27) (39, 28) (40, 28) (100, 29) (101, 29) (100, 30) (101, 30)
        CN(13),
        # M1     gold:   (164, 22)
        #        silver: (148, 16) (149, 16) (148, 17) (149, 17)
        CN(9),
        # A1     silver: (192, 32) (193, 32) (192, 33) (193, 33)
        CN(4, 'Four Silver Coins Behind TNT Blocks Secret')
    ]),
    Levels.MARINATED_RABBIT: CG(Levels.MARINATED_RABBIT).seq([
        # M0     gold:   (61, 13)
        #        silver: (74, 10) (74, 11) (74, 12)
        CN(8),
        # A1     silver: (128, 13) (129, 13) (128, 14) (129, 14)
        CN(4),
        # M2     gold:   (59, 45) (66, 57)
        CN(10),
    ]),
    Levels.A_DIAMONDUS_FOREVER: CG(Levels.A_DIAMONDUS_FOREVER).seq([
        CG('Start position branch', min_mode=True).branch(
            CG('Jazz branch', 'Jazz').seq([
                # A1     gold:   (8, 14)
                CN(5, 'Jazz Toaster Ammo and Gold Coin Below Start Secret'),
                CG('Upper and lower branches').branch(
                    CG('Upper branch').seq([
                        # A2     gold:   (115, 10) (116, 10)
                        CN(10, 'Jazz Silly Sign Detour First Room'),
                        # A5     gold:   (109, 2)
                        CN(5, 'Jazz Silly Sign Detour Fourth Room'),
                    ])
                ).branch(
                    CG('Lower branch').seq([])
                )
            ])
        ).branch(
            CG('Spaz branch', 'Spaz').seq([
                # A6     gold:   (19, 37)
                CN(5, 'Spaz Vines Below First Room'),
                # A7     gold:   (37, 50)
                CN(5, 'Spaz Buttstomp Cavern Below First Room'),
                # S3     gold:   (85, 46) (85, 47)
                CN(10),
                # A8     gold:   (111, 58) (111, 59)
                CN(10, 'Spaz Fruit, Gems and Two Gold Coins Secret')
            ])
        ),
        CG('Shared path').seq([
            # M1     gold:   (182, 20) (155, 33)
            CN(10),
            # A10    gold:   (187, 27) (188, 27)
            CN(10, 'Carrot Crates and Two Gold Coins Secret'),
            # A12    gold:   (253, 58) (253, 59)
            CN(10, 'Gold Coins Beneath Horizontal Spring Secret')
        ])
    ]),
    Levels.FOURTEEN_CARROT: CG(Levels.FOURTEEN_CARROT).seq([
        # M0     gold:   (57, 19)
        #        silver: (109, 4) (110, 3) (110, 4) (110, 5) (111, 4) (199, 21) (200, 21) (199, 22) (200, 22)
        CN(14),
        # A5     gold:   (77, 3)
        CN(5, 'Gold Coin Behind Destructible Blocks Secret'),
        # A8     silver: (161, 6) (162, 6) (163, 6) (161, 7) (162, 7) (163, 7)
        CN(6, 'Six Silver Coins and Super Gem Above Frozen Spring Secret')
    ]),
    Levels.ELECTRIC_BOOGALOO: CG(Levels.ELECTRIC_BOOGALOO).seq([
        # A1     silver: (3, 35) (5, 35) (3, 36) (5, 36)
        CN(4, 'Four Silver Coins in Room Accessed with Pipe Secret'),
        # A4     gold:   (33, 46) (35, 46)
        CN(10, 'Two Gold Coins Blocked By Horizontal Spring Secret'),
        # A8     silver: (119, 49) (120, 49) (121, 49) (122, 49) (123, 49) (124, 49)
        CN(6, 'Six Silver Coins and Fruit and Gems in Shape of \'YO\' Secret'),
        # M4     silver: (163, 33) (164, 33) (163, 34) (164, 34)
        CN(4),
        # A13    silvere: (250, 37) (251, 37) (250, 38) (251, 38) (250, 39) (251, 39)
        CN(6, 'Six Silver Coins Surrounded by Breakable Blocks Secret')
    ]),
    Levels.VOLTAGE_VILLAGE: CG(Levels.VOLTAGE_VILLAGE).seq([
        CG('Start position branch', min_mode=True).branch(
            CG('Jazz branch', 'Jazz').seq([
                # Nothing over here
            ])
        ).branch(
            CG('Spaz branch', 'Spaz').seq([
                # S3     gold:   (53, 59)
                CN(5)
            ])
        ),
        CG('Shared path').seq([
            # M1     silver: (96, 15) (97, 15) (104, 15) (105, 15)
            CN(4),
            # A3     silver: (117, 32) (118, 32) (117, 33) (118, 33)
            CN(4, 'Four Silver Coins and Extra Life Below TNT Blocks Secret'),
            # A5     gold:   (90, 1) (98, 1)
            CN(10, 'Two Gold Coins Behind Multiple Obstacles Secret'),
            # A6     silver: (61, 1) (62, 1) (63, 1) (64, 1)
            CN(4, 'Four Silver Coins Behind Breakable Blocks Secret'),
            # M2     silver: (36, 32) (37, 32) (38, 32)
            CN(3)
        ])
    ]),
    Levels.MEDIEVAL_KINEVAL: CG(Levels.MEDIEVAL_KINEVAL).seq([
        # M0     gold:   (0, 56) (0, 57) (52, 46) (53, 46) (96, 37) (96, 38) (96, 39) (96, 40)
        CN(30),
        # A1     gold:   (88, 42) (88, 43)
        CN(10, 'Two Gold Coins Behind Destructible Pillar Secret'),
        # A2     gold:   (104, 59) (104, 60)
        CN(10, 'Birdy and Two Gold Coins Below Rope Bridge Secret'),
        # A7     gold:   (172, 55) (173, 55) (174, 55) (175, 55)
        CN(20, 'Trigger Crate Detour Second Room'),
        # A8     gold:   (178, 29) (178, 30)
        CN(10, 'Gold Coins After Trigger Crate Detour Secret'),
        # M2     gold:   (208, 46) (209, 46) (208, 47) (209, 47) (199, 44) (200, 44)
        CN(30)
    ]),
    Levels.HARE_SCARE: CG(Levels.HARE_SCARE).seq([
        # M0     silver: (16, 59) (16, 60)
        CN(2),
        # A1     silver: (15, 45) (16, 45)
        CN(2, 'Two Silver Coins Below Vines Secret'),
        # A2     silver: (3, 10) (3, 11)
        CN(2, 'Two Silver Coins High Above Room Secret'),
        # M9     silver: (53, 9) (53, 10) (3, 2) (3, 3) (4, 2) (4, 3)
        CN(6)
    ]),
    Levels.GARGOYLES_LAIR: CG(Levels.GARGOYLES_LAIR).seq([
        # M0     gold:   (18, 12)
        #        silver: (55, 1) (55, 2)
        CN(7),
        # M3     silver: (12, 28) (13, 28) (12, 29) (13, 29)
        CN(4),
        # M4     gold:   (81, 5) (99, 2)
        CN(10),
        # A5     gold:   (89, 34)
        CN(5, 'Room with Green Gems and Gold Coin Secret'),
        # A6     gold:   (133, 0)
        CN(5)
    ]),
    Levels.THRILLER_GORILLA: CG(Levels.THRILLER_GORILLA).seq([
        CG('Start position branch', min_mode=True).branch(
            CG('Jazz branch', 'Jazz').seq([
                # A1     gold:   (82, 42)
                CN(5, 'Jazz Only Gold Coin Secret'),
                # J2     silver: (102, 29) (102, 30) (102, 31) (102, 32)
                CN(4)
            ])
        ).branch(
            CG('Spaz branch', 'Spaz').seq([
                # S0     gold: (31, 55)
                CN(5),
                # A4     silver: (52, 50) (53, 50) (54, 50) (55, 50)
                CN(4, 'Spaz Only Four Silver Coins Above Vine Secret')
            ])
        ),
        CG('Shared path').seq([
            CG('Up and down branches, up Jazz only', min_mode=True).branch(
                CG('Up path', 'Jazz').seq([
                    # A3     silver: (108, 8) (147, 9) (148, 9) (149, 9) (127, 25) (127, 26)
                    CN(6, 'Jazz Only Detour Above Destructible Blocks After Vine')
                ])
            ).branch(
                CG('Down path').seq([
                    # M1     silver: (64, 49) (83, 56)
                    CN(2),
                    # M2     silver: (134, 52) (135, 52) (136, 52)
                    CN(3)
                ])
            )
        ])
    ]),
    Levels.JUNGLE_JUMP: CG(Levels.JUNGLE_JUMP).seq([
        # M1     silver: (43, 30) (43, 31) (74, 7) (75, 7) (74, 8) (75, 8)
        CN(6),
        # M2     gold:   (123, 17)
        CN(5),
        # M3     silver: (123, 30) (124, 30)
        CN(2),
        # M4     silver: (115, 23) (116, 23)
        CN(2),
        # M5     silver: (129, 36) (130, 36) (129, 37) (130, 37) (156, 15) (156, 16)
        CN(6),
        # M8     silver: (211, 37) (212, 37) (211, 38) (212, 38)
        CN(4)
    ]),
    Levels.A_COLD_DAY_IN_HECK: CG(Levels.A_COLD_DAY_IN_HECK).seq([
        # M0     silver: (36, 14) (37, 14) (36, 15) (37, 15) (106, 7) (107, 7) (106, 8) (107, 8) (118, 22) (119, 22) (118, 23) (119, 23)
        CN(12),
        # M1     gold:   (192, 44)
        CN(5),
        # A2     silver: (191, 31) (192, 31) (191, 32) (192, 32)
        CN(4, 'Four Silver Coins Behind Frozen Blocks Secret'),
        # M2     silver: (232, 52) (233, 52) (234, 52)
        # This one requires a region check even if it's on the main path because it's possible to get to the warp before having Toaster access.
        CN(3, 'Room with Large Skull')
    ]),
    Levels.RABBIT_ROAST: CG(Levels.RABBIT_ROAST).seq([
        # M0     gold:   (3, 11)
        #        silver: (20, 33) (22, 33) (24, 33) (26, 33) (28, 33)
        CN(10),
        # M1     gold:   (35, 49)
        CN(5),
        # M3     silver: (111, 2) (112, 1) (112, 2) (112, 3) (113, 2)
        CN(5)
    ]),
    Levels.BURNIN_BISCUITS: CG(Levels.BURNIN_BISCUITS).seq([
        # M0     silver: (3, 34) (4, 34) (16, 46) (17, 46) (16, 47) (17, 47) (15, 4) (16, 4) (15, 5) (16, 5)
        CN(10),
        # A1     silver: (8, 60) (9, 60) (8, 61) (9, 61)
        CN(4, 'Four Silver Coins Behind Sidekick Blocks Secret'),
        # A2     silver: (37, 41) (38, 41) (37, 42) (38, 42)
        CN(4, 'Four Silver Coins in a Corner High Above Main Path Secret'),
        # A4     gold:   (93, 21)
        CN(5, 'Gold Coin Below Buttstomp Blocks Secret')
    ]),
    Levels.BAD_PITT: CG(Levels.BAD_PITT).seq([
        # M1     gold:   (42, 53)
        CN(5),
        # A1     gold:   (89, 24)
        CN(5),
        # M7     gold:   (143, 42) (175, 51)
        CN(10),
        # M9     gold:   (230, 30)
        CN(5)
    ]),
    Levels.DARN_RATZ: CG(Levels.DARN_RATZ).seq([
        # M0     silver: (63, 35) (64, 35)
        CN(2),
        # A2     silver: (66, 49) (67, 49) (66, 50) (67, 50)
        CN(4, 'Four Silver Coins and Gem Crate Secret'),
        # M3     silver: (98, 33) (98, 34) (98, 35) (98, 36)
        CN(4),
        # M5     gold:   (27, 26)
        CN(5),
        # A3     silver: (108, 25) (109, 25) (108, 26) (109, 26) (108, 27) (109, 27)
        CN(6, 'Six Silver Coins Only Accessible Before Trigger Crate Secret'),
        # M6     gold:   (144, 18)
        CN(5)
    ]),
    Levels.RETRO_RABBIT: CG(Levels.RETRO_RABBIT).seq([
        # J0     silver: (54, 39) (55, 39) (54, 40) (55, 40)
        # Despite it being a Jazz area, Spaz can drop down here. Spaz doesn't have any exclusive coins.
        CN(4),
        # M1     silver: (108, 28) (109, 28) (108, 29) (109, 29)
        CN(4),
        # M2     silver: (179, 43) (180, 43) (179, 44) (180, 44)
        CN(4),
        # A2     gold:   (214, 39)
        CN(5, 'Gold Coin Above Speed Blocks Secret'),
        # M4     silver: (206, 41) (206, 42) (206, 43) (206, 44)
        CN(4)
    ]),
    Levels.FROG_STOMP: CG(Levels.FROG_STOMP).seq([
        # No bonus warp or loose coins in this level
    ]),
    Levels.EASTER_BUNNY: CG(Levels.EASTER_BUNNY).seq([
        # M0     silver: (47, 0) (48, 0) (47, 1) (48, 1)
        CN(4),
        # A3     gold:   (189, 4)
        CN(5, 'Gold Coin Above Buttstomp Sucker Tube Secret'),
        # A4     silver: (332, 41) (333, 41) (332, 42) (333, 42)
        CN(4, 'Room at Bottom of Windy Chasm'),
        # M4     silver: (427, 51) (427, 52)
        CN(2)
    ]),
    Levels.SPRING_CHICKENS: CG(Levels.SPRING_CHICKENS).seq([
        # No bonus warp or loose coins in this level
    ]),
    Levels.SCRAMBLED_EGGS: CG(Levels.SCRAMBLED_EGGS).seq([
        # No bonus warp or loose coins in this level
    ]),
    Levels.GHOSTLY_ANTICS: CG(Levels.GHOSTLY_ANTICS).seq([]),
    Levels.SKELETONS_TURF: CG(Levels.SKELETONS_TURF).seq([]),
    Levels.GRAVEYARD_SHIFT: CG(Levels.GRAVEYARD_SHIFT).seq([]),
    Levels.TURTLE_TOWN: CG(Levels.TURTLE_TOWN).seq([]),
    Levels.SUBURBIA_COMMANDO: CG(Levels.SUBURBIA_COMMANDO).seq([]),
    Levels.URBAN_BRAWL: CG(Levels.URBAN_BRAWL).seq([]),
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
