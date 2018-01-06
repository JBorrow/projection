import uuid
import re

from .objects import Generator


class Collector(Generator):
    """
    General collector object, for example for keypoints.

    The output_text for collector objects should always be set as a HTML
    comment -- this is because collectors are dealt with later separately.
    """
    def __init__(self, input, regex=None, line=None):
        if regex is None:
            raise ValueError(
                "Please supply a string or compiled pattern to the regex\
                 input value."
            )

        self.regex = regex
        self.line = line

        # This calls Collector.parse()
        super(Collector, self).__init__(input)

        return


    def parse(self):
        """
        Use the regex to parse the information!

        This sets:
            uid, temporary_replacement, output_text.
        """
        
        self.uid = uuid.uuid4()

        self.text = re.search(self.regex, self.input)[0]

        self.temporary_replacement = str(self.uid)

        self.output_text = f"<!-- Collector {str(self.uid)} -->"

        return


    def unpack(
            self,
            input,
            line,
            regex,
            uid,
            text,
            temporary_replacement,
            output_text
        ):
        """
        Unpacks a dictionary used to temporarily store the object contents.
        """

        self.input = input
        self.line = line
        self.regex = regex
        self.uid = uid
        self.text = text
        self.temporary_replacement = temporary_replacement
        self.output_text = output_text


        return


    def pack(self):
        """
        Packs the object's contents in a dictionary. This is useful for output
        to plaintext files.
        """

        packed = {}

        packed["input"] = self.input
        packed["line"] = self.line
        packed["regex"] = self.regex
        packed["uid"] = self.uid
        packed["text"] = self.text
        packed["temporary_replacement"] = self.temporary_replacement
        packed["output_text"] = self.output_text

        return packed


