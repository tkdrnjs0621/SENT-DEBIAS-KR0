import random
import pickle
from tqdm import tqdm, trange
import numpy.linalg as LA

class BiasSubspaceGenerator:
    
    def __init__(self, SE):
        self.SE = SE
        
    def loadData_WPS(self,filePath,word_pair,do_random,print_tqdm,maxl=4):
        # loads data from visualization keyword set
        # returns a dictionary with a single word as keys and arrays of sentences that includes key as value
    
        sentence_pairs = []
        sentences = []
        
        with open(filePath, 'rb') as f:
            while(True):
                try:
                    sentences.append(pickle.load(f))
                except EOFError:
                    break
                    
        if(do_random):
            random.shuffle(sentences)
            
        sentences = sentences[0:maxl] if(len(sentences)>maxl) else sentences
                    
        for s in (tqdm(sentences) if print_tqdm else sentences):
            for p in word_pair:
                    if self.SE.ifWordInSentence(p[0],s):
                        sentence_pairs.append((self.SE.tokenizer(s).input_ids,self.SE.Replace(s,p[0],p[1])))
                    if self.SE.ifWordInSentence(p[1],s):
                        sentence_pairs.append((self.SE.Replace(s,p[1],p[0]),self.SE.tokenizer(s).input_ids))
    
        return sentence_pairs
    
    
    def get_bias_vectors(self,sentence_pairs,max_length,do_tqdm):
        vectors = []
        
        for p in (tqdm(sentence_pairs,desc="getting bias vectors from sentence pairs") if do_tqdm else sentence_pairs):
            if(len(p[0])>max_length):
                continue
                
            p0=self.SE.encode_from_tokens(p[0])
            p1=self.SE.encode_from_tokens(p[1])
            
            p0=p0/LA.norm(p0)
            p1=p1/LA.norm(p1)
            
            mean= (p0+p1)
            
            p0=p0-mean
            p1=p1-mean

            vectors.append(p0)
            vectors.append(p1)
            
        return vectors