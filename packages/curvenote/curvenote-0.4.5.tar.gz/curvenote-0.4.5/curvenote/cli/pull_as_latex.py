from curvenote.models import BlockFormat
import logging
import sys
import typer
import os
from curvenote.utils import decode_oxa_link, decode_url
from ..client import Session
from ..latex import LatexProject, OnlineTemplateLoader
from ..latex.templating import LatexBuilder


app = typer.Typer()

logger = logging.getLogger()


def url_set(ctx: typer.Context, value: str):
    if ctx.resilient_parsing:
        return
    if value:
        typer.echo("URL provided project, article and version options will be ignored")
    return value


def pull_as_latex(
    target: str = typer.Argument(
        ...,
        help=(
            "Local folder in which to construct the Latex assets. If TARGET exists it"
            "and all files will be removed and a new empty folder structure created"
        ),
    ),
    token: str = typer.Argument(
        ..., envvar="CURVENOTE_TOKEN", help="API token generated from curvenote.com"
    ),
    url: str = typer.Option(
        None,
        help=("A valid url (or oxa link) to the existing Article"),
        is_eager=True,
        callback=url_set,
    ),
    vanilla: bool = typer.Option(
        None,
        help=(
            "When set, will request vanilla LaTeX without Curvenote custom commands and environments"
        ),
    ),
):
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    try:
        session = Session(token)
    except Exception as err:
        typer.echo("Could not start an API session - check your token")
        raise typer.Exit(code=1)

    if url:
        typer.echo(f"Accessing block {url}")
        version_id, pathspec = None, None
        try:
            version_id = decode_oxa_link(url)
        except ValueError:
            pathspec = decode_url(url)
            typer.echo("Decoded {pathspec}")

        try:
            block = session.get_block(
                version_id.project if version_id is not None else pathspec.project,
                version_id.block if version_id is not None else pathspec.block,
            )
            typer.echo(f"Found & retreived block: {block.name}")
        except ValueError as err:
            typer.echo(err)
            typer.echo("Could not find block or you do not have access")
            raise typer.Exit(code=1) from err

        try:
            latex_project = LatexProject.build_single_article_by_url(
                target,
                session,
                url,
                BlockFormat.tex if vanilla else BlockFormat.tex_curvenote,
                []
            )
            latex_project.write()
        except ValueError as err:
            typer.echo(err)
            raise typer.Exit(code=1)

        typer.echo("Exiting...")
        return typer.Exit(code=0)
