import argparse
import subprocess
import os

def SearchOutput(name, path):
    response = False
    for root, dirs, files in os.walk(path):
        if name in files:
             response = True
    return response


def Converter(infile, outdir, annovar):
    script = annovar + "convert2annovar.pl"
    result = outdir + infile[:-4] + ".avinput"
    retcode = subprocess.call("perl" + " " + script + " -format vcf4 " +  infile + " > " + result, shell=True)
    if retcode == 0:
        print("Converting passed!")
    else:
        print("Converting failed!")
    return result

#def Reducer(avinput, outdir, annovar):


parser = argparse.ArgumentParser("NMDsearch", add_help=False)
parser.add_argument('--vcf', type=str, help="Annotate the input VCF-file")
parser.add_argument('--folder', type=str, help="Annotate all VCF within a folder")
parser.add_argument('--output', type=str, default=None, help="The output is stored in this folder")
parser.add_argument('--annovar', type=str, default=None, help="Location of annovar")

args, unknown = parser.parse_known_args()

programDirectory = os.path.dirname(os.path.abspath(__file__))

if args.vcf:
    parser = argparse.ArgumentParser("NMDsearch", add_help=False)
    parser.add_argument('--vcf', type=str, help="Annotate the input VCF-file")
    parser.add_argument('--output', type=str, default=None, help="The output is stored in this folder")
    parser.add_argument('--annovar', type=str, default=None, help="Location of annovar")
    args = parser.parse_args()

    name = args.vcf[:-4] + ".avinput"
    path = args.output
    if SearchOutput(name, path) == False:
        avinput = Converter(args.vcf, args.output, args.annovar)
        print("Converting output: " + avinput)
    else:
        print("Output file " + name + " already exists!")


elif args.folder:
    parser = argparse.ArgumentParser("NMDsearch", add_help=False)
    parser.add_argument('--folder', type=str, help="Annotate all VCF within a folder")
    parser.add_argument('--output', type=str, default=None, help="The output is stored in this folder")
    parser.add_argument('--annovar', type=str, default=None, help="Location of annovar")
    args = parser.parse_args()

#print(args.vcf, args.output, args.annovar)
