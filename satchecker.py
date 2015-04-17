"""
Check Kepler target pixel files (TPF) to see if the raw counts in any pixels
exceed the nominal detector full well depth.

listfile contains the target pixel filenames 
(include paths if files are not in working directory)

TO-DO:
Currently the code only runs on one file at a time. Short cadence quarters 
are split into three files. The code needs to be fixed that so short cadence
data appended and plotted together. 
"""

import numpy as np
import astropy.io.fits as pyfits
import matplotlib.pyplot as plt

# Load filenames
filenames = np.genfromtxt('listfile', dtype='str') # load filenames

# make iterable list if only one file
if filenames.size == 1:
    filenames = [str(filenames)]

for filename in filenames:

    print 'loading file:', filename  
    
    # open TPF
    hdu = pyfits.open(filename)

    # get basic info
    kic = hdu[0].header['KEPLERID']    
    quarter = hdu[0].header['QUARTER']
    title = 'KIC %d - Quarter %d' % (kic,quarter) # plot title
    savefile = 'kic%d.q%02i.png' % (kic,quarter) # plot savefile
        
    # Offset for long cadence or short cadence mode
    obsmode = hdu[0].header['OBSMODE']
    if obsmode == 'short cadence':
        offset = hdu[1].header['SCFXDOFF']
    elif obsmode == 'long cadence':
        offset = hdu[1].header['LCFXDOFF']


    raw = hdu[1].data.field('RAW_CNTS') # raw counts
    time =hdu[1].data.field('TIME')     # observation time
    blklvl = hdu[1].header['MEANBLCK']  # mean dark current
    readout= hdu[1].header['NREADOUT']  # number of readouts
    
    # calculate mean ADU/readout 
    adu = (raw - offset + blklvl*readout)/readout

    #pixel mask dimensions
    xdim = raw.shape[2]; ydim = raw.shape[1]

    # PLOT DATA
    fig, axarr = plt.subplots(ydim,xdim)
    for i in range(xdim):
        for j in range(ydim):

            adu_pix = adu[:,j,i] # adu in pixel
            
            # plot ADU in pixel
            axarr[ydim-j-1,i].plot(time, adu_pix,'-k',lw=1)
            # plot nominal full well depth
            axarr[ydim-j-1,i].plot([min(time),max(time)],[10093., 10093.],'-b', lw =1)
            
            # Adjust plots
            axarr[ydim-j-1,i].set_xticks([])
            axarr[ydim-j-1,i].set_yticks([])
            axarr[ydim-j-1,i].set_ylim(-1000,13000)
          
    fig.subplots_adjust(hspace=0) # get rid of space around cells
    fig.subplots_adjust(wspace=0)
    fig.suptitle(title,fontsize=14) # plot title
    
    plt.savefig(savefile)
    plt.close()