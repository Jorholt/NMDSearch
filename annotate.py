import argparse
import subprocess
import os
import fnmatch

def SearchOutput(pattern, path):
    response = False
    for root, dirs, files in os.walk(path):
        for name in files:
             if fnmatch.fnmatch(name, pattern):
                response = True
    return response

def Converter(infile, outdir, annovar):
    script = annovar + "convert2annovar.pl"
    result = outdir + infile[:-4] + ".avinput"
    retcode = subprocess.call("perl " + script + " -format vcf4 " +  infile + " > " + result, shell=True)
    if retcode == 0:
        print("Converting passed!")
    else:
        print("Converting failed!")
    return result

def Reducer(avinput, annovar):
    script = annovar + "variants_reduction.pl"
    humandb = annovar + "humandb/"
    result = avinput[:-8] + ".reduced"
    settings = "-protocol nonsyn_splicing,genomicSuperDups,phastConsElements46way,kaviar_20150923,exac03 -operation g,rr,r,f,f -remove -aaf_threshold 0.00001 -buildver hg19"
    retcode = subprocess.call("perl " + script + " " + avinput + " " + humandb + " " + settings + " -out " + result, shell=True)
    if retcode == 0:
        print("Reduction passed!")
    else:
        print("Reduction failed!")
    return result

def Annotater(reduced, annovar):
    script = annovar + "table_annovar.pl"
    humandb = annovar + "humandb/"
    result = reduced + ".myanno"
    settings = "-buildver hg19 -remove -otherinfo -csvout -protocol refGene,avsnp147,1000g2015aug_all,esp6500siv2_all,kaviar_20150923,exac03,clinvar_20161128,dbnsfp33a -operation g,f,f,f,f,f,f,f"
    retcode = subprocess.call("perl " + script + " " + reduced + " " + humandb + " " + settings + " -out " + result, shell=True)
    if retcode == 0:
        print("Annotation passed!")
    else:
        print("Annotation failed!")
    return result

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
        print("Output file " + name + " already exists in " + path)

    redinput = args.output + name
    name2 = args.vcf[:-4] + ".reduced*"
    if SearchOutput(name2, path) == False:
        reduced = Reducer(redinput, args.annovar)
        print("Reduction output: " + reduced)
    else:
        print("Output file " + name2 + " already exists in " + path)

    filename = input("Enter filename for annotation: ")
    name3 = filename + ".myanno*"
    anninput = args.output + filename
    if SearchOutput(name3, path) == False:
        annotated = Annotater(anninput, args.annovar)
        print("Annotation output: " + annotated)
    else:
        print("Output file " + filename + " already exists in " + path)


elif args.folder:
    parser = argparse.ArgumentParser("NMDsearch", add_help=False)
    parser.add_argument('--folder', type=str, help="Annotate all VCF within a folder")
    parser.add_argument('--output', type=str, default=None, help="The output is stored in this folder")
    parser.add_argument('--annovar', type=str, default=None, help="Location of annovar")
    args = parser.parse_args()

#print(args.vcf, args.output, args.annovar)
