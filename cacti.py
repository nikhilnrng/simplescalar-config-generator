#!/usr/bin/python

import math
from mechanize import ParseResponse, urlopen
from HTMLParser import HTMLParser

class Form_Response_Parser(HTMLParser):

  def handle_data(self, data):
    data = data.strip()
    if (data[:11] == 'Access time'):
      #print data
      self.data = float(data[18:])

class Cacti(object):

  def __init__(self):
    self.parser = Form_Response_Parser()

  def cache_latency(self,name,cache_access_time,ruu_access_time):
    Cache_Latency = int(math.ceil(cache_access_time/ruu_access_time))
    print name,'Cache Latency:',Cache_Latency,'cycles'
    return Cache_Latency

  def get_ruu_access_time(self,ruu_params):

    # [0] -> Total_RUU_Bits
    # [1] -> RUU_Read_Ports
    # [2] -> RUU_Write_Ports
    # [3] -> Num_Bits_Readout

    open_response = urlopen('http://quid.hpl.hp.com:9081/cacti/sram.y?new')
    forms = ParseResponse(open_response,backwards_compat=False)
    form = forms[0]

    form['cache_size']                            = str(ruu_params[0]/8)
    form['nrbanks']                               = str(1)
    form['rwports']                               = str(0)
    form['read_ports']                            = str(ruu_params[1])
    form['write_ports']                           = str(ruu_params[2])
    form['ser_ports']                             = str(0)
    form['output']                                = str(ruu_params[3])
    form['technode']                              = str(32)
    form['temp']                                  = str(360)
    form['data_arr_ram_cell_tech_flavor_in']      = [str(0)]
    form['data_arr_periph_global_tech_flavor_in'] = [str(0)]
    form['tag_arr_ram_cell_tech_flavor_in']       = [str(0)]
    form['tag_arr_periph_global_tech_flavor_in']  = [str(0)]
    form['interconnect_projection_type_in']       = [str(1)]
    form['wire_outside_mat_type_in']              = [str(0)]

    submit_response = urlopen(form.click()).read()
    self.parser.feed(submit_response)
    RUU_Access_Time = self.parser.data
    print 'RUU Access Time:',RUU_Access_Time,'ns'
    return RUU_Access_Time

  def get_cache_access_time(self,cache_params): 

    # [0] -> name,
    # [1] -> cache_size
    # [2] -> line_size
    # [3] -> assoc
    # [4] -> read_ports
    # [5] -> write_ports
    # [6] -> tagbits

    open_response = urlopen('http://quid.hpl.hp.com:9081/cacti/detailed.y?new')
    forms = ParseResponse(open_response,backwards_compat=False)
    form = forms[0]

    form['cache_size']                            = str(cache_params[1]/8)
    form['line_size']                             = str(cache_params[2])
    form['assoc']                                 = str(cache_params[3])
    form['nrbanks']                               = str(1)
    form['technode']                              = str(32)
    form['rwports']                               = str(0)
    form['read_ports']                            = str(cache_params[4])
    form['write_ports']                           = str(cache_params[5])
    form['ser_ports']                             = str(0)
    form['output']                                = str(cache_params[2]*8)
    form['changetag']                             = [str(1)]
    form['tagbits']                               = str(cache_params[6])
    form['access_mode']                           = [str(0)]
    form['temp']                                  = str(360)
    form['data_arr_ram_cell_tech_flavor_in']      = [str(0)]
    form['data_arr_periph_global_tech_flavor_in'] = [str(0)]
    form['tag_arr_ram_cell_tech_flavor_in']       = [str(0)]
    form['tag_arr_periph_global_tech_flavor_in']  = [str(0)]
    form['interconnect_projection_type_in']       = [str(1)]
    form['wire_outside_mat_type_in']              = [str(0)]
    
    submit_response = urlopen(form.click()).read()
    self.parser.feed(submit_response)
    Cache_Access_Time = self.parser.data
    print cache_params[0],'Access Time:',Cache_Access_Time,'ns'
    return Cache_Access_Time
