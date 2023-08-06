import re
import yaml
import deepmerge
from pathlib import Path
from copy import deepcopy
from frictionless import File
from .system import system
from .helpers import cached_property
from . import settings
from . import helpers


class Document:
    def __init__(self, source, *, target=None, format=None, project=None):

        # Infer target
        if not target:
            suffix = f".{format or settings.DEFAULT_FORMAT}"
            target = str(Path(source).with_suffix(suffix))

        # Read input
        with open(source) as file:
            input = file.read()

        # Read preface
        preface = ""
        if input.startswith("---"):
            preface, input = input.split("---", maxsplit=2)[1:]

        # Read config
        config = {}
        if project:
            config = deepcopy(project.config)
        if preface:
            deepmerge.always_merger.merge(config, yaml.safe_load(preface))

        # Save attributes
        self.__source = source
        self.__target = target
        self.__project = project
        self.__preface = preface
        self.__config = config
        self.__input = input
        self.__output = None

        # Create plugins (document needs to be ready)
        self.__plugins = system.create_plugins(self)

    @property
    def plugins(self):
        return self.__plugins

    @property
    def source(self):
        return self.__source

    @property
    def target(self):
        return self.__target

    @cached_property
    def format(self):
        file = File(self.target)
        return file.format

    @property
    def project(self):
        return self.__project

    @property
    def preface(self):
        return self.__preface

    @property
    def config(self):
        return self.__config

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, value):
        self.__input = value

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, value):
        self.__output = value

    @cached_property
    def title(self):
        prefix = "# "
        for line in self.input.splitlines():
            if line.startswith(prefix):
                return line.lstrip(prefix)

    @cached_property
    def description(self):
        pattern = re.compile(r"^\w")
        for line in self.input.splitlines():
            line = line.strip()
            if pattern.match(line):
                return line

    @cached_property
    def keywords(self):
        return ",".join(self.title.split())

    # Process

    def process(self):
        for plugin in self.plugins:
            plugin.process_document(self)

    # Output

    def print(self, print=print):
        if self.output is not None:
            print(self.output)

    def write(self):
        if self.output is not None:
            helpers.write_file(self.target, self.output)
