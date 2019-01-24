import os
import glob
import logging
import shutil

from astropy.io import fits

log = logging.getLogger('sffix')

# See: http://docs.astropy.org/en/stable/io/fits/

def split_chunk_filepath(path):
    """ Split chunk path into (basedir, basename, index, extension) 
    NOTE: extension contains the leading dot
    """
    basedir, name = os.path.split(path)
    name, ext = os.path.splitext(name)
    basename, index = name.rsplit('_', 1)
    index = int(index)
    return basedir, basename, index, ext


class UWLChunkPath(object):
    """ Convenience class to split UWL chunk paths into base directory, base
    name, chunk index and extension.
    """
    def __init__(self, fname):
        self._fname = os.path.realpath(fname)
        (self._basedir, self._basename, self._index, self._ext) = split_chunk_filepath(self._fname)

    @property
    def fname(self):
        return self._fname

    @property
    def basedir(self):
        return self._basedir

    @property
    def basename(self):
        return self._basename

    @property
    def index(self):
        """ Chunk index in the whole observation """
        return self._index

    @property
    def ext(self):
        """ File extension INCLUDING the leading dot """
        return self._ext


def get_chunk_filepaths(indir, basename, ext='.sf'):
    # NOTE: ext contains the leading dot
    pattern = os.path.join(indir, "{}_[0-9]*{}".format(basename, ext))
    filepaths = glob.glob(pattern)
    return list(map(os.path.realpath, filepaths))


def fix_observation(indir, basename, outdir=None, ext='.sf', output_suffix='_fixed'):
    """ Fix all UWL search mode observation chunks with given base path.

    Parameters
    ----------
    indir: str
        Directory in which the iput files are.

    basename: str
        Base name of the UWL observation files without the extension or the
        chunk index. For example, to process all files called 
        "uwl_181215_103929_N.sf", basename should be 
        "uwl_181215_103929"

    outdir: str or None, optional
        Output directory for fixed files. If None, use the same directory as
        the input files. (Default: None)

    ext: str, optional
        File extension of input files, with the leading dot (Default: '.sf')
    
    output_suffix: str, optional
        Suffix appended to output file before chunk index (Default: '_fixed')
        Example: "uwl_181215_103929_N.sf" becomes "uwl_181215_103929_fixed_N.sf"
    """
    if not output_suffix:
        raise ValueError("Must specify a non-empty output suffix string")

    filenames = get_chunk_filepaths(indir, basename, ext=ext)
    if not filenames:
        raise ValueError("No files with basename {!r} in directory {!r}".format(basename, indir))

    indir = os.path.dirname(filenames[0])
    if outdir is None:
        outdir = indir
    else:
        outdir = os.path.realpath(outdir)
    
    # Sort chunk names by index number
    chunks = sorted(list(map(UWLChunkPath, filenames)), key=lambda c: c.index)

    # Generate output file names
    outnames = [
        os.path.join(outdir, "{:s}{:s}_{:04d}{:s}".format(c.basename, output_suffix, c.index, c.ext))
        for c in chunks
        ]

    for chunk, outname in zip(chunks, outnames):
        log.debug("Copying {!r} to {!r}".format(chunk.fname, outname))
        shutil.copy(chunk.fname, outname)

        # NOTE: header edition is VERY fast
        with fits.open(outname, 'update') as fobj:
            primary, history, subint = list(fobj)
            log.debug("{!r} has NSUBOFFS = {:d}".format(chunk.fname, subint.header['NSUBOFFS']))
            subint.header['NSUBOFFS'] = 0
            log.debug("Set NSUBOFFS = 0 in {!r}".format(outname))
    
    log.debug("Done fixing observation {!r} in directory {!r}".format(basename, indir))
