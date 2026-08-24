# Archipelago Manual Implementation for Jazz Jackrabbit 2

This repository branch contains the implementation of a new custom Manual game
for the Archipelago multiworld project. Like all other Manual games,
it operates on a "honor system" principle where there's no game mod,
and instead you'll operate with a dedicated Manual client that helps with
keeping track of what you've received from the multiworld and communicates
the checks you're doing in-game back to the host.

For more information about Manual itself, please see its 
[documentation](https://github.com/ManualForArchipelago/Manual).
The specifics of how this particular manual implementation works can be
similarly found in its own [introduction](src/docs/en_Manual_JazzJackrabbit2_Soulweaver.md)
and its [setup guide](src/docs/setup_en.md) of sorts.

## Currently known issues
So far, the majority of work has gone towards getting the four main base 
game episodes into a decent enough state. The Shareware, the Secret Files, and
Christmas Chronicles episodes only have a skeleton implementation so far.

While some parts of logic have been fleshed out for the more developed 
episodes, these parts of logic in specific are acknowledged to be lacking
at the moment:

- Trigger crates have inconsistent logic around them. It is expected that the
  player can either destroy them with a special move, if they have obtained it,
  or break it with TNT, but for the most part these restrictions currently
  don't apply.
- Weapon access in any specific level is handled inconsistently. In particular,
  TNT can be used for destroying buttstomp scenery blocks, but ammo for it
  must in most cases be brought over from an earlier level that the player is
  able to travel from without missing access for any levels in between.
- Bonus warp logic is incomplete. Some levels with simpler coin placements
  have been set up properly, but more complex ones require careful
  consideration of when the player has access to enough coins.

## AI usage disclosure
No AI tools have been used in any part of the development of this custom game
implementation, including for code or asset generation, consulting, analysis,
or for any other reason. I'm not aware if this is also the case with the
underlying Manual client itself, so please check this with its authors
separately.
