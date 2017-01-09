#!/usr/bin/python

import math

class Config(object):
    """Consolidates all configuration parameter reads, writes, and file generation

    The Config Class assigns default values to all the configuration parameters
    and provides method to modify the parameters and ultimately generate a properly
    syntaxed configuration file.

    Args:
      params: A dictionary containing the config file parameters
      name: A string of the name of the config file
    """
    def __init__(self):
        """Init Config class attributes"""
        self.params = {}
        self.name = 'default'
        self.set_default_params()

    def set_name(self, name):
        """Set configuration file name if valid

        Args:
          name: A string config file name
        """
        if len(name) == 0:
            return
        self.name = name

    def get_name(self):
        """Get configuration file name

        Returns:
          A string config file name
        """
        return self.name

    def set_param(self, param, value):
        """Set parameter to provided value if valid

        Args:
          param: A string config file parameter
          value: A value to replace the current param value
        """
        if param not in self.params:
            print 'Error:', param, 'is not a valid parameter'
        else:
            print 'Updated', param, 'from', self.params[param],
            self.params[param] = value
            print 'to', self.params[param]

    def get_param(self, param):
        """Get value associated with given parameter

        Args:
          param: A string config file parameter

        Returns:
          The value associated with the provided param
        """
        return None if param not in self.params else self.params[param]

    def set_default_params(self):
        """Adds configuration parameters and assigns default values"""
        self.params['seed'] = 1
        self.params['nice'] = 0
        self.params['max_inst'] = 50000000
        self.params['fastfwd'] = 300000000
        self.params['fetch_ifqsize'] = 4
        self.params['fetch_mplat'] = 3
        self.params['fetch_speed'] = 1
        self.params['bpred'] = '2lev'
        self.params['bpred_bimod'] = 2048
        self.params['bpred_2lev_l1size'] = 1
        self.params['bpred_2lev_l2size'] = 1024
        self.params['bpred_2lev_hist_size'] = 8
        self.params['bpred_2lev_xor'] = 0
        self.params['bpred_comb'] = 1024
        self.params['bpred_ras'] = 8
        self.params['bpred_btb_num_sets'] = 512
        self.params['bpred_btb_associativity'] = 4
        self.params['decode_width'] = 4
        self.params['issue_width'] = 4
        self.params['issue_inorder'] = 'false'
        self.params['issue_wrongpath'] = 'true'
        self.params['commit_width'] = 4
        self.params['ruu_size'] = 16
        self.params['lsq_size'] = 8
        self.params['cache_dl1_name'] = 'dl1'
        self.params['cache_dl1_nsets'] = 128
        self.params['cache_dl1_bsize'] = 32
        self.params['cache_dl1_assoc'] = 4
        self.params['cache_dl1_repl'] = 'l'
        self.params['cache_dl1lat'] = 2
        self.params['cache_dl2_name'] = 'ul2'
        self.params['cache_dl2_nsets'] = 1024
        self.params['cache_dl2_bsize'] = 64
        self.params['cache_dl2_assoc'] = 4
        self.params['cache_dl2_repl'] = 'l'
        self.params['cache_dl2lat'] = 6
        self.params['cache_il1_name'] = 'il1'
        self.params['cache_il1_nsets'] = 512
        self.params['cache_il1_bsize'] = 32
        self.params['cache_il1_assoc'] = 1
        self.params['cache_il1_repl'] = 'l'
        self.params['cache_il1lat'] = 1
        self.params['cache_il2_name'] = 'dl2'
        self.params['cache_il2_nsets'] = 'dl2'
        self.params['cache_il2_bsize'] = ''
        self.params['cache_il2_assoc'] = ''
        self.params['cache_il2_repl'] = ''
        self.params['cache_il2lat'] = 6
        self.params['cache_flush'] = 'false'
        self.params['cache_icompress'] = 'false'
        self.params['mem_lat_first_chunk'] = 100
        self.params['mem_lat_inter_chunk'] = 20
        self.params['mem_width'] = 8
        self.params['tlb_itlb_name'] = 'itlb'
        self.params['tlb_itlb_nsets'] = 16
        self.params['tlb_itlb_bsize'] = 4096
        self.params['tlb_itlb_assoc'] = 4
        self.params['tlb_itlb_repl'] = 'l'
        self.params['tlb_dtlb_name'] = 'dtlb'
        self.params['tlb_dtlb_nsets'] = 32
        self.params['tlb_dtlb_bsize'] = 4096
        self.params['tlb_dtlb_assoc'] = 4
        self.params['tlb_dtlb_repl'] = 'l'
        self.params['tlb_lat'] = 100
        self.params['res_ialu'] = 4
        self.params['res_imult'] = 1
        self.params['res_memport'] = 2
        self.params['res_fpalu'] = 4
        self.params['res_fpmult'] = 1
        self.params['bugcompat'] = 'false'

    def create_config_file(self):
        """Opens and formats a configuration file"""
        ifile = open(self.name + '.config', 'w+')

        ifile.write('# -config\n')
        ifile.write('# -dumpconfig\n')
        ifile.write('# -h                    false' + '\n')
        ifile.write('# -v                    false' + '\n')
        ifile.write('# -d                    false' + '\n')
        ifile.write('# -i                    false' + '\n')
        ifile.write('-seed                   ' + str(self.params['seed']) + '\n')
        ifile.write('# -q                    false' + '\n')
        ifile.write('# -chkpt                <null>' + '\n')
        ifile.write('# -redir:sim            <null>' + '\n')
        ifile.write('# -redir:prog           <null>' + '\n')
        ifile.write('-nice                   ' + str(self.params['nice']) + '\n')
        ifile.write('-max:inst               ' + str(self.params['max_inst']) + '\n')
        ifile.write('-fastfwd                ' + str(self.params['fastfwd']) + '\n')
        ifile.write('# -ptrace               <null>' + '\n')
        ifile.write('-fetch:ifqsize          ' + str(self.params['fetch_ifqsize']) + '\n')
        ifile.write('-fetch:mplat            ' + str(self.params['fetch_mplat']) + '\n')
        ifile.write('-fetch:speed            ' + str(self.params['fetch_speed']) + '\n')
        ifile.write('-bpred                  ' + self.params['bpred'] + '\n')
        ifile.write('-bpred:bimod            ' + str(self.params['bpred_bimod']) + '\n')
        ifile.write('-bpred:2lev             ' + str(self.params['bpred_2lev_l1size']) + ' ' +
                    str(self.params['bpred_2lev_l2size']) + ' ' +
                    str(self.params['bpred_2lev_hist_size']) + ' ' +
                    str(self.params['bpred_2lev_xor']) + '\n')
        ifile.write('-bpred:comb             ' + str(self.params['bpred_comb']) + '\n')
        ifile.write('-bpred:ras              ' + str(self.params['bpred_ras']) + '\n')
        ifile.write('-bpred:btb              ' + str(self.params['bpred_btb_num_sets']) + ' ' +
                    str(self.params['bpred_btb_associativity']) + '\n')
        ifile.write('# -bpred:spec_update    <null>' + '\n')
        ifile.write('-decode:width           ' + str(self.params['decode_width']) + '\n')
        ifile.write('-issue:width            ' + str(self.params['issue_width']) + '\n')
        ifile.write('-issue:inorder          ' + self.params['issue_inorder'] + '\n')
        ifile.write('-issue:wrongpath        ' + self.params['issue_wrongpath'] + '\n')
        ifile.write('-commit:width           ' + str(self.params['commit_width']) + '\n')
        ifile.write('-ruu:size               ' + str(self.params['ruu_size']) + '\n')
        ifile.write('-lsq:size               ' + str(self.params['lsq_size']) + '\n')
        ifile.write('-cache:dl1              ' + self.params['cache_dl1_name'] + ':' +
                    str(self.params['cache_dl1_nsets']) + ':' +
                    str(self.params['cache_dl1_bsize']) + ':' +
                    str(self.params['cache_dl1_assoc']) + ':' +
                    str(self.params['cache_dl1_repl']) + '\n')
        ifile.write('-cache:dl1lat           ' + str(self.params['cache_dl1lat']) + '\n')
        ifile.write('-cache:dl2              ' + self.params['cache_dl2_name'] + ':' +
                    str(self.params['cache_dl2_nsets']) + ':' +
                    str(self.params['cache_dl2_bsize']) + ':' +
                    str(self.params['cache_dl2_assoc']) + ':' +
                    str(self.params['cache_dl2_repl']) + '\n')
        ifile.write('-cache:dl2lat           ' + str(self.params['cache_dl2lat']) + '\n')
        ifile.write('-cache:il1              ' + self.params['cache_il1_name'] + ':' +
                    str(self.params['cache_il1_nsets']) + ':' +
                    str(self.params['cache_il1_bsize']) + ':' +
                    str(self.params['cache_il1_assoc']) + ':' +
                    str(self.params['cache_il1_repl']) + '\n')
        ifile.write('-cache:il1lat           ' + str(self.params['cache_il1lat']) + '\n')
        ifile.write('-cache:il2              ' + self.params['cache_il2_name'] + '\n')
        ifile.write('-cache:il2lat           ' + str(self.params['cache_il2lat']) + '\n')
        ifile.write('-cache:flush            ' + self.params['cache_flush'] + '\n')
        ifile.write('-cache:icompress        ' + self.params['cache_icompress'] + '\n')
        ifile.write('-mem:lat                ' + str(self.params['mem_lat_first_chunk']) + ' ' +
                    str(self.params['mem_lat_inter_chunk']) + '\n')
        ifile.write('-mem:width              ' + str(self.params['mem_width']) + '\n')
        ifile.write('-tlb:itlb               ' + self.params['tlb_itlb_name'] + ':' +
                    str(self.params['tlb_itlb_nsets']) + ':' +
                    str(self.params['tlb_itlb_bsize']) + ':' +
                    str(self.params['tlb_itlb_assoc']) + ':' +
                    str(self.params['tlb_itlb_repl']) + '\n')
        ifile.write('-tlb:dtlb               ' + self.params['tlb_dtlb_name'] + ':' +
                    str(self.params['tlb_dtlb_nsets']) + ':' +
                    str(self.params['tlb_dtlb_bsize']) + ':' +
                    str(self.params['tlb_dtlb_assoc']) + ':' +
                    str(self.params['tlb_dtlb_repl']) + '\n')
        ifile.write('-tlb:lat                ' + str(self.params['tlb_lat']) + '\n')
        ifile.write('-res:ialu               ' + str(self.params['res_ialu']) + '\n')
        ifile.write('-res:imult              ' + str(self.params['res_imult']) + '\n')
        ifile.write('-res:memport            ' + str(self.params['res_memport']) + '\n')
        ifile.write('-res:fpalu              ' + str(self.params['res_fpalu']) + '\n')
        ifile.write('-res:fpmult             ' + str(self.params['res_fpmult']) + '\n')
        ifile.write('# -pcstat               <null>' + '\n')
        ifile.write('-bugcompat              ' + self.params['bugcompat'] + '\n')

        ifile.seek(0)
        data = ifile.read()
        print data

        ifile.close()

def get_cache_sets(size, block, assoc):
    """Calculate number of sets in a cache"""
    return size / (block * assoc)

def get_tag_bits(sets, block):
    """Calculate number of tag bits for a 42-bit address"""
    return int(42 - math.log(sets, 2) - math.log(block, 2))
