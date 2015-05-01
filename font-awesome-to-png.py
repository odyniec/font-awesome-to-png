#!/usr/bin/env python

#
# font-awesome-to-png.py
#
# Exports Font Awesome icons as PNG images.
#
# Copyright (c) 2012-2014 Michal Wojciechowski (http://odyniec.net/)
#
# Font Awesome - http://fortawesome.github.com/Font-Awesome
#

import sys, argparse, re
from os import path, access, R_OK
from PIL import Image, ImageFont, ImageDraw

# Mapping of icon names to character codes
from icons import icons

# Support Unicode literals with both Python 2 and 3
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]

    def uchr(x):
        return unichr(x)
else:
    def u(x):
        return x

    def uchr(x):
        return chr(x)

class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for icon in sorted(icons.keys()):
            print(icon)
        exit(0)


class ListUpdateAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print("icons = {")
        for icon in sorted(icons.keys()):
            print(u'    "%s": u("\\u%x"),' % (icon, ord(icons[icon])))
        print("}")
        exit(0)


def export_icon(icon, size, filename, font, color):
    image = Image.new("RGBA", (size, size), color=(0,0,0,0))

    draw = ImageDraw.Draw(image)

    # Initialize font
    font = ImageFont.truetype(font, size)

    # Determine the dimensions of the icon
    width,height = draw.textsize(icons[icon], font=font)

    draw.text(((size - width) / 2, (size - height) / 2), icons[icon],
            font=font, fill=color)

    # Get bounding box
    bbox = image.getbbox()

    # Create an alpha mask
    imagemask = Image.new("L", (size, size), 0)
    drawmask = ImageDraw.Draw(imagemask)

    # Draw the icon on the mask
    drawmask.text(((size - width) / 2, (size - height) / 2), icons[icon],
        font=font, fill=255)

    # Create a solid color image and apply the mask
    iconimage = Image.new("RGBA", (size,size), color)
    iconimage.putalpha(imagemask)

    if bbox:
        iconimage = iconimage.crop(bbox)

    borderw = int((size - (bbox[2] - bbox[0])) / 2)
    borderh = int((size - (bbox[3] - bbox[1])) / 2)

    # Create output image
    outimage = Image.new("RGBA", (size, size), (0,0,0,0))
    outimage.paste(iconimage, (borderw,borderh))

    # Save file
    outimage.save(filename)


class LoadCSSAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        global icons
        icons = LoadCSSAction._load_css(values, namespace.prefix)

    @staticmethod
    def _load_css(filename, prefix):
        import tinycss
        new_icons = {}
        parser = tinycss.make_parser("page3")

        try:
            stylesheet = parser.parse_stylesheet_file(filename)
        except IOError:
            print >> sys.stderr, ("Error: CSS file (%s) can't be opened"
                % (filename))
            exit(1)

        is_icon = re.compile(u("\." + prefix + "(.*):before,?"))
        for rule in stylesheet.rules:
            selector = rule.selector.as_css()
            for match in is_icon.finditer(selector):
                name = match.groups()[0]
                for declaration in rule.declarations:
                    if declaration.name == u"content":
                        val = declaration.value.as_css()
                        if val.startswith('"') and val.endswith('"'):
                            val = val[1:-1]
                        new_icons[name] = uchr(int(val[1:], 16))
        return new_icons


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="Exports Font Awesome icons as PNG images.")

    parser.add_argument("icon", type=str, nargs="+",
            help="The name(s) of the icon(s) to export (or \"ALL\" for all icons)")
    parser.add_argument("--color", type=str, default="black",
            help="Color (HTML color code or name, default: black)")
    parser.add_argument("--filename", type=str,
            help="The name of the output file (it must end with \".png\"). If " +
            "all files are exported, it is used as a prefix.")
    parser.add_argument("--font", type=str, default="fontawesome-webfont.ttf",
            help="Font file to use (default: fontawesome-webfont.ttf)")
    parser.add_argument("--prefix", type=str, default="fa-", help="CSS prefix")
    parser.add_argument("--css", type=str, default="", action=LoadCSSAction,
            help="Path to the CSS file defining icon names (instead of the " +
            "predefined list)")
    parser.add_argument("--list", nargs=0, action=ListAction,
            help="List available icon names and exit")
    parser.add_argument("--list-update", nargs=0, action=ListUpdateAction,
            help=argparse.SUPPRESS)
    parser.add_argument("--size", type=int, default=16,
            help="Icon size in pixels (default: 16)")

    args = parser.parse_args()
    prefix = args.prefix
    icon = args.icon
    size = args.size
    font = args.font
    color = args.color

    if args.font:
        if not path.isfile(args.font) or not access(args.font, R_OK):
            print >> sys.stderr, ("Error: Font file (%s) can't be opened"
                    % (args.font))
            exit(1)

    if args.icon == [ "ALL" ]:
        # Export all icons
        selected_icons = sorted(icons.keys())
    else:
        selected_icons = []

        # Icon name was given
        for icon in args.icon:
            # Strip the "icon-" prefix, if present
            if icon.startswith("icon-"):
                icon = icon[5:]

            if icon in icons:
                selected_icons.append(icon)
            else:
                print >> sys.stderr, "Error: Unknown icon name (%s)" % (icon)
                sys.exit(1)

    for icon in selected_icons:
        if len(selected_icons) > 1:
            # Exporting multiple icons -- treat the filename option as name prefix
            filename = (args.filename or "") + icon + ".png"
        else:
            # Exporting one icon
            if args.filename:
                filename = args.filename
            else:
                filename = icon + ".png"

        print("Exporting icon \"%s\" as %s (%ix%i pixels)" %
                (icon, filename, size, size))

        export_icon(icon, size, filename, font, color)
