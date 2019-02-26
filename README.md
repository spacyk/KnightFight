# KnightFight

### Description
Knights fighting with deadly weapons.

Script will load and validate knights movement instructions from `moves.txt`. If everythink is ok and instructions are
valid, they will be processed by the game (knights will move and fight). After that, json output with the game info will be
created and saved into `final_state.json`.

Check `ASSIGNEMENT.md` for the details.

### Usage
```
python knight_fight/main.py
```
Script has to be executed from the same folder as the `moves.txt` file is in.


### Test
```
pip install -r requirements.txt

pytest tests/battlefield_tests.py
```

### Preview
Starting positions of the knights (in the corners) and 4 special items in the middle.
```
|R|_|_|_|_|_|_|Y|
|_|_|_|_|_|_|_|_|
|_|_|A|_|_|D|_|_|
|_|_|_|_|_|_|_|_|
|_|_|_|_|_|_|_|_|
|_|_|M|_|_|H|_|_|
|_|_|_|_|_|_|_|_|
|B|_|_|_|_|_|_|G|
```
