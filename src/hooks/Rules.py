import logging
from BaseClasses import MultiWorld, CollectionState

from ..Helpers import is_option_enabled
from ..logic.BonusWarp import COIN_ACCESS_BY_LEVEL_LOOKUP, CoinPathGroup
from ..logic.Enums import Levels, Weapons
from ..logic.LevelOrder import LEVEL_ORDER_LOOKUP
from ..logic.WeaponAccess import LEVEL_WEAPON_ACCESS_LOOKUP, IN_LEVEL_TNT_RULES


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
