# Jazz Jackrabbit 2 Manual Randomizer Setup Guide

## Required Software
- Any legally obtained retail version(s) of the Jazz Jackrabbit 2 game
- The files for the episodes included in the base game (_Formerly a Prince_, _Jazz in Time_, _Flashback_, _Funky Monkeys_, and _Shareware Demo_)
- Optionally: the files for the _The Secret Files_ episode
- Optionally: the files for either the _Holiday Hare '98_ episode or the _Christmas Chronicles_ episode

It isn't necessary to play the episodes with the same game version as the files are from (i.e. feel free to copy the base game episode files into a _The Secret Files_ installation), but you must source all of them from installations you own yourself. [The release sold on GOG](https://www.gog.com/en/game/jazz_jackrabbit_2_collection) provides an easy method to gain access to every officially released episode in one neat bundle.

## Installation Procedures
As far as you've installed the base Manual APWorld as well as this JJ2-specific APWorld, you're ready to follow the usual other steps for getting a multiworld going.

## Joining a MultiWorld Game
As with any other manual implementation, you'll be using the Manual Client to connect to the multiworld. The client behaves exactly like your other text clients, but it includes a field for the type of manual game you're currently playing; you'll need to select Manual_JazzJackrabbit_Soulweaver from this dropdown before connecting.

## Multiplayer Manual
The Manual tab in the client window contains everything you'll need for managing your progress through the game.

On the left, the items you have received are shown. You should take note of the unlocks you've received in particular, as they limit the locations you're able to visit. On the right, the list of locations itself is shown. Whenever you visit a location or get a check by defeating a boss or clearing a level, you can mark it as visited by clicking on that location. The client will then inform the room about that check, and an item is sent to one of the players in return as with any automatic implementation. Locations you're not currently expected to be able to get to are grayed out and cannot be sent. On this list you can also find the victory condition, which you can send after finishing every level you've enabled and which will mark your game as complete.

**NOTE**: While level access is expected to be consistent with received level unlock items, the logic for accessing specific locations inside those levels is not thoroughly tested and may be too strict.