# sffix

Modify PSRFITS headers of multi-chunk search mode observations so that `dspsr` properly considers them time-contiguous, as it should. This is a temporary way to work around a `dspsr` bug (as of 22/01/2019) that should eventually be fixed, which affects Parkes Ultra Wide Band search mode observations (and possibly others).

### Cause of the issue

PSRFITS headers of multi-chunk files contain both a start MJD (specified by `STT_IMJD`, `STT_SMJD` and `STT_OFFS` parameters) and another parameter called `NSUBOFFS` which basically specifies a time offset from the start of the whole observation (i.e. from the start of the very first chunk). This creates an ambiguity as whether or not this offset should be added to the MJD start date specified by each chunk header. `dspsr` currently (as of 22/10/2019) applies that offset, which in the case of the Parkes UWL search mode data is the *incorrect* behaviour; each chunk header already contains the actual MJD start time of the chunk itself.

Until `dspsr` is fixed, a temporary solution is simply to set `NSUBOFFS = 0`. `sffix` provides functions and command-line scripts to create copies of PSRFITS observation with their header modified in such a way.

### Dependencies

The only external dependency is `astropy`, since the `astropy.io.fits` sub-module is used to manipulate FITS files.

### Installing the package

Clone the repository and then use *either* of two methods:
1. Type `make install`, which simply runs `pip install` in [editable mode](https://pip.pypa.io/en/latest/reference/pip_install/#editable-installs), i.e. places a soft link to the repository in your `site-packages` folder. This will also install `astropy` using `pip` if it's not present.
2. Add the root directory of the package to your `PYTHONPATH` environment variable. It's your responsibility to have `astropy` installed in this case.

To test the command line script on the test data provided with the package (a few UWL observation chunks truncated to the first 30KB), type `make test_script` in the base directory and check that there are no errors.


### Running the fix

In `sffix/apps`  there is a `fix.py` command-line script. Type `python fix.py -h` for help. You may also import the `fix_observation` function directly from the `sffix` module and use it interactively.
