"""Defines Building class.
"""

from eagers.class_definition.data_constructed import DataConstructed
from eagers.read.import_idf import import_idf
from eagers.read.import_sizes import import_sizes
from eagers.basic.file_handling import ensure_suffix


class Building(DataConstructed):
    def __init__(self,
            *args,
            name=None,
            site=None,
            sim_date=None,
            location=None,
            convection=None,
            schedule=None,
            holidays=None,
            material=None,
            window_material=None,
            surfaces=None,
            windows=None,
            doors=None,
            window_frames=None,
            zones=None,
            infiltration=None,
            mixing=None,
            occupancy=None,
            lighting_internal=None,
            plug_load=None,
            gas_load=None,
            exterior=None,
            cases=None,
            walk_ins=None,
            racks=None,
            water_use=None,
            hvac=None,
            air_demand_nodes=None,
            air_demand_equip=None,
            air_supply_nodes=None,
            air_supply_equip=None,
            plant_loop=None,
            plant_demand_nodes=None,
            plant_demand_equip=None,
            plant_supply_nodes=None,
            plant_supply_equip=None,
            pump=None,
            chiller=None,
            boiler=None,
            humidifiers=None,
            unitary_heat_cool=None,
            cooling_tower=None,
            water_heater=None,
            controller=None,
            manager=None,
            zone_controls=None,
            thermostat=None,
            setpoints=None,
            unitary_sys=None,
            fans=None,
            curves=None,
            coils_cooling=None,
            coils_heating=None,
            ground_temperatures=None,
            water_main_temperature=None,
            impact_factor=None,
            ctf=None,
            **kwargs,
            ):
        super().__init__(*args, **kwargs)
        self.name = name
        self.site = site
        self.sim_date = sim_date
        self.location = location
        self.convection = convection
        self.schedule = schedule
        self.holidays = holidays
        self.material = material
        self.window_material = window_material
        self.surfaces = surfaces
        self.windows = windows
        self.doors = doors
        self.window_frames = window_frames
        self.zones = zones
        self.infiltration = infiltration
        self.mixing = mixing
        self.occupancy = occupancy
        self.lighting_internal = lighting_internal
        self.plug_load = plug_load
        self.gas_load = gas_load
        self.exterior = exterior
        self.cases = cases
        self.walk_ins = walk_ins
        self.racks = racks
        self.water_use = water_use
        self.hvac = hvac
        self.air_demand_nodes = air_demand_nodes
        self.air_demand_equip = air_demand_equip
        self.air_supply_nodes = air_supply_nodes
        self.air_supply_equip = air_supply_equip
        self.plant_loop = plant_loop
        self.plant_demand_nodes = plant_demand_nodes
        self.plant_demand_equip = plant_demand_equip
        self.plant_supply_nodes = plant_supply_nodes
        self.plant_supply_equip = plant_supply_equip
        self.pump = pump
        self.chiller = chiller
        self.boiler = boiler
        self.humidifiers = humidifiers
        self.unitary_heat_cool = unitary_heat_cool
        self.cooling_tower = cooling_tower
        self.water_heater = water_heater
        self.controller = controller
        self.manager = manager
        self.zone_controls = zone_controls
        self.thermostat = thermostat
        self.setpoints = setpoints
        self.unitary_sys = unitary_sys
        self.fans = fans
        self.curves = curves
        self.coils_cooling = coils_cooling
        self.coils_heating = coils_heating
        self.ground_temperatures = ground_temperatures
        self.water_main_temperature = water_main_temperature
        self.impact_factor = impact_factor
        self.ctf = ctf

    @classmethod
    def from_file(cls, filename):
        """Returns a Building object using data read from IDF and EIO
        files with the same name.
        """
        building = cls(**import_idf(ensure_suffix(filename, '.idf')))
        return import_sizes(ensure_suffix(filename, '.eio'), building)

    @classmethod
    def from_energyplus(cls, filename):
        """More obvious name for from_file() method."""
        return cls.from_file(filename)
