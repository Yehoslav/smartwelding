"""
    A file containing functions for apropiate standards that will decode the
    electrode notation.
"""
import re
import logging
import math
import json
import os
from website.settings import WELDING
from enum import Enum


# Logging
FMT = "[{asctime} {levelname:^9}] {name}: {message}"
FORMATS = {
    logging.DEBUG: FMT,
    logging.INFO: f'\33[36m{FMT}\33[0m',
    logging.WARNING: f'\33[33m{FMT}\33[0m',
    logging.ERROR: f'\33[31m{FMT}\33[0m',
    logging.CRITICAL: f'\33[1m\33[31m{FMT}\33[0m',
}


class CustomFormatter(logging.Formatter):
    """A custom formatter for the logger."""

    def format(self, record):
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style='{')
        return formatter.format(record)


handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler])
logger = logging.getLogger(__name__)


class ISOError(TypeError):
    """Custom error"""


class TooManyArgumensError(TypeError):
    """Custom error"""


class SubType(Enum):
    """An Enumeration class holding indices for the two aproaches to clasify the
electrodes"""
    A = 0
    B = 1


def parser(symbol: str, pattern: str, list_of_values: dict) -> dict:
    # create the list of allowed symbols
    code_symbols = "frjcipnhg"
    special_symbols = "?123456789-"
    # Special symbols:
    #     ?       optional
    #     -       range
    #     0..9    digits deinging a range

    pattern = pattern.lower()
    # create the dictionary to hold the final result
    elements = {}
    # parse the pattern
    last_code_simbol: str
    last_symbol: str = ''

    for char in pattern:
        logger.debug(f'Parsing at: {char}')
        if char in code_symbols:
            if char not in elements:
                elements[char] = {
                    'value': '',
                    'count': 1,
                    'is_optional': False,
                    'is_variable': False,
                }
                last_code_simbol = char
            else:
                elements[char]['count'] += 1

        elif char in special_symbols:
            logger.debug('Checking a special symbol.')
            if char == '':
                raise Exception(
                    'Special symbols canot be on the beggining of the pattern'
                )

            match char:
                case '?':
                    if last_symbol == '-':
                        raise Exception('\'?\' cannot be part of a range.')
                    elements[last_code_simbol]['is_optional'] = True

                case char if char.isdigit():
                    count = elements[last_code_simbol]['count']
                    int_char = int(char)
                    logger.debug(f'{count=} --- {int_char=}')
                    if int_char * 10 <= count and int_char != 0:
                        raise ValueError(
                            'The second element in a range ' +
                            'should be greater than the first one'
                        )
                    elements[last_code_simbol]['count'] = int_char \
                        if count < 10 else count + int_char

                case '-':
                    if last_symbol in code_symbols:
                        count = elements[last_code_simbol]['count']
                        if count / 10 > 0.9:
                            # TODO make a custom exception
                            raise Exception(
                                'range supported only for digits between 0-9')
                        elements[last_code_simbol]['is_variable'] = True
                        elements[last_code_simbol]['count'] *= 10
                    else:
                        # TODO make a custom exception
                        raise Exception('A range can be started only a digit')

        if last_code_simbol == char:
            logger.debug(f'The element {char} has the following properties ' +
                         f'{elements[last_code_simbol]}')

    # parsing the given iso symbol
    parts = {}
    for code in elements:
        start_pattern_range = math.floor(elements[code]['count'] / 10)
        end_pattern_range = elements[code]['count'] % 10
        value = ''
        filtered_list = list_of_values[code]
        for i in range(end_pattern_range):
            if len(symbol) == 0:
                break
            value += symbol[0]
            # filtering the list_of_values until only one value is left
            # than if the value is variable than break the loop
            filtered_list = [val for val in filtered_list if value in val]
            logger.debug(f'The filtered_list for loop {i} is {filtered_list}')
            if (elements[code]['is_variable'] or elements[code]['is_optional']) \
                    and len(filtered_list) == 0:
                value = value[:-1]
                break
            symbol = symbol[1:]

        logger.info(f'Adding new value "{value}" to {code}')
        if value in list_of_values[code] or (elements[code]['is_optional'] and value == ''):
            elements[code]['value'] = value
        else:
            raise ISOError(
                "The electrode is not conformig to the ISO2560 standard")

    return_elemetns = {key: val['value'] for key, val in elements.items()}
    return return_elemetns


def get_json_file(path: str) -> dict:
    # TODO Use Path to build the path and see if the path exists
    path = os.path.join(WELDING, path)
    with open(path, 'r', encoding='UTF-8') as f:
        json_dict = json.load(f)
    return json_dict


