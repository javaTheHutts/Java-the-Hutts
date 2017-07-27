"""
----------------------------------------------------------------------
Author(s): Jan-Justin van Tonder
----------------------------------------------------------------------
Code for managing text cleanup and extraction of OCR output.
----------------------------------------------------------------------
"""

import re


class TextManager:
    def __init__(self):
        # Specify initial list of undesirable characters.
        self.deplorables = ['_']

    def clean_up(self, string, exclusions=None, append=True):
        # Remove undesirable characters, spaces and newlines.
        compiled_deplorable_re = self._compile_deplorables(exclusions, append)
        sanitised = re.sub(compiled_deplorable_re, '', string)
        stripped_and_sanitised = re.sub(r'(\n\s*\n)|(\n\s+)|(\s*\n)', '\n', sanitised)
        return stripped_and_sanitised.strip()

    def _compile_deplorables(self, deplorables, append):
        # Append to existing list if append is true.
        if deplorables is not None and append is True:
            self.deplorables += self._sanitise_deplorables(deplorables)
        # Overwrite existing list if append is false.
        elif deplorables is not None and append is False:
            self.deplorables = deplorables
        reg_exp = r'[^\w\d\s]'
        # If list is not empty, add additional characters to remove to regex.
        if self.deplorables:
            reg_exp += r'|[' + ''.join(self.deplorables) + ']'
        return re.compile(reg_exp, re.UNICODE)

    def _sanitise_deplorables(self, deplorables):
        sanitised = []
        for deplorable in deplorables:
            # Filter for valid inputs.
            if type(deplorable) is str and deplorable != '':
                # Escape ] and [ so as not to break the regex pattern.
                deplorable = re.sub(re.compile(r']'), '\]', deplorable)
                deplorable = re.sub(re.compile(r'\['), '\[', deplorable)
                sanitised.append(deplorable)
        return sanitised

    def dictify(self, id_string):
        # Given a string containing extracted ID text,
        # create a dictionary object from said text.
        id_info = {}
        # A list of dictionaries used to find regex matches.
        # The ID number regex is not the best performing pattern at this stage.
        find_matches = [{
            'find': 'surname',
            'regex': r'(surname\ *\n)((\w*\ *)*\n)',
            'text': True
        }, {
            'find': 'names',
            'regex': r'((fore\ *)?(names)\ *\n)((\w*\ *)*\n)',
            'text': True
        }, {
            'find': 'idNumber',
            'regex': r'((id\w*\ * )(no|number) *\s)((\w* *)*\n)',
            'text': False
        }, {
            'find': 'gender',
            'regex': r'((sex|gender)\ *\n)((\w*\ *)*\n)',
            'text': True
        }]
        # Attempt to retrieve regex matches
        for find_match in find_matches:
            key = find_match['find']
            reg_exp = find_match['regex']
            text = find_match['text']
            id_info[key] = self._get_match(id_string, reg_exp, text)
            if (key == "idNumber"):
                yy = id_info[key][:2]
                mm = id_info[key][2:4]
                dd = id_info[key][4:6]
                date_of_birth = str(yy) + "-" + str(mm) + "-" + str(dd)
                id_info['dateOfBirth'] = date_of_birth

        # Return the info we tried to find.
        return id_info

    def _get_match(self, id_string, reg_exp, text=True):
        # Compile regex pattern.
        re_pattern = re.compile(reg_exp, re.UNICODE | re.IGNORECASE)
        match_info = re.search(re_pattern, id_string)
        # Is there a match?
        if not match_info:
            return None
        else:
            # Retrieve matched string.
            match_pair = match_info.group()
            # Split the string on newline to get desired pair.
            # Strip the last newline first, however.
            match_pair = match_pair.strip().split('\n')
            # Only interested in value, not 'key'
            # e.g: Surname\n
            #      Smith\n
            # ... ignore 'Surname' so as to be able to manually specify.
            # Also strip whitespace while here.
            match = match_pair[-1].strip()
            if text:
                # If text, convert to lowercase, then capitalize each new word.
                match = match.lower().title()
            else:
                # If not text, strip everything that is not a digit.
                # It may be better for instances such as ID number?
                match = re.sub(r'[^\d]', '', match)
            return match
