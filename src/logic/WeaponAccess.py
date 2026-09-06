from .Enums import Levels, Weapons

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
    },
    Levels.GHOSTLY_ANTICS: {
        Weapons.BOUNCER: True,
        Weapons.TOASTER: True
    },
    Levels.SKELETONS_TURF: {
        Weapons.TOASTER: True
    },
    Levels.GRAVEYARD_SHIFT: {
        Weapons.BOUNCER: ['After Trigger Crate in Room Behind Sturdy Blocks Secret'],
        Weapons.TOASTER: True
    },
    Levels.TURTLE_TOWN: {
        Weapons.BOUNCER: True,
        Weapons.TOASTER: True
    },
    Levels.SUBURBIA_COMMANDO: {
        Weapons.BOUNCER: True,
        Weapons.FREEZER: True,
        Weapons.SEEKER: True,
        Weapons.TNT: True
    },
    Levels.URBAN_BRAWL: {
        Weapons.TOASTER: True
    },
    Levels.SNOW_BUNNIES: {
        Weapons.BOUNCER: True,
        Weapons.FREEZER: True,
        Weapons.SEEKER: True,
        Weapons.RF: ['RF Ammo Inside Destructible Block Platforms Secret'],
        Weapons.TNT: True
    },
    Levels.DASHING_THRU_THE_SNOW: {
        Weapons.BOUNCER: True
    },
    Levels.TINSEL_TOWN: {
        Weapons.TNT: True,
        Weapons.ELECTRO: True
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
    # Bad Pitt #1: The rest of the level
    (Levels.BAD_PITT, 1): True,
    # Suburbia Commando #0: Most of the level
    (Levels.SUBURBIA_COMMANDO, 0): False,
    # Suburbia Commando #1: The last stretch to the exit
    (Levels.SUBURBIA_COMMANDO, 1): True,
    # Snow Bunnies #0: The entire level
    (Levels.SNOW_BUNNIES, 0): True,
    # Tinsel Town #0: The entire level
    (Levels.TINSEL_TOWN, 0): True
}
