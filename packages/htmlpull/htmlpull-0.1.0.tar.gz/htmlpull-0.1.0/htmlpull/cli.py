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
    import sys
    import html5lib
    from lxml import etree
    for f in args["<file>"]:
        if f == '-':
            f = sys.stdin.buffer
        else:
            f = open(f,'rb')
        tree = html5lib.parse(f, "lxml", namespaceHTMLElements=False)
        for item in tree.xpath(args['<xpath>']):
            if not isinstance(item,str):
                item = html5lib.serialize(item)
            print(item)
