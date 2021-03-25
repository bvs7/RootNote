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


## RootState
The class RootState should contain all necessary components of a game of root. This includes:

RootState:
- Board State
  - Board Type
  - Clearing States (with ClearingIndex?) fn for str -> ClearingIndex
    - Warriors (number for each non-VB faction)
    - Buildings (Max no. of building slots)
      - Ruin (Item(s))
    - Tokens
  - Paths : Mapping[Tuple[Clearing,Clearing], PathType]
  - Forests : Set[List[Clearing]]
- Deck State (with discard pile)
  - Deck Type
  - Lizards?
- Item Cache
- Drafting Info?
- Faction States
  - State for each faction board

### Building a Game

When do each of the parts of the board state need to be decided?

RootState:
- Board State | Immediately? Needed for any other decisions
  - Board Type | During setup, before adset draft, but with basic faction assignment
  - Clearing States (with ClearingIndex?) fn for str -> ClearingIndex | Initialized before faction setup, with Board creation? Edited with faction setup
    - Suit
    - Warriors (number for each non-VB faction)
    - Buildings (Max no. of building slots)
      - Ruin (number of items under)
    - Tokens
  - Paths : Mapping[Tuple[Clearing,Clearing], PathType] | Initialized with board setup
  - Forests : Set[List[Clearing]] | Initialized with Board setup
- Deck State (with discard pile) | Initialized before basic faction choices, before adset draft, with board?
  - Deck Type
  - Lizards? | Edits the discard info upon Lizard setup
- Item Cache | Initialized with Board?
- Drafting Info?
- Faction States
  - State for each faction board

Phases of setup for states:
Board State:
- Init: Select Board Type: Init Clearings/Paths/Forests with defaults!
- Might as well separate default suits for later

Deck State:
- Init: Deck Type

Drafting Info
Faction Info

### Setup Phase
Use cases:
- Basic Setup, Simultaneous setup?
- AdSet, Rigorous setup

#### AdSet:
1) Choose Map | Choose Deck
2) Seat Players? (Not necessary to notate)
3) Draw Cards (Still nothing noted?)
4) Set Up Hirelings (Optional, not now)
5) Deal Factions to Draft Pool (Note which factions are available. Lock Last White Card assumed)
6) One by One, note faction choices and setup. Faction choice/player name, Setup choices
7) Hands assumed

So what is the path for state setup?

- Note Board Type and Beck Type in any order, Note Board clearing suits
- Note Factions in Draft Pool
- Note player choices and setup options for each faction. Init faction Boards during each
- Finish setup (Items, Turn order, etc?) Move to play phase

#### Basic Setup:
Fewest Requirements possible:

Phase 1:
- Assign Factions to Players ("Pick" with no draft -> assign?)
- Choose Board and Deck
- Choose seating order
Phase 2:
- Faction Setup

#### Shared Requirements:
- Board and Deck must be decided before any faction setup
- Seating order decided before any faction setup

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

