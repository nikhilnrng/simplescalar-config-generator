#!/usr/bin/python

import math
import xlwings
from xlwings import Book

class Estimator(object):
    """Consolidates all Real Estimator Excel file reads and writes

    Real Estimator is used to obtain read and write port data, total bit
    configurations, and transistor and area counts. Some of the data from Real
    Estimator are used for the Cacti access time and latency calculations.

    The Estimator Class is used to open up the 'real_estimator.xlsx' file as
    long as it exists in the same directory, modify the Excel file, read any
    relevant results, and ultimately save the workbook.

    Attributes:
      xlw: An xlwings object
      wbk: A xlwings Book object
    """
    def __init__(self):
        """Init Estimator class attributes"""
        self.xlw = xlwings
        self.wbk = Book('real_estimator.xlsx')

    def configure_estimator_params(self, config):
        """Set all real estimator parameters from config

        Args:
          config: A Config object
        """
        self.xlw.sheets[0].activate()

        self.xlw.Range('B3').value = config.get_param('seed')
        self.xlw.Range('B4').value = config.get_param('fetch_ifqsize')
        self.xlw.Range('B5').value = config.get_param('fetch_mplat')
        self.xlw.Range('B6').value = config.get_param('bpred')
        self.xlw.Range('B7').value = config.get_param('bpred_bimod')
        self.xlw.Range('B8').value = config.get_param('bpred_2lev_l1size')
        self.xlw.Range('B9').value = config.get_param('bpred_2lev_l2size')
        self.xlw.Range('B10').value = config.get_param('bpred_2lev_hist_size')
        self.xlw.Range('B11').value = config.get_param('decode_width')
        self.xlw.Range('B12').value = config.get_param('issue_width')
        self.xlw.Range('B13').value = config.get_param('issue_inorder')
        self.xlw.Range('B14').value = config.get_param('issue_wrongpath')
        self.xlw.Range('B15').value = config.get_param('ruu_size')
        self.xlw.Range('B16').value = config.get_param('lsq_size')
        self.xlw.Range('B17').value = config.get_param('cache_dl1_nsets')
        self.xlw.Range('B18').value = config.get_param('cache_dl1_bsize')
        self.xlw.Range('B19').value = config.get_param('cache_dl1_assoc')
        self.xlw.Range('B20').value = config.get_param('cache_dl1_repl')
        self.xlw.Range('B21').value = config.get_param('cache_dl1lat')
        self.xlw.Range('B22').value = config.get_param('cache_dl2_nsets')
        self.xlw.Range('B23').value = config.get_param('cache_dl2_bsize')
        self.xlw.Range('B24').value = config.get_param('cache_dl2_assoc')
        self.xlw.Range('B25').value = config.get_param('cache_dl2_repl')
        self.xlw.Range('B26').value = config.get_param('cache_dl2lat')
        self.xlw.Range('B27').value = config.get_param('cache_il1_nsets')
        self.xlw.Range('B28').value = config.get_param('cache_il1_bsize')
        self.xlw.Range('B29').value = config.get_param('cache_il1_assoc')
        self.xlw.Range('B30').value = config.get_param('cache_il1_repl')
        self.xlw.Range('B31').value = config.get_param('cache_il1lat')
        self.xlw.Range('B32').value = config.get_param('cache_il2_nsets')
        self.xlw.Range('B33').value = config.get_param('cache_il2_bsize')
        self.xlw.Range('B34').value = config.get_param('cache_il2_assoc')
        self.xlw.Range('B35').value = config.get_param('cache_il2_repl')
        self.xlw.Range('B36').value = config.get_param('cache_il2lat')
        self.xlw.Range('B37').value = config.get_param('cache_flush')
        self.xlw.Range('B38').value = config.get_param('cache_icompress')
        self.xlw.Range('B39').value = config.get_param('mem_lat_first_chunk')
        self.xlw.Range('B40').value = config.get_param('mem_lat_inter_chunk')
        self.xlw.Range('B41').value = config.get_param('mem_width')
        self.xlw.Range('B42').value = config.get_param('tlb_itlb_nsets')
        self.xlw.Range('B43').value = config.get_param('tlb_itlb_bsize')
        self.xlw.Range('B44').value = config.get_param('tlb_itlb_assoc')
        self.xlw.Range('B45').value = config.get_param('tlb_itlb_repl')
        self.xlw.Range('B46').value = config.get_param('tlb_dtlb_nsets')
        self.xlw.Range('B47').value = config.get_param('tlb_dtlb_bsize')
        self.xlw.Range('B48').value = config.get_param('tlb_dtlb_assoc')
        self.xlw.Range('B49').value = config.get_param('tlb_dtlb_repl')
        self.xlw.Range('B50').value = config.get_param('tlb_lat')
        self.xlw.Range('B51').value = config.get_param('res_ialu')
        self.xlw.Range('B52').value = config.get_param('res_imult')
        self.xlw.Range('B53').value = config.get_param('res_memport')
        self.xlw.Range('B54').value = config.get_param('res_fpalu')
        self.xlw.Range('B55').value = config.get_param('res_fpmult')
        self.xlw.Range('B56').value = config.get_param('bugcompat')
        self.xlw.Range('B57').value = ''
        self.xlw.Range('B58').value = config.get_param('bpred_btb_num_sets')

        self.wbk.save()

    def get_ruu_port_params(self):
        """Get RUU port parameters"""
        self.xlw.sheets[2].activate()
        ruu_read_ports = int(self.xlw.Range('B18').value)
        ruu_write_ports = int(self.xlw.Range('B19').value)
        print 'RUU Read Ports:', ruu_read_ports
        print 'RUU Write Ports:', ruu_write_ports
        return ruu_read_ports, ruu_write_ports

    def get_ruu_bit_params(self):
        """Get RUU bit parameters"""
        self.xlw.sheets[3].activate()
        total_ruu_bits = int(self.xlw.Range('B20').value)
        ruu_entry_bits = int(self.xlw.Range('B19').value)
        num_bits_readout = 152 if (ruu_entry_bits < 156) else 160
        print 'Total RUU Bits:', total_ruu_bits
        print 'RUU Entry Bits:', ruu_entry_bits
        print 'Number of Readout Bits:', num_bits_readout
        return total_ruu_bits, ruu_entry_bits, num_bits_readout

    def get_dl1_port_params(self):
        """Get DL1 cache port parameters"""
        self.xlw.sheets[2].activate()
        dl1_read_ports = int(self.xlw.Range('B30').value)
        dl1_write_ports = int(self.xlw.Range('B31').value)
        print 'DL1 Read Ports:', dl1_read_ports
        print 'DL1 Write Ports:', dl1_write_ports
        return dl1_read_ports, dl1_write_ports

    def get_dl1_bit_params(self):
        """Get DL1 cache bit parameters"""
        self.xlw.sheets[3].activate()
        total_dl1_bits = int(self.xlw.Range('B43').value)
        print 'Total DL1 Bits:', total_dl1_bits
        return total_dl1_bits

    def get_dl2_port_params(self):
        """Get DL2 cache port parameters"""
        self.xlw.sheets[2].activate()
        dl2_read_ports = int(self.xlw.Range('B34').value)
        dl2_write_ports = int(self.xlw.Range('B35').value)
        print 'DL2 Read Ports:', dl2_read_ports
        print 'DL2 Write Ports:', dl2_write_ports
        return dl2_read_ports, dl2_write_ports

    def get_dl2_bit_params(self):
        """Get DL2 cache bit parameters"""
        self.xlw.sheets[3].activate()
        total_dl2_bits = int(self.xlw.Range('B59').value)
        print 'Total IL1 Bits:', total_dl2_bits
        return total_dl2_bits

    def get_il1_port_params(self):
        """Get IL1 cache port parameters"""
        self.xlw.sheets[2].activate()
        il1_read_ports = int(self.xlw.Range('B28').value)
        il1_write_ports = int(self.xlw.Range('B29').value)
        print 'IL1 Read Ports:', il1_read_ports
        print 'IL1 Write Ports:', il1_write_ports
        return il1_read_ports, il1_write_ports

    def get_il1_bit_params(self):
        """Get IL1 cache bit parameters"""
        self.xlw.sheets[3].activate()
        total_il1_bits = int(self.xlw.Range('B51').value)
        print 'Total IL1 Bits:', total_il1_bits
        return total_il1_bits

    def get_il2_port_params(self):
        """Get IL2 cache port parameters"""
        self.xlw.sheets[2].activate()
        il2_read_ports = self.xlw.Range('B32').value
        il2_write_ports = self.xlw.Range('B33').value
        print 'IL2 Read Ports:', il2_read_ports
        print 'IL2 Write Ports:', il2_write_ports
        return il2_read_ports, il2_write_ports

    def get_il2_bit_params(self):
        """Get IL2 cache bit parameters"""
        self.xlw.sheets[3].activate()
        total_il2_bits = self.xlw.Range('B67').value
        print 'Total IL2 Bits:', total_il2_bits
        return total_il2_bits

    def get_transistor_count(self):
        """Get total transistor count"""
        self.xlw.sheets[4].activate()
        total_transistor_count = int(math.ceil(self.xlw.Range('B69').value))
        print '\nTransistor Count:', total_transistor_count
        return total_transistor_count

    def get_area(self):
        """Get total area"""
        self.xlw.sheets[5].activate()
        total_area = self.xlw.Range('B109').value * 256E-12
        print '\nTransistor Area:', total_area
        return total_area

def is_transistor_count_valid(count):
    """Check if total transistor count is valid

    Args:
      count: An integer value for the transistor count

    Returns:
      A boolean for the validity of transistor count
    """
    if count > 200000000:
        print 'Total Transistor Count Invalid...'
        print 'Total Transistor Count must be less than 200 million'
        return False
    print 'Valid Total Transistor Count (less than 200 million)'
    return True

def is_area_valid(area):
    """Check if total area is valid

    Args:
      area: A floating point value for the area

    Returns:
      A boolean for the validity of the area
    """
    if area > 25:
        print 'Total Area Invalid...'
        print 'Total Area must be less than 25 mm^2'
        return False
    print 'Valid Area (less than 25 mm^2)'
    return True
