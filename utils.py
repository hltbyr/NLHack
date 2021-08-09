def detect_number(line, rigorous=False):
    '''
    Takes an array of words and returns the indices of numbers.
    If rigorous True, words that include numbers will be divided. Ex. abc20xyz --> abc, 20, xyz
    Returns the new line and indices of numbers
    '''
    indices = []
    new_line = []
    offset = 0
    for index, word in enumerate(line):
        try:
            number = float(word)
            indices.append(index + offset)
            new_line.append(str(number))
        except:
            if(rigorous):
                divided = num_in_str(word)
                nl, idcs = [word], []
                if(len(divided) > 1):
                    nl, idcs = detect_number(divided, False)
                
                new_line.extend(nl)
                for i in idcs:
                    indices.append(i + index + offset)
                
                offset += len(nl) - 1
            else:
                new_line.append(word)

    
    return new_line, indices

#Takes an str and seperates numerical parts from others
def num_in_str(s):
    if(len(s) == 1):
        return [s]
    div = []
    flag = False
    buffer = ""
    for c in s:
        try:
            num = int(c)
            if(flag==False and len(buffer) > 0):
                div.append(buffer)
                buffer = ""
            buffer += str(num)
            flag = True       
        except:
            
            if(flag==True and (c == "." or c == ",")):
                buffer += str(c)
                continue

            if(flag==True and len(buffer) > 0):
                div.append(buffer)
                buffer = ""
            buffer += str(c)
            flag=False
    
    if(len(buffer) > 0):
        div.append(buffer)
    
    return div

def tokenize_for_char_based(text, char_set, min_token=4, min_char=15, unk_eliminate_ratio=0.3):
    '''
    Takes a chunck of text, splits them into sentences then splits sentences into tokens.
    Returns a 2D array examples->tokens
    char_set = list of valid chars
    min_token = min token size of a sentence
    min_char = min character length of a sentence
    unk_eliminate_ratio = eliminates the sentence if unknown char ratio is bigger this (between 0-1)
    '''
    results = []
    from Corpus.TurkishSplitter import TurkishSplitter
    sentences = TurkishSplitter().split(text)
    translator = str.maketrans({chr(10): ' ', chr(9): ' '})
    for sentence in sentences:
        sentence = str(sentence)
        sentence = sentence.translate(translator)

        if(len(sentence) < min_char):
            continue
        
        unks = [1 if (c not in char_set and c != " ") else 0 for c in sentence]
        unk_ratio = sum(unks) / len(unks)
        if(unk_ratio > unk_eliminate_ratio):
            continue

        sentence_split = sentence.split(" ")

        if(len(sentence_split) < min_token):
            continue
        
        results.append(sentence_split)
    
    return results

