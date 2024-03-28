# Power Off

A power off screen using rofi run prompt and python.

## Dependencies

- Rofi
- Python 3.11 or higher

## How I integrated it

I use hyprland as my wayland compositor, so I setup a keybinding to run the
script, it is executable. If you're planning to use it, you'll have to change
the shebang to a python binary that you own. It can be just the standard
`#!/usr/bin/python`, but I want to have more control over the version that I'm
using to have access to all the latest python features.

An alternative method is making a symlink to your `/usr/local/bin` folder. Then
you can use it like a command line tool. Assuming you're in the projec's
folder, you can do:

```bash
sudo ln -s $PWD/main.py /usr/local/bin/poweroff
```

I renamed it to poweroff so that you can just say `poweroff` at your terminal
and execute the program.
