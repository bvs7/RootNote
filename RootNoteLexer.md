
// TODO: Inserted actions from Crafted Improvements! (Better Burrow Bank, Stand and Deliver, Command Warren, Cobbler, Sappers, Codebreakers?, Armourers, Brutal Tactics, Tax Collector, Royal Claim)

// TODO: E&P Crafter Improvements! (Saboteurs, Propaganda Bureau, False Orders, Fox|Mouse|Rabbit Partisans, Eyrie Emigre, Informants, League of Adventurous Mice, Master Engravers?, Murine Broker, Charm Offensive, Swap Meet, Coffin Makers)

// TODO: Expansion factions!

// TODO: Expansion Vagabonds

# `ROOT_GAME`:
`DRAFT`\
`SETUP`\
`PLAY`

### `BUILDING`:
`[sawmill|workshop|recruiter|roost|base]`

### `TOKEN`:
`[wood|keep|sympathy]`

### `SUIT`:
`M|F|R|B`

### `CLEARING`:
`[1|2|3|4|5|6|7|8|9|10|11|12]`

### `FOREST`:
`Forest ([CLEARING]{3,})` // Forests specified by vertex clearings

### `FACTION`:
`[MC|ED|WA|VB]`
<!-- |V2|RC|LC|UD|CC]` -->

### `NAME`:
`"[^"\n]*"` // For now, allow anything as a name as long as it is between double quotes?

### `NUMBER`:
`[0-9]*`

# `DRAFT`:
`[DRAFT_POOL]?`\
`BOARD`\
`DECK`\
`FACTION_CHOICES_TURN_ORDER`

### `DRAFT_POOL`:
`Pool:`\
`[FACTION]{3,9}`

### `BOARD`:
`Board: [Autumn|Winter|Lake|Mountain] [CLEARING_SPEC]?`\
// Clearing specification Not needed for Autumn/Defaults

### `CLEARING_SPEC`:
`([SUIT CLEARING]{12})`

### `DECK`:
`Deck: [Standard | E&P]`

### `FACTION_CHOICES_TURN_ORDER`:
`[FACTION: NAME]{2,6}`

# `SETUP`:
`Setup:`
`[MC_SETUP]?`\
`[ED_SETUP]?`\
`[WA_SETUP]?`\
`[VB_SETUP]?`\
<!-- `[V2_SETUP]?`\
`[RC_SETUP]?`\
`[LC_SETUP]?`\
`[UD_SETUP]?`\
`[CC_SETUP]?` -->

### `MC_SETUP`:
`FACTION:`
`Place Keep in CLEARING`\
`[MC_BUILD]{3}` // Check for building correctness in semantic analysis

### `ED_SETUP`:
`FACTION: Place Roost in CLEARING`\
`ED_LEADER`

### `ED_LEADER`:
`Choose Leader [Builder|Charismatic|Commander|Despot]`

### `WA_SETUP`:
`Draw Supporters`

### `VB_SETUP`:
`VB_CHARACTER`\
`FOREST`\
`[REVEAL_QUEST]{3}

### `VB_CHARACTER`:
`Choose Character: [Thief|Tinker|Ranger]`
<!-- |Vagrant|Arbiter|Scoundrel|Adventurer|Ronin|Harrier]` -->

### `REVEAL QUEST`:
`Reveal Quest [SUIT ITEM+ITEM|QUEST_NAME]`

### `ITEM`:
`[sword|torch|boot|crossbow|hammer|bag|tea|coins]`

### `QUEST_NAME`
// TODO

# `PLAY`:
Begin Play:
`[FACTION_TURN]*`
`WIN`

### `FACTION_TURN`:
`FACTION: TURN`

