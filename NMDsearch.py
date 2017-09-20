import argparse

parser = argparse.ArgumentParser("Filter NMD genes", add_help=False)
parser.add_argument('--csv', type=str, help="Select csv-file to be filterd")
parser.add_argument('--genes', type=str, help="Select list of genes")

args = parser.parse_args()

name = args.genes
Genefile = open(name)
genes = Genefile.read()
geneList = genes.splitlines()
Genefile.close()

#print(geneList)
#print(geneList[:10])
#print(geneList[-10:])

csv = args.csv
CSVfile = open(csv)
variantfile = CSVfile.read()
variants = variantfile.splitlines()
CSVfile.close()

print(csv)

header = variants[0].split(sep=",")
#print(header)
Geneindex = header.index("Gene.refGene")

outfile = []
outfile.append(variants[0])

for i in range(1, len(variants)):
    line = variants[i].split(sep=",")
#    print(line[Geneindex])
    if line[Geneindex] in geneList:
        print(line[Geneindex])
        outfile.append(variants[i])

#print(outfile[:10])