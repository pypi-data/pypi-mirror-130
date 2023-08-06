def cli():
    """HTML Pull.

    Usage:
      htmlpull xpath [-0] <xpath> [--] <file> ... 
      htmlpull -h | --help | --version

    Arguments:
      xpath        xpath to select elements
      file         html file, - for stdin

    Options:
      -h --help     Show this screen.
      --version     Show version.
    """
    import docopt
    args = docopt.docopt(cli.__doc__)
    files = args["<file>"]
    xpath = args['<xpath>']
    endl = '\0' if args["-0"] else '\n'
    import sys
    import html5lib
    from lxml import etree
    for f in files:
        if f == '-':
            f = sys.stdin.buffer
        else:
            f = open(f, 'rb')

        tree = html5lib.parse(f, "lxml", namespaceHTMLElements=False)

        items = tree.xpath(xpath)

        for item in items:
            if not isinstance(item, str):
                item = html5lib.serialize(item)
            print(item, end=endl)
