import os
import logging
import argparse
from sffix import fix_observation

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Modify PSRFITS headers of a multi-chunk observation so \
        that dspsr properly considers them time-contiguous. This means \
        creating a copy of the observation where NSUBOFFS=0 in all chunk \
        headers.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "basename",
        type=str,
        help="Base name of the observation. For example, to process all files \
        called 'uwl_181215_103929_N.sf', basename should be 'uwl_181215_103929'"
    )
    parser.add_argument(
        "-i",
        "--indir",
        type=str,
        default=os.getcwd(),
        help="Directory in which the input files are, defaults to the current \
        directory.",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        type=str,
        default=None,
        help="Output directory for fixed files. If not specified, use the same\
        directory as the input files.",
    )
    parser.add_argument(
        "-e",
        "--ext",
        type=str,
        default="sf",
        help="File extension of input files, without the leading dot.",
    )
    parser.add_argument(
        "-s",
        "--suffix",
        type=str,
        default="_fixed",
        help="Suffix appended to output file before chunk index. Example: \
        'uwl_181215_103929_N.sf' becomes 'uwl_181215_103929_fixed_N.sf'",
    )
    args = parser.parse_args()
    return args


def main():
    logging.basicConfig(
        level=logging.DEBUG, 
        format="[%(levelname)s - %(asctime)s] %(message)s"
        )
    args = parse_arguments()

    fix_observation(
        args.indir,
        args.basename, 
        outdir=args.outdir, 
        ext='.{}'.format(args.ext),
        output_suffix=args.suffix
        )


if __name__ == '__main__':
    main()