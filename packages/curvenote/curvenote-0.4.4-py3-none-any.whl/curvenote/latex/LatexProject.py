import os
import logging
import yaml
from curvenote.latex.utils.decorators import log_and_raise_errors
from typing import Tuple, Union, List, NamedTuple
from curvenote.models import BlockFormat, Project
from ..client import Session
from ..utils import decode_url, decode_oxa_link
from .LatexArticle import LatexArticle
from .utils import LocalMarker, escape_latex
from .templating import DocModel, TemplateOptions, TemplateRenderer

logger = logging.getLogger()


class ProjectItem(NamedTuple):
    path: str
    filename: str
    item: LatexArticle


class LatexProject:
    def __init__(
        self,
        session: Session,
        target_folder: str,
    ):
        self.session = session

        self.target_folder = os.path.abspath(target_folder)
        self.assets_folder = os.path.join(self.target_folder, "assets")
        self.images_folder = os.path.join(self.target_folder, "assets", "images")

        self.create_folders()

        self.articles: List[ProjectItem] = []
        self.reference_list: List[LocalMarker] = []
        self.figure_list: List[LocalMarker] = []

    @classmethod
    def build_single_article_by_name(
        cls,
        target_folder: str,
        session: Session,
        project_id_or_obj: Union[str, Project],
        article_id: str,
        version: int,
        tex_format: BlockFormat,
    ):
        latex_project = cls(session, target_folder)
        latex_project.add_article(project_id_or_obj, article_id, version, tex_format)
        latex_project.reconcile()
        return latex_project

    @classmethod
    def build_single_article_by_url(
        cls, target_folder: str, session: Session, url: str, tex_format: BlockFormat
    ):
        vid, pathspec = None, None
        try:
            vid = decode_oxa_link(url)
        except ValueError:
            pathspec = decode_url(url)

        latex_project = cls(session, target_folder)

        logging.info("writing to %s", {latex_project.target_folder})
        latex_project.create_folders()

        if vid:
            latex_project.add_article(vid.project, vid.block, vid.version, tex_format)
        else:
            if not pathspec.block:
                raise ValueError("URL does not include a block id")
            latex_project.add_article(
                pathspec.project,
                pathspec.block,
                pathspec.version,
                tex_format,
            )

        latex_project.reconcile()
        return latex_project

    def create_folders(self):
        logger.info("Creating %s", self.assets_folder)
        os.makedirs(self.assets_folder, exist_ok=True)

        logger.info("Creating %s", self.images_folder)
        os.makedirs(self.images_folder, exist_ok=True)

    def next_index(self):
        return len(self.articles)

    @log_and_raise_errors(lambda *args: "Could not add article to LaTeX project")
    def add_article(
        self,
        project_id: Union[str, Project],
        article_id: str,
        version: int,
        fmt: BlockFormat,
    ):
        logging.info("adding article using ids/names")
        latex_article = LatexArticle(self.session, project_id, article_id)
        latex_article.fetch(fmt, version)
        latex_article.localize(
            self.session, self.assets_folder, self.reference_list, self.figure_list
        )
        filename = f"{self.next_index()}_{latex_article.block.name}"
        self.articles.append(
            ProjectItem(
                path=f"documents/{filename}", item=latex_article, filename=filename
            )
        )
        logging.info("added article")

    def reconcile(self):
        for article in self.articles:
            article.item.reconcile_figures(self.figure_list)

    def dump(self) -> Tuple[DocModel, List[str], str]:
        logging.info("Dumping data and content...")
        if len(self.articles) < 1:
            raise ValueError("Need at least one article")

        # TODO - in book mode (compact == False) we would need to
        # return a list of strings
        content: List[str] = []
        for article in self.articles:
            content.append(article.item.content)

        first = self.articles[0]

        authors = []
        for author in first.item.authors:
            if author.user:
                user = next((u for u in first.item.users if u.id == author.user), None)
                if user:
                    authors.append(
                        dict(
                            username=user.username,
                            name=user.display_name,
                            bio=user.bio,
                            location=user.location,
                            website=user.website,
                            github=user.github,
                            twitter=user.twitter,
                            affiliation=user.affiliation,
                            orcid=user.orcid,
                        )
                    )
            elif author.plain:
                authors.append(dict(name=escape_latex(author.plain)))
            else:
                logging.info("found empty author, skipping...")

        data = DocModel(
            dict(
                doc=dict(
                    oxalink=first.item.oxalink(self.session.site_url),
                    title=escape_latex(first.item.title),
                    authors=authors,
                    date=first.item.date,
                    tags=[escape_latex(tag) for tag in first.item.tags],
                ),
                tagged=dict(),
                curvenote=dict(defs=r"\input{curvenote.def}"),
                options=dict(docclass=""),
            )
        )

        logging.info("Dumping bibtex...")
        bibtex = ""
        if len(self.reference_list) > 0:
            # de-duplicate the bib entries
            bib_entries = list(set(self.reference_list))
            for reference in bib_entries:
                bibtex += str(reference.content) + "\n"

        return data, content, bibtex

    def write(self):
        """
        Will write 3 files
         - docmodel.yml
         - context.tex
         - main.bib
        """
        data, content, bibtex = self.dump()

        docmodel_filename = os.path.join(self.target_folder, "docmodel.yml")
        with open(docmodel_filename, "w") as file:
            yaml.dump(data, file)
        logging.info(f"DocModel file created: {docmodel_filename}")

        content_filename = os.path.join(self.target_folder, "content.tex")
        with open(content_filename, "w") as file:
            for chunk in content:
                file.write(chunk)
                file.write("\n")
        logging.info(f"Content file created: {content_filename}")

        bib_filename = os.path.join(self.target_folder, "main.bib")
        with open(bib_filename, "w") as file:
            file.write(bibtex)
        logging.info(f"Bib file created: {bib_filename}")
