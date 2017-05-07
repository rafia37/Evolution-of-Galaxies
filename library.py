from astropy.io import fits, ascii
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import glob, pdb, string





def stack_spectra(fname, plot = False, section = False):
    hdu = fits.open(fname)
    temp1 = fname.split('/')
    temp2 = temp1[1].split('.')
    field = temp2[0]
    image = hdu[0].data
    header = hdu[0].header
    wavelen = header["CRVAL1"] + np.array(header["CDELT1"])*range(header['NAXIS1'])
    if (section == False):
        flux = np.mean(image, axis = 0)
    else:
        flux = np.mean(image[section[0]:section[1]], axis = 0)
    if plot == True:
        plt.plot(wavelen, flux)
        plt.xlabel("Wavelength")
        plt.ylabel("Flux")
        plt.title("Stacked Spectra of %s" % field)
    
    hdu.close()
    
    return image, flux, wavelen








def binning(x, y, bin_pts, spectra_plot = False, filename = False):
    """
    x = quantity to be divided into bins [must be sorted]
    y = quantity that falls into the bins [must be sorted]
    bin_pts = Number of points in each bin
    """
    start = 0
    bin_start = x[start]
    bin_edge = []
    bin_size = []
    distribution = []
    flux = []
    wavelength = []
    count = 0
    while (bin_start < x[-1]):
        stop = start + bin_pts
        if (stop < len(x)):
            count += 1
            bin_stop = x[stop]
            dist = len(y[start:stop])
            distribution.append(dist)
            bin_edge.append(bin_start)
            bin_size.append((bin_stop - bin_start))
            if filename != False:
                _, flx, wave = stack_spectra(filename, section = [start, stop])
                flux.append(flx)
                wavelength.append(wave)
            start, bin_start = stop, bin_stop
        else:
            break
    
    if (spectra_plot == True):
        for i in range(count):
            plt.subplot(count/2, 2, i+1)
            plt.plot(wavelength[i], flux[i])
    else:
        plt.bar(bin_edge, distribution, align = 'edge', width = bin_size)
        
    return distribution, bin_edge





def gen_hist(fname, hist): 

#hist options: mass, chi2

    result = Table(ascii.read(fname))

    if hist == 'mass':
        mass = result['best.stellar.m_star']
        ind = np.where(np.isfinite(mass) == True)[0]
        plt.hist(np.log10(mass[ind]))
        plt.title('Distribution of stellar mass')
        plt.show()
        
    if hist == 'chi2':
        chi2 = result['best.reduced_chi_square']
        ind = np.where(np.isfinite(chi2) == True)[0]
        plt.hist(np.log10(chi2[ind]))
        plt.show()




"""
def duplicates(column):
    col = list(column)
    
    counts = Counter(col)
    ascii.write(counts.items(), 'count.csv')
    for s,num in counts.items():
        #print s, num
        if num > 1:
            for suffix in list(string.ascii_lowercase)[0:num]:
                ind = col.index(s)
                col[ind] = str(s) + suffix
                #pdb.set_trace()
                print s, 'converted to', col[ind] 
    return np.array(col)
"""


def duplicates(column):
    col = [str(a) for a in column.data]
    counts  = Counter(col)
    N       = np.array(counts.values())
    idx_dup = np.where(N > 1)[0]
    keys    = np.array(counts.keys())
    for ii in xrange(len(idx_dup)):
        s = keys[idx_dup[ii]]
        print ii, s
        t_dup = [cc for cc in xrange(len(col)) if s in col[cc]]
        suffix0 = list(string.ascii_lowercase[0:len(t_dup)])
        for ind,suffix in zip(t_dup,suffix0):
            col[ind] = s + suffix
            print ii, s, 'converted to', col[ind] 
    return np.array(col)