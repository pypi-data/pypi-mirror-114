# -*- coding: utf-8 -*-

"""Main module."""
import os
import typing
from pathlib import Path
from urllib.parse import urljoin

import pyperclip
from wand.color import Color
from wand.image import Image

PathLike = typing.Union[str, os.PathLike]


def convert(
    img: Image,
    size: int,
    filename: PathLike,
    background: str = "white",
    gravity: str = "center",
    alpha: bool = False,
    colors: int = 256,
    interpolate: str = "nearest",
) -> None:
    img.interpolate_method = interpolate
    img.alpha_channel = alpha
    img.transform(resize="%dx%d^" % (size, size))
    img.crop(width=size, height=size, gravity=gravity)
    img.quantize(colors, None, 0, False, False)
    img.save(filename=filename)


favicons = [
    "apple-icon-57x57.png",
    "apple-icon-60x60.png",
    "apple-icon-72x72.png",
    "apple-icon-76x76.png",
    "apple-icon-114x114.png",
    "apple-icon-120x120.png",
    "apple-icon-144x144.png",
    "apple-icon-152x152.png",
    "apple-icon-180x180.png",
    "android-icon-192x192.png",
    "favicon-32x32.png",
    "favicon-96x96.png",
    "favicon-16x16.png",
    "ms-icon-144x144.png",
    "favicon.ico",
]

usage = """<link rel="apple-touch-icon" sizes="57x57" href="%s">
<link rel="apple-touch-icon" sizes="60x60" href="%s">
<link rel="apple-touch-icon" sizes="72x72" href="%s">
<link rel="apple-touch-icon" sizes="76x76" href="%s">
<link rel="apple-touch-icon" sizes="114x114" href="%s">
<link rel="apple-touch-icon" sizes="120x120" href="%s">
<link rel="apple-touch-icon" sizes="144x144" href="%s">
<link rel="apple-touch-icon" sizes="152x152" href="%s">
<link rel="apple-touch-icon" sizes="180x180" href="%s">
<link rel="icon" type="image/png" sizes="192x192"  href="%s">
<link rel="icon" type="image/png" sizes="32x32" href="%s">
<link rel="icon" type="image/png" sizes="96x96" href="%s">
<link rel="icon" type="image/png" sizes="16x16" href="%s">
<meta name="msapplication-TileColor" content="#ffffff">
<meta name="msapplication-TileImage" content="%s">
<link rel="icon" href="%s">"""


def generate(
    image: Image, _output: PathLike, base: str = "/", normalize_urls: bool = True
) -> None:
    output = Path(_output)

    if output.exists() and not output.is_dir():
        raise ValueError("%s does exist and is not a directory" % output)

    favicon_urls = tuple([base + favicon for favicon in favicons])
    if normalize_urls:
        favicon_urls = tuple([urljoin(base + "/", favicon) for favicon in favicons])

    # make sure the output dir exists
    output.mkdir(parents=True, exist_ok=True)

    ico_sizes = [32, 16, 32, 48, 64]
    ico = None
    with image as img:
        for size in ico_sizes:
            print("Processing favicon.ico (%dx%d)" % (size, size))
            with img.clone() as i:
                i.interpolate_method = "nearest"
                i.alpha_channel = False
                # i.resize(size, size, filter="point")
                i.transform(resize="%dx%d^" % (size, size))
                i.crop(width=size, height=size, gravity="center")
                i.quantize(256, None, 0, False, False)
                if ico is None:
                    ico = i.clone()
                else:
                    ico.sequence.append(i)
        if ico is not None:
            ico.save(filename=output / "favicon.ico")

        for size in [57, 60, 72, 76, 114, 120, 144, 152, 180]:
            print("Processing apple icon (%dx%d)" % (size, size))
            convert(img.clone(), size, output / ("apple-icon-%dx%d.png" % (size, size)))

        for size in [36, 48, 72, 96, 114, 192]:
            print("Processing android icon (%dx%d)" % (size, size))
            convert(
                img.clone(), size, output / ("android-icon-%dx%d.png" % (size, size))
            )

        for size in [16, 32, 96]:
            print("Processing favicon (%dx%d)" % (size, size))
            convert(img.clone(), size, output / ("favicon-%dx%d.png" % (size, size)))

        for size in [70, 144, 150, 310]:
            print("Processing ms icon (%dx%d)" % (size, size))
            convert(img.clone(), size, output / ("ms-icon-%dx%d.png" % (size, size)))

    # print usage
    templated = usage % favicon_urls
    print("")
    print("To use the favicons, paste this into the <head> of your website.")
    try:
        pyperclip.copy(templated)
        print("We already copied it into your clipboard!")
    except pyperclip.PyperclipException:
        pass
    print("")
    print(templated)


def generate_from_image(
    image: PathLike, output: PathLike, base: str = "/", normalize_urls: bool = True
) -> None:
    img = Image(filename=Path(image), background=Color("white"))
    generate(img, output, base=base, normalize_urls=normalize_urls)


def generate_from_color(
    color: str, output: PathLike, base: str = "/", normalize_urls: bool = True
) -> None:
    img = Image(width=1000, height=1000, background=Color(color))
    generate(img, output, base=base, normalize_urls=normalize_urls)
