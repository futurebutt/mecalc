### Specific To-Dos:
* Distinguish ability flat values from percent bonuses more clearly; split them into categories somehow. Bonus calculation right now mixes adds values together indifferently to flat vs. percent. For example: Nemesis talent bonus calculations for Lift, Warp, etc.
* Refactor for consistent order of operations across all summaries.
* There only needs to be a single Armor summary. Which armors are unlocked can be listed under Shepard summary, along with total sum damage reduction and hardening from all sources.
* Enums are... a bit all over the place. They make it hard to tell whether calculations are complete from looking at them in the summary functions. It might be best to have them be as granular as possible: any percent bonus that applies to multiple things should instead be broken into those multiple things.
* I don't even know if enums are the way here, but it's not back breaking to at least put them to the best use possible before deciding whether to toss them (and possible associated stuff) out for some other structure(s).
* Refactor summary.py to minimize code repition since there's so many similarities. Doesn't need to be extremely clever, just more economical and consistently structured across summary methods so they all read exactly the same way. This may follow the above two points.
* GUI: display rank number next to bars.
* GUI: set rank directly. maybe by clicking TalentPoint labels.
### General To-Dos:
* GUI + Talents: reset rank
* GUI: load sets of talents (Soldier, Adept, etc.)
* GUI: easier-to-read output formatting.
* GUI: select/show/hide/skip desired summaries.
* GUI: static elements, maybe openable/closeable for summary items.
* GUI: display calculations on mouseover.