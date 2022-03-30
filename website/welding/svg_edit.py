"""Testing editing svgs from python"""
import os
from dataclasses import dataclass

from website.settings import APP_STATICFILES_DIR


# from cairosvg import svg2pdf

@dataclass
class BaseMaterial:
    thickness: float
    group: str
    norm: str
    name: str


@dataclass
class FillerMaterial:
    norm: str
    # TODO: since filler material thickness is standardized consider creating an Enum
    thickness: float
    name: str
    dry: bool


class WPSMessages:
    """A data objet with the parameters needed to create a WPS"""
    filler_material: FillerMaterial
    base_material1: BaseMaterial
    base_material2: BaseMaterial

    def __init__(self, filler_material, base_material1, base_material2):
        self.filler_material = filler_material
        self.base_material1 = base_material1
        self.base_material2 = base_material2


def generate_svg(data: WPSMessages):
    """Generates a WPS with the given data."""
    with open(os.path.join(APP_STATICFILES_DIR, 'svg/wps-template.svg'), 'r', encoding='UTF-8') as file:
        dwg = file.read()

    dwg = dwg.replace('$nr_procedeu', '111') \
        .replace('$nume_material1', data.base_material1.name) \
        .replace('$nume_material2', data.base_material2.name) \
        .replace('$grosime1', str(data.base_material1.thickness)) \
        .replace('$grosime2', str(data.base_material2.thickness)) \
        .replace('$tip_imbinare', 'tip imbinare') \
        .replace('$pozitia', 'flat PA') \
        .replace('$uscare', 'N/A') \
        .replace('$norma1', 'N/A') \
        .replace('$tpr', '100')

    return dwg


def generate_pdf(data: WPSMessages):
    """Generates a WPS with the given data."""
    with open('../static/svg/test.svg', 'r', encoding='UTF-8') as file:
        dwg = file.read()

    with open('../static/svg/sect1.svg', 'r', encoding='UTF-8') as file:
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

    # svg2pdf(dwg, write_to='test2.pdf')
