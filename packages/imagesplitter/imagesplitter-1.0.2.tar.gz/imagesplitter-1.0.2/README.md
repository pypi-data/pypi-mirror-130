# image-splitter
Split an image into multiple columns or rows and serve as a printable PDF.

## Getting Started

### Installation

You can run `setup.py` through `./setup.py install` or `python3 setup.py install`.

### Usage

This project has a command line entry point that allows you to use it with the `imagesplitter` command. You may also use `python3 -m imagesplitter`.

```
imagesplitter [options] image columns rows
options:
    -h                  Help
    -d, --dpi           DPI of printer (defaults to 300).
    -w, --paperwidth    Width of paper in inches (defaults to 8.5).
    -y, --paperheight   Height of paper in inches (defaults to 11).
    -o, --output        File to output to (defaults to out.pdf).
```

## Examples

Examples can be found in the [examples](examples) directory.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Authors

* Willow Ciesialka
