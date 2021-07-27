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
    words = list(filter(None, words))
    return words

def get_syllables_sentence(sentence, debug=False):
    words = get_words_sentence(sentence)
    processed_words = [get_syllables_word(word) for word in words]
    if debug:
        print("\n".join(["-".join(r) for r in processed_words]))
    return processed_words

def digits_to_word(number):
    return number

