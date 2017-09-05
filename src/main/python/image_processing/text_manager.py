"""
----------------------------------------------------------------------
Authors: Stephan Nell, Marno Hermann, Jan-Justin van Tonder
----------------------------------------------------------------------
This file contains the logic used to manage the text cleanup and
extraction of OCR output.
----------------------------------------------------------------------
"""

import re
from fuzzywuzzy import fuzz
from datetime import datetime
from hutts_utils.hutts_logger import logger


class TextManager:
    """
    This class is encapsulates the logic required to clean the OCR output string produced from an image of an ID.
    It additionally encapsulates the logic required to isolate and retrieve the various ID field values to use
    for further processing.

    Attributes:
        deplorables (list): A list of strings that contain characters that is to be filtered out from the OCR output
            string during string cleaning.
        match_contexts (list): A list of dictionaries that contain the contextual information used in the process of
            retrieving field values from the OCR output string.
            e.g. {
                    'field': 'surname',     // The field name - can be set to anything one desires.
                    'find': ['surname'],    // A list of strings to be used for matching field names
                                            // in the OCR output strings (used to know what to look for).
                    'field_type': True,     // Indicates if the field value is to be treated as alphanumeric or
                                            // just numeric or just alphabetical characters
                                            // (e.g. indicates that all numbers from field value should be removed
                                            //  if the field type is TEXT_ONLY).
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
    def __init__(self):
        """
        Responsible for initialising the TextManager object.
        """
        # Logging for debugging purposes.
        logger.debug('Initialising TextManager...')
        # Specify initial list of undesirable characters.
        self._deplorables = ['_']
        # Specify initial list of contexts for string image_processing when populating
        # the ID information dictionary to send as output.
        self.match_contexts = [{
            'field': 'identity_number',
            'find': ['id no', 'identity number'],
            'field_type': FieldType.NUMERIC_ONLY,
            'multi_line': False
        }, {
            'field': 'surname',
            'find': ['surname'],
            'field_type': FieldType.TEXT_ONLY,
            'to_uppercase': False,
            'multi_line': True,
            'multi_line_end': ['names', 'fore names']
        }, {
            'field': 'names',
            'find': ['names', 'fore names'],
            'field_type': FieldType.TEXT_ONLY,
            'to_uppercase': False,
            'multi_line': True,
            'multi_line_end': ['sex', 'country of birth']
        }, {
            'field': 'sex',
            'find': ['sex'],
            'field_type': FieldType.TEXT_ONLY,
            'to_uppercase': True,
            'multi_line': False
        }, {
            'field': 'date_of_birth',
            'find': ['date of birth'],
            'field_type': FieldType.MIXED,
            'to_uppercase': False,
            'multi_line': False
        }, {
            'field': 'country_of_birth',
            'find': ['country of birth'],
            'field_type': FieldType.TEXT_ONLY,
            'to_uppercase': True,
            'multi_line': False
        }, {
            'field': 'status',
            'find': ['status'],
            'field_type': FieldType.TEXT_ONLY,
            'to_uppercase': False,
            'multi_line': False
        }, {
            'field': 'nationality',
            'find': ['nationality'],
            'field_type': FieldType.TEXT_ONLY,
            'to_uppercase': True,
            'multi_line': False
        }]

    def clean_up(self, in_string, deplorables=None):
        """
        This function serves to receive an input string, clean it up through removing undesirable characters and
        unnecessary whitespace, and to return the cleaned string.

        Authors:
            Jan-Justin van Tonder

        Args:
            in_string (str): The input string that is to be cleaned.
            deplorables (list, Optional): A list of characters that are to be filtered from the input string.

        Returns:
            str: A string that has been stripped of undesirable characters and unnecessary whitespace.

        Raises:
            TypeError: If in_string is not a string.
            TypeError: If deplorables is not a list of strings.
        """
        # Check if the correct argument types have been passed in.
        if type(in_string) is not str:
            raise TypeError(
                'Bad type for arg in_string - expected string. Received type "%s".' %
                type(in_string).__name__
            )
        if deplorables and (type(deplorables) is not list or type(deplorables[0]) is not str):
            raise TypeError(
                'Bad type for arg deplorables - expected list of strings. Received type "%s".' %
                type(deplorables).__name__
            )
        # Remove undesirable characters, spaces and newlines.
        compiled_deplorable_re = self._compile_deplorables(deplorables)
        sanitised = re.sub(compiled_deplorable_re, '', in_string)
        # Remove empty lines in-between text-filled lines.
        stripped_and_sanitised = re.sub(r'(\n\s*\n)', '\n', sanitised)
        # Remove multiple spaces before and after text-filled line.
        clean_text = re.sub(r'(\s*\n\s*)', '\n', stripped_and_sanitised)
        # Remove multiple spaces in-between text-filled line.
        clean_text = re.sub(r'( +)', ' ', clean_text)
        # Lastly, strip the trailing and leading spaces.
        clean_text = clean_text.strip()
        # Return cleaned text.
        return clean_text

    def _compile_deplorables(self, deplorables):
        """
        This function is responsible for compiling a regex pattern that is used to filter out the characters that
        were deemed undesirable from a string.

        Authors:
            Jan-Justin van Tonder

        Args:
            deplorables (list): A list of characters that are to be filtered from the input string.

        Returns:
            A compiled regex pattern used to match undesirable characters in a string.
        """
        # Append to existing list of undesirable characters if there is a given list of
        # undesirable characters
        if deplorables is not None:
            self._deplorables += self._sanitise_deplorables(deplorables)
        # Define a class of characters that we wish to keep for the regex
        # that is to be compiled.
        reg_exp = r'[^\w\d\s-]'
        # If the existing list of undesirable characters is not empty,
        # add the list of undesirable characters to the regex that is to be compiled.
        reg_exp += r'|[' + ''.join(self._deplorables) + ']'
        # Returned a compiled regular expression pattern to use for matching.
        return re.compile(reg_exp, re.UNICODE)

    @staticmethod
    def _sanitise_deplorables(deplorables):
        """
        This function serves as a helper function, which sanitises a list of characters that is to be removed.
        It escapes or removes characters that may impede a regex pattern that is compiled within this class.

        Authors:
            Jan-Justin van Tonder

        Args:
            deplorables (list): A list of characters that are to be filtered from an input string.

        Returns:
            (list): A list of sanitised characters.

        Raises:
            TypeError: If deplorables is not a list of strings.
        """
        # List of sanitised deplorables
        sanitised = []
        for deplorable in deplorables:
            # Filter for valid inputs.
            if type(deplorable) is str and deplorable:
                # Escape ], [, - and ^ so as not to break the regex pattern.
                deplorable = re.sub(re.compile(r']'), '\]', deplorable)
                deplorable = re.sub(re.compile(r'\['), '\[', deplorable)
                deplorable = re.sub(re.compile(r'-'), '\-', deplorable)
                deplorable = re.sub(re.compile(r'^'), '\^', deplorable)
                sanitised.append(deplorable)
            else:
                raise TypeError(
                    'Bad type for arg deplorables - expected list of strings. Received type "%s".' %
                    type(deplorables).__name__
                )
        return sanitised

    def dictify(self, id_string, barcode_data=None, fuzzy_min_ratio=65, max_multi_line=2):
        """
        This function is responsible for generating a dictionary object containing the relevant ID information,
        such as names, surname, ID number, etc., from a given input string containing said relevant information.

        Authors:
            Jan-Justin van Tonder

        Args:
            id_string (str): A string containing some ID information.
            barcode_data (dict, Optional): A dictionary object containing information extracted from a barcode.
            fuzzy_min_ratio (int): The threshold ratio for a minimum, acceptable ratio of fuzziness when comparing
                two strings.
            max_multi_line (int): Specifies the maximum number of lines that is to be extracted from fields that are
                noted as running onto multiple lines.

        Returns:
            (dict): A dictionary object containing the relevant, extracted ID information.

        Raises:
            TypeError: If id_string is not a string.
            TypeError: If barcode_data is not a dictionary.
        """
        # Check if arguments passed in are the correct type.
        if type(id_string) is not str:
            raise TypeError(
                'Bad type for arg id_string - expected string. Received type "%s".' %
                type(id_string).__name__
            )
        if barcode_data and type(barcode_data) is not dict:
            raise TypeError(
                'Bad type for arg barcode_data - expected dictionary. Received type "%s".' %
                type(barcode_data).__name__
            )
        # Given a string containing extracted ID text,
        # create a dictionary object and populate it with
        # relevant information from said text.
        id_info = {}
        # Attempt to populate id_info.
        logger.debug('Extracting details from the given text string...')
        self._populate_id_information(id_string, id_info, fuzzy_min_ratio, max_multi_line)
        # Check if barcode data, containing the id number, exists and
        # if so, save it and extract some relevant information from it.
        # It should overwrite any existing fields that can be extracted from the id number, since
        # the information embedded within the id number is more reliable, at least theoretically.
        if barcode_data:
            logger.debug('Extracting details from barcode data...')
            id_info['identity_number'] = barcode_data['identity_number']
            self._id_number_information_extraction(id_info, barcode_data['identity_number'])
        # Perform some custom post-processing on the information that was extracted.
        logger.debug('Standardising some field values...')
        self._post_process(id_info)
        # Return the info that was found.
        return id_info

    @staticmethod
    def _id_number_information_extraction(id_info, id_number):
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
        date_of_birth = '%s-%s-%s' % (yy, mm, dd)
        id_info['date_of_birth'] = date_of_birth
        # Extract gender digit from ID Number.
        gender_digit = id_number[6:7]
        # Populate id_info with gender info.
        # Currently, the genders on South African IDs are binary, meaning an individual is
        # either male or female.
        id_info['sex'] = 'F' if gender_digit < '5' else 'M'
        # Extract status digit from ID Number.
        status_digit = id_number[10:11]
        # Populate id_info with status info.
        id_info['status'] = 'Citizen' if status_digit == '0' else 'Non Citizen'

    def _populate_id_information(self, id_string, id_info, fuzzy_min_ratio, max_multi_line):
        """
        This function is responsible for populating a dictionary object with information that it is able to find
        and extract from a given string containing ID information.

        Authors:
            Jan-Justin van Tonder

        Args:
            id_string (str): A string containing some ID information.
            id_info (dict): A dictionary object used to house extracted ID information.
            fuzzy_min_ratio (int): The threshold ratio for a minimum, acceptable ratio of fuzziness when comparing
                two strings.
            max_multi_line (int): Specifies the maximum number of lines that is to be extracted from fields that are
                noted as running onto multiple lines.
        """
        # Split the id_string on the newline character to generate a list.
        id_string_list = id_string.split('\n')
        # Attempt to retrieve matches.
        for match_context in self.match_contexts:
            # Logging for debugging purposes.
            logger.debug('Searching for field value for "%s"' % match_context['field'])
            # Extract desired field name from context as key.
            key = match_context['field']
            # Only retrieve information if it does not exist or it could not previously
            # be determined.
            id_info[key] = self._get_match(id_string_list, match_context, fuzzy_min_ratio, max_multi_line)
            # Logging for debugging purposes.
            logger.debug('%s value found for "%s"' % ('Field' if id_info[key] else 'No field', match_context['field']))
        # If the ID number has been retrieved, use it to extract other useful information.
        # It should overwrite any existing fields that can be extracted from the id number, since
        # the information embedded within the id number is more reliable, at least theoretically.
        if id_info['identity_number']:
            self._id_number_information_extraction(id_info, id_info['identity_number'])

    @staticmethod
    def _get_match(id_string_list, match_context, fuzzy_min_ratio, max_multi_line):
        """
        This function is responsible for searching through a list of lines from an ID string, and extracting the
        relevant ID information based on some context for image_processing that is provided as input. Fuzzy string
        matching is performed on field names in order to extract field values. This process is assisted with a context
        that is is to be provided.

        Authors:
            Jan-Justin van Tonder

        Args:
            id_string_list (list): An ID string that has been broken down into a list of individual lines.
            match_context (dict): A dictionary object that provides context for the information that is to be extracted.
            fuzzy_min_ratio (int): The threshold ratio for a minimum, acceptable ratio of fuzziness when comparing
                two strings.
            max_multi_line (int): Specifies the maximum number of lines that is to be extracted from fields that are
                noted as running onto multiple lines.
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

        Returns:
            (str): A string containing the extracted information, if a match was found.
            (None): If nothing was matched or an extracted value is an empty string.
        """
        best_match_ratio = fuzzy_min_ratio
        match = None
        skip_to_index = -1
        id_num_lines = len(id_string_list)
        # Iterate over the id_string list to find fuzzy matches.
        for current_index, current_line in enumerate(id_string_list):
            move_to_next_field = False
            # Check to see if we can jump ahead and ignore the current index.
            if skip_to_index > current_index:
                continue
            for match_check in match_context['find']:
                # Is there a match?
                match_ratio = fuzz.token_set_ratio(current_line, match_check)
                if match_ratio >= best_match_ratio:
                    best_match_ratio = match_ratio
                    # If we are looking for the ID number and the last few characters of the line
                    # are numeric, then the ID number is on the same line instead of a new line.
                    if match_context['field'] == 'identity_number' and current_line[-3:].isnumeric():
                        match = current_line
                    # The field value is on a separate line or separate lines.
                    elif current_index + 1 < id_num_lines:
                        # We are only interested in field value, not field name.
                        # e.g: Surname\n
                        #      Smith\n
                        #      ...
                        # ignore 'Surname' so as to be able to manually specify field name
                        # in the context settings.
                        # Retrieve the field value on the very next line.
                        match = id_string_list[current_index + 1]
                        # If the field value exists over multiple lines.
                        if match_context['multi_line']:
                            # Determine the lower bound index for field values that span multiple lines.
                            lower_index = current_index + 2
                            if lower_index >= id_num_lines:
                                # There is nothing to find in this case.
                                continue
                            # Determine the upper bound index for field values that span multiple lines.
                            upper_index = current_index + max_multi_line + 1
                            if upper_index > id_num_lines:
                                # Don't go out of bounds.
                                upper_index = id_num_lines
                            # Iterate ahead to retrieve the field value that spans over multiple lines.
                            for forward_index in range(lower_index, upper_index):
                                # For ech of the specified endpoints, check if the end of the field value has
                                # been reached.
                                for end_point in match_context['multi_line_end']:
                                    end_point_ratio = fuzz.token_set_ratio(end_point, id_string_list[forward_index])
                                    if end_point_ratio >= fuzzy_min_ratio:
                                        move_to_next_field = True
                                        skip_to_index = forward_index
                                        break
                                # Break out of the current look ahead loop if an endpoint was found.
                                if move_to_next_field:
                                    break
                                # Otherwise, add the line to the field value.
                                match += ' %s' % id_string_list[forward_index].strip()
                    # Check if a legitimate match was found before proceeding.
                    if not match:
                        continue
                    # If the field value should only be text, strip everything that is numeric.
                    if match_context['field_type'] == FieldType.TEXT_ONLY:
                        match = re.sub(r'[^\w\s-]', '', match)
                    # If the field value ought to be numeric only, strip everything that is not numeric.
                    elif match_context['field_type'] == FieldType.NUMERIC_ONLY:
                        match = re.sub(r'[^\d]', '', match)
                    # Check if conversion to uppercase was specified.
                    if 'to_uppercase' in match_context and match_context['to_uppercase']:
                        match = match.upper()
                    # If the field value does not require to be converted to uppercase.
                    elif 'to_uppercase' in match_context and not match_context['to_uppercase']:
                        # Convert to lowercase and capitalise the character of each new word.
                        match = match.lower().title()
        # Final check to see if an empty string ('', not None) is the match found, return None if this is the case.
        if not match:
            return None
        # Otherwise return what we have found.
        return match

    @staticmethod
    def _post_process(id_info):
        """
        A function for standardising and formatting id_info values for custom, or future, use.

        Authors:
            Jan-Justin van Tonder

        Args:
            id_info (dict): A dictionary object used to house extracted ID information.

        Returns:
            (dict): The original id_info, with some customised field values.
        """
        if 'date_of_birth' in id_info and id_info['date_of_birth']:
            # Due to the preference of extracting the date of birth from the id number as opposed to
            # the ocr output, there tends to be a discrepancy in the date format retrieved, therefore,
            # standardise it for future use.
            try:
                # Attempt to parse the different dates that could appear for formatting.
                current_date_of_birth = re.sub(' ', '', id_info['date_of_birth'])
                # If the current date contains a '-', then it was extracted from the id number, therefore,
                # parse it in the format 'YY-MM-DD'
                if '-' in current_date_of_birth:
                    standardised_date_of_birth = datetime.strptime(current_date_of_birth, '%y-%m-%d')
                # Otherwise it was extracted from the OCR output, therefore, parse it in the
                # format 'DD MMM YYYY'
                else:
                    standardised_date_of_birth = datetime.strptime(current_date_of_birth, '%d%b%Y')
                # Standardise the date by formatting it according to ISO date format standard,
                # which is 'YYYY-MM-DD'
                id_info['date_of_birth'] = datetime.strftime(standardised_date_of_birth, '%Y-%m-%d')
            except ValueError:
                # Could not parse the date so log and keep it as is.
                logger.warning('Could not parse date "%s" for formatting. Keeping date as is.')
        if 'sex' in id_info and id_info['sex']:
            # Generally, South African IDs indicate sex with a single character, however, our use requires
            # the full, explicit word for the individual's sex.
            id_info['sex'] = 'Female' if id_info['sex'] == 'F' else 'Male'


class FieldType(enumerate):
    """
    An enumerator used to specify the field type for extracted id information.
    """
    TEXT_ONLY = 1
    NUMERIC_ONLY = 2
    MIXED = 3
