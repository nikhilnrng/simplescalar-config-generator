#!/usr/bin/python

class Config(object):

  def __init__(self):
    self.params = {}
    self.name = 'default'
    self.set_default_params()

  def set_name(self,name):
    if len(name) == 0:
      return
    self.name = name

  def get_name(self):
    return self.name

  def set_param(self,param,value):
    if param not in self.params:
      print 'Error:',param,'is not a valid parameter'
    else:
      print 'Updated',param,'from',self.params[param],
      self.params[param] = value
      print 'to',self.params[param]

  def get_param(self,param):
    return self.params[param]

  def set_default_params(self):

    self.params['seed']                     = 1
    self.params['nice']                     = 0
    self.params['max_inst']                 = 50000000
    self.params['fastfwd']                  = 300000000
    self.params['fetch_ifqsize']            = 4
    self.params['fetch_mplat']              = 3
    self.params['fetch_speed']              = 1
    self.params['bpred']                    = '2lev'
    self.params['bpred_bimod']              = 2048
    self.params['bpred_2lev_l1size']        = 1
    self.params['bpred_2lev_l2size']        = 1024
    self.params['bpred_2lev_hist_size']     = 8
    self.params['bpred_2lev_xor']           = 0
    self.params['bpred_comb']               = 1024
    self.params['bpred_ras']                = 8
    self.params['bpred_btb_num_sets']       = 512
    self.params['bpred_btb_associativity']  = 4
    self.params['decode_width']             = 4
    self.params['issue_width']              = 4
    self.params['issue_inorder']            = 'false'
    self.params['issue_wrongpath']          = 'true'
    self.params['commit_width']             = 4
    self.params['ruu_size']                 = 16
    self.params['lsq_size']                 = 8
    self.params['cache_dl1_name']           = 'dl1'
    self.params['cache_dl1_nsets']          = 128
    self.params['cache_dl1_bsize']          = 32
    self.params['cache_dl1_assoc']          = 4
    self.params['cache_dl1_repl']           = 'l'
    self.params['cache_dl1lat']             = 2
    self.params['cache_dl2_name']           = 'ul2'
    self.params['cache_dl2_nsets']          = 1024
    self.params['cache_dl2_bsize']          = 64
    self.params['cache_dl2_assoc']          = 4
    self.params['cache_dl2_repl']           = 'l'
    self.params['cache_dl2lat']             = 6
    self.params['cache_il1_name']           = 'il1'
    self.params['cache_il1_nsets']          = 512
    self.params['cache_il1_bsize']          = 32
    self.params['cache_il1_assoc']          = 1
    self.params['cache_il1_repl']           = 'l'
    self.params['cache_il1lat']             = 1
    self.params['cache_il2_name']           = 'dl2'
    self.params['cache_il2_nsets']          = 'dl2'
    self.params['cache_il2_bsize']          = ''
    self.params['cache_il2_assoc']          = ''
    self.params['cache_il2_repl']           = ''
    self.params['cache_il2lat']             = 6
    self.params['cache_flush']              = 'false'
    self.params['cache_icompress']          = 'false'
    self.params['mem_lat_first_chunk']      = 100
    self.params['mem_lat_inter_chunk']      = 20
    self.params['mem_width']                = 8
    self.params['tlb_itlb_name']            = 'itlb'
    self.params['tlb_itlb_nsets']           = 16
    self.params['tlb_itlb_bsize']           = 4096
    self.params['tlb_itlb_assoc']           = 4
    self.params['tlb_itlb_repl']            = 'l'
    self.params['tlb_dtlb_name']            = 'dtlb'
    self.params['tlb_dtlb_nsets']           = 32
    self.params['tlb_dtlb_bsize']           = 4096
    self.params['tlb_dtlb_assoc']           = 4
    self.params['tlb_dtlb_repl']            = 'l'
    self.params['tlb_lat']                  = 100
    self.params['res_ialu']                 = 4
    self.params['res_imult']                = 1
    self.params['res_memport']              = 2
    self.params['res_fpalu']                = 4
    self.params['res_fpmult']               = 1
    self.params['bugcompat']                = 'false'

  def create_config_file(self):

    f = open(self.name+'.config','w+')

    f.write('# -config                    '+'\n')
    f.write('# -dumpconfig                '+'\n')
    f.write('# -h                    false'+'\n')
    f.write('# -v                    false'+'\n')
    f.write('# -d                    false'+'\n')
    f.write('# -i                    false'+'\n')
    f.write('-seed                   '+str(self.params['seed'])+'\n')
    f.write('# -q                    false'+'\n')
    f.write('# -chkpt                <null>'+'\n')
    f.write('# -redir:sim            <null>'+'\n')
    f.write('# -redir:prog           <null>'+'\n')
    f.write('-nice                   '+str(self.params['nice'])+'\n')
    f.write('-max:inst               '+str(self.params['max_inst'])+'\n')
    f.write('-fastfwd                '+str(self.params['fastfwd'])+'\n')
    f.write('# -ptrace               <null>'+'\n')
    f.write('-fetch:ifqsize          '+str(self.params['fetch_ifqsize'])+'\n')
    f.write('-fetch:mplat            '+str(self.params['fetch_mplat'])+'\n')
    f.write('-fetch:speed            '+str(self.params['fetch_speed'])+'\n')
    f.write('-bpred                  '+self.params['bpred']+'\n')
    f.write('-bpred:bimod            '+str(self.params['bpred_bimod'])+'\n')
    f.write('-bpred:2lev             '+str(self.params['bpred_2lev_l1size'])+' '+
                                       str(self.params['bpred_2lev_l2size'])+' '+
                                       str(self.params['bpred_2lev_hist_size'])+' '+
                                       str(self.params['bpred_2lev_xor'])+'\n')
    f.write('-bpred:comb             '+str(self.params['bpred_comb'])+'\n')
    f.write('-bpred:ras              '+str(self.params['bpred_ras'])+'\n')
    f.write('-bpred:btb              '+str(self.params['bpred_btb_num_sets'])+' '+
                                       str(self.params['bpred_btb_associativity'])+'\n')
    f.write('# -bpred:spec_update    <null>'+'\n')
    f.write('-decode:width           '+str(self.params['decode_width'])+'\n')
    f.write('-issue:width            '+str(self.params['issue_width'])+'\n')
    f.write('-issue:inorder          '+self.params['issue_inorder']+'\n')
    f.write('-issue:wrongpath        '+self.params['issue_wrongpath']+'\n')
    f.write('-commit:width           '+str(self.params['commit_width'])+'\n')
    f.write('-ruu:size               '+str(self.params['ruu_size'])+'\n')
    f.write('-lsq:size               '+str(self.params['lsq_size'])+'\n')
    f.write('-cache:dl1              '+self.params['cache_dl1_name']+':'+
                                       str(self.params['cache_dl1_nsets'])+':'+
                                       str(self.params['cache_dl1_bsize'])+':'+
                                       str(self.params['cache_dl1_assoc'])+':'+
                                       str(self.params['cache_dl1_repl'])+'\n')
    f.write('-cache:dl1lat           '+str(self.params['cache_dl1lat'])+'\n')
    f.write('-cache:dl2              '+self.params['cache_dl2_name']+':'+
                                       str(self.params['cache_dl2_nsets'])+':'+
                                       str(self.params['cache_dl2_bsize'])+':'+
                                       str(self.params['cache_dl2_assoc'])+':'+
                                       str(self.params['cache_dl2_repl'])+'\n')
    f.write('-cache:dl2lat           '+str(self.params['cache_dl2lat'])+'\n')
    f.write('-cache:il1              '+self.params['cache_il1_name']+':'+
                                       str(self.params['cache_il1_nsets'])+':'+
                                       str(self.params['cache_il1_bsize'])+':'+
                                       str(self.params['cache_il1_assoc'])+':'+
                                       str(self.params['cache_il1_repl'])+'\n')
    f.write('-cache:il1lat           '+str(self.params['cache_il1lat'])+'\n')
    f.write('-cache:il2              '+self.params['cache_il2_name']+'\n')
    f.write('-cache:il2lat           '+str(self.params['cache_il2lat'])+'\n')
    f.write('-cache:flush            '+self.params['cache_flush']+'\n')
    f.write('-cache:icompress        '+self.params['cache_icompress']+'\n')
    f.write('-mem:lat                '+str(self.params['mem_lat_first_chunk'])+' '+
                                       str(self.params['mem_lat_inter_chunk'])+'\n')
    f.write('-mem:width              '+str(self.params['mem_width'])+'\n')
    f.write('-tlb:itlb               '+self.params['tlb_itlb_name']+':'+
                                       str(self.params['tlb_itlb_nsets'])+':'+
                                       str(self.params['tlb_itlb_bsize'])+':'+
                                       str(self.params['tlb_itlb_assoc'])+':'+
                                       str(self.params['tlb_itlb_repl'])+'\n')
    f.write('-tlb:dtlb               '+self.params['tlb_dtlb_name']+':'+
                                       str(self.params['tlb_dtlb_nsets'])+':'+
                                       str(self.params['tlb_dtlb_bsize'])+':'+
                                       str(self.params['tlb_dtlb_assoc'])+':'+
                                       str(self.params['tlb_dtlb_repl'])+'\n')
    f.write('-tlb:lat                '+str(self.params['tlb_lat'])+'\n')
    f.write('-res:ialu               '+str(self.params['res_ialu'])+'\n')
    f.write('-res:imult              '+str(self.params['res_imult'])+'\n')
    f.write('-res:memport            '+str(self.params['res_memport'])+'\n')
    f.write('-res:fpalu              '+str(self.params['res_fpalu'])+'\n')
    f.write('-res:fpmult             '+str(self.params['res_fpmult'])+'\n')
    f.write('# -pcstat               <null>'+'\n')
    f.write('-bugcompat              '+self.params['bugcompat']+'\n')

    f.seek(0)
    data = f.read()
    print data
    
    f.close()
