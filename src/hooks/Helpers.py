from typing import Optional, Any
from BaseClasses import MultiWorld

def enabled_if_either_hh_or_cc(multiworld: MultiWorld, player: int, thing: dict[str, Any]) -> Optional[bool]:
    from ..Helpers import get_option_value

    enable_cc = get_option_value(multiworld, player, 'enable_cc') == True
    enable_hh = get_option_value(multiworld, player, 'enable_hh') == True

    individual_level_unlock_keys = get_option_value(multiworld, player, 'individual_level_unlock_keys') == True

    if 'category' in thing.keys():
        if 'Individual Level Unlocks' in thing['category'] and not individual_level_unlock_keys:
            return False
        elif 'Progressive Level Unlocks' in thing['category'] and individual_level_unlock_keys:
            return False

        if 'Holiday Hare Content' in thing['category'] and 'Christmas Chronicles Content' in thing['category']:
            return enable_cc or enable_hh

    return None

def enabled_if_either_cc_or_tsf(multiworld: MultiWorld, player: int, thing: dict[str, Any]) -> Optional[bool]:
    from ..Helpers import get_option_value

    enable_cc = get_option_value(multiworld, player, 'enable_cc') == True
    enable_tsf = get_option_value(multiworld, player, 'enable_tsf') == True

    if 'category' in thing.keys():
        if 'The Secret Files Content' in thing['category'] and 'Christmas Chronicles Content' in thing['category']:
            return enable_cc or enable_tsf

    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    return None


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item: dict[str, Any]) -> Optional[bool]:
    lori_check = enabled_if_either_cc_or_tsf(multiworld, player, item)
    xmas_levels_check = enabled_if_either_hh_or_cc(multiworld, player, item)

    if lori_check is not None:
        return lori_check
    elif xmas_levels_check is not None:
        return xmas_levels_check
        
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location: dict[str, Any]) -> Optional[bool]:
    xmas_levels_check = enabled_if_either_hh_or_cc(multiworld, player, location)

    if xmas_levels_check is not None:
        return xmas_levels_check
    
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the event, False to disable it, or None to use the default behavior
def before_is_event_enabled(multiworld: MultiWorld, player: int, event: dict[str, Any]) -> Optional[bool]:
    xmas_levels_check = enabled_if_either_hh_or_cc(multiworld, player, event)

    if xmas_levels_check is not None:
        return xmas_levels_check
    
    return None
