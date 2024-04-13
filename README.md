# Power Menu

A power menu using rofi run prompt and python. Naturally, only runs on Linux.

## Dependencies

- Rofi
- Python 3.11 or higher

## Integration

I've just setup a keybinding to run the script using the full path for the
python executable and the full path for the main.py file.

An alternative method is making the file executable by adding a shebang at the
start of the file like `#!/usr/bin/python` and doing:

```bash
chmod +x main.py
```

Then, you can create a symlink to your `/usr/local/bin` folder so you can use
it like a command line tool. Assuming you're in the project's folder, you can
do:

```bash
sudo ln -s $PWD/main.py /usr/local/bin/powermenu
```

I renamed it to powermenu without extension so that you can just say
`powermenu` at your terminal and execute the program.
