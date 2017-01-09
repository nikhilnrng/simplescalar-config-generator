#!/usr/bin/python

import math
import xlwings as xw
from xlwings import Book

class Estimator(object):

  def __init__(self):
    self.wb = Book('real_estimator.xlsx')

  def configure_estimator_params(self,config):

    xw.sheets[0].activate()

    xw.Range('B3').value   =  config.get_param('seed')
    xw.Range('B4').value   =  config.get_param('fetch_ifqsize')
    xw.Range('B5').value   =  config.get_param('fetch_mplat')
    xw.Range('B6').value   =  config.get_param('bpred')
    xw.Range('B7').value   =  config.get_param('bpred_bimod')
    xw.Range('B8').value   =  config.get_param('bpred_2lev_l1size')
    xw.Range('B9').value   =  config.get_param('bpred_2lev_l2size')
    xw.Range('B10').value  =  config.get_param('bpred_2lev_hist_size')
    xw.Range('B11').value  =  config.get_param('decode_width')
    xw.Range('B12').value  =  config.get_param('issue_width')
    xw.Range('B13').value  =  config.get_param('issue_inorder')
    xw.Range('B14').value  =  config.get_param('issue_wrongpath')
    xw.Range('B15').value  =  config.get_param('ruu_size')
    xw.Range('B16').value  =  config.get_param('lsq_size')
    xw.Range('B17').value  =  config.get_param('cache_dl1_nsets')
    xw.Range('B18').value  =  config.get_param('cache_dl1_bsize')
    xw.Range('B19').value  =  config.get_param('cache_dl1_assoc')
    xw.Range('B20').value  =  config.get_param('cache_dl1_repl')
    xw.Range('B21').value  =  config.get_param('cache_dl1lat')
    xw.Range('B22').value  =  config.get_param('cache_dl2_nsets')
    xw.Range('B23').value  =  config.get_param('cache_dl2_bsize')
    xw.Range('B24').value  =  config.get_param('cache_dl2_assoc')
    xw.Range('B25').value  =  config.get_param('cache_dl2_repl')
    xw.Range('B26').value  =  config.get_param('cache_dl2lat')
    xw.Range('B27').value  =  config.get_param('cache_il1_nsets')
    xw.Range('B28').value  =  config.get_param('cache_il1_bsize')
    xw.Range('B29').value  =  config.get_param('cache_il1_assoc')
    xw.Range('B30').value  =  config.get_param('cache_il1_repl')
    xw.Range('B31').value  =  config.get_param('cache_il1lat')
    xw.Range('B32').value  =  config.get_param('cache_il2_nsets')
    xw.Range('B33').value  =  config.get_param('cache_il2_bsize')
    xw.Range('B34').value  =  config.get_param('cache_il2_assoc')
    xw.Range('B35').value  =  config.get_param('cache_il2_repl') 
    xw.Range('B36').value  =  config.get_param('cache_il2lat')
    xw.Range('B37').value  =  config.get_param('cache_flush')
    xw.Range('B38').value  =  config.get_param('cache_icompress')
    xw.Range('B39').value  =  config.get_param('mem_lat_first_chunk')
    xw.Range('B40').value  =  config.get_param('mem_lat_inter_chunk')
    xw.Range('B41').value  =  config.get_param('mem_width')
    xw.Range('B42').value  =  config.get_param('tlb_itlb_nsets')
    xw.Range('B43').value  =  config.get_param('tlb_itlb_bsize')
    xw.Range('B44').value  =  config.get_param('tlb_itlb_assoc')
    xw.Range('B45').value  =  config.get_param('tlb_itlb_repl') 
    xw.Range('B46').value  =  config.get_param('tlb_dtlb_nsets')
    xw.Range('B47').value  =  config.get_param('tlb_dtlb_bsize')
    xw.Range('B48').value  =  config.get_param('tlb_dtlb_assoc')
    xw.Range('B49').value  =  config.get_param('tlb_dtlb_repl')
    xw.Range('B50').value  =  config.get_param('tlb_lat')
    xw.Range('B51').value  =  config.get_param('res_ialu')
    xw.Range('B52').value  =  config.get_param('res_imult')
    xw.Range('B53').value  =  config.get_param('res_memport')
    xw.Range('B54').value  =  config.get_param('res_fpalu')
    xw.Range('B55').value  =  config.get_param('res_fpmult')
    xw.Range('B56').value  =  config.get_param('bugcompat')
    xw.Range('B57').value  =  ''
    xw.Range('B58').value  =  config.get_param('bpred_btb_num_sets')

    self.wb.save()

  def get_ruu_port_params(self):
    xw.sheets[2].activate()
    RUU_Read_Ports = int(xw.Range('B18').value)
    RUU_Write_Ports = int(xw.Range('B19').value)
    print 'RUU Read Ports:',RUU_Read_Ports
    print 'RUU Write Ports:',RUU_Write_Ports
    return RUU_Read_Ports,RUU_Write_Ports

  def get_ruu_bit_params(self):
    xw.sheets[3].activate()
    Total_RUU_Bits = int(xw.Range('B20').value)
    RUU_Entry_Bits = int(xw.Range('B19').value)
    Num_Bits_Readout = 152 if (RUU_Entry_Bits < 156) else 160
    print 'Total RUU Bits:',Total_RUU_Bits
    print 'RUU Entry Bits:',RUU_Entry_Bits
    print 'Number of Readout Bits:',Num_Bits_Readout
    return Total_RUU_Bits,RUU_Entry_Bits,Num_Bits_Readout

  def get_dl1_port_params(self):
    xw.sheets[2].activate()
    DL1_Read_Ports = int(xw.Range('B30').value)
    DL1_Write_Ports = int(xw.Range('B31').value)
    print 'DL1 Read Ports:',DL1_Read_Ports
    print 'DL1 Write Ports:',DL1_Write_Ports
    return DL1_Read_Ports,DL1_Write_Ports

  def get_dl1_bit_params(self):
    xw.sheets[3].activate()
    Total_DL1_Bits = int(xw.Range('B43').value)
    print 'Total DL1 Bits:',Total_DL1_Bits
    return Total_DL1_Bits

  def get_dl2_port_params(self):
    xw.sheets[2].activate()
    DL2_Read_Ports = int(xw.Range('B34').value)
    DL2_Write_Ports = int(xw.Range('B35').value)
    print 'DL2 Read Ports:',DL2_Read_Ports
    print 'DL2 Write Ports:',DL2_Write_Ports
    return DL2_Read_Ports,DL2_Write_Ports

  def get_dl2_bit_params(self):
    xw.sheets[3].activate()
    Total_DL2_Bits = int(xw.Range('B59').value)
    print 'Total IL1 Bits:',Total_DL2_Bits
    return Total_DL2_Bits

  def get_il1_port_params(self):
    xw.sheets[2].activate()
    IL1_Read_Ports = int(xw.Range('B28').value)
    IL1_Write_Ports = int(xw.Range('B29').value)
    print 'IL1 Read Ports:',IL1_Read_Ports
    print 'IL1 Write Ports:',IL1_Write_Ports
    return IL1_Read_Ports,IL1_Write_Ports

  def get_il1_bit_params(self):
    xw.sheets[3].activate()
    Total_IL1_Bits = int(xw.Range('B51').value)
    print 'Total IL1 Bits:',Total_IL1_Bits
    return Total_IL1_Bits

  def get_il2_port_params(self):
    xw.sheets[2].activate()
    IL2_Read_Ports = xw.Range('B32').value
    IL2_Write_Ports = xw.Range('B33').value
    print 'IL2 Read Ports:',IL2_Read_Ports
    print 'IL2 Write Ports:',IL2_Write_Ports
    return IL2_Read_Ports,IL2_Write_Ports

  def get_il2_bit_params(self):
    xw.sheets[3].activate()
    Total_IL2_Bits = xw.Range('B67').value
    print 'Total IL2 Bits:',Total_IL2_Bits
    return Total_IL2_Bits

  def get_transistor_count(self):
    xw.sheets[4].activate()
    Total_Transistor_Count = int(math.ceil(xw.Range('B69').value))
    print '\nTransistor Count:',Total_Transistor_Count
    return Total_Transistor_Count

  def get_area(self):
    xw.sheets[5].activate()
    Total_Area = xw.Range('B109').value * 256E-12
    print '\nTransistor Area:',Total_Area
    return Total_Area

  def is_transistor_count_valid(self,count):
    if count > 200000000:
      print 'Total Transistor Count Invalid...'
      print 'Total Transistor Count must be less than 200 million'
      return False
    print 'Valid Total Transistor Count (less than 200 million)'
    return True

  def is_area_valid(self,area):
    if area > 25:
      print 'Total Area Invalid...'
      print 'Total Area must be less than 25 mm^2'
      return False
    print 'Valid Area (less than 25 mm^2)'
    return True
