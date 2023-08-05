# -*- coding: utf-8 -*-

"""Console script for favico."""
import re
import sys
import typing

import click

from favico import generate_from_color, generate_from_image

baseKey = "base"
normalizeKey = "normalize"


@click.group()
@click.option("-b", "--base", type=str, default="/")
@click.option("--normalize-urls/--no-normalize-urls", default=True)
@click.pass_context
def main(
    ctx: click.Context,
    base: typing.Optional[str],
    normalize_urls: typing.Optional[bool],
) -> int:
    """Console script for favico."""
    ctx.obj[baseKey] = base
    ctx.obj[normalizeKey] = normalize_urls
    return 0


@main.command()
@click.argument("image", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
@click.pass_context
def image(ctx: click.Context, image: str, output: str) -> int:
    norm_urls = ctx.obj[normalizeKey]
    generate_from_image(
        image,
        output,
        base=ctx.obj[baseKey] or "/",
        normalize_urls=norm_urls if norm_urls is not None else True,
    )
    return 0


def validate_color(ctx: click.Context, param: click.Parameter, value: str) -> str:
    hex_regex = r"^#(?:[0-9a-fA-F]{3}){1,2}$"
    if not re.match(hex_regex, value):
        raise click.BadParameter(f"{value} is not a valid hex color")
    return value


@main.command()
@click.argument("color", type=str, callback=validate_color)
@click.argument("output", type=click.Path(exists=False))
@click.pass_context
def color(ctx: click.Context, color: str, output: str) -> int:
    norm_urls = ctx.obj[normalizeKey]
    generate_from_color(
        color,
        output,
        base=ctx.obj[baseKey] or "/",
        normalize_urls=norm_urls if norm_urls is not None else True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma: no cover
