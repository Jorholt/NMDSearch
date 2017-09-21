import argparse
import csv

parser = argparse.ArgumentParser("Filter NMD genes", add_help=False)
parser.add_argument('--csv', type=str, help="Select csv-file to be filterd")
parser.add_argument('--genes', type=str, help="Select list of genes")

args = parser.parse_args()

name = args.genes
Genefile = open(name)
genes = Genefile.read()
geneList = genes.splitlines()
Genefile.close()

with open(args.csv, 'r') as CSVfile:
    variants = list(csv.reader(CSVfile))

header = variants[0]
Geneindex = header.index("Gene.refGene")

outfile = []
outfile.append(header)

for i in range(1, len(variants)):
    if variants[i][Geneindex] in geneList:
        outfile.append(variants[i])

filename = args.csv[:-4] + "." +  args.genes[:-4] + ".csv"
print(filename)
with open(filename, "w") as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL)
    for row in outfile:
        wr.writerow(row)