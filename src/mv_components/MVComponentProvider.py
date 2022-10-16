from masonite.facades import View
from masonite.providers import Provider
from . import _render, _render_with_collection, config_loader
from masonite.commands import Command
from inflection import camelize, underscore
import os, pathlib


class CreateComponentCommand(Command):
    """
    Creates a new mv-component

    view-component:make
        {name : Name of component}
        {--f|flag : An optional argument for the command}
        {--o|option=default: An optional argument for the command with default value}
    """

    def handle(self):
        name = self.argument('name')
        COMPONENTS_DIR = config_loader()
        """templates folder must be root directory of components path."""
        file_name_py = f"{camelize(name)}.py"
        file_name_html = f"{camelize(name)}.html"
        full_directory_path = os.path.join(os.getcwd() + '\\templates', COMPONENTS_DIR)

        if os.path.exists(os.path.join(full_directory_path, file_name_py)) or os.path.exists(os.path.join(full_directory_path, file_name_html)):
            self.line(
                f'<error>Component "{name}" Already Exists ({full_directory_path}\\{file_name_py} or {file_name_html})</error>'
            )
            return

        stub = str(pathlib.Path(__file__).parent.absolute()) + r"\stubs\component.stub"
        f = open(stub).read()
        component = f.replace("__CLASS__", camelize(name))
        f = open(os.path.join(full_directory_path, file_name_py), 'w').write(component)
        f = open(os.path.join(full_directory_path, file_name_html), 'w').write("")
        self.info(f"Component created: {name}")


class MVComponentProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        View.add_extension('mv_components.mv_component_ext.MVComponentExt')
        View.share(_render())
        View.share(_render_with_collection())
        self.application.make("commands").add(CreateComponentCommand())

    def boot(self):
        pass
