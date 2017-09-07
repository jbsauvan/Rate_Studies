#! /usr/bin/env python
import ROOT
import numpy as np
from rate_studies.event_reading import read_digis
from rate_studies.output import init_tree, fill_tree


def main(input_file_name, output_name):
    input_tree = ROOT.TChain('hgcalTriggerNtuplizer/HGCalTriggerNtuple')
    input_tree.Add(input_file_name)
    output_file = ROOT.TFile.Open(output_name, 'recreate')
    output_tree = init_tree()
    nentries = input_tree.GetEntries()
    for entry in xrange(nentries):
    #  for entry in xrange(50):
        if entry%(nentries/100)==0:
            print 'Event {0}/{1}'.format(entry,nentries)
        digis = read_digis(input_tree, entry)
        fill_tree(digis, output_tree)
        event = input_tree.event
        

    output_tree.Write()
    output_file.Close()



if __name__=='__main__':
    import sys
    import optparse
    ROOT.gROOT.SetBatch(1)
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--input', dest='input_file', help='Input file name', default='tree.root')
    parser.add_option('--output', dest='output_file', help='Output file name', default='test.root')
    (opt, args) = parser.parse_args()
    main(opt.input_file, opt.output_file)
