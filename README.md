# RootNote

A language for noting moves in a Root Game

## Road Map

- [ ] RootState. Data classes and operations for simulating the current state of the game.
  - [ ] [Optional] RootState Agnostics. Let the state be partially undefined. (don't know exactly where wood was placed, the suits of clearings, cards in discard pile, etc.)
  - [ ] [Optional] RootState for Expansions.
- [ ] RootMove. A Base Class for a "Move" which is an atomic decision made in game.
- [ ] RootState takes RootMove objects and updates state, or raises an error/warning if the mvoe seems impossible.
  - [ ] [Optional] RootLog compilation. Upon taking a RootMove, a RootState can output the appropriate RootLog to record physical part movements.
- [ ] RootNote Parser. Parse text lines into RootMoves using a Grammar
  - [ ] [Optional] Command Line Note Taking. Enter a line of RootNote, see updated RootState, options to see more details or undo moves
  - [ ] [Optional] RootNote Interpreter. Parse a file of RootNote and output ending RootState or RootLog
- [ ] RootNote Language Server. Create a Language Server that Checks, Suggests Completions, Marks Errors or Warnings, and returns State in helpful ways. Enable Very easy RootNote taking.

## Example Code
Some goals for eventual examples of RootNote code:
```
MC:
March 3[N]->[NW], 4[NW]->[W]
Overwork [NW] {Bird-Dominance}
Build [W] Sawmill
# MC has 29 points!
ED:
Decree {M} Recruit, {B} Build
Recruit [SE], [SCW], [SCE]
Move 2[SE]->[SCE], 4[SCE]->[SCW], 5[SCW]->[CW]
Battle MC [CW] (3,2) # Eyrie has 4, MC has 0
Build [CW]
```

Clearings can be identified by either a directional scheme (North, South, Central, West, East, Mid, etc) or by Bot Priority Markers? Or, use a custom mapping

### Types:
#### Independent of Factions:
- BoardType
- Suit
- PathType
- DeckType
- Card (Base type, with functional methods)
- TurnPhase
- GamePhase (Setup or Turn(Faction))

#### Dependent on Factions, used in general?:
- Faction
- Building
- Token


How to organize everything?

There are General Parts:

Types
State
Actions
Parser

Then there are faction parts for each of these

F[Types]
F[State]
F[Actions]
F[Parser]

And Bases for building things?

Base_Types
Base_State?
Base_Actions?
Base_Parser?

Dependencies seem to go:

Types -> F[Types] -> Base_Types

Base_State -> Types
State -> F[State] -> Base_State

Base_Actions -> Types
Actions -> F[Actions] -> Base_Actions

Base_Parser -> Types
Base_Parser -> State?
Base_Parser -> Actions?
Parser -> F[Parser] -> Base_Parser

So, Types is its own module?
No, Base is its own module
Each faction is its own module? Or just own file?

lets do fewer modules for now...

with ordered imports?

Desired behavior of dependent types:
- Check if obj is building/token/faction
- Get faction of building/token
- Get list of buildings/tokens/buildings+tokens