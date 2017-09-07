#! /usr/bin/env python
import ROOT
import numpy as np
from root_numpy import fill_hist
from rate_studies.event_reading import read_digi_samples

pulse_0 = 0.817
pulse_1 = 0.163
pulse_ratio = pulse_1/pulse_0


def intime(arr):
    it = arr[2] - (arr[1]-arr[0]*pulse_ratio)*pulse_ratio
    return it

def main(input_file_name, output_name):
    input_tree = ROOT.TChain('hgcalTriggerNtuplizer/HGCalTriggerNtuple')
    input_tree.Add(input_file_name)
    output_file = ROOT.TFile.Open(output_name, 'recreate')
    n2p5 = ROOT.TH2F('n2p5', 'n2p5', 28, 0.5, 28.5, 5, 1.5, 3.)
    n0p5 = ROOT.TH2F('n0p5', 'n0p5', 28, 0.5, 28.5, 5, 1.5, 3.)
    ntot = ROOT.TH2F('ntot', 'ntot', 28, 0.5, 28.5, 5, 1.5, 3.)
    n2p5_etainc = ROOT.TH1F('n2p5_etainc', 'n2p5_etainc', 28, 0.5, 28.5)
    n0p5_etainc = ROOT.TH1F('n0p5_etainc', 'n0p5_etainc', 28, 0.5, 28.5)
    n0p5_it = ROOT.TH2F('n0p5_it', 'n0p5_it', 28, 0.5, 28.5, 5, 1.5, 3.)
    n0p5_itoot = ROOT.TH2F('n0p5_itoot', 'n0p5_itoot', 28, 0.5, 28.5, 5, 1.5, 3.)
    n0p5_itoot_noit = ROOT.TH2F('n0p5_itoot_noit', 'n0p5_itoot_noit', 28, 0.5, 28.5, 5, 1.5, 3.)
    n2p5_bxm1 = ROOT.TH2F('n2p5_bxm1', 'n2p5_bxm1', 28, 0.5, 28.5, 5, 1.5, 3.)
    n0p5_it_etainc = ROOT.TH1F('n0p5_it_etainc', 'n0p5_it_etainc', 28, 0.5, 28.5)
    n0p5_itoot_etainc = ROOT.TH1F('n0p5_itoot_etainc', 'n0p5_itoot_etainc', 28, 0.5, 28.5)
    n0p5_itoot_noit_etainc = ROOT.TH1F('n0p5_itoot_noit_etainc', 'n0p5_itoot_noit_etainc', 28, 0.5, 28.5)
    n2p5_bxm1_etainc = ROOT.TH1F('n2p5_bxm1_etainc', 'n2p5_bxm1_etainc', 28, 0.5, 28.5)
    nentries = input_tree.GetEntries()
    for entry in xrange(nentries):
    #  for entry in xrange(1):
        if nentries<100 or entry%(nentries/100)==0:
            print 'Event {0}/{1}'.format(entry,nentries)
        digi_eta, digi_layer, digi_subdet, digi_samples, digi_adcs = read_digi_samples(input_tree, entry)
        # Look at 2.5 / 0.5 ratio
        bx0_ismax = np.apply_along_axis(arr=digi_samples, axis=1, func1d=np.argmax)==2
        is_adc = digi_adcs[:,2]==1
        select = np.logical_and.reduce((bx0_ismax, is_adc, digi_subdet==3))
        selected_samples = digi_samples[select][:,2]
        selected_eta = np.abs(digi_eta[select])
        selected_layer = digi_layer[select]
        layer_eta = np.column_stack((selected_layer, selected_eta))
        fill_hist(ntot, layer_eta)
        fill_hist(n0p5, layer_eta[selected_samples>0.5])
        fill_hist(n2p5, layer_eta[selected_samples>2.5])
        fill_hist(n0p5_etainc, selected_layer[selected_samples>0.5])
        fill_hist(n2p5_etainc, selected_layer[selected_samples>2.5])
        # Look at OOT contamination
        all_adc = np.apply_along_axis(arr=digi_adcs, axis=1, func1d=np.sum)==5
        bx0_intime = np.apply_along_axis(arr=digi_samples[all_adc], axis=1, func1d=intime)
        bx0_full = digi_samples[all_adc][:,2]
        bxm1_full = digi_samples[all_adc][:,1]
        selected_eta = np.abs(digi_eta[all_adc])
        selected_layer = digi_layer[all_adc]
        layer_eta = np.column_stack((selected_layer, selected_eta))
        fill_hist(n0p5_it, layer_eta[bx0_intime>0.5])
        fill_hist(n0p5_itoot, layer_eta[bx0_full>0.5])
        fill_hist(n0p5_itoot_noit, layer_eta[np.logical_and(bx0_full>0.5,bx0_intime<0.5)])
        fill_hist(n2p5_bxm1, layer_eta[np.logical_and(bxm1_full>2.5,bx0_full>0.5)])
        fill_hist(n0p5_it_etainc, selected_layer[bx0_intime>0.5])
        fill_hist(n0p5_itoot_etainc, selected_layer[bx0_full>0.5])
        fill_hist(n0p5_itoot_noit_etainc, selected_layer[np.logical_and(bx0_full>0.5,bx0_intime<0.5)])
        fill_hist(n2p5_bxm1_etainc, selected_layer[bxm1_full>2.5])
        
    n2p5Over0p5 = n2p5.Clone('n2p5Over0p5')
    n0p5Overtot = n0p5.Clone('n0p5Overtot')
    n2p5Over0p5.Divide(n0p5)
    n0p5Overtot.Divide(ntot)
    n2p5.Write()
    n0p5.Write()
    ntot.Write()
    n2p5Over0p5.Write()
    n0p5Overtot.Write()
    n2p5Over0p5_etainc = n2p5_etainc.Clone('n2p5Over0p5_etainc')
    n2p5Over0p5_etainc.Divide(n0p5_etainc)
    n2p5Over0p5_etainc.Write()
    nitootOverit = n0p5_itoot.Clone('nitootOverit')
    nitootnoitOverit = n0p5_itoot_noit.Clone('nitootnoitOverit')
    nbxm1Overit = n2p5_bxm1.Clone('nbxm1Overit')
    nitootOverit.Divide(n0p5_it)
    nitootnoitOverit.Divide(n0p5_it)
    nbxm1Overit.Divide(n0p5_it)
    n0p5_it.Write()
    n0p5_itoot.Write()
    n0p5_itoot_noit.Write()
    nitootOverit.Write()
    nitootnoitOverit.Write()
    nbxm1Overit.Write()
    nitootOverit_etainc = n0p5_itoot_etainc.Clone('nitootOverit_etainc')
    nitootnoitOverit_etainc = n0p5_itoot_noit_etainc.Clone('nitootnoitOverit_etainc')
    nbxm1Overit_etainc = n2p5_bxm1_etainc.Clone('nbxm1Overit_etainc')
    nitootOverit_etainc.Divide(n0p5_it_etainc)
    nitootnoitOverit_etainc.Divide(n0p5_it_etainc)
    nbxm1Overit_etainc.Divide(n0p5_it_etainc)
    n0p5_it_etainc.Write()
    n0p5_itoot_etainc.Write()
    n0p5_itoot_noit_etainc.Write()
    nitootOverit_etainc.Write()
    nitootnoitOverit_etainc.Write()
    nbxm1Overit_etainc.Write()
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
