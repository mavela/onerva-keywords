
import gzip
import sys
import math
from analyze import print_text, print_text_filt

class NGram(object):

    def __init__(self,ng):
        self.ng=ng
        self.counts={} #key: corpus  value: count

    def count(self,corpus,occ_num=1):
        """Count an occurrence of the ngram in a given corpus"""
        self.counts[corpus]=self.counts.get(corpus,0)+occ_num


    def __str__(self):
        return self.ng

    def ll(self,corpus_name,corpus_counts,total):
       # print("ll firing")
        """corpus_counts: count for every corpus, total: the grand total of all ngrams"""
        #http://ucrel.lancs.ac.uk/llwizard.html
        sum_O_i=sum(c for c in self.counts.values())

        O_1=self.counts.get(corpus_name,0)
        N_1=corpus_counts[corpus_name]
        E_1=N_1*sum_O_i/total

        O_2=sum_O_i-O_1 #Reference
        N_2=total-corpus_counts[corpus_name] #all other corpora but this one -> reference
        E_2=N_2*sum_O_i/total

        #Skip zero-counts
        ll=0.0
        if O_1>0:
            ll+= O_1*math.log(O_1/E_1)
        if O_2>0:
            ll+=O_2*math.log(O_2/E_2) 

        return 2.0*ll
        

def get_corpus_counts(ngrams):
    corpus_counts={} #{corpus_name:total_count}
    for ng in ngrams.values():
        for corpus,count in ng.counts.items():
            corpus_counts[corpus]=corpus_counts.get(corpus,0)+count
    return corpus_counts, sum(count for count in corpus_counts.values())


def read(f_name,corpus_name,ngrams,max_lines=0):
    """ngrams: {ngram:NGram object}"""
    cols = ["ID","FORM","LEMMA","UPOS","XPOS","FEAT","HEAD","DEPREL","DEPS","MISC"] 
    if f_name.endswith(".gz"):
        f=gzip.open(f_name,"r")
    elif f_name.endswith(".conllu"):
#        print("conllu!")
        f = print_text_filt(f_name, sys.argv[3], 1000000, sys.argv[4])
        f=f.split("\n")
    else:
        f=open(f_name,"r")
    for line_idx,line in enumerate(f):
        line=line.strip()
        line=line.split(" ")
        for i in line:
            i = i.lower()
            if i.isalpha():
                if i not in ngrams:
                    ng=NGram(i)
                    ngrams[i]=ng
                else:
                    ng=ngrams[i]
                    ng.count(corpus_name)

def highest_ll_ngrams(corpus_name,ngrams,corpus_counts,total):
    res=[]
    
    for ng in ngrams.values():
        res.append((ng,ng.ll(corpus_name,corpus_counts,total))) 
    #Res is now a list of (NGram(),ll-value)
    res.sort(reverse=True,key=lambda x: x[1]) #sort descending on that ll-value
    return res


if __name__=="__main__":
    ngrams={} #key: ngram_string, value: NGram()
    corpora=[("Input_Corpus",sys.argv[1]),("Reference Corpus",sys.argv[2])]
    for corpus_name,corpus_file in corpora:
        print ("Reading", corpus_name, "...")
        read(corpus_file,corpus_name,ngrams)
#        print("file, name,grans", corpus_file,corpus_name,ngrams)
        print ("done!")
    
    corpus_counts,total=get_corpus_counts(ngrams)
    
    show_max=400
    for corpus_name,_ in corpora:
      #  print("name,ngrams,counts,total", corpus_name,ngrams,corpus_counts,total)
        ngrams_and_ll=highest_ll_ngrams(corpus_name,ngrams,corpus_counts,total)[:show_max]
        print ("-"*50)
        print ("Corpus name", corpus_name)
        print("Keyword, keyness value")
        for ng,ll in ngrams_and_ll:
            try:
                Prop =  ng.counts.get(corpus_name,0) / sum(ng.counts.values())
            except:
                print(corpus_name, ng, ng.counts.values())
                Prop = 1
            if Prop > float(sys.argv[5]):
                # neitsytmaarianlahja 0.05
                # murtoviivoja 0.09
                # mirdja 0.39
                # miesjanainen 0.045
                # nousukkaita 0.10
                # vangittujasieluja 0.135
                # yksinäisia 0.24
                print(ng.ng, round(ll,2))
            else:
                continue



            
