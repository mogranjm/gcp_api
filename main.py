from pygoodwe import SingleInverter
from .src.config import INVERTER_ID, INVERTER_USER, INVERTER_PASS


def main():
    inv = SingleInverter(INVERTER_ID, INVERTER_USER, INVERTER_PASS)

    current_output_kw = inv.data['inverter']['output_power'] / 1000
    total_production_today = inv.data['inverter']['eday']
