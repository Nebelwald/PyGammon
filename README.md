# PyGammon
PyGammon is a python implementation of Backgammon.
The purpose is to create and test different AI models.

## Backgammon rules
English: https://en.wikipedia.org/wiki/Backgammon#Rules  
German: https://de.wikipedia.org/wiki/Backgammon#Spielbeginn_und_Spielablauf

## How to call
```
$ python py_gammon.py -h
usage: py_gammon.py [-h] -w {human,ai} -b {human,ai} [-i]

Python implementation of Backgammon to create and test AI models.

options:
  -h, --help            show this help message and exit
  -w {human,ai}, --white {human,ai}
  -b {human,ai}, --black {human,ai}
  -i, --interactive

'Interactive' mode will pause the game after each move of an AI to follow its strategy.

```
e.g.:
```
$ python py_gammon.py -w human -b ai -i
```
Note: As more AI models will be implemented, more keywords will be added to select the different AI models.

## Logging
The same output that gets written to the terminal gets written to a log file in
```
<dir/of/py_gammon.py>/log/
```

## Gameboard
```     
 ↙12←11←10← 9← 8← 7← 6← 5← 4← 3← 2← 1
↓╔═════════════════╦═════════════════╗
↓║5W│  │  │  │3B│  ║5B│  │  │  │  │2W║ 0B
↓╠═══════ 0W ══════╬═══════ 0B ══════╣
↓║5B│  │  │  │3W│  ║5W│  │  │  │  │2B║ 0W
↓╚═════════════════╩═════════════════╝
 ↘13→14→15→16→17→18→19→20→21→22→23→24
```
The view is always from the WHITE players perspective.


## Player models
The player models include an interface for human input (so that a human can play against an AI) and the AI models.

### Human interface
The input is entered by
```
<pos,width>, e.g. 1,2
```

### AI model: "Always move last token"
This AI opponent is a very simple one that follows the policy to always move the last possible token. For each move it can make, it iterates from the last position to the first index and tries to move a token.

## LICENCE
All rights reserved.  
Copyright (c) 2024, Leonhard Klingert
