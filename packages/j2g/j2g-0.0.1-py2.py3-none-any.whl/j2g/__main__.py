
if __name__ == '__main__':
    from .out import *
    import argparse

    parser = argparse.ArgumentParser(
        prog="j2g",
        description=f'This is a json graph util %(prog)s version={version}. {author}',
        add_help=True,
    )
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s version={version}. {author}')
    # TODO: schema
    # parser.add_argument("--schema", action="store_true", help="source type is json schema")
    parser.add_argument("-f", "--format", choices=["pdf", "jpg", "png"], default="pdf", help="Type of the output file")
    parser.add_argument("-n", "--root_node_name", dest="root_node_name", default="", help="root node name")
    parser.add_argument("-p", "--power", action="store_true", help="If the output file exists, overwrite it.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet work, do not display a completion message.")
    parser.add_argument("source", help="json file")
    parser.add_argument("destination", help="Prefix the output file.")

    args = parser.parse_args()
    # foo = schema_graph if args.schema else json_graph
    foo = json_graph

    import json
    import os

    with open(args.source, 'r', encoding='utf-8') as f:
        destination = args.destination if args.destination else args.source
        dest=".".join([destination, args.format])
        if not args.power and os.path.exists(dest):
            print(f"File '{dest}' already exists.")
            exit(1)

        js = json.loads(f.read())
        dot = foo(js, args.root_node_name)
        dot.render(destination, format=args.format)
        if not args.quiet:
            print(f"File {dest} has been created.")
