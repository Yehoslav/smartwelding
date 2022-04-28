import json


class Steel:

    def __init__(self, steel_data: dict):
        self.C = steel_data['C'] if 'C' in steel_data else 0
        self.Si = steel_data['Si'] if 'Si' in steel_data else 0
        self.Mn = steel_data['Mn'] if 'Mn' in steel_data else 0
        self.Ni = steel_data['Ni'] if 'Ni' in steel_data else 0
        self.P  = steel_data['P'] if 'S' in steel_data else 0
        self.S  = steel_data['S'] if 'S' in steel_data else 0
        self.Cr = steel_data['Cr'] if 'Cr' in steel_data else 0
        self.Mo = steel_data['Mo'] if 'Mo' in steel_data else 0
        self.V  = steel_data['V'] if 'V' in steel_data else 0
        self.N = steel_data['N'] if 'N' in steel_data else 0
        self.Nb = steel_data['Nb'] if 'Nb' in steel_data else 0
        self.Ti = steel_data['Ti'] if 'Ti' in steel_data else 0
        self.Al = steel_data['Al'] if 'Al' in steel_data else 0
        self.Cu = steel_data['Cu'] if 'Cu' in steel_data else 0

    def __str__(self):
        return f"{self.C}%C, {self.Mn}%Mn, {self.Cr}%Cr, {self.Mo}%Mo," + \
               f"{self.V}%V, {self.Ni}%Ni, {self.Cu}%Cu"


def ceiiw(steel: Steel):
    return steel.C + steel.Mn / 6 + (steel.Cr + steel.Mo + steel.V) / 5 + (steel.Ni + steel.Cu) / 15

def ceiiw_formula(steel: Steel) -> str:
    return f"{steel.C}%C + {steel.Mn}%Mn/6 + ({steel.Cr}%Cr + {steel.Mo}%Mo + {steel.V}%V)/5" + \
           f"+ ({steel.Ni}%Ni + {steel.Cu}%Cu)/15"

def cewes(steel: Steel) -> float:
    return steel.C + steel.Si/24 + steel.Mn/6 + steel.Ni/40 + steel.Cr/5 + steel.Mo/4 + steel.V/14


def main():
    steel_data = {'C': 5, 'Ni':2}
    steel = Steel(steel_data)

    print(round(ceiiw(steel), 2))
    print(round(cewes(steel), 2))


if __name__ == '__main__':
    main()
