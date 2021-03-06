"""
Contains the configuration object. This object:

    + Loads the configuration file
    + Runs the parser
    + Hands outputs to the database.
"""


from ..io import Database
from .generators import Collector, Section, Removal
from .objects import Parser
from .postprocess import \
    assign_section_line_numbers, \
    assign_section_text, \
    assign_collector_line_numbers, \
    assign_removal_line_numbers, \
    assign_removal_text


import yaml
import re


class Config(object):
    """
    Main configuration object.

    To access the final output text, you will need to use

        Config.parser.text,

    as Config.text_data is the line-by-like data.
    """
    def __init__(self, tex_filename, config_filename):
        with open(config_filename, "r") as file:
            self.raw_data = yaml.load(file)

        with open(tex_filename, "r") as file:
            self.text_data = file.readlines()

        self.generators = {}

        self.get_sections()
        self.get_collectors()
        self.get_removals()

        self.parser = Parser(self.text_data, self.generators)
        self.postprocessing_run()
        
        self.db = Database(self.raw_data["meta"]["database"])
        self.write_to_db()
        del self.db

        return


    def make_section(self, kwargs):
        """
        Make a section object!

        We have to do this because otherwise we run into problems with
        late binding.
        """
        def f(input):
            return Section(input, **kwargs)

        return f


    def make_collector(self, kwargs):
        """
        Make a collector object!
        """
        def f(input):
            return Collector(input, **kwargs)

        return f


    def make_removal(self, kwargs):
        """
        Make a removal object!
        """
        def f(input):
            return Removal(input, **kwargs)

        return f

        
    def get_sections(self):
        """
        Get the section generators.
        """

        for section in self.raw_data["sections"]:
            regex = r"%%\\{:s}\{{(.*?)\}}".format(section["syntax"])

            compiled = re.compile(regex, re.VERBOSE)

            arguments = {
                "regex": regex,
                "id": section["name"],
                "line": None,
                "capture": 1,
                "level": section["level"]
            }

            self.generators[compiled] = self.make_section(arguments)

        return


    def get_collectors(self):
        """
        Get the collector generators.
        """

        for collector in self.raw_data["collectors"]:
            regex = r"%%\\{:s}\{{.*?\}}".format(collector["syntax"])
        
            compiled = re.compile(regex, re.VERBOSE)

            arguments = {
                "regex": regex,
                "id": collector["name"],
                "capture": 0
            }

            self.generators[compiled] = self.make_collector(arguments)

        return


    def get_removals(self):
        """
        Get the removal generators.
        """

        for removal in self.raw_data["removals"]:
            for se in ["start", "end"]:
                regex = r"%%\\{:s}".format(removal["syntax"][se])

                compiled = re.compile(regex, re.VERBOSE)

                arguments = {
                    "regex": regex,
                    "id": removal["name"],
                    "se": se[0]
                }

                self.generators[compiled] = self.make_removal(arguments)

        return


    def postprocessing_run(self):
        """
        Run all of the postprocessing functions.
        """
        
        for section in self.raw_data["sections"]:
            assign_section_line_numbers(self.parser, id=section["name"])
            assign_section_text(self.parser, id=section["name"])

        for collector in self.raw_data["collectors"]:
            assign_collector_line_numbers(self.parser, id=collector["name"])

        for removal in self.raw_data["removals"]:
            assign_removal_line_numbers(self.parser, id=removal["name"])
            assign_removal_text(self.parser, id=removal["name"])

        return


    def write_to_db(self):
        """
        Write sections and collectors to database.
        """

        for match in self.parser.matches.values():
            if isinstance(match, Collector):
                self.db.insert_collector(tuple(match.pack().values()))
            elif isinstance(match, Section):
                self.db.insert_section(tuple(match.pack().values()))
            elif isinstance(match, Removal):
                self.db.insert_removal(tuple(match.pack().values()))
            else:
                continue

        return

