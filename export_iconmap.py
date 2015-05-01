def export_iconmap(filename, prefix):
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