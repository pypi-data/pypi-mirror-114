import typer
import yaml
import logging
from pathlib import Path
from .. import TemplateLoader, LatexBuilder, DocModel


def build(
    target_folder: Path = typer.Argument(
        ...,
        help=(
            "Local folder in which to construct the Latex assets. If TARGET exists it"
            "and all files will be removed and a new empty folder structure created"
        ),
        resolve_path=True,
        dir_okay=True,
        file_okay=False,
    ),
    docmodel_file: str = typer.Argument(
        ...,
        help=(
            "Path to a YAML file containing the DocModel required to render the template"
            "The DocModel is a dict structure that wih fields that conform to the Curvenote DocModal"
            "schema, additional data can be specified and these will be passed to the template but"
            "defined fields need to confirm to the appropriate types"
        ),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
    content_file: str = typer.Argument(
        ...,
        help=(
            "Path to a YAML file containing the DocModel required to render the template"
        ),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
    template_path: str = typer.Option(
        None,
        help=(
            "Path to a Curvenote compatible LaTeX template folder."
            "This is intended for use with local Curvenote templates or in template development"
        ),
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
    ),
    user_options: str = typer.Option(
        None,
        help=(
            "A path to a local YAML file containing user options to apply to the tempalte."
        ),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
):
    typer.echo(f"Target folder: {target_folder}")
    typer.echo(f"Doc Model file: {docmodel_file}")
    typer.echo(f"Content file: {content_file}")
    if template_path:
        typer.echo(f"Using template at: {template_path}")
    else:
        typer.echo("Using built in template")
    if user_options:
        typer.echo(f"User Options file: {user_options}")
    else:
        typer.echo("No user options set")

    content = ""
    try:
        with open(content_file) as cfile:
            content = cfile.read()
        typer.echo("Loaded content")
    except:
        typer.echo("Could not read content")
        raise typer.Exit(code=1)

    docmodel = {}
    try:
        with open(docmodel_file) as dfile:
            docmodel = yaml.load(dfile.read(), Loader=yaml.FullLoader)
        typer.echo("Loaded data")
    except:
        typer.echo("Could not load data (DocModel)")
        raise typer.Exit(code=1)

    loader = TemplateLoader(str(target_folder))
    if template_path:
        template_options, renderer = loader.initialise_from_path(str(template_path))
    else:
        template_options, renderer = loader.initialise_with_default()
    typer.echo("Template loaded")

    builder = LatexBuilder(template_options, renderer, str(target_folder))
    builder.build(DocModel(dict(doc=docmodel)), [content])

    typer.echo("Done!")