class ISO2560:
    pattern_a = r'FRRJC1-5?I1-2N?P?H2-3?'
    pattern_b = r'FRRIIC1-5?P1-2?J?H2-3?'
    # TODO: Generate the valuelists from the json
    value_list_a = {
        'f': ['E'],
        'r': ['35', '38', '42', '46', '50', ],
        'j': ['Z', 'A', '0', '1', '2', '3', '4', '5', '6', ],
        'c': ['Mo', 'MnMo', '1Ni', 'Mn1Ni', '2Ni', 'Mn2Ni', '3Ni',
              '1NiMo', 'Z'],
        'i': ['A', 'B', 'C', 'R', 'RR', 'RC', 'RB', 'RA', ],
        'n': ['1', '2', '3', '4', '5', '6', '7', '8', ],
        'p': ['1', '2', '3', '4', '5', ],
        'h': ['H5', 'H10', 'H15'],
    }

    value_list_b = {
        'f': ['E'],
        'r': ['43', '49', '55', '57', ],
        'i': ['03', '10', '11', '12', '13', '14', '15', '16', '18',
              '19', '20', '24', '27', '28', '40', '45', '48', ],
        'c': ['-1', '-P1', '-1M3', '-3M2', '-3M3', '-N1', '-N2', '-N3',
              '-3N3', '-N5', '-N7', '-N13', '-N2M3', '-NC', '-CC',
                      '-NCC', '-NCC1', '-NCC2', '-G'],
        'p': ['A', 'P', 'AP'],
        'j': ['U'],
        'h': ['H5', 'H10', 'H15'],
    }

    a_keys = {'strength': [
        """{1:^6}: Yield strength    = {2} N/mm^2 \n\
                \r{0:<6}  Ultimate strength = {3} - {4} N/mm^2\n\
                \r{0:<6}  Elongation        = {5} %
                """,
        lambda str_values: (
            str_values[0],
            str_values[1][0],
            str_values[1][1],
            str_values[2])
    ],
        'impact': [
        "\r{1:^6}: Guaranteed impact strength of 47 J at {2}°C",
        lambda x: [x, ],
    ],
        'chemical_composition': [
        """
                \r{1:^6}: {2}%Mn \n\
                \r{0:<6}  {3}%Mo \n\
                \r{0:<6}  {4}%Ni
                """,
        lambda ch_value: (
            ch_value[0][1] if ch_value[0][0] == 0
            else f"{ch_value[0][0]} - {ch_value[0][1]}",
            ch_value[1][1] if ch_value[1][0] == 0
            else f"{ch_value[1][0]} - {ch_value[1][1]}",
            ch_value[2][1] if ch_value[2][0] == 0
            else f"{ch_value[2][0]} - {ch_value[2][1]}",
        )
    ],
        'covering': [
        "\r{1:^6}: {2}",
        lambda x: tuple([x]),
    ],
        'eff-and-current': [
        """
                \r{1:^6}: the nominal electrode efficiency is {2} \n\
                \r{0:<6}  welding can be done in {3}
                """,
        lambda eff_value: (
            f"< {eff_value[0][1]}" if eff_value[0][0] == 0
            else f"> {eff_value[0][0]}" if eff_value[0][1] == 0
            else f"{eff_value[0][0]} - {eff_value[0][1]}",
            eff_value[1],
        )
    ],
        'position': [
        "\r{1:^6}: the welding positions are {2}",
        lambda x: tuple([', '.join(x)]),
    ],
    }

    b_keys = {'strength': [
        "{1:^6}: Ultimate strength = {2} N/mm^2 \n",
        lambda str_values: (str_values, )
    ],
        'covering': [
        "\r{1:^6}: {2}, {3}, using {4} \n",
        lambda covering: (
            covering[0],
            covering[1],
            covering[2],
        ),
    ],
        'chemical_composition': [
        "\r{1:^6}: {2} \n",
        lambda ch_value: (
            ', '.join('%'.join([str(j), i])
                      for i, j in zip(*ch_value)),
        )
    ],
        'thermal_treatment': [
        "\r{1:^6}: {2} \n",
        lambda thermal: (thermal, ),
    ],
        'impact': [
        "\r{1:^6}: Guaranteed impact strength of {2}",
        lambda x: [x, ],
    ],
    }

    def create_response_a(self, values, subtype):
        iso2560 = get_json_file('iso2560.json')
        fields = []
        iso2560a = iso2560['A' if subtype == SubType.A else 'B']
        keys = self.a_keys if subtype == SubType.A else self.b_keys

        for key, value in zip(keys, list(values.values())[1:]):
            logger.debug(f'{key=}, {value=}')
            if value == '':
                value = 'nos'
            fields.append(
                keys[key][0].format(
                    ' ',
                    value,
                    *keys[key][1](iso2560a[key][value])
                )
            )

        return fields

    def decode(self, symbol: str, subtype: SubType):
        """Retruns an electrode object containing the information based on the given symbol."""
        # TODO create a pattern for each type of symbols
        # TODO create a custom regex parser
        symbol = ''.join(symbol.split(' '))
        pattern = self.pattern_a if subtype == SubType.A else self.pattern_b
        value_list = self.value_list_a if subtype == SubType.A \
            else self.value_list_b
        val = parser(symbol, pattern, value_list)
        response = ''.join(self.create_response_a(val, subtype))
        return response