## `TURN`:
`[MC_TURN|ED_TURN|WA_TURN|VB_TURN]`
<!-- |V2_TURN|RC_TURN|LC_TURN|UD_TURN|CC_TURN]` -->

## `MC_TURN`:
`[CRAFT]*`\
`[ [MC_SPEND_BIRD]* [MC_ACTION] ]{0,3}`\ // Can spend bird cards between actions
`[MC_SPEND_BIRD]*`\
`[DRAW]?`\
`[DISCARD]?`

### `CRAFT`:
`Craft CARD`

### `MC_SPEND_BIRD`:
`Spend CARD: MC_ACTION` // Marquise spends a bird card to get a free action

### `MC_ACTION`:
`BATTLE | MC_MARCH | MC_RECRUIT | MC_BUILD | OVERWORK`

### `BATTLE`:
`Battle x FACTION in CLEARING [AMBUSH]? BATTLE_ROLLS` // Vagabond battle is a separate spec\
`[BATTLE_RESPONSE]*`

### `AMBUSH`:
`SUIT Ambush [(SUIT Ambush)]?` // Could be cancelled

### `BATTLE_ROLLS`:
`(NUMBER, NUMBER)[->(NUMBER,NUMBER)]?` // Space for counting extra hits?

### `BATTLE_RESPONSE`:
`VB_DAMAGE | REMOVE | HOSTILE`

### `REMOVE`:
`* Remove [BUILDING|TOKEN]{1,}`\
`[OUTRAGE]?`

### `HOSTILE`:
`* FACTION Hostile to FACTION` // First Faction can be VB or V2?

### `MC_MARCH`:
`March MOVE[, MOVE]?`

### `MOVE`:
`Move NUMBER from CLEARING to CLEARING` // Vagabond move is separate again\
`[OUTRAGE]?` 

### `MC_RECRUIT`:
`Recruit [CLEARING]*` // Clearings specified if incomplete recruit due to lack of warriors

### `MC_BUILD`:
`Build MC_BUILDING in CLEARING [wood: [CLEARING]*]?` // Note the clearings wood comes from (if not trivial) 

### `MC_BUILDING`:
`[sawmill|workshop|recruiter]`

### `OVERWORK`:
`Overwork CARD CLEARING`

### `DRAW`:
`Draw NUMBER`

### `DISCARD`:
`Discard NUMBER [CARD]*`

## `ED_TURN`:
`[Emergency Orders]?`\
`[ED_DECREE]{0,2}`// Optional in case win?\
`[New Roost]?`\
`[CRAFT]*`\
`[ED_RESOLVE_DECREE]?`// Optional in case win?\ 
`[ED_SCORE]?`\
`[DRAW]?`\
`[DISCARD]?`

### `ED_DECREE`:
`Decree CARD SUIT [recruit|move|battle|build]`

### `ED_RESOLVE_DECREE`:
`[ED_RECRUIT]*`
`[ED_MOVE]*`
`[ED_BATTLE]*`
`[ED_BUILD]*`
`[ED_TURMOIL]?`

### `ED_RECRUIT`:
`[SUIT] Recruit [NUMBER]? CLEARING`

### `ED_MOVE`:
`[SUIT] Move NUMBER from CLEARING to CLEARING`\
`[OUTRAGE]?` 

### `ED_BATTLE`:
`[SUIT] Battle x FACTION in CLEARING [AMBUSH]? BATTLE_ROLLS`\
`[BATTLE_RESPONSE]*`

### `ED_BUILD`:
`SUIT Build in CLEARING`

### `ED_TURMOIL`:
`Turmoil -NUMBER ED_LEADER`

### `ED_SCORE`:
`Score NUMBER`

## `WA_TURN`:
`[WA_REVOLT]*`\
`[WA_SPREAD_SYMPATHY]?`\
`[CRAFT|WA_MOBILIZE|WA_TRAIN]*`\
`[MOVE|BATTLE|WA_RECRUIT|WA_ORGANIZE]*`\

### `OUTRAGE`:
`* Outrage [x|draw]`

### `WA_REVOLT`:
`Revolt CLEARING CARD,CARD`

### `WA_SPREAD_SYMPATHY`:
`Spread [CLEARING [CARD]*]{1,}`

### `WA_MOBILIZE`:
`Mobilize NUMBER`

### `WA_TRAIN`:
`Train CARD`

### `WA_RECRUIT`:
`Recruit [NUMBER]? CLEARING`

### `WA_ORGANIZE`:
`Organize CLEARING`

### `VB_TURN`
`[VB_REFRESH]?`\
`[VB_SLIP]?`\
`[VB_MOVE | VB_BATTLE | VB_EXPLORE | VB_AID | VB_QUEST | VB_STRIKE | VB_REPAIR | CRAFT | VB_SPECIAL]*`\
`[VB_EVENINGS_REST]?`\
`[DRAW]?`\
`[DISCARD]?`\
`[VB_REMOVE_ITEMS]?`

### `VB_REFRESH`:
`Refresh [VB_ITEM]*`

### `VB_TIEM`:
`ITEM[\.]?[x]?` // For Specifying exhausted or broken items?

### `VB_SLIP`:
`Slip [from [CLEARING|FOREST]]? to [CLEARING|FOREST]`

### `VB_MOVE`:
`Move [from [CLEARING|FOREST]]? to CLEARING`

### `VB_BATTLE`:
`Battle x FACTION [in CLEARING]? [AMBUSH]? BATTLE_ROLLS` // Vagabond battle is a separate spec\
`[BATTLE_RESPONSE]*`

### `VB_DAMAGE`:
`* Damage [VB_ITEM]*`

### `VB_EXPLORE`:
`Explore for ITEM [in CLEARING]? [left ITEM]?` // If two VB, item can be left

### `VB_AID`:
`[Aid VB_ITEM, CARD to FACTION for VB_ITEM  |`\
` Aid FACTION with VB_ITEM, CARD for VB_ITEM]`\
`[* Improve Relations FACTION NUMBER]?`

### `VB_STRIKE`:
`Strike x FACTION`\
`[BATTLE_RESPONSE]?` // Either remove building or hostile, not both?

### `VB_REPAIR`:
`Repair VB_ITEM`

### `VB_SPECIAL`:
`[VB_STEAL | VB_DAY_LABOR | VB_HIDEOUT]`

### `VB_STEAL`:
`Steal from FACTION`

### `VB_DAY_LABOR`:
`Day Labor CARD`

### `VB_HIDEOUT`:
`Hideout [VB_ITEM]{1,3}`

### `VB_EVENINGS_REST`:
`Evening's Rest`

### `VB_REMOVE_ITEMS`:
`Remove [VB_ITEM]+`

## `WIN`:
`FACTION wins`\
`[FACTION NUMBER]{2,6}`

# MISC

### `SPECIAL_WORDS`:
```
sawmill | workshop | recruiter | base |
wood | keep | sympathy |
Pool | Board | Spring | Winter | Lake | Mountain |
Deck | Standard | E&P | Place Keep | 
Leader | Builder | Charismatic | Commander | Despot |
Draw Supporters | Thief | Tinker | Ranger |
Forest | Reveal Quest | sword | torch | boot | crossbow |
hammer | bag | tea | coins |
Craft | Spend | Battle | x | Ambush
Remove | Hostile | March | Move | Recruit | Build |
Overwork | Draw | Discard |
Emergency Orders | New Roost | Decree | Turmoil | Score |
Outrage | Revolt | Spread | Mobilize | Train | Organize |
Refresh | Slip | Damage | Explore | Aid | Improve Relations |
Strike | Repair | Steal | Day Labor | Hideout | Evening's Rest |
wins | to | for | from | with | in | left
```