import math as m
import numpy as np


tdcOnsetfC_ = 60.
adcLSB_ = 100./(2**10)
tdcLSB_ = 10000./(2**12)
fCperMIP_ = [1.25,2.57,3.88]

def mip(data):
    value = data[0]
    isadc = bool(data[1])
    thickness = int(data[2])
    amplitude = 0
    if not isadc:
        amplitude = ( m.floor(tdcOnsetfC_/adcLSB_) + 1.0 )* adcLSB_ + value * tdcLSB_
    else:
        amplitude = value * adcLSB_
    return amplitude / fCperMIP_[thickness-1]


def read_digis(tree, entry):
    tree.GetEntry(entry)
    digi_data = np.array(tree.hgcdigi_data)
    digi_isadc = np.array(tree.hgcdigi_isadc)
    digi_wafertype = np.array(tree.hgcdigi_wafertypeL)
    digi_simenergy = np.array(tree.hgcdigi_simenergy)
    digi_mip = np.apply_along_axis(mip, axis=1, arr=np.column_stack((digi_data, digi_isadc, digi_wafertype)))
    return np.column_stack((digi_mip, digi_simenergy))

def read_digi_samples(tree, entry):
    tree.GetEntry(entry)
    digi_eta = np.array(tree.hgcdigi_eta)
    digi_layer = np.array(tree.hgcdigi_layer)
    digi_subdet = np.array(tree.hgcdigi_subdet)
    digi_samples = np.array(tree.hgcdigi_mip)
    digi_adcs = np.array(tree.hgcdigi_isadc)
    return digi_eta, digi_layer, digi_subdet, digi_samples, digi_adcs

