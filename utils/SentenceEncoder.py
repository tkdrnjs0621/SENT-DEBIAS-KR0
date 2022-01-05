import transformers
from transformers import BertTokenizer, BertModel
import numpy as np
from sklearn.decomposition import PCA
import pickle
import json
import torch
from tqdm import tqdm, trange

class SentenceEncoder:
    
    def __init__(self, name):
        
        self.tokenizer = BertTokenizer.from_pretrained(name)
        self.model = BertModel.from_pretrained(name)
        self.bias_subspace = []
        
    def tokenize(self, word):
        # returns token vector from a word (or a sentence)
        
        return self.tokenizer(word).input_ids
    
    def ifSingleWord(self,word):
        # checks if a word is encoded as signle vector from the tokenize
        
        return len(self.tokenizer(word).input_ids)==3
        
    def encode(self,sentence):
        # returns encoded vector from string sentence
        
        return self.model((self.tokenizer(sentence, return_tensors="pt")).input_ids).last_hidden_state[0][0].detach().numpy()
    
    def encode_from_tokens(self,sentence):
        # returns encoded vector from token vector
        
        return self.model(torch.tensor([sentence])).last_hidden_state[0][0].detach().numpy()  
    
    def encode_remove_bias_from_tokens(self,sentence):
        # returns encoded vector from token vector
        
        v = self.model(torch.tensor([sentence])).last_hidden_state[0][0].detach().numpy()  
        hv = v*0
        for bias_vector in self.bias_subspace:
            hv = hv + np.dot(bias_vector, v)*bias_vector
        v2=v-hv
    
    def set_bias_subspace(self,bias_subspace):
        #sets bias subspace
        
        self.bias_subspace.clear()
        for i in bias_subspace:
            self.bias_subspace.append(i)
    
    def encode_remove_bias(self,sentence):
        #returns encoded vector with bias removed
        
        v = self.model((self.tokenizer(sentence, return_tensors="pt")).input_ids).last_hidden_state[0][0].detach().numpy()
        hv = v*0
        for bias_vector in self.bias_subspace:
            hv = hv + np.dot(bias_vector, v)*bias_vector
        v2=v-hv
        
        return v2    
    
    def ifWordInSentence(self,word,sentence):
        # checks if a word is in a sentence
        
        if(word in sentence):
            return self.tokenizer(word).input_ids[1] in self.tokenizer(sentence).input_ids
        else:
            return False
    
    def Replace(self,sentence,target,obj):
        # returns replaced sentence from target to obj
        # inputs are all string, while return value is token set
    
        _s =self.tokenizer(sentence).input_ids
        _t =self.tokenizer(target).input_ids[1]
        _o =self.tokenizer(obj).input_ids[1]
        _r = []
        
        for i in range(len(_s)):
            if(_s[i]==_t):
                _r.append(_o)
            else:
                _r.append(_s[i])
                
        return _r
    
    
    