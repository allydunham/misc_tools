#!/usr/bin/env python3
"""
Fetch species specific Ensembl identifiers for a list of gene names and species
"""
import os
import argparse
import fileinput
import restful


def main(args):
    """Main script"""
    if args.genomes:
        server = 'http://rest.ensemblgenomes.org'
    else:
        server = 'http://rest.ensembl.org'

    # Import species
    species = []
    if os.path.isfile(args.species) or args.species == '-':
        with fileinput.input(args.species) as species_file:
            for i in species_file:
                species.append('_'.join(i.strip().lower().split()))
    else:
        spe = args.species.strip().lower().split(',')
        for i in spe:
            species.append('_'.join(i.split()))

    # Import Gene list
    if os.path.isfile(args.genes) or args.genes == '-':
        genes = []
        with fileinput.input(args.genes) as genes_file:
            for i in genes_file:
                genes.append(i.strip())
    else:
        genes = args.genes.strip().split(',')

    # initialise dict to store IDs
    id_lookup = {}

    # Perform rest requests
    rest = restful.RestClient(server, 0.1)
    for spe in species:
        res = rest.rest('/lookup/symbol/' + spe,
                        header={"Content-Type": "application/json",
                                "Accept" : "application/json"},
                        data='{ "symbols" : ["' + '","'.join(genes) + '"]}')

        id_lookup[spe] = res.json()

    # Output matrix of species/gene IDs
    if args.head:
        print('Gene', *species, sep='\t')

    for gene in genes:
        ids = []
        for spe in species:
            try:
                ids.append(id_lookup[spe][gene]['id'])
            except KeyError:
                ids.append('NA')

        print(gene, *ids, sep='\t')

def parse_args():
    """Process input arguments"""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('species', metavar='S', type=str,
                        help="File containing a list of species to search in\
                              or a comma separated list passed directly")

    parser.add_argument('genes', metavar='G', type=str,
                        help="File containing a list of genes to search for or\
                              a comma separated list passed directly")

    parser.add_argument('--genomes', '-g', action='store_true',
                        help="Use Ensembl Genomes rest server\
                              (for non-vertebrate queries)")

    parser.add_argument('--head', action='store_true',
                        help="Include a header line in the output")

    return parser.parse_args()

if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
