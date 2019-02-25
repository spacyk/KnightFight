# KnightFight

### Description
Knights fighting with deadly weapons, lot of blood everywhere

Script will load and validate knights movement instructions from `moves.txt`. If everythink is ok and instructions are
valid, they will be processed by the game (knights will move and fight). After that json output with the game info will be
created and saved into `final_state.json`.

### Usage
```
python main.py
```
Script has to be executed from the same folder as the `moves.txt` file is in.


### Test

```
pip install -r requirements.txt

pytest test.py
```

### Preview

```
 _ _ _ _ _ _ _(y)
|_|_|_|_|_|_|_|_|
|_|_|_|_|_|_|_|_|
|R|_|A|_|_|D|_|_|
|_|_|_|_|_|_|_|_|
|_|_|_|_|_|_|_|_|
|_|_|M|_|_|H|_|_|
|_|_|_|_|_|_|_|G|
|_|B|_|_|_|_|_|_|
```
