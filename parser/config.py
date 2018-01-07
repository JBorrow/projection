from .generators import Collector, Section
from .objects import Parser
from .io import Database

import .postprocess as pp

import yaml
import re


class Config(object):
    def __init__(self, tex_filename, config_filename):
        with open(config_filename, "r") as file:
            self.raw_data = yaml.load(file)

        with open(tex_filename, "r") as file:
            self.text_data = text_file.readlines()

        self.generators = {}

        self.get_sections()
        self.get_collectors()

        self.parser = Parser(self.text_data, generators)
        self.postprocessing_run()
    
        
        self.db = Database(self.raw_data["meta"]["database"])
        self.write_to_db()
        del self.db

        return

        
    def get_sections(self):
        """
        Get the section generators.
        """

        for section in self.raw_data["sections"]:
            regex = "%%\\{:s}{{(.*?)}}".format(section["syntax"])

            compiled = re.compile(regex)

            arguments = {
                "regex": regex,
                "id": section["name"],
                "line": None,
                "capture": 1,
                "level": section["level"]
            }

            self.generators[compiled] = lambda x: Section(x, **arguments)

        return


    def get_collectors(self):
        """
        Get the collector generators.
        """

        for collector in self.raw_data["collectors"]:
            regex = "%%\\{:s}{{.*?}}".format(collector["syntax"])
        
            compiled = re.compile(regex)

            arguments = {
                "regex": regex,
                "id": collector["name"],
                "capture": 0
            }

            self.generators[compiled] = lambda x: Collector(x, **arguments)

        return


    def postprocessing_run(self):
        """
        Run all of the postprocessing functions.
        """
        
        for section in self.raw_data["sections"]:
            pp.assign_section_line_numbers(self.parser, id=section["name"])
            pp.assign_section_text(self.parser, id=section["name"])

        for collector in self.raw_data["collector"]:
            pp.assign_collector_line_numbers(self.parser, id=collector["name"])

        return


    def write_to_db(self):
        """
        Write sections and collectors to database.
        """

        for match in self.parser.matches.values():
            if isinstance(match, Collector):
                self.db.insert_collector(match.pack().values())
            elif isinstance(match, Section):
                self.db.insert_section(match.pack().values())
            else:
                continue

        return

