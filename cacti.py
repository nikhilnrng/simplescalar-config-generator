#!/usr/bin/python

import math
from HTMLParser import HTMLParser
from mechanize import ParseResponse, urlopen

class FormResponseParser(HTMLParser):
    """Parse Cacti form response to obtain relevant access times

    Attributes:
      data: A variable storing the parsed access time
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = None

    def handle_data(self, data):
        data = data.strip()
        if data[:11] == 'Access time':
            self.data = float(data[18:])

class Cacti(object):
    """Consolidates all Cacti tool form submissions and response parsing

    Cacti is used to obtain the access times for the RUU and caches in the CPU. It
    requires data from Real Estimator and other input data from the original config
    file. The tool returns relevant data, but the access time is the only required
    attribute from the Cacti tool.

    The Cacti Class accesses the forms from the Cacti RUU and Cache URLs, dynamically
    fills out the forms, and then uses a modified HTMLParser object to access times.

    Attributes:
      parser: A FormResponseParser object that parses the HTML Response
      ruu_url: A string url to the online cacti RUU tool webpage
      cache_url: A string url to the online cacti cache tool webpage
    """
    def __init__(self):
        """Init Cacti class attributes"""
        self.parser = FormResponseParser()
        self.ruu_url = 'http://quid.hpl.hp.com:9081/cacti/sram.y?new'
        self.cache_url = 'http://quid.hpl.hp.com:9081/cacti/detailed.y?new'

    def get_ruu_access_time(self, ruu_params):
        """Access online Cacti tool and dynamically fill out form to acquire RUU access time

        Args:
          ruu_params[0]: An integer total RUU bits
          ruu_params[1]: An integer RUU read ports
          ruu_params[2]: An integer RUU write ports
          ruu_params[3]: An integer number for RUU readout bits

        Returns:
          A floating point RUU access time
        """
        open_response = urlopen(self.ruu_url)
        forms = ParseResponse(open_response, backwards_compat=False)
        form = forms[0]

        form['cache_size'] = str(ruu_params[0]/8)
        form['nrbanks'] = str(1)
        form['rwports'] = str(0)
        form['read_ports'] = str(ruu_params[1])
        form['write_ports'] = str(ruu_params[2])
        form['ser_ports'] = str(0)
        form['output'] = str(ruu_params[3])
        form['technode'] = str(32)
        form['temp'] = str(360)
        form['data_arr_ram_cell_tech_flavor_in'] = [str(0)]
        form['data_arr_periph_global_tech_flavor_in'] = [str(0)]
        form['tag_arr_ram_cell_tech_flavor_in'] = [str(0)]
        form['tag_arr_periph_global_tech_flavor_in'] = [str(0)]
        form['interconnect_projection_type_in'] = [str(1)]
        form['wire_outside_mat_type_in'] = [str(0)]

        submit_response = urlopen(form.click()).read()
        self.parser.feed(submit_response)
        ruu_access_time = self.parser.data
        print 'RUU Access Time:', ruu_access_time, 'ns'
        return ruu_access_time

    def get_cache_access_time(self, cache_params):
        """Access online Cacti tool and dynamically fill out form to acquire cache access time

        Args:
          cache_params[0]: A string cache name
          cache_params[1]: An integer cache size
          cache_params[2]: An integer line size
          cache_params[3]: An integer set associativity
          cache_params[4]: An integer cache read ports
          cache_params[5]: An integer cache write ports
          cache_params[6]: An integer address tag bit count

        Returns:
          A floating point cache access time
        """
        open_response = urlopen(self.cache_url)
        forms = ParseResponse(open_response, backwards_compat=False)
        form = forms[0]

        form['cache_size'] = str(cache_params[1]/8)
        form['line_size'] = str(cache_params[2])
        form['assoc'] = str(cache_params[3])
        form['nrbanks'] = str(1)
        form['technode'] = str(32)
        form['rwports'] = str(0)
        form['read_ports'] = str(cache_params[4])
        form['write_ports'] = str(cache_params[5])
        form['ser_ports'] = str(0)
        form['output'] = str(cache_params[2]*8)
        form['changetag'] = [str(1)]
        form['tagbits'] = str(cache_params[6])
        form['access_mode'] = [str(0)]
        form['temp'] = str(360)
        form['data_arr_ram_cell_tech_flavor_in'] = [str(0)]
        form['data_arr_periph_global_tech_flavor_in'] = [str(0)]
        form['tag_arr_ram_cell_tech_flavor_in'] = [str(0)]
        form['tag_arr_periph_global_tech_flavor_in'] = [str(0)]
        form['interconnect_projection_type_in'] = [str(1)]
        form['wire_outside_mat_type_in'] = [str(0)]

        submit_response = urlopen(form.click()).read()
        self.parser.feed(submit_response)
        cache_access_time = self.parser.data
        print cache_params[0], 'Access Time:', cache_access_time, 'ns'
        return cache_access_time

def cache_latency(name, cache_access_time, ruu_access_time):
    """Calculate cache latency in cycles"""
    latency = int(math.ceil(cache_access_time / ruu_access_time))
    print name, 'Cache Latency:', latency, 'cycles'
    return latency
