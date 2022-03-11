"""Testing editing svgs from python"""
import os

from cairosvg import svg2pdf

from website.settings import WELDING


class WPSMessages:
    """A data objet with the parameters needed to create a WPS"""
    thickness: str
    bevel: str
    joint: str
    material: str
    preparation: str

    def __init__(self, messages: dict | None):
        if messages is not None:
            self.set_attributes(messages)
        else:
            self.set_attributes(
                {
                    'thickness': 'th',
                    'bevel': '',
                    'joint': '',
                    'material': '',
                    'preparation': ''
                }
            )

    def set_attributes(self, attributes: dict):
        self.thickness = attributes['thickness']
        self.bevel = attributes['bevel']
        self.joint = attributes['joint']
        self.material = attributes['material']
        self.preparation = attributes['preparation']

    def __str__(self):
        return f"thickness: {self.thickness}\nbevel: {self.bevel}"


def generate_svg(data: WPSMessages):
    """Generates a WPS with the given data."""
    with open(os.path.join(WELDING, 'test.svg'), 'r', encoding='UTF-8') as file:
        dwg = file.read()

    dwg = dwg.replace('$manuf', 'Wojciech Grzegorczyk') \
        .replace('$material', data.material) \
        .replace('$joint_nr', 'P1') \
        .replace('$joint_type', data.joint) \
        .replace('$thickness', data.thickness) \
        .replace('$position', 'flat PA') \
        .replace('$out_diameter', '---') \
        .replace('$clean', data.preparation) \
        .replace('$sealing_run', 'Single-side welding')

    return dwg


def generate_pdf(data: WPSMessages):
    """Generates a WPS with the given data."""
    with open('test.svg', 'r', encoding='UTF-8') as file:
        dwg = file.read()

    with open('sect1.svg', 'r', encoding='UTF-8') as file:
        sect = file.read()

    dwg = dwg.replace('$manuf', 'Wojciech Grzegorczyk') \
        .replace('$material', data.material) \
        .replace('$joint_nr', 'P1') \
        .replace('$joint_type', data.joint) \
        .replace('$thickness', data.thickness) \
        .replace('$position', 'flat PA') \
        .replace('$out_diameter', '---') \
        .replace('$clean', data.preparation) \
        .replace('$sealing_run', 'Single-side welding') \
        .replace('<!-- img -->', sect)

    with open('test2.svg', 'w', encoding='UTF-8') as file:
        file.write(dwg)

    svg2pdf(dwg, write_to='test2.pdf')