def create_keep_prob_dict(corpus_path, save_path=None, verbose=0):
    '''
    Creates keep prob dict {word-->keep_prob} of given corpus
    corpus_path = path to corpus (.gz pandas file with texts in 'Text' column)
    save_path = if path is not None, the result will be saved to given path, otherwise the method will return the result
    '''
    import string
    import math
    from tqdm import tqdm
    import pandas as pd
    from collections import Counter
    from joblib import Parallel, delayed

    data = pd.read_pickle(corpus_path, compression="gzip")
    
    total_token=0
    data = data.dropna()

    if(verbose>0):
        print("Data has {} rows".format(len(data)))
        
    assert data.isnull().values.any() == False, "Data has nan values"
    
    def for_joblib(text):
        tokens = []
        preprocessed = tokenize_for_char_based(text, char_set=string.printable+"üÜiİöÖğĞşŞçÇ", min_token=0, min_char=0, unk_eliminate_ratio=1.0)
        for sentence in preprocessed:
            tokens.extend(sentence)
        return tokens

    tokens = Parallel(n_jobs = -1, verbose = 1)((delayed(for_joblib)(text) for text in data))
    tokens.extend(tokens)
    tokens = [item for sublist in tokens for item in sublist]
    
    total_token = len(tokens)
    counter = Counter(tokens)

    if(verbose > 0):
        print("Most common 5 is --> {}".format(counter.most_common(5)))
        print("Least common 5 is --> {}".format(counter.most_common()[-5:]))
    
    counter = dict(counter)
    counter = dict([(key,value/total_token) for key, value in counter.items()])
    
    def keep_prob(freq):
        prob = (math.sqrt(freq/0.001) + 1) * (0.001 / freq)
        return min(prob,1)
    
    counter = dict([(key,keep_prob(value)) for key, value in counter.items()])

    if(save_path != None):
        import pickle
        with open('data/' + save_path, 'wb') as handle:
            pickle.dump(counter, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        return counter


def get_syllables_word(word):
    vowel = "aeıioöuüAEIİOÖUÜ"
    syllables = []
    found_vowel = False
    syllable = ""
    for letter in reversed(word): # working in reverse order
        if letter in vowel: # is it vowel?
            if found_vowel:
                syllables.append(syllable)
                syllable = ""
            syllable += letter
            found_vowel = True
        else:
            syllable += letter
            if found_vowel:
                syllables.append(syllable)
                found_vowel = False
                syllable = ""
    if len(syllable) > 0: 
        if found_vowel:
            syllables.append(syllable)
        else:
            syllables[-1]+=syllable
    syllables = [syllable[::-1] for syllable in syllables[::-1]] # reverse both syllables and letters again
    return syllables

def get_words_sentence(sentence):
    import re
    # manually lowering I/İ to handle errors
    sentence = sentence.replace("I","ı").replace("İ","i").lower() # TODO Do we need to lower the cases? 
    punctuations = r'\.\,\?\!\:\;\-\[\]\(\)\{\}\"\'\…\~'
    sentence = re.sub(r'(['+punctuations+r'])', r' \1 ', sentence)
    sentence = re.sub(r'[^a-z ğüşıöç'+punctuations+r']', r' ', sentence) # [^a-zA-Z ğĞüÜşŞıİöÖçÇ] 
    words = sentence.split(" ")
    words = list(filter(None, words)) # remove empty strings
    return words

def get_syllables_sentence(sentence, debug=False):
    words = get_words_sentence(sentence)
    processed_words = [get_syllables_word(word) for word in words]
    if debug:
        print("\n".join(["-".join(r) for r in processed_words]))
    return processed_words

def digits_to_word(number):
    number = int(number)
    negative = number < 0
    print(number, end=": ")
    number = str(abs(number))
    if number == '0':
        return 'sıfır'
    
    def three_digit_to_word(three_number):
        result = []
        units_tr = ['','bir','iki','üç','dört','beş','altı','yedi','sekiz','dokuz']
        tens_tr = ['','on','yirmi','otuz','kırk','elli','altmış','yetmiş','seksen','doksan']

        for scale, num in enumerate(reversed(three_number)):
            num = int(num)
            if scale == 0:
                result.append(units_tr[num])
            elif scale == 1:
                result.append(tens_tr[num])
            elif scale > 1 and num > 0:
                result.append("yüz")
            if num > 1:
                if scale > 1:
                    result.append(units_tr[num])
        result = list(filter(None, result))
        return " ".join(reversed(result))
    
    scales_tr = ['','bin','milyon','milyar','trilyon','trilyar']
    
    result = []
    number = ('  '+number)[::-1] # to easily split
    for scale_idx, three_num in enumerate(zip(number[0::3], number[1::3], number[2::3])):
        three_num = "".join(three_num)[::-1].strip()
        three_num_word = three_digit_to_word(three_num)
        
        if int(three_num) > 0:
            result.append(scales_tr[scale_idx])
            #print(scales_tr[scale_idx])
        if not (scale_idx == 1 and int(three_num) == 1):
            result.append(three_num_word)
            #print(three_num_word)

    if negative: result.append("eksi")
    result = list(filter(None, result))
    return " ".join(reversed(result))


#Testing
if __name__ == "__main__":
    create_keep_prob_dict('data/merged.gz', save_path="keep_probs.pickle", verbose=1)
    
    