#!/usr/bin/env python

#
# font-awesome-to-png.py
#
# Exports Font Awesome icons as PNG images.
#
# Copyright (c) 2012-2013 Michal Wojciechowski (http://odyniec.net/)
#
# Font Awesome - http://fortawesome.github.com/Font-Awesome
#

import sys, argparse
from os import path, access, R_OK
import Image, ImageFont, ImageDraw

# Support Unicode literals with both Python 2 and 3
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

# Mapping of icon names to character codes
icons = {
    "glass": u("\uf000"),
    "music": u("\uf001"),
    "search": u("\uf002"),
    "envelope-alt": u("\uf003"),
    "heart": u("\uf004"),
    "star": u("\uf005"),
    "star-empty": u("\uf006"),
    "user": u("\uf007"),
    "film": u("\uf008"),
    "th-large": u("\uf009"),
    "th": u("\uf00a"),
    "th-list": u("\uf00b"),
    "ok": u("\uf00c"),
    "remove": u("\uf00d"),
    "zoom-in": u("\uf00e"),
    "zoom-out": u("\uf010"),
    "power-off": u("\uf011"),
    "off": u("\uf011"),
    "signal": u("\uf012"),
    "gear": u("\uf013"),
    "cog": u("\uf013"),
    "trash": u("\uf014"),
    "home": u("\uf015"),
    "file-alt": u("\uf016"),
    "time": u("\uf017"),
    "road": u("\uf018"),
    "download-alt": u("\uf019"),
    "download": u("\uf01a"),
    "upload": u("\uf01b"),
    "inbox": u("\uf01c"),
    "play-circle": u("\uf01d"),
    "rotate-right": u("\uf01e"),
    "repeat": u("\uf01e"),
    "refresh": u("\uf021"),
    "list-alt": u("\uf022"),
    "lock": u("\uf023"),
    "flag": u("\uf024"),
    "headphones": u("\uf025"),
    "volume-off": u("\uf026"),
    "volume-down": u("\uf027"),
    "volume-up": u("\uf028"),
    "qrcode": u("\uf029"),
    "barcode": u("\uf02a"),
    "tag": u("\uf02b"),
    "tags": u("\uf02c"),
    "book": u("\uf02d"),
    "bookmark": u("\uf02e"),
    "print": u("\uf02f"),
    "camera": u("\uf030"),
    "font": u("\uf031"),
    "bold": u("\uf032"),
    "italic": u("\uf033"),
    "text-height": u("\uf034"),
    "text-width": u("\uf035"),
    "align-left": u("\uf036"),
    "align-center": u("\uf037"),
    "align-right": u("\uf038"),
    "align-justify": u("\uf039"),
    "list": u("\uf03a"),
    "indent-left": u("\uf03b"),
    "indent-right": u("\uf03c"),
    "facetime-video": u("\uf03d"),
    "picture": u("\uf03e"),
    "pencil": u("\uf040"),
    "map-marker": u("\uf041"),
    "adjust": u("\uf042"),
    "tint": u("\uf043"),
    "edit": u("\uf044"),
    "share": u("\uf045"),
    "check": u("\uf046"),
    "move": u("\uf047"),
    "step-backward": u("\uf048"),
    "fast-backward": u("\uf049"),
    "backward": u("\uf04a"),
    "play": u("\uf04b"),
    "pause": u("\uf04c"),
    "stop": u("\uf04d"),
    "forward": u("\uf04e"),
    "fast-forward": u("\uf050"),
    "step-forward": u("\uf051"),
    "eject": u("\uf052"),
    "chevron-left": u("\uf053"),
    "chevron-right": u("\uf054"),
    "plus-sign": u("\uf055"),
    "minus-sign": u("\uf056"),
    "remove-sign": u("\uf057"),
    "ok-sign": u("\uf058"),
    "question-sign": u("\uf059"),
    "info-sign": u("\uf05a"),
    "screenshot": u("\uf05b"),
    "remove-circle": u("\uf05c"),
    "ok-circle": u("\uf05d"),
    "ban-circle": u("\uf05e"),
    "arrow-left": u("\uf060"),
    "arrow-right": u("\uf061"),
    "arrow-up": u("\uf062"),
    "arrow-down": u("\uf063"),
    "mail-forward": u("\uf064"),
    "share-alt": u("\uf064"),
    "resize-full": u("\uf065"),
    "resize-small": u("\uf066"),
    "plus": u("\uf067"),
    "minus": u("\uf068"),
    "asterisk": u("\uf069"),
    "exclamation-sign": u("\uf06a"),
    "gift": u("\uf06b"),
    "leaf": u("\uf06c"),
    "fire": u("\uf06d"),
    "eye-open": u("\uf06e"),
    "eye-close": u("\uf070"),
    "warning-sign": u("\uf071"),
    "plane": u("\uf072"),
    "calendar": u("\uf073"),
    "random": u("\uf074"),
    "comment": u("\uf075"),
    "magnet": u("\uf076"),
    "chevron-up": u("\uf077"),
    "chevron-down": u("\uf078"),
    "retweet": u("\uf079"),
    "shopping-cart": u("\uf07a"),
    "folder-close": u("\uf07b"),
    "folder-open": u("\uf07c"),
    "resize-vertical": u("\uf07d"),
    "resize-horizontal": u("\uf07e"),
    "bar-chart": u("\uf080"),
    "twitter-sign": u("\uf081"),
    "facebook-sign": u("\uf082"),
    "camera-retro": u("\uf083"),
    "key": u("\uf084"),
    "gears": u("\uf085"),
    "cogs": u("\uf085"),
    "comments": u("\uf086"),
    "thumbs-up-alt": u("\uf087"),
    "thumbs-down-alt": u("\uf088"),
    "star-half": u("\uf089"),
    "heart-empty": u("\uf08a"),
    "signout": u("\uf08b"),
    "linkedin-sign": u("\uf08c"),
    "pushpin": u("\uf08d"),
    "external-link": u("\uf08e"),
    "signin": u("\uf090"),
    "trophy": u("\uf091"),
    "github-sign": u("\uf092"),
    "upload-alt": u("\uf093"),
    "lemon": u("\uf094"),
    "phone": u("\uf095"),
    "unchecked": u("\uf096"),
    "check-empty": u("\uf096"),
    "bookmark-empty": u("\uf097"),
    "phone-sign": u("\uf098"),
    "twitter": u("\uf099"),
    "facebook": u("\uf09a"),
    "github": u("\uf09b"),
    "unlock": u("\uf09c"),
    "credit-card": u("\uf09d"),
    "rss": u("\uf09e"),
    "hdd": u("\uf0a0"),
    "bullhorn": u("\uf0a1"),
    "bell": u("\uf0a2"),
    "certificate": u("\uf0a3"),
    "hand-right": u("\uf0a4"),
    "hand-left": u("\uf0a5"),
    "hand-up": u("\uf0a6"),
    "hand-down": u("\uf0a7"),
    "circle-arrow-left": u("\uf0a8"),
    "circle-arrow-right": u("\uf0a9"),
    "circle-arrow-up": u("\uf0aa"),
    "circle-arrow-down": u("\uf0ab"),
    "globe": u("\uf0ac"),
    "wrench": u("\uf0ad"),
    "tasks": u("\uf0ae"),
    "filter": u("\uf0b0"),
    "briefcase": u("\uf0b1"),
    "fullscreen": u("\uf0b2"),
    "group": u("\uf0c0"),
    "link": u("\uf0c1"),
    "cloud": u("\uf0c2"),
    "beaker": u("\uf0c3"),
    "cut": u("\uf0c4"),
    "copy": u("\uf0c5"),
    "paperclip": u("\uf0c6"),
    "paper-clip": u("\uf0c6"),
    "save": u("\uf0c7"),
    "sign-blank": u("\uf0c8"),
    "reorder": u("\uf0c9"),
    "list-ul": u("\uf0ca"),
    "list-ol": u("\uf0cb"),
    "strikethrough": u("\uf0cc"),
    "underline": u("\uf0cd"),
    "table": u("\uf0ce"),
    "magic": u("\uf0d0"),
    "truck": u("\uf0d1"),
    "pinterest": u("\uf0d2"),
    "pinterest-sign": u("\uf0d3"),
    "google-plus-sign": u("\uf0d4"),
    "google-plus": u("\uf0d5"),
    "money": u("\uf0d6"),
    "caret-down": u("\uf0d7"),
    "caret-up": u("\uf0d8"),
    "caret-left": u("\uf0d9"),
    "caret-right": u("\uf0da"),
    "columns": u("\uf0db"),
    "sort": u("\uf0dc"),
    "sort-down": u("\uf0dd"),
    "sort-up": u("\uf0de"),
    "envelope": u("\uf0e0"),
    "linkedin": u("\uf0e1"),
    "rotate-left": u("\uf0e2"),
    "undo": u("\uf0e2"),
    "legal": u("\uf0e3"),
    "dashboard": u("\uf0e4"),
    "comment-alt": u("\uf0e5"),
    "comments-alt": u("\uf0e6"),
    "bolt": u("\uf0e7"),
    "sitemap": u("\uf0e8"),
    "umbrella": u("\uf0e9"),
    "paste": u("\uf0ea"),
    "lightbulb": u("\uf0eb"),
    "exchange": u("\uf0ec"),
    "cloud-download": u("\uf0ed"),
    "cloud-upload": u("\uf0ee"),
    "user-md": u("\uf0f0"),
    "stethoscope": u("\uf0f1"),
    "suitcase": u("\uf0f2"),
    "bell-alt": u("\uf0f3"),
    "coffee": u("\uf0f4"),
    "food": u("\uf0f5"),
    "file-text-alt": u("\uf0f6"),
    "building": u("\uf0f7"),
    "hospital": u("\uf0f8"),
    "ambulance": u("\uf0f9"),
    "medkit": u("\uf0fa"),
    "fighter-jet": u("\uf0fb"),
    "beer": u("\uf0fc"),
    "h-sign": u("\uf0fd"),
    "plus-sign-alt": u("\uf0fe"),
    "double-angle-left": u("\uf100"),
    "double-angle-right": u("\uf101"),
    "double-angle-up": u("\uf102"),
    "double-angle-down": u("\uf103"),
    "angle-left": u("\uf104"),
    "angle-right": u("\uf105"),
    "angle-up": u("\uf106"),
    "angle-down": u("\uf107"),
    "desktop": u("\uf108"),
    "laptop": u("\uf109"),
    "tablet": u("\uf10a"),
    "mobile-phone": u("\uf10b"),
    "circle-blank": u("\uf10c"),
    "quote-left": u("\uf10d"),
    "quote-right": u("\uf10e"),
    "spinner": u("\uf110"),
    "circle": u("\uf111"),
    "mail-reply": u("\uf112"),
    "reply": u("\uf112"),
    "github-alt": u("\uf113"),
    "folder-close-alt": u("\uf114"),
    "folder-open-alt": u("\uf115"),
    "expand-alt": u("\uf116"),
    "collapse-alt": u("\uf117"),
    "smile": u("\uf118"),
    "frown": u("\uf119"),
    "meh": u("\uf11a"),
    "gamepad": u("\uf11b"),
    "keyboard": u("\uf11c"),
    "flag-alt": u("\uf11d"),
    "flag-checkered": u("\uf11e"),
    "terminal": u("\uf120"),
    "code": u("\uf121"),
    "reply-all": u("\uf122"),
    "mail-reply-all": u("\uf122"),
    "star-half-full": u("\uf123"),
    "star-half-empty": u("\uf123"),
    "location-arrow": u("\uf124"),
    "crop": u("\uf125"),
    "code-fork": u("\uf126"),
    "unlink": u("\uf127"),
    "question": u("\uf128"),
    "info": u("\uf129"),
    "exclamation": u("\uf12a"),
    "superscript": u("\uf12b"),
    "subscript": u("\uf12c"),
    "eraser": u("\uf12d"),
    "puzzle-piece": u("\uf12e"),
    "microphone": u("\uf130"),
    "microphone-off": u("\uf131"),
    "shield": u("\uf132"),
    "calendar-empty": u("\uf133"),
    "fire-extinguisher": u("\uf134"),
    "rocket": u("\uf135"),
    "maxcdn": u("\uf136"),
    "chevron-sign-left": u("\uf137"),
    "chevron-sign-right": u("\uf138"),
    "chevron-sign-up": u("\uf139"),
    "chevron-sign-down": u("\uf13a"),
    "html5": u("\uf13b"),
    "css3": u("\uf13c"),
    "anchor": u("\uf13d"),
    "unlock-alt": u("\uf13e"),
    "bullseye": u("\uf140"),
    "ellipsis-horizontal": u("\uf141"),
    "ellipsis-vertical": u("\uf142"),
    "rss-sign": u("\uf143"),
    "play-sign": u("\uf144"),
    "ticket": u("\uf145"),
    "minus-sign-alt": u("\uf146"),
    "check-minus": u("\uf147"),
    "level-up": u("\uf148"),
    "level-down": u("\uf149"),
    "check-sign": u("\uf14a"),
    "edit-sign": u("\uf14b"),
    "external-link-sign": u("\uf14c"),
    "share-sign": u("\uf14d"),
    "compass": u("\uf14e"),
    "collapse": u("\uf150"),
    "collapse-top": u("\uf151"),
    "expand": u("\uf152"),
    "euro": u("\uf153"),
    "eur": u("\uf153"),
    "gbp": u("\uf154"),
    "dollar": u("\uf155"),
    "usd": u("\uf155"),
    "rupee": u("\uf156"),
    "inr": u("\uf156"),
    "yen": u("\uf157"),
    "jpy": u("\uf157"),
    "renminbi": u("\uf158"),
    "cny": u("\uf158"),
    "won": u("\uf159"),
    "krw": u("\uf159"),
    "bitcoin": u("\uf15a"),
    "btc": u("\uf15a"),
    "file": u("\uf15b"),
    "file-text": u("\uf15c"),
    "sort-by-alphabet": u("\uf15d"),
    "sort-by-alphabet-alt": u("\uf15e"),
    "sort-by-attributes": u("\uf160"),
    "sort-by-attributes-alt": u("\uf161"),
    "sort-by-order": u("\uf162"),
    "sort-by-order-alt": u("\uf163"),
    "thumbs-up": u("\uf164"),
    "thumbs-down": u("\uf165"),
    "youtube-sign": u("\uf166"),
    "youtube": u("\uf167"),
    "xing": u("\uf168"),
    "xing-sign": u("\uf169"),
    "youtube-play": u("\uf16a"),
    "dropbox": u("\uf16b"),
    "stackexchange": u("\uf16c"),
    "instagram": u("\uf16d"),
    "flickr": u("\uf16e"),
    "adn": u("\uf170"),
    "bitbucket": u("\uf171"),
    "bitbucket-sign": u("\uf172"),
    "tumblr": u("\uf173"),
    "tumblr-sign": u("\uf174"),
    "long-arrow-down": u("\uf175"),
    "long-arrow-up": u("\uf176"),
    "long-arrow-left": u("\uf177"),
    "long-arrow-right": u("\uf178"),
    "apple": u("\uf179"),
    "windows": u("\uf17a"),
    "android": u("\uf17b"),
    "linux": u("\uf17c"),
    "dribbble": u("\uf17d"),
    "skype": u("\uf17e"),
    "foursquare": u("\uf180"),
    "trello": u("\uf181"),
    "female": u("\uf182"),
    "male": u("\uf183"),
    "gittip": u("\uf184"),
    "sun": u("\uf185"),
    "moon": u("\uf186"),
    "archive": u("\uf187"),
    "bug": u("\uf188"),
    "vk": u("\uf189"),
    "weibo": u("\uf18a"),
    "renren": u("\uf18b")
}

class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for icon in sorted(icons.keys()):
            print(icon)
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

    if bbox:
        image = image.crop(bbox)

    borderw = int((size - (bbox[2] - bbox[0])) / 2)
    borderh = int((size - (bbox[3] - bbox[1])) / 2)

    # Create background image
    bg = Image.new("RGBA", (size, size), (0,0,0,0))

    bg.paste(image, (borderw,borderh))

    # Save file
    bg.save(filename)

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
parser.add_argument("--list", nargs=0, action=ListAction,
        help="List available icon names and exit")
parser.add_argument("--size", type=int, default=16,
        help="Icon size in pixels (default: 16)")

args = parser.parse_args()
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

