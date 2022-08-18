import glob
import sys
from analyze import print_text
from analyze import print_text_filt

print(glob.glob(sys.argv[1]+"/*conllu")) # whole dir of files?


target = sys.argv[2] # target file
#inari.txt-norm.txt.conllu 

out = sys.argv[2]#.split("-")[0]
out=out.replace("data-small/", "")
out=out.split("-")[0]
out=out.replace(".txt", "")
out=out.replace("../", "")
print("out", out)

fout  = open("temp/"+out+".ref.conllu", "w")
#fout = open("temp_conllu/"+out+".ref.conllu", "w")
print(fout)
for file in glob.glob(sys.argv[1]+"/*conllu"):
    if file == target:
        continue
    else:
#        f = print_text_filt(file, "LEMMA", 1000000, "stop.txt")
 #       f=f.split("\n")
        file=open(file, "r")
        for line in file:
            line=line.strip()
            fout.write(line)
            fout.write("\n")
fout.close()

        
