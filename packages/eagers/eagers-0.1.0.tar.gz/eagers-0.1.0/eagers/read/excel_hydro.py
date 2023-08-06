"""Excel interface for hydro functionality.
"""
import datetime

from .excel_interface import BaseTemplateReader


class HydroTemplateReader(BaseTemplateReader):
    """Hydro template reader class."""

    _default_filename = 'hydro_template'
    _sheet_properties = {
        'Fossil': dict(
            read_method='_read_fossil_sheet',
        ),
        'Utilities': dict(
            read_method='_read_utilities_sheet',
        ),
        'Network': dict(
            read_method='_read_network_sheet',
        ),
        'Hydroelectric': dict(
            read_method='_read_hydroelectric_sheet',
        ),
        'Inflows': dict(
            read_method='_read_inflows_sheet',
        ),
        'Outflows': dict(
            read_method='_read_outflows_sheet',
        ),
    }

    @classmethod
    def _read_fossil_sheet(cls, ws):
        linelimits = 100
        
        header = [cell.value for cell in ws[1]]

        gens = []
           
        for row in ws.iter_rows(min_row=2, max_row=linelimits):
 
            gen = {}
            for key, cell in zip(header, row):
                gen[key] = cell.value
            gens.append(gen)

        return gens

    @classmethod
    def _read_utilities_sheet(cls, ws):
        linelimits = 100

        header = [cell.value for cell in ws[1]]

        gens = []

        for row in ws.iter_rows(min_row=2,max_row=linelimits):

            gen = {}
            for key, cell in zip(header, row):
                gen[key] = cell.value
                gens.append(gen)
        
        return gens

    @classmethod
    def _read_network_sheet(cls, ws):
        linelimits = 100
         
        header = [cell.value for cell in ws[1]]

        gens = []
        for row in ws.iter_rows(min_row=2,max_row=linelimits):
            gen = {}
            for key, cell in zip(header, row):
                gen[key] = cell.value
                gens.append(gen)

        return gens  

    @classmethod
    def _read_hydroelectric_sheet(cls, ws):
        linelimits = 100
         
        header = [cell.value for cell in ws[1]]

        gens = []
        for row in ws.iter_rows(min_row=2,max_row=linelimits):
            gen = {}
            for key, cell in zip(header, row):
                gen[key] = cell.value
                gens.append(gen)

        return gens

    @classmethod
    def _read_inflows_sheet(cls, ws):
        linelimits = 100
         
        header = [cell.value for cell in ws[1]]

        gens = []
        for row in ws.iter_rows(min_row=2,max_row=linelimits):
            gen = {}
            for key, cell in zip(header, row):
                gen[key] = cell.value
                gen = datetime.datetime.strptime(gen)
                gens.append(gen)

        return gens


    @classmethod
    def _read_outflows_sheet(cls, ws):
        linelimits = 100
         
        header = [cell.value for cell in ws[1]]

        gens = []
        for row in ws.iter_rows(min_row=2,max_row=linelimits):
            gen = {}
            for key, cell in zip(header, row):
                gen[key] = cell.value
                gen = datetime.datetime.strptime(gen)
                gens.append(gen)

        return gens
    
