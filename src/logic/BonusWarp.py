import logging
from typing import Self

from .Enums import Levels, StartPositionCharacterName

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
                # J1     gold:   (112, 8) (112, 9) (189, 8)
                CN(15),
                # A2     gold:   (163, 6)
                CN(5, 'Jazz Only Gold Coin Secret'),
                # J3     gold:   (20, 23) (56, 31) (57, 31)
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
                # A8     gold:   (130, 61)
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
                CN(1, 'Spaz Silver Coins Behind Blocks Entrance Side Secret'),
                # S1     silver: (36, 42) (36, 43) (36, 44)
                CN(3, 'Spaz Silver Coins Behind Blocks Exit Side Secret'),
                # S1     silver: (36, 45)
                CN(1)
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
        # A7     gold:   (119, 20)
        CN(5, 'Gold Coin Blocked By Spring Secret'),
        # A8     silver: (161, 6) (162, 6) (163, 6) (161, 7) (162, 7) (163, 7)
        CN(6, 'Six Silver Coins and Super Gem Above Frozen Spring Secret')
    ]),
    Levels.ELECTRIC_BOOGALOO: CG(Levels.ELECTRIC_BOOGALOO).seq([
        # M1     silver: (5, 57) (5, 58) (7, 57) (7, 58) (15, 57) (15, 58) (17, 57) (17, 58)
        CN(8),
        # A1     silver: (3, 35) (5, 35) (3, 36) (5, 36)
        CN(4, 'Four Silver Coins in Room Accessed with Pipe Secret'),
        # A4     gold:   (33, 46) (35, 46)
        CN(10, 'Two Gold Coins Blocked By Horizontal Spring Secret'),
        # A8     silver: (119, 49) (120, 49) (121, 49) (122, 49) (123, 49) (124, 49)
        CN(6, 'Six Silver Coins and Fruit and Gems in Shape of \'YO\' Secret'),
        # M4     silver: (163, 33) (164, 33) (163, 34) (164, 34)
        CN(4),
        # A13    silver: (250, 37) (251, 37) (250, 38) (251, 38) (250, 39) (251, 39)
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
        # M0     gold    (28, 45)
        CN(5),
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
    Levels.GHOSTLY_ANTICS: CG(Levels.GHOSTLY_ANTICS).seq([
        # M0     gold:   (35, 5) (89, 14)
        CN(10),
        # M3     silver: (139, 69)
        CN(1),
        # M7     gold:   (208, 82)
        #        silver: (124, 119) (125, 119) (124, 120) (125, 120)
        CN(9),
        # A6     silver: (119, 87) (120, 87) (119, 88) (120, 88)
        CN(4, 'Silver Coins Below Trigger Crate Ledge')
    ]),
    Levels.SKELETONS_TURF: CG(Levels.SKELETONS_TURF).seq([
        # M0     gold:   (237, 7) (253, 14)
        #        silver: (147, 34) (147, 35) (150, 34) (150, 35) (153, 34) (153, 35) (156, 34) (156, 35)
        CN(18),
        # A1     silver: (1, 42) (2, 42) (1, 43) (2, 43)
        CN(4, 'Four Silver Coins on Roof Above Start'),
        # A3     silver: (282, 3) (283, 3) (282, 4) (283, 4)
        CN(4, 'Four Silver Coins Above Vines')
    ]),
    Levels.GRAVEYARD_SHIFT: CG(Levels.GRAVEYARD_SHIFT).seq([
        # No bonus warp or loose coins in this level
    ]),
    Levels.TURTLE_TOWN: CG(Levels.TURTLE_TOWN).seq([
        # M1     gold:   (115, 39)
        CN(5),
        # A4     silver: (1, 65) (1, 66) (1, 67) (1, 68) (1, 69)
        CN(5, 'Five Silver Coins Chute Secret'),
        # M6     gold:   (336, 97) (179, 115)
        #        silver: (294, 70) (295, 70) (294, 71) (295, 71) (250, 133) (251, 133) (250, 134) (251, 134)
        CN(18)
    ]),
    Levels.SUBURBIA_COMMANDO: CG(Levels.SUBURBIA_COMMANDO).seq([
        # M0     silver: (0, 6)
        CN(1),
        # A4     gold:   (96, 17)
        CN(5, 'Gold Coin High Above End of Topmost Section Secret'),
        # M4     gold:   (74, 35)
        #        silver: (115, 29) (116, 29) (115, 30) (116, 30)
        # The gold coin is tricky, but can be obtained with just a regular dash jump.
        CN(9),
        # M7     gold: (46, 123) (50, 123)
        CN(10)
    ]),
    Levels.URBAN_BRAWL: CG(Levels.URBAN_BRAWL).seq([
        # M0     gold: (16, 5)
        CN(5),
        # M4     silver: (185, 107) (186, 107) (185, 108) (186, 108)
        CN(4),
        # A2     silver: (255, 80) (256, 80) (257, 80) (255, 81) (256, 81) (257, 81) (255, 82) (256, 82) (257, 82)
        CN(9, 'Manhole Loop Onto the Roof of Building With Nine Silver Coins'),
        # M7     silver: (213, 138) (214, 138) (213, 139) (214, 139)
        CN(4)
    ]),
    Levels.SNOW_BUNNIES: CG(Levels.SNOW_BUNNIES).seq([
        # M0     silver: (25, 12) (26, 12) (25, 13) (26, 13)
        CN(4),
        # A1     gold:   (76, 9)
        CN(5, 'Gold Coin High Above Hidden Spring Secret'),
        # M1     silver: (84, 41) (85, 41) (84, 42) (85, 42)
        CN(4),
        # A3     silver: (194, 0) (195, 0) (194, 1) (195, 1)
        CN(4, 'Four Silver Coins and Goodies on Vines Above Spike Pit'),
        # M4     silver: (334, 1) (335, 1) (334, 2) (335, 2) (403, 0) (404, 0) (403, 1) (404, 1)
        CN(8)
    ]),
    Levels.DASHING_THRU_THE_SNOW: CG(Levels.DASHING_THRU_THE_SNOW).seq([
        # M0     gold:   (1, 1)
        CN(5),
        # A2     silver: (153, 1) (154, 1) (155, 1) (156, 1) (157, 1)
        CN(5, 'Five Silver Coins in Sucker Tube Secret'),
        # M4     gold: (687, 42) (687, 43)
        #        silver: (507, 46) (508, 46) (507, 47) (508, 47) (507, 48) (508, 48) (528, 43) (545, 43)
        CN(18)
    ]),
    Levels.TINSEL_TOWN: CG(Levels.TINSEL_TOWN).seq([
        # A4     silver: (184, 33) (185, 33) (184, 34) (185, 34)
        CN(4, 'TNT Block Bypass into Room With Four Silver Coins Secret'),
        # M2     silver: (247, 39) (248, 39) (247, 40) (248, 40)
        CN(4),
        # M8     silver: (402, 1) (403, 1) (402, 2) (403, 2)
        CN(4),
        # A10    gold:   (560, 6)
        CN(5, 'Burrowsville Upper Layer'),
        # A14    silver: (608, 47) (609, 47) (610, 47)
        CN(3, 'Three Silver Coins Above Spring Secret'),
        # M13    gold:   (700, 36)
        CN(5)
    ]),
}
