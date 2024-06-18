# 🗒️ MEDITOR

## 🤖 Abstract

Fun project to mess with `pytest`. Basically I'm trying to reproduce vim functionality in pygame window.
I am big fan of vim and neovim. Especially Vim motions are best possible way to navigate through your projects (in my opinion).
I don't know how far I would improve that project. It is only for-fun side quest for me, which I'll be working on
during my spare time (which I don't have much 🥲)

## Description

For now program has 2 modes:
    - NORMAL MODE
    - INSERT MODE
Those are the same as for VIM, so I won't be explaining those.

## Known bugs

- (FIXED) When cursor is on long line, and for example going line down, the X position of the cursor is still the same as before. It should changes.
- (FIXED) When going from longer line to shorter, B (vim motion) doesn't work properly.

## TODO

- VISUAL MODE
- Deleting lines, words, characters and so on. Basically just `d` vim keybind. For now there is only Backspace and Delete keys.
- Splitting vertically and horizontally + moving between panes (<C-w>l / <C-w>h and so on)
- VISUAL LINE MODE
- VERTICAL VISUAL MODE (BLOCK VISUAL MODE)
- Program should work on existing buffer (file).
    - Opening file
    - Saving file
- Maybe some kind of file explorer?
- Highlighting (python first)
- Encapsulation
- Add option to insert commands (command mode)
- Cursor rectangle is shaped to match letter width and height. I though it would be great idea but
it definitelly looks weird. Moreover, I still don't know how to implement fixed size of rectangle, when letters has
different width. I have to research about rendering fonts I think.