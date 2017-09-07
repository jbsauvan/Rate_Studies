import ROOT
from array import array
import numpy as np


ndigis = array('i', [0])
ndigis_simmatch = array('i', [0])
ndigis_1mip = array('i', [0])
ndigis_2mip = array('i', [0])
ndigis_3mip = array('i', [0])
ndigis_4mip = array('i', [0])
ndigis_5mip = array('i', [0])

def init_tree():
    tree = ROOT.TTree("rate", 'rate')
    tree.Branch('ndigis', ndigis, 'ndigis/I')
    tree.Branch('ndigis_simmatch', ndigis_simmatch, 'ndigis_simmatch/I')
    tree.Branch('ndigis_1mip', ndigis_1mip, 'ndigis_1mip/I')
    tree.Branch('ndigis_2mip', ndigis_2mip, 'ndigis_2mip/I')
    tree.Branch('ndigis_3mip', ndigis_3mip, 'ndigis_3mip/I')
    tree.Branch('ndigis_4mip', ndigis_4mip, 'ndigis_4mip/I')
    tree.Branch('ndigis_5mip', ndigis_5mip, 'ndigis_5mip/I')
    return tree

def fill_tree(digis, tree):
    ndigis[0] = len(digis)
    digis_threshold = digis[digis[:,0]>=1.][:,0]
    ndigis_1mip[0] = len(digis_threshold)
    digis_threshold = digis_threshold[digis_threshold>=2.]
    ndigis_2mip[0] = len(digis_threshold)
    digis_threshold = digis_threshold[digis_threshold>=3.]
    ndigis_3mip[0] = len(digis_threshold)
    digis_threshold = digis_threshold[digis_threshold>=4.]
    ndigis_4mip[0] = len(digis_threshold)
    digis_threshold = digis_threshold[digis_threshold>=5.]
    ndigis_5mip[0] = len(digis_threshold)
    ndigis_simmatch[0] = np.count_nonzero(digis[:,1]>0.)
    tree.Fill()
    return tree


