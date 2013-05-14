Font Awesome to PNG
===================

This program allows you to extract the awesome
[Font Awesome] (http://fortawesome.github.com/Font-Awesome/) icons as PNG images
of specified size.

### Usage

    font-awesome-to-png.py [-h] [--color COLOR] [--filename FILENAME]
                           [--font FONT] [--list] [--size SIZE]
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
      --list               List available icon names and exit
      --size SIZE          Icon size in pixels (default: 16)

To use the program, you need the Font Awesome TTF file, which is available in
[Font Awesome Github repository] (https://github.com/FortAwesome/Font-Awesome).

### Examples

Export the "play" and "stop" icons as 24x24 pixels images:

    font-awesome-to-png.py --size 24 play stop

Export the asterisk icon as 32x32 pixels image, in blue:

    font-awesome-to-png.py --size 32 --color blue asterisk

Export all icons as 16x16 pixels images:

    font-awesome-to-png.py ALL
    
Export all icons as 24x24 pixels images, in gray (note HTML colors must be in quotes):

    font-awesome-to-png.py --size 24 --color "#666666" ALL

### System Requirements

* Python must be installed
* The Python PIL package is required and must be compiled with support for libfreetype
* The file font-awesome-webfont.ttf should exist in the same directory as font-awesome-to-png.py

### Troublshooting

The error "ImportError: No module named Image" indicates that PIL is not installed

	sudo pip install PIL

The error "ImportError: The _imagingft C module is not installed" indicates libfreetype is not installed or was not properly linked when PIL was installed

	sudo pip uninstall PIL
	ln -s /usr/X11/include/freetype2 /usr/local/include/
	ln -s /usr/X11/include/ft2build.h /usr/local/include/
	ln -s /usr/X11/lib/libfreetype.6.dylib /usr/local/lib/
	ln -s /usr/X11/lib/libfreetype.6.dylib /usr/local/lib/libfreetype.dylib
	sudo pip install PIL