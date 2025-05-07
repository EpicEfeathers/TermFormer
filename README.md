# TermFormer: A Terminal Platformer
[![wakatime](https://wakatime.com/badge/user/bf51f838-e5c2-44d9-90ed-ec0da6b90b26/project/9784436c-bbbd-4409-bc19-b488c8e32a30.svg)](https://wakatime.com/badge/user/bf51f838-e5c2-44d9-90ed-ec0da6b90b26/project/9784436c-bbbd-4409-bc19-b488c8e32a30)
[![language](https://img.shields.io/badge/Language-python-yellow)](https://www.python.org)
[![creator](https://img.shields.io/badge/Creator-EpicEfeathers-0051FF?logo=github)](https://github.com/EpicEfeathers)




A terminal platformer game & level editor built using python and the [asciimatics](https://github.com/peterbrittain/asciimatics) library (mainly as a proof of concept).

## About

Originally built as a capstone project for a computer programming class, this project has turned into an exploration of the possibilities of terminal games, even in popular genres like platformers.

In the main game, the user plays as an "o", trying to make their way to a flag, avoiding spikes and trap along the way. For controls, see [Gameplay Controls](#gameplay)

The `Level Editor` includes 5 different tools (pen, dropper, spike, spawn position, and flag), 256 colours (found [here](https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg)) for both the foreground and the background, save slots, and more!  
These levels are loadable straight from the editor to the main game, with zero hassle. Just navigate to the `main menu`, select `Play Custom Level`, and choose the correct slot.


Saw this cool video the other day which highlights other possibilities: [
Minecraft, but it runs in the terminal](https://www.youtube.com/watch?v=6zfXM-6yPJQ)


>ABOUT THE GAME AND LEVEL EDITOR (SUCH AS TOOL TYPES)
<a href="https://example.com" target="_blank">Click me</a>

## Example
Gameplay:
video

Level Editor:
video

## Necessary Libraries
- [asciimatics](https://github.com/peterbrittain/asciimatics)
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

## Ideas
- Enemies
- Abilities (dash?)
- Bounce pads

## Notes
- This project was created using the [asciimatics](https://github.com/peterbrittain/asciimatics) package, but might have been better suited for another package like [blessed](https://github.com/jquast/blessed).
    - As asciimatics is better for animations and other projects, blessed, which is lower-level with fewer built-in features, would likely have been better for this project
- Using the `ESC` key will often have a delayed response, as terminals wait briefly to check if it is part of an [escape sequence](https://en.wikipedia.org/wiki/Escape_sequence#:~:text=In%20computer%20science%2C%20an%20escape,(and%20possibly%20terminating)%20characters.).
- Chart of all valid terminal colours: [color chart](https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg)
- the JSON file could definitely be optimized
    - Could compress the file size
- Testing had not been done on Windows or Linux systems
- It is likely buggy, as I am the only one testing this
- There are many learning oppurtinities to make it better
    - Should have rewritten the `popup_creator.add_coloured_text` and `popup_creator.add_text` functions to be more similar in how they are called
    - Should have made the base `popup` class better to avoid repeated code
- If background is not erasing properly in the level editor, make sure to **DRAG** when using the same colour as the background.
- Adjusting screen size while playing / editing will reset everything!