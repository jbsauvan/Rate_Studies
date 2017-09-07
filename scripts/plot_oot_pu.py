#! /usr/bin/env python
import ROOT

def style():
    # ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat()
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetFrameLineWidth(1)
    ROOT.gStyle.SetPadBottomMargin(0.13)
    ROOT.gStyle.SetPadLeftMargin(0.13)
    ROOT.gStyle.SetPadTopMargin(0.05)
    ROOT.gStyle.SetPadRightMargin(0.03)

    ROOT.gStyle.SetLabelFont(42,"X")
    ROOT.gStyle.SetLabelFont(42,"Y")
    ROOT.gStyle.SetLabelSize(0.04,"X")
    ROOT.gStyle.SetLabelSize(0.04,"Y")
    ROOT.gStyle.SetLabelOffset(0.01,"Y")
    ROOT.gStyle.SetTickLength(0.03,"X")
    ROOT.gStyle.SetTickLength(0.03,"Y")
    ROOT.gStyle.SetLineWidth(1)
    ROOT.gStyle.SetTickLength(0.04 ,"Z")

    ROOT.gStyle.SetTitleSize(0.1)
    ROOT.gStyle.SetTitleFont(42,"X")
    ROOT.gStyle.SetTitleFont(42,"Y")
    ROOT.gStyle.SetTitleSize(0.07,"X")
    ROOT.gStyle.SetTitleSize(0.05,"Y")
    ROOT.gStyle.SetTitleOffset(0.8,"X")
    ROOT.gStyle.SetTitleOffset(1.2,"Y")
    ROOT.gStyle.SetOptStat(0)
    #  ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetPaintTextFormat("3.2f")
    ROOT.gROOT.ForceStyle()


def main(input_file_name, output_name):
    style()
    input_file = ROOT.TFile.Open(input_file_name)
    ## 1D histos vs layer
    nitootOverit_etainc = input_file.Get('nitootOverit_etainc')
    nbxm1Overit_etainc = input_file.Get('nbxm1Overit_etainc')
    c_nitootOverit_etainc = ROOT.TCanvas('c_nitootOverit_etainc', '', 500, 500)
    nitootOverit_etainc.SetLineWidth(2)
    nitootOverit_etainc.SetAxisRange(1., 1.4, 'Y')
    nitootOverit_etainc.SetXTitle('layer')
    nitootOverit_etainc.SetYTitle('N(>0.5mip,IT+OOT) / N(>0.5mip,IT)')
    nitootOverit_etainc.Draw('hist')
    c_nitootOverit_etainc.Print("oot_overhead.png")
    c_nbxm1Overit_etainc = ROOT.TCanvas('c_nbxm1Overit_etainc', '', 500, 500)
    nbxm1Overit_etainc.SetLineWidth(2)
    nbxm1Overit_etainc.SetAxisRange(0., 0.5, 'Y')
    nbxm1Overit_etainc.SetXTitle('layer')
    nbxm1Overit_etainc.SetYTitle('N(>2.5mip,bx=-1) / N(>0.5mip,IT)')
    nbxm1Overit_etainc.Draw('hist')
    c_nbxm1Overit_etainc.Print("previousbx_overhead.png")
    ## 2D histos vs layer-eta
    nitootOverit = input_file.Get('nitootOverit')
    nbxm1Overit = input_file.Get('nbxm1Overit')
    c_nitootOverit = ROOT.TCanvas('c_nitootOverit', '', 500, 500)
    c_nitootOverit.SetRightMargin(0.12)
    nitootOverit.SetXTitle('layer')
    nitootOverit.SetYTitle('|#eta|')
    nitootOverit.Draw('col z')
    c_nitootOverit.Print("oot_overhead_eta_layer.png")
    c_nbxm1Overit = ROOT.TCanvas('c_nbxm1Overit', '', 500, 500)
    c_nbxm1Overit.SetRightMargin(0.12)
    nbxm1Overit.SetXTitle('layer')
    nbxm1Overit.SetYTitle('|#eta|')
    nbxm1Overit.Draw('col z')
    c_nbxm1Overit.Print("previousbx_overhead_eta_layer.png")



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
