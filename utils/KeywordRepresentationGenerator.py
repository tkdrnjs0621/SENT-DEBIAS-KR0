import pickle
from sklearn.manifold import TSNE
from tqdm import tqdm, trange
import numpy.linalg as LA
import random

class KeywordRepresentationGenerator:
    
    def __init__(self, SE):
        self.SE = SE
        
    def loadData_VSK(self,filePath,keywordset,do_tqdm):
        # loads data from visualization keyword set
        # returns a dictionary with a single word as keys and arrays of sentences that includes key as value
        
        _sentences = []
        
        with open(filePath, 'rb') as f:
            while(True):
                try:
                    _sentences.append(pickle.load(f))
                except EOFError:
                    break
        length = len(_sentences)
        
        sentences = {}
        
        for key, l in keywordset.items():
            sentences[key]=[]
            
        with open(filePath, 'rb') as f:
            for i in (tqdm(range(length))if do_tqdm else range(length)):
                try:
                    s = (pickle.load(f))
                    for key, l in keywordset.items():
                        for value in l:
                            if self.SE.ifWordInSentence(value,s):
                                sentences[key].append(s)
                                
                except EOFError:
                    break
                    
        return sentences
    
    def get_both_keyword_reps(self,total,do_random,maxl=200):
        # returns both  keyword representations
        keyword_reps = {}
        debiased_keyword_reps = {}
        
        for key, value in total.items():
            if(do_random):
                random.shuffle(value)
                
            keyword_reps[key]=[]
            debiased_keyword_reps[key]=[]
            
            for i in tqdm(range(maxl),desc="modeling "+key):
                if(i>=len(value)):
                    break
                    
                keyword_reps[key].append(self.SE.encode(value[i]))
                debiased_keyword_reps[key].append(self.SE.encode_remove_bias(value[i]))
                
        return keyword_reps, debiased_keyword_reps
    
    def norm_and_reduce(self, vectors,print_debug):
        #returns normalized and 2D-reduced vector 
        
        num_keys = len(vectors)
        maxl = len(vectors[list(vectors.keys())[0]])
        
        normed_reps=[]
        lens=[]
        
        for key in vectors.keys():
            for v in vectors[key]:
                normed_reps.append(v/LA.norm(v))
            lens.append(len(vectors[key]))
            
        if(print_debug):
            print(lens)
        
        vectors_2d = TSNE(n_components=2).fit_transform(normed_reps)
        
        if(print_debug):
            print("tSNE complete")
        
        avg_2d = {}
        
        sum=None
        
        count=0
        for i in range(num_keys):
            sum=0*vectors_2d[0]

            for j in range(lens[i]):
                sum+=vectors_2d[count+j]
            avg_2d[list(vectors.keys())[i]]=sum/maxl

            count+=lens[i]
        
        return avg_2d