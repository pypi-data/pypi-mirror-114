import logging
import os
import pkg_resources
from typing import Dict, Tuple
from zipfile import ZipFile
from .templating import TemplateLoader, TemplateRenderer, TemplateOptions
from ..utils import download
from ..client import Session


TEMPLATES_PATH = pkg_resources.resource_filename("curvenote", "latex/templates")
DEFAULT_TEMPLATE_PATH = os.path.join(TEMPLATES_PATH, "default")


class OnlineTemplateLoader(TemplateLoader):
    def initialise_from_template_api(
        self, session: Session, template_name: str
    ) -> Tuple[TemplateOptions, TemplateRenderer]:
        logging.info("Writing to target folder: %s", self._target_folder)

        logging.info("Looking up template %s", template_name)
        try:
            link = session.get_template_download_link(template_name)
        except ValueError as err:
            logging.error("could not download template %s", template_name)
            raise ValueError(f"could not download template: {template_name}") from err

        # fetch template to local folder
        logging.info("Found template, downloading...")
        zip_filename = os.path.join(
            self._target_folder, f"{template_name}.template.zip"
        )
        download(link, zip_filename)

        # unzip
        logging.info("Download complete, unzipping...")
        with ZipFile(zip_filename, "r") as zip_file:
            zip_file.extractall(self._target_folder)
        logging.info("Unzipped to %s", self._target_folder)
        os.remove(zip_filename)
        logging.info("Removed %s", zip_filename)

        # success -- update members
        self._template_name = template_name
        renderer = TemplateRenderer()
        renderer.use_from_folder(self._target_folder)

        return TemplateOptions(self._target_folder), renderer
