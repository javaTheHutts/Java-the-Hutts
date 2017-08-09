"""
----------------------------------------------------------------------
Author(s): Stephan Nell, Marno Hermann, Jan-Justin van Tonder
----------------------------------------------------------------------
This file contains the logic used to manage the text cleanup and
extraction of OCR output.
----------------------------------------------------------------------
"""

import re
from fuzzywuzzy import fuzz


class TextManager:
    """
    This class is encapsulates the logic required to clean the OCR output string produced from an image of an ID.
    It additionally encapsulates the logic required to isolate and retrieve the various ID field values to use
    for further processing.

    Attributes:
        _deplorables (list): A list of strings that contain characters that is to be filtered out from the OCR output
            string during string cleaning.

        fuzzy_min_ratio (int): The threshold ratio for a minimum, acceptable ratio of fuzziness when comparing
            two strings.

        _max_multi_line (int): Specifies the maximum number of lines that is to be extracted from fields that are noted
            as running onto multiple lines.
            e.g. Given OCR output such as :
                ...
                Names\n
                This is a long\n
                long list of names\n
                that spans multiple\n
                lines\n
                ...
                max_multi_line = 2, means that only the string:
                "This is a long list of names" is retrieved.

        match_contexts (list): A list of dictionaries that contain the contextual information used in the process of
            retrieving field values from the OCR output string.
            e.g. {
                    'field': 'surname',     // The field name - can be set to anything one desires.
                    'find': ['surname'],    // A list of strings to be used for matching field names
                                            // in the OCR output strings (used to know what to look for).
                    'text': True,           // Indicates if the field value is to be treated as alphanumeric or
                                            // just numeric (removes all text from field value if it's false).
                    'to_uppercase': False,  // Indicates that the retrieved field value must be converted to all
                                            // uppercase.
                    'multi_line': True,     // Indicates that the field value spans multiple lines.
                    'multi_line_end': [     // (Optional, unless multi_line is true) A list of strings specifying the
                                            // the next field name that indicates the end of the multi-line field
                                            // value.
                      'names', 'fore names'
                    ]
                }
    """
    def __init__(self, fuzzy_min_ratio=65):
        """
        Responsible for initialising the TextManager object.
        Args:
            fuzzy_min_ratio (int): The threshold value for the minimum ratio of fuzziness when comparing
            two strings.
        """
        # Specify initial list of undesirable characters.
        self._deplorables = ['_']
        # Specify initial list of contexts for string extraction when populating
        # the ID information dictionary to send as output.
        self.match_contexts = [{
            'field': 'identity_number',
            'find': ['id no', 'identity number'],
            'text': False,
            'multi_line': False
        }, {
            'field': 'surname',
            'find': ['surname'],
            'text': True,
            'to_uppercase': False,
            'multi_line': True,
            'multi_line_end': ['names', 'fore names']
        }, {
            'field': 'names',
            'find': ['names', 'fore names'],
            'text': True,
            'to_uppercase': False,
            'multi_line': True,
            'multi_line_end': ['sex']
        }, {
            'field': 'sex',
            'find': ['sex'],
            'text': True,
            'to_uppercase': True,
            'multi_line': False
        }, {
            'field': 'date_of_birth',
            'find': ['date of birth'],
            'text': True,
            'to_uppercase': False,
            'multi_line': False
        }, {
            'field': 'country_of_birth',
            'find': ['country of birth'],
            'text': True,
            'to_uppercase': True,
            'multi_line': False
        }, {
            'field': 'status',
            'find': ['status'],
            'text': True,
            'to_uppercase': False,
            'multi_line': False
        }, {
            'field': 'nationality',
            'find': ['nationality'],
            'text': True,
            'to_uppercase': True,
            'multi_line': False
        }]
        # Set the minimum ratio of fuzziness for fuzzy string matching used.
        self.fuzzy_min_ratio = fuzzy_min_ratio
        # Set the maximum number of lines for a multi line field in the id string to extract
        self._max_multi_line = 2

    def clean_up(self, in_string, deplorables=None, append_to_deplorables=True):
        """
        This function serves to receive an input string, clean it up through removing undesirable characters and
        unnecessary whitespace, and to return the cleaned string.

        Authors:
            Jan-Justin van Tonder

        Args:
            in_string (str): The input string that is to be cleaned.
            deplorables (list, Optional): A list of characters that are to be filtered from the input string.
            append_to_deplorables (bool, Optional): Indicates whether the list of exclusions should be appended to the
                existing list of exclusions in the class if true, if false it will overwrite the existing list.

        Returns:
            str: A string that has been stripped of undesirable characters and unnecessary whitespace.

        Raises:
            TypeError: If in_string is not a string.
            TypeError: If deplorables is not a list of strings.
            TypeError: If append_to_deplorables is not a bool.
        """
        # Check if the correct argument types have been passed in.
        if type(in_string) is not str:
            raise TypeError('Bad type for arg in_string - expected string. Received type ' + str(type(in_string)))
        if deplorables and (type(deplorables) is not list or type(deplorables[0]) is not str):
            raise TypeError('Bad type for arg deplorables - expected list of strings. Received type '
                            + str(type(deplorables)))
        if type(append_to_deplorables) is not bool:
            raise TypeError('Bad type for arg append_to_deplorables - expected bool. Received type '
                            + str(type(append_to_deplorables)))
        # Remove undesirable characters, spaces and newlines.
        compiled_deplorable_re = self._compile_deplorables(deplorables, append_to_deplorables)
        sanitised = re.sub(compiled_deplorable_re, '', in_string)
        # Remove empty lines in between text-filled lines.
        stripped_and_sanitised = re.sub(r'(\n\s*\n)', '\n', sanitised)
        # Remove multiple spaces before text-filled line.
        clean_text = re.sub(r'(\s*\n\s*)', '\n', stripped_and_sanitised)
        # Return cleaned text with additional stripping for good measure.
        return clean_text.strip()

    def _compile_deplorables(self, deplorables, append_to_deplorables):
        """
        This function is responsible for compiling a regex pattern that is used to filter out the characters that
        were deemed undesirable from a string.

        Authors:
            Jan-Justin van Tonder

        Args:
            deplorables (list): A list of characters that are to be filtered from the input string.
            append_to_deplorables (bool): Indicates whether the list of characters to be should be appended to the
                existing list of characters to be excluded in the class if true, if false it will overwrite the
                existing list.

        Returns:
            A compiled regex pattern used to match undesirable characters in a string.
        """
        # Append to existing list of undesirable characters if there is a given list of
        # undesirable characters and append_to_deplorables is true.
        if deplorables is not None and append_to_deplorables is True:
            self._deplorables += self._sanitise_deplorables(deplorables)
        # Overwrite existing list of undesirable characters if there is a given list of
        # undesirable characters and append_to_deplorables is false.
        elif deplorables is not None and append_to_deplorables is False:
            self._deplorables = deplorables
        # Define a class of characters that we wish to keep for the regex
        # that is to be compiled.
        reg_exp = r'[^\w\d\s-]'
        # If the existing list undesirable characters is not empty,
        # add the list of undesirable characters to the regex that is to be compiled.
        if self._deplorables:
            reg_exp += r'|[' + ''.join(self._deplorables) + ']'
        # Returned a compiled regular expression pattern to use for matching.
        return re.compile(reg_exp, re.UNICODE)

    def _sanitise_deplorables(self, deplorables):
        """
        This function serves as a helper function which sanitises a list of characters that is to be removed.
        It escapes or removes characters that may impede a regex pattern that is compiled within this class.

        Authors:
            Jan-Justin van Tonder

        Args:
            deplorables (list): A list of characters that are to be filtered from an input string.

        Returns:
            (list): A list of sanitised characters.
        """
        # List of sanitised deplorables
        sanitised = []
        for deplorable in deplorables:
            # Filter for valid inputs.
            if type(deplorable) is str and deplorable:
                # Escape ] and [ so as not to break the regex pattern.
                deplorable = re.sub(re.compile(r']'), '\]', deplorable)
                deplorable = re.sub(re.compile(r'\['), '\[', deplorable)
                sanitised.append(deplorable)
        return sanitised

    def dictify(self, id_string, barcode_data=None):
        """
        This function is responsible for generating a dictionary object containing the relevant ID information,
        such as names, surname, ID number, etc., from a given input string containing said relevant information.

        Authors:
            Jan-Justin van Tonder

        Args:
            id_string (str): A string containing some ID information.
            barcode_data (dict, Optional): A dictionary object containing information extracted from a barcode.

        Returns:
            (dict): A dictionary object containing the relevant, extracted ID information.

        Raises:
            TypeError: If id_string is not a string.
            TypeError: If barcode_data is not a dictionary.
        """
        # Check if arguments passed in are the correct type.
        if type(id_string) is not str:
            raise TypeError('Bad type for arg id_string - expected string. Received type ' + str(type(id_string)))
        if barcode_data and type(barcode_data) is not dict:
            raise TypeError('Bad type for arg id_string - expected dictionary. Received type '
                            + str(type(barcode_data)))
        # Given a string containing extracted ID text,
        # create a dictionary object and populate it with
        # relevant information from said text.
        id_info = {}
        # Check if barcode data, containing the id number, exists and
        # if so, save it and extract some relevant information from it.
        if barcode_data:
            id_info['identity_number'] = barcode_data['identity_number']
            self._id_number_information_extraction(id_info, barcode_data['identity_number'])
        # Attempt to populate id_info.
        self._populate_id_information(id_string, id_info)
        # Return the info that was found.
        return id_info

    def _id_number_information_extraction(self, id_info, id_number):
        """
        This function is responsible for extracting information from a given ID number and populating a given
        dictionary object with said information.

        Authors:
            Marno Hermann
            Stephan Nell
            Jan-Justin van Tonder

        Args:
            id_info (dict): A dictionary object containing extracted ID information.
            id_number (str): An ID number.

        Return:
            (dict): A dictionary object populated with information extracted from an ID number.
        """
        # Extract date of birth digits from ID number.
        yy = id_number[:2]
        mm = id_number[2:4]
        dd = id_number[4:6]
        # Populate id_info with date of birth.
        date_of_birth = str(yy) + "-" + str(mm) + "-" + str(dd)
        id_info['date_of_birth'] = date_of_birth
        # Extract gender digit from ID Number.
        gender_digit = id_number[6:7]
        # Populate id_info with gender info.
        id_info['sex'] = 'F' if gender_digit < '5' else 'M'
        # Extract status digit from ID Number.
        status_digit = id_number[10:11]
        # Populate id_info with status info.
        id_info['status'] = 'Citizen' if status_digit == '0' else 'Non Citizen'

    def _populate_id_information(self, id_string, id_info):
        """
        This function is responsible for populating a dictionary object with information that it is able to find
        and extract from a given string containing ID information.

        Authors:
            Jan-Justin van Tonder

        Args:
            id_string (str): A string containing some ID information.
            id_info (dict): A dictionary object used to house extracted ID information.
        """
        # Split the id_string on the newline character to generate a list.
        id_string_list = id_string.split('\n')
        # Attempt to retrieve matches.
        for match_context in self.match_contexts:
            # Extract desired field name from context as key.
            key = match_context['field']
            # Only retrieve information if it does not exist or it could not previously
            # be determined.
            if key not in id_info or not id_info[key]:
                id_info[key] = self._get_match(id_string_list, match_context)
                # If the ID number has been retrieved, use it to extract other useful
                # information.
                if key == 'identity_number' and id_info[key]:
                    self._id_number_information_extraction(id_info, id_info[key])

    def _get_match(self, id_string_list, match_context):
        """
        This function is responsible for searching through a list of lines from an ID string, and extracting the
        relevant ID information based on some context for extraction that is provided as input. Fuzzy string matching
        is performed on field names in order to extract field values. This process is assisted with a context that is
        is to be provided.

        Authors:
            Jan-Justin van Tonder

        Args:
            id_string_list (list): An ID string that has been broken down into a list of individual lines.
            match_context (dict): A dictionary object that provides context for the information that is to be extracted.

        Returns:
            (str): A string containing the extracted information, if a match was found.
            (None): If nothing was matched or an extracted value is an empty string.
        """
        best_match_ratio = self.fuzzy_min_ratio
        match = None
        skip_to_index = -1
        id_num_lines = len(id_string_list)
        # Iterate over the id_string list to find fuzzy matches.
        for current_index, current_line in enumerate(id_string_list):
            move_to_next_field = False
            if skip_to_index > current_index:
                continue
            for match_check in match_context['find']:
                # Is there a match?
                match_ratio = fuzz.token_set_ratio(current_line, match_check)
                if match_ratio >= best_match_ratio:
                    # Only interested in field value, not field name.
                    # e.g: Surname\n
                    #      Smith\n
                    #      ...
                    # ignore 'Surname' so as to be able to manually specify field name
                    # in the context settings.
                    best_match_ratio = match_ratio
                    # If we are looking for the ID number and the last few characters of the line
                    # are numeric, then the ID number is on the same line instead of a new line.
                    if match_context['field'] == 'identity_number' and current_line[-3:].isnumeric():
                        match = current_line
                    # The field value is on a seperate line or lines.
                    elif current_index + 1 < id_num_lines:
                        # Retrieve the field value on the very next line.
                        match = id_string_list[current_index + 1]
                        # If the field value exists over multiple lines.
                        if match_context['multi_line']:
                            # Determine the lower bound index for field values that span multiple lines.
                            lower_index = current_index + 2
                            if lower_index >= id_num_lines:
                                continue
                            # Determine the upper bound index for field values that span multiple lines.
                            upper_index = current_index + self._max_multi_line + 1
                            if upper_index > id_num_lines:
                                upper_index = id_num_lines
                            # Iterate ahead to retrieve the field value that spans over multiple lines.
                            for forward_index in range(lower_index, upper_index):
                                # For ech of the specified endpoints, check if the end of the field value has
                                # been reached.
                                for end_point in match_context['multi_line_end']:
                                    end_point_ratio = fuzz.token_set_ratio(end_point, id_string_list[forward_index])
                                    if end_point_ratio >= self.fuzzy_min_ratio:
                                        move_to_next_field = True
                                        skip_to_index = forward_index
                                        break
                                # Break out of the current loop if an endpoint was found.
                                if move_to_next_field:
                                    break
                                # Otherwise, add the line to the field value.
                                match += ' ' + id_string_list[forward_index].strip()
                    # Check if a match was found during the current iteration before processing further.
                    if not match:
                        continue
                    # Check if the field value is text and does not require to be converted to uppercase.
                    if match_context['text'] and not match_context['to_uppercase']:
                        # Convert to lowercase and capitilise the character of each new word.
                        match = match.lower().title()
                    # Check if conversion to uppercase was specified.
                    elif match_context['text'] and match_context['to_uppercase']:
                        match = match.upper()
                    # The field value is not text.
                    else:
                        # If not text, strip everything that is not a digit.
                        # This may be better for instances such as an ID number.
                        match = re.sub(r'[^\d]', '', match)
        # Final check to see if an empty string may be returned.
        if not match:
            return None
        # Otherwise return what we have found.
        return match
