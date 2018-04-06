#!/usr/bin/env python3
"""
Script to convert GTF files into a bed
"""
import argparse
import fileinput
import sys
from format_chroms import format_chrom

def main(args):
    """Main script"""
    print('#chrom', 'start', 'stop', 'id',
          'name' if args.name else 'score', 'strand',
          sep='\t')

    with fileinput.input(args.gtf) as gtf_file:
        for line in gtf_file:
            # ignore commented lines
            if not line[0] == '#':
                # Split line
                line = line.strip().split('\t')

                # Filter lines not containing genes
                if not args.gene or line[2] == 'gene':
                    # extract additional data
                    dat = [x.strip().split() for x in line[-1].strip().split(';')[:-1]]
                    data = {key:value.strip('"') for key, value in dat}

                    # Extract score
                    if args.name:
                        try:
                            score = data['gene_name']
                        except KeyError:
                            score = 'NA'
                    else:
                        score = line[7]

                    # Extract id
                    try:
                        gene_id = data['gene_id']
                    except KeyError:
                        gene_id = 'NA'

                    chrom = format_chrom(line[0], prefix=args.prefix, rome=args.roman)

                    # Bed file base 0, gtf is base 1
                    print(chrom, int(line[3]) - 1, int(line[4]) - 1,
                          gene_id, score, line[6],
                          sep='\t', file=sys.stdout)

def parse_args():
    """Process input arguments"""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('gtf', metavar='G', help="GTF File")

    parser.add_argument('--gene', '-g', action='store_true',
                        help="Filter to gene regions only")

    parser.add_argument('--name', '-n', action='store_true',
                        help="Keep transcript names in the score column")

    parser.add_argument('--roman', '-r', action='store_true',
                        help="Use roman chromosome notation")

    parser.add_argument('--prefix', '-p', default='chromosome',
                        help="Prefix to append before chromosome number")

    return parser.parse_args()

if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
