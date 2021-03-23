# RootNote

A language for noting moves in a Root Game

Need a grammar for move types
-  Specific grammar for each faction's turn?

State objects to record the state of the game during interpretation. This allows for implict moves to be generated.

Eventually, a Language Server Protocol language for RootNote, to allow real time error checking and code completion of RootNote!

Some goals for eventual examples of RootNote code:
```
MC:
March 3[N]->[NW], 4[NW]->[W]
Overwork [NW] {Bird-Dominance}
Build [W] Sawmill
# MC has 29 points!
ED:
Decree {M} Recruit, {B} Build
Recruit [SE], [SMW], [SME]
Move 2[SE]->[SME], 4[SME]->[SMW], 5[SMW]->[CW]
Battle MC [CW] (3,2) # Eyrie has 4, MC has 0
Build [CW]
```

Clearings can be identified by either a directional scheme (North, South, Central, West, East, Mid, etc) or by Bot Priority Markers? Or, use a custom mapping defined at top


