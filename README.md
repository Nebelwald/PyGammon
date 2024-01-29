# PyGammon
PyGammon is a python implementation of Backgammon.

## Gameboard
```
            ↓ WHITE player ↓          
 ↙12←11←10← 9← 8← 7← 6← 5← 4← 3← 2← 1
↓╔═════════════════╦═════════════════╗
↓║5B│  │  │  │3W│  ║5W│  │  │  │  │2B║ 0W
↓╠═══════ 0B ══════╬═══════ 0W ══════╣
↓║5W│  │  │  │3B│  ║5B│  │  │  │  │2W║ 0B
↓╚═════════════════╩═════════════════╝
 ↘13→14→15→16→17→18→19→20→21→22→23→24
            ↑ BLACK player ↑
```

The input is encoded by
```
<pos>,<width> (e.g. 1,2)
```

## AI opponents
It is planned to implement several AI opponents.

### "Always move last tokens"
This AI opponent is a very simple one that follows the policy to always move the last possible token. For each move it can make, it iterates from the last position to the first index and tries to move a token.
