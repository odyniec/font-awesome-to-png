#!/usr/bin/env python
# coding=utf-8
#
# font-awesome-to-png.py
#
# Exports Font Awesome icons as PNG images.
#


# Copyright (c) 2012-2013 Michal Wojciechowski (http://odyniec.net/)
#
# Font Awesome - http://fortawesome.github.com/Font-Awesome
#
import sys
import argparse
from os import path, \
    access, \
    R_OK
from PIL import Image, \
    ImageFont, \
    ImageDraw

# Support Unicode literals with both Python 2 and 3
if sys.version < '3':
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

# Mapping of icon names to character codes
icons = {   "fa-glass": u("\uf000"),
            "fa-music": u("\uf001"),
            "fa-search": u("\uf002"),
            "fa-envelope-o": u("\uf003"),
            "fa-heart": u("\uf004"),
            "fa-star": u("\uf005"),
            "fa-star-o": u("\uf006"),
            "fa-user": u("\uf007"),
            "fa-film": u("\uf008"),
            "fa-th-large": u("\uf009"),
            "fa-th": u("\uf00a"),
            "fa-th-list": u("\uf00b"),
            "fa-check": u("\uf00c"),
            "fa-times": u("\uf00d"),
            "fa-search-plus": u("\uf00e"),
            "fa-search-minus": u("\uf010"),
            "fa-power-off": u("\uf011"),
            "fa-signal": u("\uf012"),
            "fa-cog": u("\uf013"),
            "fa-trash-o": u("\uf014"),
            "fa-home": u("\uf015"),
            "fa-file-o": u("\uf016"),
            "fa-clock-o": u("\uf017"),
            "fa-road": u("\uf018"),
            "fa-download": u("\uf019"),
            "fa-arrow-circle-o-down": u("\uf01a"),
            "fa-arrow-circle-o-up": u("\uf01b"),
            "fa-inbox": u("\uf01c"),
            "fa-play-circle-o": u("\uf01d"),
            "fa-repeat": u("\uf01e"),
            "fa-refresh": u("\uf021"),
            "fa-list-alt": u("\uf022"),
            "fa-lock": u("\uf023"),
            "fa-flag": u("\uf024"),
            "fa-headphones": u("\uf025"),
            "fa-volume-off": u("\uf026"),
            "fa-volume-down": u("\uf027"),
            "fa-volume-up": u("\uf028"),
            "fa-qrcode": u("\uf029"),
            "fa-barcode": u("\uf02a"),
            "fa-tag": u("\uf02b"),
            "fa-tags": u("\uf02c"),
            "fa-book": u("\uf02d"),
            "fa-bookmark": u("\uf02e"),
            "fa-print": u("\uf02f"),
            "fa-camera": u("\uf030"),
            "fa-font": u("\uf031"),
            "fa-bold": u("\uf032"),
            "fa-italic": u("\uf033"),
            "fa-text-height": u("\uf034"),
            "fa-text-width": u("\uf035"),
            "fa-align-left": u("\uf036"),
            "fa-align-center": u("\uf037"),
            "fa-align-right": u("\uf038"),
            "fa-align-justify": u("\uf039"),
            "fa-list": u("\uf03a"),
            "fa-outdent": u("\uf03b"),
            "fa-indent": u("\uf03c"),
            "fa-video-camera": u("\uf03d"),
            "fa-picture-o": u("\uf03e"),
            "fa-pencil": u("\uf040"),
            "fa-map-marker": u("\uf041"),
            "fa-adjust": u("\uf042"),
            "fa-tint": u("\uf043"),
            "fa-pencil-square-o": u("\uf044"),
            "fa-share-square-o": u("\uf045"),
            "fa-check-square-o": u("\uf046"),
            "fa-arrows": u("\uf047"),
            "fa-step-backward": u("\uf048"),
            "fa-backward": u("\uf04a"),
            "fa-play": u("\uf04b"),
            "fa-pause": u("\uf04c"),
            "fa-stop": u("\uf04d"),
            "fa-forward": u("\uf04e"),
            "fa-step-forward": u("\uf051"),
            "fa-eject": u("\uf052"),
            "fa-chevron-left": u("\uf053"),
            "fa-chevron-right": u("\uf054"),
            "fa-plus-circle": u("\uf055"),
            "fa-minus-circle": u("\uf056"),
            "fa-times-circle": u("\uf057"),
            "fa-check-circle": u("\uf058"),
            "fa-question-circle": u("\uf059"),
            "fa-info-circle": u("\uf05a"),
            "fa-crosshairs": u("\uf05b"),
            "fa-times-circle-o": u("\uf05c"),
            "fa-check-circle-o": u("\uf05d"),
            "fa-ban": u("\uf05e"),
            "fa-arrow-left": u("\uf060"),
            "fa-arrow-right": u("\uf061"),
            "fa-arrow-up": u("\uf062"),
            "fa-arrow-down": u("\uf063"),
            "fa-share": u("\uf064"),
            "fa-expand": u("\uf065"),
            "fa-compress": u("\uf066"),
            "fa-plus": u("\uf067"),
            "fa-minus": u("\uf068"),
            "fa-asterisk": u("\uf069"),
            "fa-exclamation-circle": u("\uf06a"),
            "fa-gift": u("\uf06b"),
            "fa-leaf": u("\uf06c"),
            "fa-fire": u("\uf06d"),
            "fa-eye": u("\uf06e"),
            "fa-eye-slash": u("\uf070"),
            "fa-exclamation-triangle": u("\uf071"),
            "fa-plane": u("\uf072"),
            "fa-calendar": u("\uf073"),
            "fa-random": u("\uf074"),
            "fa-comment": u("\uf075"),
            "fa-magnet": u("\uf076"),
            "fa-chevron-up": u("\uf077"),
            "fa-chevron-down": u("\uf078"),
            "fa-retweet": u("\uf079"),
            "fa-shopping-cart": u("\uf07a"),
            "fa-folder": u("\uf07b"),
            "fa-folder-open": u("\uf07c"),
            "fa-arrows-v": u("\uf07d"),
            "fa-arrows-h": u("\uf07e"),
            "fa-bar-chart-o": u("\uf080"),
            "fa-twitter-square": u("\uf081"),
            "fa-camera-retro": u("\uf083"),
            "fa-key": u("\uf084"),
            "fa-cogs": u("\uf085"),
            "fa-comments": u("\uf086"),
            "fa-thumbs-o-up": u("\uf087"),
            "fa-thumbs-o-down": u("\uf088"),
            "fa-star-half": u("\uf089"),
            "fa-heart-o": u("\uf08a"),
            "fa-sign-out": u("\uf08b"),
            "fa-linkedin-square": u("\uf08c"),
            "fa-thumb-tack": u("\uf08d"),
            "fa-external-link": u("\uf08e"),
            "fa-sign-in": u("\uf090"),
            "fa-trophy": u("\uf091"),
            "fa-github-square": u("\uf092"),
            "fa-upload": u("\uf093"),
            "fa-lemon-o": u("\uf094"),
            "fa-phone": u("\uf095"),
            "fa-square-o": u("\uf096"),
            "fa-bookmark-o": u("\uf097"),
            "fa-phone-square": u("\uf098"),
            "fa-twitter": u("\uf099"),
            "fa-github": u("\uf09b"),
            "fa-unlock": u("\uf09c"),
            "fa-credit-card": u("\uf09d"),
            "fa-rss": u("\uf09e"),
            "fa-hdd-o": u("\uf0a0"),
            "fa-bullhorn": u("\uf0a1"),
            "fa-bell": u("\uf0f3"),
            "fa-certificate": u("\uf0a3"),
            "fa-hand-o-right": u("\uf0a4"),
            "fa-hand-o-left": u("\uf0a5"),
            "fa-hand-o-up": u("\uf0a6"),
            "fa-hand-o-down": u("\uf0a7"),
            "fa-arrow-circle-left": u("\uf0a8"),
            "fa-arrow-circle-right": u("\uf0a9"),
            "fa-arrow-circle-up": u("\uf0aa"),
            "fa-arrow-circle-down": u("\uf0ab"),
            "fa-globe": u("\uf0ac"),
            "fa-wrench": u("\uf0ad"),
            "fa-tasks": u("\uf0ae"),
            "fa-filter": u("\uf0b0"),
            "fa-briefcase": u("\uf0b1"),
            "fa-arrows-alt": u("\uf0b2"),
            "fa-users": u("\uf0c0"),
            "fa-link": u("\uf0c1"),
            "fa-cloud": u("\uf0c2"),
            "fa-flask": u("\uf0c3"),
            "fa-scissors": u("\uf0c4"),
            "fa-files-o": u("\uf0c5"),
            "fa-paperclip": u("\uf0c6"),
            "fa-floppy-o": u("\uf0c7"),
            "fa-square": u("\uf0c8"),
            "fa-bars": u("\uf0c9"),
            "fa-list-ul": u("\uf0ca"),
            "fa-list-ol": u("\uf0cb"),
            "fa-strikethrough": u("\uf0cc"),
            "fa-underline": u("\uf0cd"),
            "fa-table": u("\uf0ce"),
            "fa-magic": u("\uf0d0"),
            "fa-truck": u("\uf0d1"),
            "fa-pinterest": u("\uf0d2"),
            "fa-pinterest-square": u("\uf0d3"),
            "fa-google-plus-square": u("\uf0d4"),
            "fa-google-plus": u("\uf0d5"),
            "fa-money": u("\uf0d6"),
            "fa-caret-down": u("\uf0d7"),
            "fa-caret-up": u("\uf0d8"),
            "fa-caret-left": u("\uf0d9"),
            "fa-caret-right": u("\uf0da"),
            "fa-columns": u("\uf0db"),
            "fa-sort": u("\uf0dc"),
            "fa-sort-asc": u("\uf0dd"),
            "fa-sort-desc": u("\uf0de"),
            "fa-envelope": u("\uf0e0"),
            "fa-linkedin": u("\uf0e1"),
            "fa-undo": u("\uf0e2"),
            "fa-gavel": u("\uf0e3"),
            "fa-tachometer": u("\uf0e4"),
            "fa-comment-o": u("\uf0e5"),
            "fa-comments-o": u("\uf0e6"),
            "fa-bolt": u("\uf0e7"),
            "fa-sitemap": u("\uf0e8"),
            "fa-umbrella": u("\uf0e9"),
            "fa-clipboard": u("\uf0ea"),
            "fa-lightbulb-o": u("\uf0eb"),
            "fa-exchange": u("\uf0ec"),
            "fa-cloud-download": u("\uf0ed"),
            "fa-cloud-upload": u("\uf0ee"),
            "fa-user-md": u("\uf0f0"),
            "fa-stethoscope": u("\uf0f1"),
            "fa-suitcase": u("\uf0f2"),
            "fa-bell-o": u("\uf0a2"),
            "fa-coffee": u("\uf0f4"),
            "fa-cutlery": u("\uf0f5"),
            "fa-file-text-o": u("\uf0f6"),
            "fa-building-o": u("\uf0f7"),
            "fa-hospital-o": u("\uf0f8"),
            "fa-ambulance": u("\uf0f9"),
            "fa-fighter-jet": u("\uf0fb"),
            "fa-beer": u("\uf0fc"),
            "fa-h-square": u("\uf0fd"),
            "fa-plus-square": u("\uf0fe"),
            "fa-angle-double-left": u("\uf100"),
            "fa-angle-double-right": u("\uf101"),
            "fa-angle-double-up": u("\uf102"),
            "fa-angle-double-down": u("\uf103"),
            "fa-angle-left": u("\uf104"),
            "fa-angle-right": u("\uf105"),
            "fa-angle-up": u("\uf106"),
            "fa-angle-down": u("\uf107"),
            "fa-desktop": u("\uf108"),
            "fa-laptop": u("\uf109"),
            "fa-tablet": u("\uf10a"),
            "fa-mobile": u("\uf10b"),
            "fa-circle-o": u("\uf10c"),
            "fa-quote-left": u("\uf10d"),
            "fa-quote-right": u("\uf10e"),
            "fa-spinner": u("\uf110"),
            "fa-circle": u("\uf111"),
            "fa-reply": u("\uf112"),
            "fa-github-alt": u("\uf113"),
            "fa-folder-o": u("\uf114"),
            "fa-folder-open-o": u("\uf115"),
            "fa-smile-o": u("\uf118"),
            "fa-frown-o": u("\uf119"),
            "fa-meh-o": u("\uf11a"),
            "fa-gamepad": u("\uf11b"),
            "fa-keyboard-o": u("\uf11c"),
            "fa-flag-o": u("\uf11d"),
            "fa-flag-checkered": u("\uf11e"),
            "fa-terminal": u("\uf120"),
            "fa-code": u("\uf121"),
            "fa-reply-all": u("\uf122"),
            "fa-mail-reply-all": u("\uf122"),
            "fa-star-half-o": u("\uf123"),
            "fa-location-arrow": u("\uf124"),
            "fa-crop": u("\uf125"),
            "fa-code-fork": u("\uf126"),
            "fa-chain-broken": u("\uf127"),
            "fa-question": u("\uf128"),
            "fa-info": u("\uf129"),
            "fa-exclamation": u("\uf12a"),
            "fa-superscript": u("\uf12b"),
            "fa-subscript": u("\uf12c"),
            "fa-eraser": u("\uf12d"),
            "fa-puzzle-piece": u("\uf12e"),
            "fa-microphone": u("\uf130"),
            "fa-microphone-slash": u("\uf131"),
            "fa-shield": u("\uf132"),
            "fa-calendar-o": u("\uf133"),
            "fa-fire-extinguisher": u("\uf134"),
            "fa-rocket": u("\uf135"),
            "fa-maxcdn": u("\uf136"),
            "fa-chevron-circle-left": u("\uf137"),
            "fa-chevron-circle-right": u("\uf138"),
            "fa-chevron-circle-up": u("\uf139"),
            "fa-chevron-circle-down": u("\uf13a"),
            "fa-html5": u("\uf13b"),
            "fa-css3": u("\uf13c"),
            "fa-anchor": u("\uf13d"),
            "fa-unlock-alt": u("\uf13e"),
            "fa-bullseye": u("\uf140"),
            "fa-ellipsis-h": u("\uf141"),
            "fa-ellipsis-v": u("\uf142"),
            "fa-rss-square": u("\uf143"),
            "fa-play-circle": u("\uf144"),
            "fa-ticket": u("\uf145"),
            "fa-minus-square": u("\uf146"),
            "fa-minus-square-o": u("\uf147"),
            "fa-level-up": u("\uf148"),
            "fa-level-down": u("\uf149"),
            "fa-check-square": u("\uf14a"),
            "fa-pencil-square": u("\uf14b"),
            "fa-external-link-square": u("\uf14c"),
            "fa-share-square": u("\uf14d"),
            "fa-compass": u("\uf14e"),
            "fa-caret-square-o-down": u("\uf150"),
            "fa-caret-square-o-up": u("\uf151"),
            "fa-caret-square-o-right": u("\uf152"),
            "fa-eur": u("\uf153"),
            "fa-gbp": u("\uf154"),
            "fa-usd": u("\uf155"),
            "fa-inr": u("\uf156"),
            "fa-jpy": u("\uf157"),
            "fa-rub": u("\uf158"),
            "fa-krw": u("\uf159"),
            "fa-btc": u("\uf15a"),
            "fa-file": u("\uf15b"),
            "fa-file-text": u("\uf15c"),
            "fa-sort-alpha-asc": u("\uf15d"),
            "fa-sort-alpha-desc": u("\uf15e"),
            "fa-sort-amount-asc": u("\uf160"),
            "fa-sort-amount-desc": u("\uf161"),
            "fa-sort-numeric-asc": u("\uf162"),
            "fa-sort-numeric-desc": u("\uf163"),
            "fa-thumbs-up": u("\uf164"),
            "fa-thumbs-down": u("\uf165"),
            "fa-youtube-square": u("\uf166"),
            "fa-youtube": u("\uf167"),
            "fa-xing": u("\uf168"),
            "fa-xing-square": u("\uf169"),
            "fa-youtube-play": u("\uf16a"),
            "fa-dropbox": u("\uf16b"),
            "fa-stack-overflow": u("\uf16c"),
            "fa-instagram": u("\uf16d"),
            "fa-flickr": u("\uf16e"),
            "fa-adn": u("\uf170"),
            "fa-bitbucket": u("\uf171"),
            "fa-bitbucket-square": u("\uf172"),
            "fa-tumblr": u("\uf173"),
            "fa-tumblr-square": u("\uf174"),
            "fa-long-arrow-down": u("\uf175"),
            "fa-long-arrow-up": u("\uf176"),
            "fa-long-arrow-left": u("\uf177"),
            "fa-long-arrow-right": u("\uf178"),
            "fa-apple": u("\uf179"),
            "fa-windows": u("\uf17a"),
            "fa-android": u("\uf17b"),
            "fa-linux": u("\uf17c"),
            "fa-dribbble": u("\uf17d"),
            "fa-skype": u("\uf17e"),
            "fa-foursquare": u("\uf180"),
            "fa-trello": u("\uf181"),
            "fa-female": u("\uf182"),
            "fa-male": u("\uf183"),
            "fa-gittip": u("\uf184"),
            "fa-sun-o": u("\uf185"),
            "fa-moon-o": u("\uf186"),
            "fa-archive": u("\uf187"),
            "fa-bug": u("\uf188"),
            "fa-vk": u("\uf189"),
            "fa-weibo": u("\uf18a"),
            "fa-renren": u("\uf18b"),
            "fa-pagelines": u("\uf18c"),
            "fa-stack-exchange": u("\uf18d"),
            "fa-arrow-circle-o-right": u("\uf18e"),
            "fa-arrow-circle-o-left": u("\uf190"),
            "fa-caret-square-o-left": u("\uf191"),
            "fa-dot-circle-o": u("\uf192"),
            "fa-wheelchair": u("\uf193"),
            "fa-vimeo-square": u("\uf194"),
            "fa-try": u("\uf195")}


class ListAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        for icon in sorted(icons.keys()):
            print "font-awesome-to-png.py:403", icon
        exit(0)


def export_icon(icon, size, filename, font, color):
    image = Image.new("RGBA", (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Initialize font
    font = ImageFont.truetype(font, size)

    # Determine the dimensions of the icon
    width, height = draw.textsize(icons[icon], font=font)
    draw.text(((size - width) / 2, (size - height) / 2), icons[icon], font=font, fill=color)

    # Get bounding box
    bbox = image.getbbox()

    if bbox:
        image = image.crop(bbox)

    borderw = int((size - (bbox[2] - bbox[0])) / 2)
    borderh = int((size - (bbox[3] - bbox[1])) / 2)

    # Create background image
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg.paste(image, (borderw, borderh))

    # Save file
    bg.save(filename)


parser = argparse.ArgumentParser(description="Exports Font Awesome icons as PNG images.")
parser = argparse.ArgumentParser(description="Exports Font Awesome icons as PNG images.")


parser.add_argument("icon", type=str, nargs="+", help="The name(s) of the icon(s) to export (or \"ALL\" for all icons)")


parser.add_argument("--color", type=str, default="black", help="Color (HTML color code or name, default: black)")


parser.add_argument("--filename", type=str, help="The name of the output file (it must end with \".png\"). If " + "all files are exported, it is used as a prefix.")


parser.add_argument("--font", type=str, default="fontawesome-webfont.ttf", help="Font file to use (default: fontawesome-webfont.ttf)")


parser.add_argument("--list", nargs=0, action=ListAction, help="List available icon names and exit")


parser.add_argument("--size", type=int, default=16, help="Icon size in pixels (default: 16)")
args = parser.parse_args()
icon = args.icon
size = args.size
font = args.font
color = args.color

if args.font:
    if not path.isfile(args.font) or not access(args.font, R_OK):
        print >> sys.stderr
        exit(1)

if args.icon == ["ALL"]:

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
            print >> sys.stderr
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

    try:
        print "Exporting icon \"%s\" as %s (%ix%i pixels)" % (icon, filename, size, size)
        export_icon(icon, size, filename, font, color)
    except:
        print
        print "Error, exporting icon \"%s\" as %s (%ix%i pixels)" % (icon, filename, size, size)
        print
        raise
