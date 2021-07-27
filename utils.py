def digits_to_words(num):
    '''
    Takes and str of a float number returns it in words
    Ex: 569 --> beş yüz altmış dokuz
    '''
    ones = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
    tenths = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
    hundreds = []

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





#Testing
if __name__ == "__main__":
    s = "123serhat33.16gg1.7 ve55,02 125.189 x 569".split(" ")

    print(s)
    print(detect_number(s, rigorous=True))