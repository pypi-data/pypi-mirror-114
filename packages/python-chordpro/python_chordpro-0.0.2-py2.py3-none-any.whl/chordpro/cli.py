from argparse import ArgumentParser

from chordpro.base import Song
from chordpro.renderers.html import render as render_html
from chordpro.renderers.text import render as render_text


def get_args():
    """Parse the command line arguments"""
    parser = ArgumentParser()
    parser.add_argument('input', metavar='FILENAME', help='Input ChordPro file')
    parser.add_argument('-o', '--output', metavar='FILENAME', help='Output to a file')
    parser.add_argument('-f', '--format', metavar='FORMAT', choices=['html', 'text'], default='html',
                        help='Output format')
    parser.add_argument('-p', '--param', metavar='KEY=VALUE', action='append', help='Parameter to send to renderer')
    return parser.parse_args()


def main():
    """The command line entrypoint"""
    args = get_args()
    render_params = {kv.split('=')[0]: kv.split('=')[-1] for kv in args.param} if args.param else {}
    # Prepare the params
    for key, value in render_params.items():
        if value.lower() == "true":
            render_params[key] = True
        elif value.lower() == "false":
            render_params[key] = False
        elif value.isdigit():
            render_params[key] = int(value)

    song = Song(args.input)
    if args.format == 'text':
        output = render_text(song, **render_params)
    else:
        output = render_html(song, **render_params)
    if args.output:
        with open(args.output, 'w') as html_file:
            html_file.write(output)
    else:
        print(output)
