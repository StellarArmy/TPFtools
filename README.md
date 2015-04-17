# TPFtools
Tools to analyze Kepler target pixel files. 

Right now the only code is `satchecker.py`, which checks to see if any pixels saturated. It's pretty bare bones right now, and could use some enhancements.

# Getting Started
Here's how to get started looking at the target pixel files.

## Put filenames in a listfile
Put all of the TPFs you want to analyze in a file called listfile. That should contain the full path to the files. For example, my listfile only contains one file for Quarter 1 of the long cadence data for the active M dwarf system GJ 1245AB (KIC8451881).

    cat listfile
    /path/to/directory/kplr008451881-2009166043257_lpd-targ.fits

## Run `satchecker.py`
`satchecker.py` will run on the the files in `listfile` save the plots in png format. Here's an example of the output.

![Example Output]
(https://github.com/jlurie/TPFtools/blob/master/kic8451881.q01.png)

## What does it all mean?
The black lines denote the raw counts in each pixel, plotted over the entire quarter. The blue line is the nominal full well depth of the detector. Each Kepler short (long) cadence image is actually the sum of 9 (270) 6 second exposures. If a cadence is above the blue line, it means the mean counts of the exposures in that cadence were above the full well depth of the detector.

**N.B.** If you see periodic dips every three days, those are reaction wheel desaturations. Sadly, no, you did not just discover a new eclipsing binary. 

## I have points above the blue line. Did my target saturate?

Maybe. The details are complicated. The short answer is if this is happening to your target, take anything you measure with a grain of salt. The effects for flares and other impulsive phenomena are discussed in [Lurie et al. (2015)](http://adsabs.harvard.edu/abs/2015ApJ...800...95L)

