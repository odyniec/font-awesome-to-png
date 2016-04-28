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
    "glass": u("\uf000"),
    "music": u("\uf001"),
    "search": u("\uf002"),
    "envelope-o": u("\uf003"),
    "heart": u("\uf004"),
    "star": u("\uf005"),
    "star-o": u("\uf006"),
    "user": u("\uf007"),
    "film": u("\uf008"),
    "th-large": u("\uf009"),
    "th": u("\uf00a"),
    "th-list": u("\uf00b"),
    "check": u("\uf00c"),
    "times": u("\uf00d"),
    "search-plus": u("\uf00e"),
    "search-minus": u("\uf010"),
    "power-off": u("\uf011"),
    "signal": u("\uf012"),
    "cog": u("\uf013"),
    "trash-o": u("\uf014"),
    "home": u("\uf015"),
    "file-o": u("\uf016"),
    "clock-o": u("\uf017"),
    "road": u("\uf018"),
    "download": u("\uf019"),
    "arrow-circle-o-down": u("\uf01a"),
    "arrow-circle-o-up": u("\uf01b"),
    "inbox": u("\uf01c"),
    "play-circle-o": u("\uf01d"),
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
    "outdent": u("\uf03b"),
    "indent": u("\uf03c"),
    "video-camera": u("\uf03d"),
    "picture-o": u("\uf03e"),
    "pencil": u("\uf040"),
    "map-marker": u("\uf041"),
    "adjust": u("\uf042"),
    "tint": u("\uf043"),
    "pencil-square-o": u("\uf044"),
    "share-square-o": u("\uf045"),
    "check-square-o": u("\uf046"),
    "arrows": u("\uf047"),
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
    "plus-circle": u("\uf055"),
    "minus-circle": u("\uf056"),
    "times-circle": u("\uf057"),
    "check-circle": u("\uf058"),
    "question-circle": u("\uf059"),
    "info-circle": u("\uf05a"),
    "crosshairs": u("\uf05b"),
    "times-circle-o": u("\uf05c"),
    "check-circle-o": u("\uf05d"),
    "ban": u("\uf05e"),
    "arrow-left": u("\uf060"),
    "arrow-right": u("\uf061"),
    "arrow-up": u("\uf062"),
    "arrow-down": u("\uf063"),
    "share": u("\uf064"),
    "expand": u("\uf065"),
    "compress": u("\uf066"),
    "plus": u("\uf067"),
    "minus": u("\uf068"),
    "asterisk": u("\uf069"),
    "exclamation-circle": u("\uf06a"),
    "gift": u("\uf06b"),
    "leaf": u("\uf06c"),
    "fire": u("\uf06d"),
    "eye": u("\uf06e"),
    "eye-slash": u("\uf070"),
    "exclamation-triangle": u("\uf071"),
    "plane": u("\uf072"),
    "calendar": u("\uf073"),
    "random": u("\uf074"),
    "comment": u("\uf075"),
    "magnet": u("\uf076"),
    "chevron-up": u("\uf077"),
    "chevron-down": u("\uf078"),
    "retweet": u("\uf079"),
    "shopping-cart": u("\uf07a"),
    "folder": u("\uf07b"),
    "folder-open": u("\uf07c"),
    "arrows-v": u("\uf07d"),
    "arrows-h": u("\uf07e"),
    "bar-chart": u("\uf080"),
    "twitter-square": u("\uf081"),
    "facebook-square": u("\uf082"),
    "camera-retro": u("\uf083"),
    "key": u("\uf084"),
    "cogs": u("\uf085"),
    "comments": u("\uf086"),
    "thumbs-o-up": u("\uf087"),
    "thumbs-o-down": u("\uf088"),
    "star-half": u("\uf089"),
    "heart-o": u("\uf08a"),
    "sign-out": u("\uf08b"),
    "linkedin-square": u("\uf08c"),
    "thumb-tack": u("\uf08d"),
    "external-link": u("\uf08e"),
    "sign-in": u("\uf090"),
    "trophy": u("\uf091"),
    "github-square": u("\uf092"),
    "upload": u("\uf093"),
    "lemon-o": u("\uf094"),
    "phone": u("\uf095"),
    "square-o": u("\uf096"),
    "bookmark-o": u("\uf097"),
    "phone-square": u("\uf098"),
    "twitter": u("\uf099"),
    "facebook": u("\uf09a"),
    "github": u("\uf09b"),
    "unlock": u("\uf09c"),
    "credit-card": u("\uf09d"),
    "rss": u("\uf09e"),
    "hdd-o": u("\uf0a0"),
    "bullhorn": u("\uf0a1"),
    "bell": u("\uf0f3"),
    "certificate": u("\uf0a3"),
    "hand-o-right": u("\uf0a4"),
    "hand-o-left": u("\uf0a5"),
    "hand-o-up": u("\uf0a6"),
    "hand-o-down": u("\uf0a7"),
    "arrow-circle-left": u("\uf0a8"),
    "arrow-circle-right": u("\uf0a9"),
    "arrow-circle-up": u("\uf0aa"),
    "arrow-circle-down": u("\uf0ab"),
    "globe": u("\uf0ac"),
    "wrench": u("\uf0ad"),
    "tasks": u("\uf0ae"),
    "filter": u("\uf0b0"),
    "briefcase": u("\uf0b1"),
    "arrows-alt": u("\uf0b2"),
    "users": u("\uf0c0"),
    "link": u("\uf0c1"),
    "cloud": u("\uf0c2"),
    "flask": u("\uf0c3"),
    "scissors": u("\uf0c4"),
    "files-o": u("\uf0c5"),
    "paperclip": u("\uf0c6"),
    "floppy-o": u("\uf0c7"),
    "square": u("\uf0c8"),
    "bars": u("\uf0c9"),
    "list-ul": u("\uf0ca"),
    "list-ol": u("\uf0cb"),
    "strikethrough": u("\uf0cc"),
    "underline": u("\uf0cd"),
    "table": u("\uf0ce"),
    "magic": u("\uf0d0"),
    "truck": u("\uf0d1"),
    "pinterest": u("\uf0d2"),
    "pinterest-square": u("\uf0d3"),
    "google-plus-square": u("\uf0d4"),
    "google-plus": u("\uf0d5"),
    "money": u("\uf0d6"),
    "caret-down": u("\uf0d7"),
    "caret-up": u("\uf0d8"),
    "caret-left": u("\uf0d9"),
    "caret-right": u("\uf0da"),
    "columns": u("\uf0db"),
    "sort": u("\uf0dc"),
    "sort-desc": u("\uf0dd"),
    "sort-asc": u("\uf0de"),
    "envelope": u("\uf0e0"),
    "linkedin": u("\uf0e1"),
    "undo": u("\uf0e2"),
    "gavel": u("\uf0e3"),
    "tachometer": u("\uf0e4"),
    "comment-o": u("\uf0e5"),
    "comments-o": u("\uf0e6"),
    "bolt": u("\uf0e7"),
    "sitemap": u("\uf0e8"),
    "umbrella": u("\uf0e9"),
    "clipboard": u("\uf0ea"),
    "lightbulb-o": u("\uf0eb"),
    "exchange": u("\uf0ec"),
    "cloud-download": u("\uf0ed"),
    "cloud-upload": u("\uf0ee"),
    "user-md": u("\uf0f0"),
    "stethoscope": u("\uf0f1"),
    "suitcase": u("\uf0f2"),
    "bell-o": u("\uf0a2"),
    "coffee": u("\uf0f4"),
    "cutlery": u("\uf0f5"),
    "file-text-o": u("\uf0f6"),
    "building-o": u("\uf0f7"),
    "hospital-o": u("\uf0f8"),
    "ambulance": u("\uf0f9"),
    "medkit": u("\uf0fa"),
    "fighter-jet": u("\uf0fb"),
    "beer": u("\uf0fc"),
    "h-square": u("\uf0fd"),
    "plus-square": u("\uf0fe"),
    "angle-double-left": u("\uf100"),
    "angle-double-right": u("\uf101"),
    "angle-double-up": u("\uf102"),
    "angle-double-down": u("\uf103"),
    "angle-left": u("\uf104"),
    "angle-right": u("\uf105"),
    "angle-up": u("\uf106"),
    "angle-down": u("\uf107"),
    "desktop": u("\uf108"),
    "laptop": u("\uf109"),
    "tablet": u("\uf10a"),
    "mobile": u("\uf10b"),
    "circle-o": u("\uf10c"),
    "quote-left": u("\uf10d"),
    "quote-right": u("\uf10e"),
    "spinner": u("\uf110"),
    "circle": u("\uf111"),
    "reply": u("\uf112"),
    "github-alt": u("\uf113"),
    "folder-o": u("\uf114"),
    "folder-open-o": u("\uf115"),
    "smile-o": u("\uf118"),
    "frown-o": u("\uf119"),
    "meh-o": u("\uf11a"),
    "gamepad": u("\uf11b"),
    "keyboard-o": u("\uf11c"),
    "flag-o": u("\uf11d"),
    "flag-checkered": u("\uf11e"),
    "terminal": u("\uf120"),
    "code": u("\uf121"),
    "reply-all": u("\uf122"),
    "star-half-o": u("\uf123"),
    "location-arrow": u("\uf124"),
    "crop": u("\uf125"),
    "code-fork": u("\uf126"),
    "chain-broken": u("\uf127"),
    "question": u("\uf128"),
    "info": u("\uf129"),
    "exclamation": u("\uf12a"),
    "superscript": u("\uf12b"),
    "subscript": u("\uf12c"),
    "eraser": u("\uf12d"),
    "puzzle-piece": u("\uf12e"),
    "microphone": u("\uf130"),
    "microphone-slash": u("\uf131"),
    "shield": u("\uf132"),
    "calendar-o": u("\uf133"),
    "fire-extinguisher": u("\uf134"),
    "rocket": u("\uf135"),
    "maxcdn": u("\uf136"),
    "chevron-circle-left": u("\uf137"),
    "chevron-circle-right": u("\uf138"),
    "chevron-circle-up": u("\uf139"),
    "chevron-circle-down": u("\uf13a"),
    "html5": u("\uf13b"),
    "css3": u("\uf13c"),
    "anchor": u("\uf13d"),
    "unlock-alt": u("\uf13e"),
    "bullseye": u("\uf140"),
    "ellipsis-h": u("\uf141"),
    "ellipsis-v": u("\uf142"),
    "rss-square": u("\uf143"),
    "play-circle": u("\uf144"),
    "ticket": u("\uf145"),
    "minus-square": u("\uf146"),
    "minus-square-o": u("\uf147"),
    "level-up": u("\uf148"),
    "level-down": u("\uf149"),
    "check-square": u("\uf14a"),
    "pencil-square": u("\uf14b"),
    "external-link-square": u("\uf14c"),
    "share-square": u("\uf14d"),
    "compass": u("\uf14e"),
    "caret-square-o-down": u("\uf150"),
    "caret-square-o-up": u("\uf151"),
    "caret-square-o-right": u("\uf152"),
    "eur": u("\uf153"),
    "gbp": u("\uf154"),
    "usd": u("\uf155"),
    "inr": u("\uf156"),
    "jpy": u("\uf157"),
    "rub": u("\uf158"),
    "krw": u("\uf159"),
    "btc": u("\uf15a"),
    "file": u("\uf15b"),
    "file-text": u("\uf15c"),
    "sort-alpha-asc": u("\uf15d"),
    "sort-alpha-desc": u("\uf15e"),
    "sort-amount-asc": u("\uf160"),
    "sort-amount-desc": u("\uf161"),
    "sort-numeric-asc": u("\uf162"),
    "sort-numeric-desc": u("\uf163"),
    "thumbs-up": u("\uf164"),
    "thumbs-down": u("\uf165"),
    "youtube-square": u("\uf166"),
    "youtube": u("\uf167"),
    "xing": u("\uf168"),
    "xing-square": u("\uf169"),
    "youtube-play": u("\uf16a"),
    "dropbox": u("\uf16b"),
    "stack-overflow": u("\uf16c"),
    "instagram": u("\uf16d"),
    "flickr": u("\uf16e"),
    "adn": u("\uf170"),
    "bitbucket": u("\uf171"),
    "bitbucket-square": u("\uf172"),
    "tumblr": u("\uf173"),
    "tumblr-square": u("\uf174"),
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
    "gratipay": u("\uf184"),
    "sun-o": u("\uf185"),
    "moon-o": u("\uf186"),
    "archive": u("\uf187"),
    "bug": u("\uf188"),
    "vk": u("\uf189"),
    "weibo": u("\uf18a"),
    "renren": u("\uf18b"),
    "pagelines": u("\uf18c"),
    "stack-exchange": u("\uf18d"),
    "arrow-circle-o-right": u("\uf18e"),
    "arrow-circle-o-left": u("\uf190"),
    "caret-square-o-left": u("\uf191"),
    "dot-circle-o": u("\uf192"),
    "wheelchair": u("\uf193"),
    "vimeo-square": u("\uf194"),
    "try": u("\uf195"),
    "plus-square-o": u("\uf196"),
    "space-shuttle": u("\uf197"),
    "slack": u("\uf198"),
    "envelope-square": u("\uf199"),
    "wordpress": u("\uf19a"),
    "openid": u("\uf19b"),
    "university": u("\uf19c"),
    "graduation-cap": u("\uf19d"),
    "yahoo": u("\uf19e"),
    "google": u("\uf1a0"),
    "reddit": u("\uf1a1"),
    "reddit-square": u("\uf1a2"),
    "stumbleupon-circle": u("\uf1a3"),
    "stumbleupon": u("\uf1a4"),
    "delicious": u("\uf1a5"),
    "digg": u("\uf1a6"),
    "pied-piper": u("\uf1a7"),
    "pied-piper-alt": u("\uf1a8"),
    "drupal": u("\uf1a9"),
    "joomla": u("\uf1aa"),
    "language": u("\uf1ab"),
    "fax": u("\uf1ac"),
    "building": u("\uf1ad"),
    "child": u("\uf1ae"),
    "paw": u("\uf1b0"),
    "spoon": u("\uf1b1"),
    "cube": u("\uf1b2"),
    "cubes": u("\uf1b3"),
    "behance": u("\uf1b4"),
    "behance-square": u("\uf1b5"),
    "steam": u("\uf1b6"),
    "steam-square": u("\uf1b7"),
    "recycle": u("\uf1b8"),
    "car": u("\uf1b9"),
    "taxi": u("\uf1ba"),
    "tree": u("\uf1bb"),
    "spotify": u("\uf1bc"),
    "deviantart": u("\uf1bd"),
    "soundcloud": u("\uf1be"),
    "database": u("\uf1c0"),
    "file-pdf-o": u("\uf1c1"),
    "file-word-o": u("\uf1c2"),
    "file-excel-o": u("\uf1c3"),
    "file-powerpoint-o": u("\uf1c4"),
    "file-image-o": u("\uf1c5"),
    "file-archive-o": u("\uf1c6"),
    "file-audio-o": u("\uf1c7"),
    "file-video-o": u("\uf1c8"),
    "file-code-o": u("\uf1c9"),
    "vine": u("\uf1ca"),
    "codepen": u("\uf1cb"),
    "jsfiddle": u("\uf1cc"),
    "life-ring": u("\uf1cd"),
    "circle-o-notch": u("\uf1ce"),
    "rebel": u("\uf1d0"),
    "empire": u("\uf1d1"),
    "git-square": u("\uf1d2"),
    "git": u("\uf1d3"),
    "hacker-news": u("\uf1d4"),
    "tencent-weibo": u("\uf1d5"),
    "qq": u("\uf1d6"),
    "weixin": u("\uf1d7"),
    "paper-plane": u("\uf1d8"),
    "paper-plane-o": u("\uf1d9"),
    "history": u("\uf1da"),
    "circle-thin": u("\uf1db"),
    "header": u("\uf1dc"),
    "paragraph": u("\uf1dd"),
    "sliders": u("\uf1de"),
    "share-alt": u("\uf1e0"),
    "share-alt-square": u("\uf1e1"),
    "bomb": u("\uf1e2"),
    "futbol-o": u("\uf1e3"),
    "tty": u("\uf1e4"),
    "binoculars": u("\uf1e5"),
    "plug": u("\uf1e6"),
    "slideshare": u("\uf1e7"),
    "twitch": u("\uf1e8"),
    "yelp": u("\uf1e9"),
    "newspaper-o": u("\uf1ea"),
    "wifi": u("\uf1eb"),
    "calculator": u("\uf1ec"),
    "paypal": u("\uf1ed"),
    "google-wallet": u("\uf1ee"),
    "cc-visa": u("\uf1f0"),
    "cc-mastercard": u("\uf1f1"),
    "cc-discover": u("\uf1f2"),
    "cc-amex": u("\uf1f3"),
    "cc-paypal": u("\uf1f4"),
    "cc-stripe": u("\uf1f5"),
    "bell-slash": u("\uf1f6"),
    "bell-slash-o": u("\uf1f7"),
    "trash": u("\uf1f8"),
    "copyright": u("\uf1f9"),
    "at": u("\uf1fa"),
    "eyedropper": u("\uf1fb"),
    "paint-brush": u("\uf1fc"),
    "birthday-cake": u("\uf1fd"),
    "area-chart": u("\uf1fe"),
    "pie-chart": u("\uf200"),
    "line-chart": u("\uf201"),
    "lastfm": u("\uf202"),
    "lastfm-square": u("\uf203"),
    "toggle-off": u("\uf204"),
    "toggle-on": u("\uf205"),
    "bicycle": u("\uf206"),
    "bus": u("\uf207"),
    "ioxhost": u("\uf208"),
    "angellist": u("\uf209"),
    "cc": u("\uf20a"),
    "ils": u("\uf20b"),
    "meanpath": u("\uf20c"),
    "buysellads": u("\uf20d"),
    "connectdevelop": u("\uf20e"),
    "dashcube": u("\uf210"),
    "forumbee": u("\uf211"),
    "leanpub": u("\uf212"),
    "sellsy": u("\uf213"),
    "shirtsinbulk": u("\uf214"),
    "simplybuilt": u("\uf215"),
    "skyatlas": u("\uf216"),
    "cart-plus": u("\uf217"),
    "cart-arrow-down": u("\uf218"),
    "diamond": u("\uf219"),
    "ship": u("\uf21a"),
    "user-secret": u("\uf21b"),
    "motorcycle": u("\uf21c"),
    "street-view": u("\uf21d"),
    "heartbeat": u("\uf21e"),
    "venus": u("\uf221"),
    "mars": u("\uf222"),
    "mercury": u("\uf223"),
    "transgender": u("\uf224"),
    "transgender-alt": u("\uf225"),
    "venus-double": u("\uf226"),
    "mars-double": u("\uf227"),
    "venus-mars": u("\uf228"),
    "mars-stroke": u("\uf229"),
    "mars-stroke-v": u("\uf22a"),
    "mars-stroke-h": u("\uf22b"),
    "neuter": u("\uf22c"),
    "genderless": u("\uf22d"),
    "facebook-official": u("\uf230"),
    "pinterest-p": u("\uf231"),
    "whatsapp": u("\uf232"),
    "server": u("\uf233"),
    "user-plus": u("\uf234"),
    "user-times": u("\uf235"),
    "bed": u("\uf236"),
    "viacoin": u("\uf237"),
    "train": u("\uf238"),
    "subway": u("\uf239"),
    "medium": u("\uf23a"),
    "y-combinator": u("\uf23b"),
    "optin-monster": u("\uf23c"),
    "opencart": u("\uf23d"),
    "expeditedssl": u("\uf23e"),
    "battery-full": u("\uf240"),
    "battery-three-quarters": u("\uf241"),
    "battery-half": u("\uf242"),
    "battery-quarter": u("\uf243"),
    "battery-empty": u("\uf244"),
    "mouse-pointer": u("\uf245"),
    "i-cursor": u("\uf246"),
    "object-group": u("\uf247"),
    "object-ungroup": u("\uf248"),
    "sticky-note": u("\uf249"),
    "sticky-note-o": u("\uf24a"),
    "cc-jcb": u("\uf24b"),
    "cc-diners-club": u("\uf24c"),
    "clone": u("\uf24d"),
    "balance-scale": u("\uf24e"),
    "hourglass-o": u("\uf250"),
    "hourglass-start": u("\uf251"),
    "hourglass-half": u("\uf252"),
    "hourglass-end": u("\uf253"),
    "hourglass": u("\uf254"),
    "hand-rock-o": u("\uf255"),
    "hand-paper-o": u("\uf256"),
    "hand-scissors-o": u("\uf257"),
    "hand-lizard-o": u("\uf258"),
    "hand-spock-o": u("\uf259"),
    "hand-pointer-o": u("\uf25a"),
    "hand-peace-o": u("\uf25b"),
    "trademark": u("\uf25c"),
    "registered": u("\uf25d"),
    "creative-commons": u("\uf25e"),
    "gg": u("\uf260"),
    "gg-circle": u("\uf261"),
    "tripadvisor": u("\uf262"),
    "odnoklassniki": u("\uf263"),
    "odnoklassniki-square": u("\uf264"),
    "get-pocket": u("\uf265"),
    "wikipedia-w": u("\uf266"),
    "safari": u("\uf267"),
    "chrome": u("\uf268"),
    "firefox": u("\uf269"),
    "opera": u("\uf26a"),
    "internet-explorer": u("\uf26b"),
    "television": u("\uf26c"),
    "contao": u("\uf26d"),
    "500px": u("\uf26e"),
    "amazon": u("\uf270"),
    "calendar-plus-o": u("\uf271"),
    "calendar-minus-o": u("\uf272"),
    "calendar-times-o": u("\uf273"),
    "calendar-check-o": u("\uf274"),
    "industry": u("\uf275"),
    "map-pin": u("\uf276"),
    "map-signs": u("\uf277"),
    "map-o": u("\uf278"),
    "map": u("\uf279"),
    "commenting": u("\uf27a"),
    "commenting-o": u("\uf27b"),
    "houzz": u("\uf27c"),
    "vimeo": u("\uf27d"),
    "black-tie": u("\uf27e"),
    "fonticons": u("\uf280"),
    "reddit-alien": u("\uf281"),
    "edge": u("\uf282"),
    "credit-card-alt": u("\uf283"),
    "codiepie": u("\uf284"),
    "modx": u("\uf285"),
    "fort-awesome": u("\uf286"),
    "usb": u("\uf287"),
    "product-hunt": u("\uf288"),
    "mixcloud": u("\uf289"),
    "scribd": u("\uf28a"),
    "pause-circle": u("\uf28b"),
    "pause-circle-o": u("\uf28c"),
    "stop-circle": u("\uf28d"),
    "stop-circle-o": u("\uf28e"),
    "shopping-bag": u("\uf290"),
    "shopping-basket": u("\uf291"),
    "hashtag": u("\uf292"),
    "bluetooth": u("\uf293"),
    "bluetooth-b": u("\uf294"),
    "percent": u("\uf295"),
    "gitlab": u("\uf296"),
    "wpbeginner": u("\uf297"),
    "wpforms": u("\uf298"),
    "envira": u("\uf299"),
    "universal-access": u("\uf29a"),
    "wheelchair-alt": u("\uf29b"),
    "question-circle-o": u("\uf29c"),
    "blind": u("\uf29d"),
    "audio-description": u("\uf29e"),
    "volume-control-phone": u("\uf2a0"),
    "braille": u("\uf2a1"),
    "assistive-listening-systems": u("\uf2a2"),
    "american-sign-language-interpreting": u("\uf2a3"),
    "deaf": u("\uf2a4"),
    "glide": u("\uf2a5"),
    "glide-g": u("\uf2a6"),
    "sign-language": u("\uf2a7"),
    "low-vision": u("\uf2a8"),
    "viadeo": u("\uf2a9"),
    "viadeo-square": u("\uf2aa"),
    "snapchat": u("\uf2ab"),
    "snapchat-ghost": u("\uf2ac"),
    "snapchat-square": u("\uf2ad"),
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
