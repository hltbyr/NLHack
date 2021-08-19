import os
import pandas as pd
from utils import tokenize_for_char_based
import tensorflow as tf
import numpy as np
import tqdm
from joblib import Parallel, delayed
import string
import time
import pickle
from tqdm import tqdm
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def load_keep_probs(keep_prob_path):
    #sorted from most freq to least
    import pickle
    with open(keep_prob_path, 'rb') as f:
        keep_probs = pickle.load(f)
    keep_probs = dict(sorted(keep_probs.items(), key=lambda item: item[1]))
    return keep_probs

def save_lines_from_data(data_path):
    data = pd.read_pickle(data_path, compression="gzip")
    data = data.fillna(" ")
    
    def for_joblib(text):
        preprocessed = tokenize_for_char_based(text, char_set=string.printable+"üÜiİöÖğĞşŞçÇ", min_token=5, min_char=25, unk_eliminate_ratio=0.1, split=False)
        return preprocessed
    
    lines = Parallel(n_jobs = -1, verbose = 1)((delayed(for_joblib)(text) for text in data))
    lines.extend(lines)
    lines = [item for sublist in lines for item in sublist]


    with open('data/' + 'lines.pickle', 'wb') as handle:
        pickle.dump(lines, handle, protocol=4)

def save_dataset(lines_path, keep_prob_path, char_set, max_word_len, window_size=2, neg_sample_size = 5):

    with open(lines_path, 'rb') as f:
        lines = pickle.load(f)
    keep_probs = load_keep_probs(keep_prob_path)
    words = list(keep_probs.keys())
    word_count = len(words)
    print("Number of lines {}".format(len(lines)))


    def to_idx(word, char_set=char_set, max_word_len=max_word_len):
        if(len(word) < max_word_len):
            res = [char_set.index(c) if c in char_set else -1 for c in word]
            res += [-1 for _ in range(max_word_len-len(word))]
        else:
            res = [char_set.index(c) if c in char_set else -1 for c in word[:max_word_len]]
        return res
        #return tf.one_hot(res,len(char_set)).numpy()

    targets = []
    contexts = []
    labels = []

    for line in tqdm(lines[:250000]):
        line = line.split(" ")
        for i,word in enumerate(line):
            word = word.rstrip()
            for j in range(i - window_size, i + window_size+1):
                if j==i or j<0 or j>=len(line):
                    continue
                
                flag=True
                try:
                    prob = keep_probs[word]
                except:
                    continue
                flag = np.random.rand() < prob
                if flag == False:
                    continue
                
                targets.append(to_idx(word))
                contexts.append(to_idx(line[j]))
                labels.append(1)

            for _ in range(neg_sample_size):
                if flag == False:
                    continue
                idx = int(abs(np.random.rand() - 0.25) * word_count)
                targets.append(to_idx(word))
                contexts.append(to_idx(words[idx]))
                labels.append(0)
        
    print("---------finished--------")
    
    with open('data/' + 'train_data/targets.pickle', 'wb') as handle:
        pickle.dump(targets, handle)
    with open('data/' + 'train_data/contexts.pickle', 'wb') as handle:
        pickle.dump(contexts, handle)
    with open('data/' + 'train_data/labels.pickle', 'wb') as handle:
        pickle.dump(labels, handle)


#testing
if __name__ == "__main__":
    save_lines_from_data("data/merged.gz")
    
    
        
    
    
    
        
