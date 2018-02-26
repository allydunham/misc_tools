#!/usr/bin/env python3
"""
Fetch genomic locations for a list of Ensembl identifiers
"""
import os
import sys
import argparse
import fileinput
import re
import restful
import roman

def main(args):
    """Main script"""
    if args.genomes:
        server = 'http://rest.ensemblgenomes.org'
    else:
        server = 'http://rest.ensembl.org'

    # Import IDs
    ids = []
    if os.path.isfile(args.ids) or args.ids == '-':
        with fileinput.input(args.ids) as id_file:
            for i in id_file:
                ids.append(i.strip())
    else:
        ids = args.ids.strip().split(',')

    # Perform rest requests
    rest = restful.RestClient(server, 0.1)
    data = '{ "ids" : ["' + '", "'.join(set(ids)) + '"] }'
    lookup = rest.rest("/lookup/id",
                       header={"Content-Type":"application/json",
                               "Accept" : "application/json"},
                       data=data)

    lookup = lookup.json()

    # Indicate unmatched IDs
    flag = False
    for key, value in lookup.items():
        if value is None:
            if flag:
                print("The following IDs were unmapped:", file=sys.stderr)
                flag = True
            print(key, sep='\n')

    # Output tab separated table of loci
    if args.head:
        print('#chrom', 'start', 'stop', 'id', 'name', 'strand', sep='\t')

    for key, value in lookup.items():
        if not value is None:
            # Error check absence of names
            if not 'display_name' in value.keys():
                value['display_name'] = 'NA'

            print(format_chrom(value['seq_region_name'], args.chr, args.roman),
                  value['start'] - args.pad, value['end'] + args.pad, key,
                  value['display_name'], value['strand'])

def format_chrom(chrom, prefix='chr', rome=False):
    """Reformat a chromosome name. Non-roman numerals will\
       pass through if rome=False"""

    num = re.sub('[Cc]hromosome|[Cc]hr', '', chrom.strip())
    if rome:
        if not roman.is_roman(num):
            num = roman.int_to_roman(int(num))
    else:
        if roman.is_roman(num):
            num = roman.roman_to_int(num)

    return prefix + str(num)

def parse_args():
    """Process input arguments"""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('ids', metavar='I', type=str,
                        help="File containing a list of ensembl IDs to search for\
                              or a comma separated list passed directly")

    parser.add_argument('--genomes', '-g', action='store_true',
                        help="Use Ensembl Genomes rest server\
                              (for non-vertebrate queries)")

    parser.add_argument('--head', action='store_true',
                        help="Include a header line in the output")

    parser.add_argument('--roman', action='store_true',
                        help="Format chromosme numbers as Roman numerals")

    parser.add_argument('--chr', '-c', default='',
                        help="Prefex to append to chromosome numbers")

    parser.add_argument('--pad', '-p', default=0, type=int,
                        help="Amount of flanking sequence to include in loci")

    return parser.parse_args()

if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
