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

@dataclass
class Gas:
    gas_type: str
    debit: float


@dataclass
class HeatTreatment:
    preheat: int
    postheat: int


@dataclass
class Refractary:
    electrode_type: str
    diameter: float


@dataclass
class ProjectData:
    joint_type: str
    position: str
    # TODO: Create and enum for the Welding Processes
    w_process: str


class WPSData:
    """A data objet with the parameters needed to create a WPS"""
    project_data: ProjectData
    filler_material: FillerMaterial
    base_material1: BaseMaterial
    base_material2: BaseMaterial
    gas_cover: Gas
    gas_root: Gas
    heat_tratment: HeatTreatment
    refractary: Refractary

    def __init__(self,
                 filler_material,
                 base_material1,
                 base_material2,
                 refractary,
                 gas_cover,
                 gas_root,
                 project_data,
                 heat_tratment):
        self.filler_material = filler_material
        self.base_material1 = base_material1
        self.base_material2 = base_material2
        self.gas_cover = gas_cover
        self.gas_root = gas_root
        self.heat_tratment = heat_tratment
        self.refractary = refractary
        self.project_data = project_data


def generate_svg(data: WPSData):
    """Generates a WPS with the given data."""
    with open(os.path.join(APP_STATICFILES_DIR, 'svg/wps-template.svg'), 'r', encoding='UTF-8') as file:
        dwg = file.read()

    dwg = dwg.replace('$nr_procedeu', data.project_data.w_process) \
        .replace('$marca_mat_adaos', data.filler_material.name) \
        .replace('$norma_mat_adaos', data.filler_material.norm) \
        .replace('$dim_mat_adaos', str(data.filler_material.thickness)) \
        .replace('$nume_material1', data.base_material1.name) \
        .replace('$nume_material2', data.base_material2.name) \
        .replace('$grosime1', str(data.base_material1.thickness)) \
        .replace('$grosime2', str(data.base_material2.thickness)) \
        .replace('$tip_imbinare',data.project_data.joint_type) \
        .replace('$pozitia', data.project_data.position) \
        .replace('$uscare', "Da" if data.filler_material.dry else "Fara") \
        .replace('$norma1', data.base_material1.norm) \
        .replace('$norma2', data.base_material2.norm) \
        .replace('$grupa1', data.base_material1.group) \
        .replace('$grupa2', data.base_material2.group) \
        .replace('$tip_el_nefuzibil', data.refractary.electrode_type) \
        .replace('$diam_el_nefuzibil', data.refractary.diameter) \
        .replace('$gaz_protectie', data.gas_cover.gas_type) \
        .replace('$deb_gaz_protectie', data.gas_cover.debit) \
        .replace('$gaz_radacina', data.gas_root.gas_type) \
        .replace('$deb_gaz_radacina', data.gas_root.debit) \
        .replace('$t_strat', data.heat_tratment.postheat) \
        .replace('$tpr', data.heat_tratment.preheat)

    return dwg


def generate_pdf(data: WPSData):
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
