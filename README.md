# This project is deprecated in favor of [icon-font-to-png](https://github.com/Pythonity/icon-font-to-png)

This project is deprecated in favor of the new, refactored and more universal [icon-font-to-png](https://github.com/Pythonity/icon-font-to-png).
Please use it instead, as it fixes all issues this version has (icons being cut off, outdated font, etc.) and is being actively maintained. It also comes with a wrapper script for backwards-compatibility with this version.

---

Font Awesome to PNG
===================

This program allows you to extract the awesome
[Font Awesome] (http://fortawesome.github.com/Font-Awesome/) or any other iconfont icons as PNG images
of specified size.

### Setup

```bash
pip install image tinycss
```

### Usage

    font-awesome-to-png.py [-h] [--color COLOR] [--filename FILENAME]
                           [--font FONT] [--css CSS] [--list] [--size SIZE]
                           icon [icon ...]

    positional arguments:
      icon                 The name(s) of the icon(s) to export (or "ALL" for
                           all icons)

    optional arguments:
      --color COLOR        Color (HTML color code or name, default: black)
      --filename FILENAME  The name of the output file (it must end with
                           ".png"). If all files are exported, it is used as a
                           prefix.
      --font FONT          Font file to use (default: fontawesome-webfont.ttf)
      --css CSS            Path to the CSS file defining icon names (instead of
                           the predefined list)
      --list               List available icon names and exit
      --size SIZE          Icon size in pixels (default: 16)

    hidden optional arguments:
     --list-update         List available icon names and codes in format suitable
                           for updating the program source.

To use the program, you need the Font Awesome TTF file, which is available in
[Font Awesome Github repository] (https://github.com/FortAwesome/Font-Awesome).

The internal icon list is matched to Font Awesome 4.1.0.  To use a later/different
version, use font-awesome.css from the Font Awesome GitHub repository.

### Examples

Export the "play" and "stop" icons as 24x24 pixels images:

    font-awesome-to-png.py --size 24 play stop

Export the asterisk icon as 32x32 pixels image, in blue:

    font-awesome-to-png.py --size 32 --color blue asterisk

Export all icons as 16x16 pixels images:

    font-awesome-to-png.py ALL
