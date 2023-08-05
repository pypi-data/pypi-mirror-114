"""Main controller module."""

import logging
from pathlib import Path
from jinja2 import Environment, PackageLoader
from . import pkgname

logger = logging.getLogger(__name__)


class PybootError(Exception):
    """Basic exception raised by the program."""


class Pyboot(object):
    """Controller class."""

    def __init__(self):
        """Set internal folder names."""
        self._template_folder = 'template'
        self._template_pkgname = 'package_name'

    def create_project(self, name, directory):
        """Create the project from the template."""
        loader = PackageLoader(pkgname, self._template_folder)
        env = Environment(loader=loader)
        for elt in env.list_templates(extensions=['in', 'py-tpl', 'cfg', 'md']):
            try:
                # generate content
                tpl = env.get_template(elt)
                content = tpl.render(name=name)

            except UnicodeDecodeError:
                raise PybootError('A template contains non utf-8 characters')

            # get paths
            input_file = Path(tpl.filename)
            output_file = directory / self.map_path(input_file, name, directory)

            # create folders
            Path.mkdir(output_file.parent, parents=True, exist_ok=True)

            if not output_file.exists():
                with open(output_file, 'w') as f:
                    f.write(content)
            else:
                logger.info(f'file already exists: {output_file}')

    def map_path(self, input_path, name, directory):
        """Build the relative file path to create in the destination folder."""
        # keep parts under the template folder
        parts = list(input_path.parts)
        for i, part in enumerate(reversed(parts)):
            if part == 'template':
                break
            # rename package_name
            parts[-i-1] = part.replace('package_name', name)

        # rename extension
        parts[-1] = parts[-1].replace('.py-tpl', '.py')

        # return the relative part
        return Path(*parts[-i:])
