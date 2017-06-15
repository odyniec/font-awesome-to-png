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

# Mapping of icon names to character codes
icons = {
    "adjust": u("\uf042"),
    "adn": u("\uf170"),
    "align-center": u("\uf037"),
    "align-justify": u("\uf039"),
    "align-left": u("\uf036"),
    "align-right": u("\uf038"),
    "ambulance": u("\uf0f9"),
    "anchor": u("\uf13d"),
    "android": u("\uf17b"),
    "angellist": u("\uf209"),
    "angle-double-down": u("\uf103"),
    "angle-double-left": u("\uf100"),
    "angle-double-right": u("\uf101"),
    "angle-double-up": u("\uf102"),
    "angle-down": u("\uf107"),
    "angle-left": u("\uf104"),
    "angle-right": u("\uf105"),
    "angle-up": u("\uf106"),
    "apple": u("\uf179"),
    "archive": u("\uf187"),
    "area-chart": u("\uf1fe"),
    "arrow-circle-down": u("\uf0ab"),
    "arrow-circle-left": u("\uf0a8"),
    "arrow-circle-o-down": u("\uf01a"),
    "arrow-circle-o-left": u("\uf190"),
    "arrow-circle-o-right": u("\uf18e"),
    "arrow-circle-o-up": u("\uf01b"),
    "arrow-circle-right": u("\uf0a9"),
    "arrow-circle-up": u("\uf0aa"),
    "arrow-down": u("\uf063"),
    "arrow-left": u("\uf060"),
    "arrow-right": u("\uf061"),
    "arrow-up": u("\uf062"),
    "arrows": u("\uf047"),
    "arrows-alt": u("\uf0b2"),
    "arrows-h": u("\uf07e"),
    "arrows-v": u("\uf07d"),
    "asterisk": u("\uf069"),
    "at": u("\uf1fa"),
    "automobile": u("\uf1b9"),
    "backward": u("\uf04a"),
    "ban": u("\uf05e"),
    "bank": u("\uf19c"),
    "bar-chart": u("\uf080"),
    "bar-chart-o": u("\uf080"),
    "barcode": u("\uf02a"),
    "bars": u("\uf0c9"),
    "beer": u("\uf0fc"),
    "behance": u("\uf1b4"),
    "behance-square": u("\uf1b5"),
    "bell": u("\uf0f3"),
    "bell-o": u("\uf0a2"),
    "bell-slash": u("\uf1f6"),
    "bell-slash-o": u("\uf1f7"),
    "bicycle": u("\uf206"),
    "binoculars": u("\uf1e5"),
    "birthday-cake": u("\uf1fd"),
    "bitbucket": u("\uf171"),
    "bitbucket-square": u("\uf172"),
    "bitcoin": u("\uf15a"),
    "bold": u("\uf032"),
    "bolt": u("\uf0e7"),
    "bomb": u("\uf1e2"),
    "book": u("\uf02d"),
    "bookmark": u("\uf02e"),
    "bookmark-o": u("\uf097"),
    "briefcase": u("\uf0b1"),
    "btc": u("\uf15a"),
    "bug": u("\uf188"),
    "building": u("\uf1ad"),
    "building-o": u("\uf0f7"),
    "bullhorn": u("\uf0a1"),
    "bullseye": u("\uf140"),
    "bus": u("\uf207"),
    "cab": u("\uf1ba"),
    "calculator": u("\uf1ec"),
    "calendar": u("\uf073"),
    "calendar-o": u("\uf133"),
    "camera": u("\uf030"),
    "camera-retro": u("\uf083"),
    "car": u("\uf1b9"),
    "caret-down": u("\uf0d7"),
    "caret-left": u("\uf0d9"),
    "caret-right": u("\uf0da"),
    "caret-square-o-down": u("\uf150"),
    "caret-square-o-left": u("\uf191"),
    "caret-square-o-right": u("\uf152"),
    "caret-square-o-up": u("\uf151"),
    "caret-up": u("\uf0d8"),
    "cc": u("\uf20a"),
    "cc-amex": u("\uf1f3"),
    "cc-discover": u("\uf1f2"),
    "cc-mastercard": u("\uf1f1"),
    "cc-paypal": u("\uf1f4"),
    "cc-stripe": u("\uf1f5"),
    "cc-visa": u("\uf1f0"),
    "certificate": u("\uf0a3"),
    "chain": u("\uf0c1"),
    "chain-broken": u("\uf127"),
    "check": u("\uf00c"),
    "check-circle": u("\uf058"),
    "check-circle-o": u("\uf05d"),
    "check-square": u("\uf14a"),
    "check-square-o": u("\uf046"),
    "chevron-circle-down": u("\uf13a"),
    "chevron-circle-left": u("\uf137"),
    "chevron-circle-right": u("\uf138"),
    "chevron-circle-up": u("\uf139"),
    "chevron-down": u("\uf078"),
    "chevron-left": u("\uf053"),
    "chevron-right": u("\uf054"),
    "chevron-up": u("\uf077"),
    "child": u("\uf1ae"),
    "circle": u("\uf111"),
    "circle-o": u("\uf10c"),
    "circle-o-notch": u("\uf1ce"),
    "circle-thin": u("\uf1db"),
    "clipboard": u("\uf0ea"),
    "clock-o": u("\uf017"),
    "close": u("\uf00d"),
    "cloud": u("\uf0c2"),
    "cloud-download": u("\uf0ed"),
    "cloud-upload": u("\uf0ee"),
    "cny": u("\uf157"),
    "code": u("\uf121"),
    "code-fork": u("\uf126"),
    "codepen": u("\uf1cb"),
    "coffee": u("\uf0f4"),
    "cog": u("\uf013"),
    "cogs": u("\uf085"),
    "columns": u("\uf0db"),
    "comment": u("\uf075"),
    "comment-o": u("\uf0e5"),
    "comments": u("\uf086"),
    "comments-o": u("\uf0e6"),
    "compass": u("\uf14e"),
    "compress": u("\uf066"),
    "copy": u("\uf0c5"),
    "copyright": u("\uf1f9"),
    "credit-card": u("\uf09d"),
    "crop": u("\uf125"),
    "crosshairs": u("\uf05b"),
    "css3": u("\uf13c"),
    "cube": u("\uf1b2"),
    "cubes": u("\uf1b3"),
    "cut": u("\uf0c4"),
    "cutlery": u("\uf0f5"),
    "dashboard": u("\uf0e4"),
    "database": u("\uf1c0"),
    "dedent": u("\uf03b"),
    "delicious": u("\uf1a5"),
    "desktop": u("\uf108"),
    "deviantart": u("\uf1bd"),
    "digg": u("\uf1a6"),
    "dollar": u("\uf155"),
    "dot-circle-o": u("\uf192"),
    "download": u("\uf019"),
    "dribbble": u("\uf17d"),
    "dropbox": u("\uf16b"),
    "drupal": u("\uf1a9"),
    "edit": u("\uf044"),
    "eject": u("\uf052"),
    "ellipsis-h": u("\uf141"),
    "ellipsis-v": u("\uf142"),
    "empire": u("\uf1d1"),
    "envelope": u("\uf0e0"),
    "envelope-o": u("\uf003"),
    "envelope-square": u("\uf199"),
    "eraser": u("\uf12d"),
    "eur": u("\uf153"),
    "euro": u("\uf153"),
    "exchange": u("\uf0ec"),
    "exclamation": u("\uf12a"),
    "exclamation-circle": u("\uf06a"),
    "exclamation-triangle": u("\uf071"),
    "expand": u("\uf065"),
    "external-link": u("\uf08e"),
    "external-link-square": u("\uf14c"),
    "eye": u("\uf06e"),
    "eye-slash": u("\uf070"),
    "eyedropper": u("\uf1fb"),
    "facebook": u("\uf09a"),
    "facebook-square": u("\uf082"),
    "fast-backward": u("\uf049"),
    "fast-forward": u("\uf050"),
    "fax": u("\uf1ac"),
    "female": u("\uf182"),
    "fighter-jet": u("\uf0fb"),
    "file": u("\uf15b"),
    "file-archive-o": u("\uf1c6"),
    "file-audio-o": u("\uf1c7"),
    "file-code-o": u("\uf1c9"),
    "file-excel-o": u("\uf1c3"),
    "file-image-o": u("\uf1c5"),
    "file-movie-o": u("\uf1c8"),
    "file-o": u("\uf016"),
    "file-pdf-o": u("\uf1c1"),
    "file-photo-o": u("\uf1c5"),
    "file-picture-o": u("\uf1c5"),
    "file-powerpoint-o": u("\uf1c4"),
    "file-sound-o": u("\uf1c7"),
    "file-text": u("\uf15c"),
    "file-text-o": u("\uf0f6"),
    "file-video-o": u("\uf1c8"),
    "file-word-o": u("\uf1c2"),
    "file-zip-o": u("\uf1c6"),
    "files-o": u("\uf0c5"),
    "film": u("\uf008"),
    "filter": u("\uf0b0"),
    "fire": u("\uf06d"),
    "fire-extinguisher": u("\uf134"),
    "flag": u("\uf024"),
    "flag-checkered": u("\uf11e"),
    "flag-o": u("\uf11d"),
    "flash": u("\uf0e7"),
    "flask": u("\uf0c3"),
    "flickr": u("\uf16e"),
    "floppy-o": u("\uf0c7"),
    "folder": u("\uf07b"),
    "folder-o": u("\uf114"),
    "folder-open": u("\uf07c"),
    "folder-open-o": u("\uf115"),
    "font": u("\uf031"),
    "forward": u("\uf04e"),
    "foursquare": u("\uf180"),
    "frown-o": u("\uf119"),
    "futbol-o": u("\uf1e3"),
    "gamepad": u("\uf11b"),
    "gavel": u("\uf0e3"),
    "gbp": u("\uf154"),
    "ge": u("\uf1d1"),
    "gear": u("\uf013"),
    "gears": u("\uf085"),
    "gift": u("\uf06b"),
    "git": u("\uf1d3"),
    "git-square": u("\uf1d2"),
    "github": u("\uf09b"),
    "github-alt": u("\uf113"),
    "github-square": u("\uf092"),
    "gittip": u("\uf184"),
    "glass": u("\uf000"),
    "globe": u("\uf0ac"),
    "google": u("\uf1a0"),
    "google-plus": u("\uf0d5"),
    "google-plus-square": u("\uf0d4"),
    "google-wallet": u("\uf1ee"),
    "graduation-cap": u("\uf19d"),
    "group": u("\uf0c0"),
    "h-square": u("\uf0fd"),
    "hacker-news": u("\uf1d4"),
    "hand-o-down": u("\uf0a7"),
    "hand-o-left": u("\uf0a5"),
    "hand-o-right": u("\uf0a4"),
    "hand-o-up": u("\uf0a6"),
    "hdd-o": u("\uf0a0"),
    "header": u("\uf1dc"),
    "headphones": u("\uf025"),
    "heart": u("\uf004"),
    "heart-o": u("\uf08a"),
    "history": u("\uf1da"),
    "home": u("\uf015"),
    "hospital-o": u("\uf0f8"),
    "html5": u("\uf13b"),
    "ils": u("\uf20b"),
    "image": u("\uf03e"),
    "inbox": u("\uf01c"),
    "indent": u("\uf03c"),
    "info": u("\uf129"),
    "info-circle": u("\uf05a"),
    "inr": u("\uf156"),
    "instagram": u("\uf16d"),
    "institution": u("\uf19c"),
    "ioxhost": u("\uf208"),
    "italic": u("\uf033"),
    "joomla": u("\uf1aa"),
    "jpy": u("\uf157"),
    "jsfiddle": u("\uf1cc"),
    "key": u("\uf084"),
    "keyboard-o": u("\uf11c"),
    "krw": u("\uf159"),
    "language": u("\uf1ab"),
    "laptop": u("\uf109"),
    "lastfm": u("\uf202"),
    "lastfm-square": u("\uf203"),
    "leaf": u("\uf06c"),
    "legal": u("\uf0e3"),
    "lemon-o": u("\uf094"),
    "level-down": u("\uf149"),
    "level-up": u("\uf148"),
    "life-bouy": u("\uf1cd"),
    "life-buoy": u("\uf1cd"),
    "life-ring": u("\uf1cd"),
    "life-saver": u("\uf1cd"),
    "lightbulb-o": u("\uf0eb"),
    "line-chart": u("\uf201"),
    "link": u("\uf0c1"),
    "linkedin": u("\uf0e1"),
    "linkedin-square": u("\uf08c"),
    "linux": u("\uf17c"),
    "list": u("\uf03a"),
    "list-alt": u("\uf022"),
    "list-ol": u("\uf0cb"),
    "list-ul": u("\uf0ca"),
    "location-arrow": u("\uf124"),
    "lock": u("\uf023"),
    "long-arrow-down": u("\uf175"),
    "long-arrow-left": u("\uf177"),
    "long-arrow-right": u("\uf178"),
    "long-arrow-up": u("\uf176"),
    "magic": u("\uf0d0"),
    "magnet": u("\uf076"),
    "mail-forward": u("\uf064"),
    "mail-reply": u("\uf112"),
    "mail-reply-all": u("\uf122"),
    "male": u("\uf183"),
    "map-marker": u("\uf041"),
    "maxcdn": u("\uf136"),
    "meanpath": u("\uf20c"),
    "medkit": u("\uf0fa"),
    "meh-o": u("\uf11a"),
    "microphone": u("\uf130"),
    "microphone-slash": u("\uf131"),
    "minus": u("\uf068"),
    "minus-circle": u("\uf056"),
    "minus-square": u("\uf146"),
    "minus-square-o": u("\uf147"),
    "mobile": u("\uf10b"),
    "mobile-phone": u("\uf10b"),
    "money": u("\uf0d6"),
    "moon-o": u("\uf186"),
    "mortar-board": u("\uf19d"),
    "music": u("\uf001"),
    "navicon": u("\uf0c9"),
    "newspaper-o": u("\uf1ea"),
    "openid": u("\uf19b"),
    "outdent": u("\uf03b"),
    "pagelines": u("\uf18c"),
    "paint-brush": u("\uf1fc"),
    "paper-plane": u("\uf1d8"),
    "paper-plane-o": u("\uf1d9"),
    "paperclip": u("\uf0c6"),
    "paragraph": u("\uf1dd"),
    "paste": u("\uf0ea"),
    "pause": u("\uf04c"),
    "paw": u("\uf1b0"),
    "paypal": u("\uf1ed"),
    "pencil": u("\uf040"),
    "pencil-square": u("\uf14b"),
    "pencil-square-o": u("\uf044"),
    "phone": u("\uf095"),
    "phone-square": u("\uf098"),
    "photo": u("\uf03e"),
    "picture-o": u("\uf03e"),
    "pie-chart": u("\uf200"),
    "pied-piper": u("\uf1a7"),
    "pied-piper-alt": u("\uf1a8"),
    "pied-piper-square": u("\uf1a7"),
    "pinterest": u("\uf0d2"),
    "pinterest-square": u("\uf0d3"),
    "plane": u("\uf072"),
    "play": u("\uf04b"),
    "play-circle": u("\uf144"),
    "play-circle-o": u("\uf01d"),
    "plug": u("\uf1e6"),
    "plus": u("\uf067"),
    "plus-circle": u("\uf055"),
    "plus-square": u("\uf0fe"),
    "plus-square-o": u("\uf196"),
    "power-off": u("\uf011"),
    "print": u("\uf02f"),
    "puzzle-piece": u("\uf12e"),
    "qq": u("\uf1d6"),
    "qrcode": u("\uf029"),
    "question": u("\uf128"),
    "question-circle": u("\uf059"),
    "quote-left": u("\uf10d"),
    "quote-right": u("\uf10e"),
    "ra": u("\uf1d0"),
    "random": u("\uf074"),
    "rebel": u("\uf1d0"),
    "recycle": u("\uf1b8"),
    "reddit": u("\uf1a1"),
    "reddit-square": u("\uf1a2"),
    "refresh": u("\uf021"),
    "remove": u("\uf00d"),
    "renren": u("\uf18b"),
    "reorder": u("\uf0c9"),
    "repeat": u("\uf01e"),
    "reply": u("\uf112"),
    "reply-all": u("\uf122"),
    "retweet": u("\uf079"),
    "rmb": u("\uf157"),
    "road": u("\uf018"),
    "rocket": u("\uf135"),
    "rotate-left": u("\uf0e2"),
    "rotate-right": u("\uf01e"),
    "rouble": u("\uf158"),
    "rss": u("\uf09e"),
    "rss-square": u("\uf143"),
    "rub": u("\uf158"),
    "ruble": u("\uf158"),
    "rupee": u("\uf156"),
    "save": u("\uf0c7"),
    "scissors": u("\uf0c4"),
    "search": u("\uf002"),
    "search-minus": u("\uf010"),
    "search-plus": u("\uf00e"),
    "send": u("\uf1d8"),
    "send-o": u("\uf1d9"),
    "share": u("\uf064"),
    "share-alt": u("\uf1e0"),
    "share-alt-square": u("\uf1e1"),
    "share-square": u("\uf14d"),
    "share-square-o": u("\uf045"),
    "shekel": u("\uf20b"),
    "sheqel": u("\uf20b"),
    "shield": u("\uf132"),
    "shopping-cart": u("\uf07a"),
    "sign-in": u("\uf090"),
    "sign-out": u("\uf08b"),
    "signal": u("\uf012"),
    "sitemap": u("\uf0e8"),
    "skype": u("\uf17e"),
    "slack": u("\uf198"),
    "sliders": u("\uf1de"),
    "slideshare": u("\uf1e7"),
    "smile-o": u("\uf118"),
    "soccer-ball-o": u("\uf1e3"),
    "sort": u("\uf0dc"),
    "sort-alpha-asc": u("\uf15d"),
    "sort-alpha-desc": u("\uf15e"),
    "sort-amount-asc": u("\uf160"),
    "sort-amount-desc": u("\uf161"),
    "sort-asc": u("\uf0de"),
    "sort-desc": u("\uf0dd"),
    "sort-down": u("\uf0dd"),
    "sort-numeric-asc": u("\uf162"),
    "sort-numeric-desc": u("\uf163"),
    "sort-up": u("\uf0de"),
    "soundcloud": u("\uf1be"),
    "space-shuttle": u("\uf197"),
    "spinner": u("\uf110"),
    "spoon": u("\uf1b1"),
    "spotify": u("\uf1bc"),
    "square": u("\uf0c8"),
    "square-o": u("\uf096"),
    "stack-exchange": u("\uf18d"),
    "stack-overflow": u("\uf16c"),
    "star": u("\uf005"),
    "star-half": u("\uf089"),
    "star-half-empty": u("\uf123"),
    "star-half-full": u("\uf123"),
    "star-half-o": u("\uf123"),
    "star-o": u("\uf006"),
    "steam": u("\uf1b6"),
    "steam-square": u("\uf1b7"),
    "step-backward": u("\uf048"),
    "step-forward": u("\uf051"),
    "stethoscope": u("\uf0f1"),
    "stop": u("\uf04d"),
    "strikethrough": u("\uf0cc"),
    "stumbleupon": u("\uf1a4"),
    "stumbleupon-circle": u("\uf1a3"),
    "subscript": u("\uf12c"),
    "suitcase": u("\uf0f2"),
    "sun-o": u("\uf185"),
    "superscript": u("\uf12b"),
    "support": u("\uf1cd"),
    "table": u("\uf0ce"),
    "tablet": u("\uf10a"),
    "tachometer": u("\uf0e4"),
    "tag": u("\uf02b"),
    "tags": u("\uf02c"),
    "tasks": u("\uf0ae"),
    "taxi": u("\uf1ba"),
    "tencent-weibo": u("\uf1d5"),
    "terminal": u("\uf120"),
    "text-height": u("\uf034"),
    "text-width": u("\uf035"),
    "th": u("\uf00a"),
    "th-large": u("\uf009"),
    "th-list": u("\uf00b"),
    "thumb-tack": u("\uf08d"),
    "thumbs-down": u("\uf165"),
    "thumbs-o-down": u("\uf088"),
    "thumbs-o-up": u("\uf087"),
    "thumbs-up": u("\uf164"),
    "ticket": u("\uf145"),
    "times": u("\uf00d"),
    "times-circle": u("\uf057"),
    "times-circle-o": u("\uf05c"),
    "tint": u("\uf043"),
    "toggle-down": u("\uf150"),
    "toggle-left": u("\uf191"),
    "toggle-off": u("\uf204"),
    "toggle-on": u("\uf205"),
    "toggle-right": u("\uf152"),
    "toggle-up": u("\uf151"),
    "trash": u("\uf1f8"),
    "trash-o": u("\uf014"),
    "tree": u("\uf1bb"),
    "trello": u("\uf181"),
    "trophy": u("\uf091"),
    "truck": u("\uf0d1"),
    "try": u("\uf195"),
    "tty": u("\uf1e4"),
    "tumblr": u("\uf173"),
    "tumblr-square": u("\uf174"),
    "turkish-lira": u("\uf195"),
    "twitch": u("\uf1e8"),
    "twitter": u("\uf099"),
    "twitter-square": u("\uf081"),
    "umbrella": u("\uf0e9"),
    "underline": u("\uf0cd"),
    "undo": u("\uf0e2"),
    "university": u("\uf19c"),
    "unlink": u("\uf127"),
    "unlock": u("\uf09c"),
    "unlock-alt": u("\uf13e"),
    "unsorted": u("\uf0dc"),
    "upload": u("\uf093"),
    "usd": u("\uf155"),
    "user": u("\uf007"),
    "user-md": u("\uf0f0"),
    "users": u("\uf0c0"),
    "video-camera": u("\uf03d"),
    "vimeo-square": u("\uf194"),
    "vine": u("\uf1ca"),
    "vk": u("\uf189"),
    "volume-down": u("\uf027"),
    "volume-off": u("\uf026"),
    "volume-up": u("\uf028"),
    "warning": u("\uf071"),
    "wechat": u("\uf1d7"),
    "weibo": u("\uf18a"),
    "weixin": u("\uf1d7"),
    "wheelchair": u("\uf193"),
    "wifi": u("\uf1eb"),
    "windows": u("\uf17a"),
    "won": u("\uf159"),
    "wordpress": u("\uf19a"),
    "wrench": u("\uf0ad"),
    "xing": u("\uf168"),
    "xing-square": u("\uf169"),
    "yahoo": u("\uf19e"),
    "yelp": u("\uf1e9"),
    "yen": u("\uf157"),
    "youtube": u("\uf167"),
    "youtube-play": u("\uf16a"),
    "youtube-square": u("\uf166"),
}


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
        icons = LoadCSSAction._load_css(values)

    @staticmethod
    def _load_css(filename):
        import tinycss
        new_icons = {}
        parser = tinycss.make_parser("page3")

        try:
            stylesheet = parser.parse_stylesheet_file(filename)
        except IOError:
            print >> sys.stderr, ("Error: CSS file (%s) can't be opened"
                % (filename))
            exit(1)

        is_icon = re.compile(u("\.fa-(.*):before,?"))
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
