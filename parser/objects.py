import re
import ltmd


class Parser(object):
    """
    Main parser class for the system. This should:

    + Take the text in, and search for all instances of the generators
      that are passed to it
    + Use these generators to get the output strings
    + Replace the initial strings with placeholders ready for the main pandoc
      processing loop
    + Run pandoc (via ltmd).
    + Replace the placeholder strings with output.
    """
    def __init__(self, text, generators):
        """
        Initial processing loop.
        """
        self.original_text = text
        self.text = text
        self.original_matches = {}
        self.matches = {}
        self.generators = generators

        # initial match extraction
        self.find_matches()
        self.original_matches = self.matches.copy()

        # replace matches with temp strings
        self.replace_with_temp()

        # put our text through pandoc
        self.pandoc_it()

        # go find our new line numbers
        self.find_new_line_numbers()

        # second replace loop - swap things out for comments, essentially
        self.replace_temp_with_final()



    def find_matches(self):
        for number, line in enumerate(self.text):
            match = self.match(line):
            
            if match:
                self.matches[number] = match(line)

        return


    def match(self, line):
        """
        Looks for a match in the generators object.

        If there is a match to the line, the matching generator is returned.

        If not, then this function returns false.
        """

        for expression, generator in self.generators.items():
            matches = expression.findall(line)

            if matches:
                return generator

        else:
            return False


    def replace_with_temp(self):
        """
        Replace all the matches in the text string with their temporary strings
        that will 'go through' pandoc.
        """
        for line_number, match in self.matches.items():
            self.text[line_number] = match.temporary_replacement

        return


    def pandoc_it(self, image_prepend=None, extra=None):
        """
        Put the text trough ltmd (pandoc!) and convert it to markdown.
        We'll then split it back into a list of lines (as that's a more
        convenient way of storing it).
        """
        if image_prepend is None:
            image_prepend = "/"

        if extra is None:
            extra = ["--mathjax"]

        joined_text = "\n".join(self.text)

        # See the ltmd API reference
        pre_processed = ltmd.PreProcess(joined_text, ImgPrepend=image_prepend)
        pandocced = ltmd.RunPandoc(pre_processed.ParsedText, extra=extra)
        post_processed = ltmd.PostProcess(pandocced, pre_processed.parsed_data)
        
        output_text = post_processed.ParsedText
        # End of ltmd use

        unjoined_text = output_text.split("\n")

        self.text = unjoined_text

        return

       
    def find_new_line_numbers(self):
        """
        The line numbers may have changed now that we have put our stuff
        through pandoc. Let's fix that!

        What we _do_ know though is that our matches will still be in the
        same order! Therefore we only need to test against a single item.
        """
        new_matches = {}

        match_items = self.matches.items()
        search_items = [x[1] for x in match_items]
       
        # Set initial check
        check_for = match_items.pop(0)

        for line_number, generator in enumerate(self.text):
            if generator.temporary_replacement == check_for:
                new_matches[line_number] = generator
               
                try:
                    check_for = search_items.pop(0)
                except IndexError:
                    # We've found _all_ of our matches!
                    self.matches = new_matches

                    return

        # We didn't find some matches - clean up and then raise an
        # Exception in case someone wants to catch it.
        self.matches = new_matches

        not_found = [x.temporary_replacement for x in search_items]
        raise Exception(f"{not_found}\
                          The above items were not found in the\
                          post-pandoc text.")

        return 
        

    def replace_temp_with_final(self):
        """
        Replace the temporary things that were used to track our items through
        pandoc with our final text.
        
        This should preserve line numbers.
        """
        
        for line_number, match in self.matches:
            self.text[line_number] = match.output_text

        return

