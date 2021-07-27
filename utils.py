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

