# TermFormer: A Terminal Platformer
[![wakatime](https://wakatime.com/badge/user/bf51f838-e5c2-44d9-90ed-ec0da6b90b26/project/9784436c-bbbd-4409-bc19-b488c8e32a30.svg)](https://wakatime.com/badge/user/bf51f838-e5c2-44d9-90ed-ec0da6b90b26/project/9784436c-bbbd-4409-bc19-b488c8e32a30)
[![language](https://img.shields.io/badge/Language-python-yellow)](https://www.python.org)
[![creator](https://img.shields.io/badge/Creator-EpicEfeathers-0051FF?logo=github)](https://github.com/EpicEfeathers)
![creator](https://img.shields.io/badge/>1800_lines_of_code-048100)


A terminal platformer game & level editor built using python and the [asciimatics](https://github.com/peterbrittain/asciimatics) library (mainly as a proof of concept).

## About

Originally built as a capstone project for a computer programming class, this project has turned into an exploration of the possibilities of terminal games, even in popular genres like platformers.

In the main game, the user controls an `o`, trying to make their way to a flag, avoiding spikes and traps along the way. For controls, see [Gameplay Controls](#gameplay).

The `Level Editor` includes 5 different tools (pen, dropper, spike, spawn position, and flag), 256 colours (found [here](https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg)) for both the foreground and the background, save slots, and more! For help with controls, see [Level Editor Controls](#level-editor).  
These levels are loadable straight from the editor to the main game, with zero hassle. Just navigate to the `main menu`, select `Play Custom Level`, and choose the correct slot.



Saw this cool video the other day which highlights other possibilities for this type of project: [
Minecraft, but it runs in the terminal](https://www.youtube.com/watch?v=6zfXM-6yPJQ)

## Example
Gameplay:

[Watch gameplay]("media/gameplay.mp4")

Level Editor:

[Watch level editor]("media/level editor.mp4")

Loading Level:

[Watch custom level]("media/custom level.mp4")




## Necessary Libraries
- [asciimatics](https://github.com/peterbrittain/asciimatics)
- [pygame](https://github.com/pygame-community/pygame-ce)
- [pynput](https://github.com/moses-palmer/pynput)
- [webbrowser](https://github.com/python/cpython/blob/main/Lib/webbrowser.py)

## Controls

### Gameplay:
- Use **WASD** and **Space** to move
- Press **Q** or **ESC** to pause
- Use **Arrow Keys (↑/↓)** and **Enter** to navigate menus


### Level Editor
- Press **H** to see the help menu
- **Click** or **Drag** to draw
- Press **S** to save (save indicator appears at the bottom of the editor)
- Press **Enter** to change pen colour
- Press **B** to change background colour
- Press **Space** to shuffle through tools
- Use keys **1-5** to select specific tools
- Use **ESC** (or the key used to open the popup) to close menus

## Tool Types
| Tool | Description|
|------|------------|
|**Pen** | Draws blocks on the screen. Uses pen colour (`enter` to change). If colour is the same as the background, it will `erase` blocks.
|**Dropper** | Selects colour from anywhere on the screen.
|**Spike** | Draws spikes on the screen. Uses pen colour (`enter` to change).
|**Spawn position** | Changes the character's spawn position.
|**Flag** | Changes the flag's position.


## Ideas
- Enemies
- Add abilities
    - dash left or right
- Bounce pads
- Secrets / Easter Eggs
- Add multiple levels to the main game
- Add shadows??
- Add settings (to toggle music on/off, change controls)
- Add my own music?
- Add a better way to close the game than ctrl + c

## Notes
> [!WARNING]
> This project has not been tested on windows or linux devices!

- This project was created using the [asciimatics](https://github.com/peterbrittain/asciimatics) package, but might have been better suited for another package like [blessed](https://github.com/jquast/blessed).
    - As asciimatics is better for animations and other projects, blessed, which is lower-level with fewer built-in features, would likely have been better for this project
- Using the `ESC` key will often have a delayed response, as terminals wait briefly to check if it is part of an [escape sequence](https://en.wikipedia.org/wiki/Escape_sequence#:~:text=In%20computer%20science%2C%20an%20escape,(and%20possibly%20terminating)%20characters.).
- Chart of all valid terminal colours: [color chart](https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg)
- Level data in the JSON files could be optimized to reduce size and increase performance.
- Testing had not been done on Windows or Linux systems
- It is likely buggy, as I am the only one testing this
- There are many learning opportunities to make it better
    - Should have rewritten the `popup_creator.add_coloured_text` and `popup_creator.add_text` functions to be more similar in how they are called
    - Should have made the base `popup` class better to avoid repeated code
    - Could have cleaned up the main game and level editor files
- Adjusting screen size while playing / editing will reset everything!
