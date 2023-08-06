#!/usr/bin/env python3
'''Main module.'''

import argparse
import PIL.Image as Image
import imagesplitter.splitter as imagesplitter
import imagesplitter.printerpaper as printerpaper


def main(args: argparse.Namespace):
    '''Main function.

    :param args: Command line arguments.
    :type args: argparse.Namespace'''
    img = Image.open(args.input)

    dpi = (args.dpi, args.dpi)

    paper = printerpaper.PrinterPaper(args.paperwidth, args.paperheight, dpi)
    splits = imagesplitter.split_image(img, args.columns, args.rows)

    pdf = [paper.fill_image(v) for v in splits]

    pdf[0].save(args.output, save_all=True, append_images=pdf[1:], dpi=dpi)

def cli():
    '''Command Line Entrypoint.'''
    parser = argparse.ArgumentParser(prog="imagesplitter", \
     description="Split image into columns*row images and serve as a printable PDF.")
    parser.add_argument('input', type=argparse.FileType('rb'),\
         help="Path to image to process.")
    parser.add_argument('columns', type=int,\
         help="Number of columns.")
    parser.add_argument('rows', type=int,\
         help="Number of rows.")
    parser.add_argument('-d', '--dpi', type=float,\
         help="DPI of your printer.", default=300)
    parser.add_argument('-w', '--paperwidth', type=float,\
         help="Specify Paper Width in inches.", default=8.5)
    parser.add_argument('-y', '--paperheight', type=float,\
         help="Specify Paper Height in inches.", default=11)
    parser.add_argument('-o', '--output', type=argparse.FileType('wb'),\
         help="Output file", default=open("out.pdf", "wb"))
    args = parser.parse_args()

    try:
        main(args)
    finally:
        args.input.close()
        args.output.close()

if __name__ == "__main__":
    cli()
     