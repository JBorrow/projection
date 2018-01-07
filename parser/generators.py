import uuid
import re

from .objects import Generator


class Collector(Generator):
    """
    General collector object, for example for keypoints.

    The output_text for collector objects should always be set as a HTML
    comment -- this is because collectors are dealt with later separately.

    Capture is the capturing group to look for -- this is helpful if you have
    regex of the following form:

    %%\lookfor{(.*?)}

    and you want the text in the first capturing group -- this would correspond
    to capture=1 (rather than the default capture=0).

    id is a unique identifier for this _type_ of collector (for example, the
    string 'Keypoint' for a keypoint).
    """
    def __init__(self, input, regex=None, id=None, line=None, capture=0):
        if regex is None and not isinstance(input, dict):
            raise ValueError(
                "Please supply a string or compiled pattern to the regex\
                 input value."
            )

        self.regex = regex
        self.id = id
        self.line = line
        self.capture = capture

        # This calls Collector.parse()
        super(Collector, self).__init__(input)

        return


    def parse(self):
        """
        Use the regex to parse the information!

        This sets:
            uid, temporary_replacement, output_text.
        """
        
        self.uid = str(uuid.uuid4())

        self.text = re.search(self.regex, self.input)[self.capture]

        self.temporary_replacement = self.uid

        self.output_text = f"<!-- Collector {self.uid} -->"

        return


    def unpack(
            self,
            input,
            line,
            capture,
            regex,
            uid,
            text,
            temporary_replacement,
            output_text,
            id
        ):
        """
        Unpacks a dictionary used to temporarily store the object contents.
        """

        self.input = input
        self.line = line
        self.capture = capture
        self.regex = regex
        self.uid = uid
        self.text = text
        self.temporary_replacement = temporary_replacement
        self.output_text = output_text
        self.id = id


        return


    def pack(self):
        """
        Packs the object's contents in a dictionary. This is useful for output
        to plaintext files.
        """

        packed = {}

        packed["input"] = self.input
        packed["line"] = self.line
        packed["capture"] = self.capture
        packed["regex"] = self.regex
        packed["uid"] = self.uid
        packed["text"] = self.text
        packed["temporary_replacement"] = self.temporary_replacement
        packed["output_text"] = self.output_text
        packed["id"] = self.id

        return packed


class Section(Generator):
    """
    General sectioning class.

    Level gives the 'heading level'. For example, level 1 corresponds to:

        # Heading

    level 5 to

        ##### Heading

    etc.
    """
    def __init__(self, input, regex=None, id=None, line=None, capture=0, level=1):
        if regex is None and not isinstance(input, dict):
            raise ValueError(
                "Please supply a string or compiled pattern to the regex\
                 input value."
            )

        self.regex = regex
        self.id = id
        self.line = line
        self.level = level
        self.capture = capture

        self.startline = None
        self.endline = None

        # This calls Section.parse()
        super(Section, self).__init__(input)

        return


    def parse(self):
        """
        Use the regex to parse the information!

        This sets:
            uid, temporary_replacement, output_text.
        """
        
        self.uid = str(uuid.uuid4())

        self.text = re.search(self.regex, self.input)[self.capture]

        self.temporary_replacement = self.uid

        self.output_text = f"{'#'*self.level} {self.text}"

        return


    def unpack(
            self,
            input,
            line,
            level,
            capture,
            regex,
            uid,
            text,
            temporary_replacement,
            output_text,
            startline,
            endline,
            id
        ):
        """
        Unpacks a dictionary used to temporarily store the object contents.
        """

        self.input = input
        self.line = line
        self.level = level
        self.capture = capture
        self.regex = regex
        self.uid = uid
        self.text = text
        self.temporary_replacement = temporary_replacement
        self.output_text = output_text
        self.startline = startline
        self.endline = endline
        self.id = id


        return


    def pack(self):
        """
        Packs the object's contents in a dictionary. This is useful for output
        to plaintext files.
        """

        packed = {}

        packed["input"] = self.input
        packed["line"] = self.line
        packed["level"] = self.level
        packed["capture"] = self.capture
        packed["regex"] = self.regex
        packed["uid"] = self.uid
        packed["text"] = self.text
        packed["temporary_replacement"] = self.temporary_replacement
        packed["output_text"] = self.output_text
        packed["startline"] = self.startline
        packed["endline"] = self.endline
        packed["id"] = self.id

        return packed

