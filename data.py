import string
import pandas as pd
from utils import tokenize_for_char_based

#testing
if __name__ == "__main__":
    #path = "data/merged.gz"
    #data = pd.read_pickle(path, compression="gzip")
    text = "Amerika'da gündemden düşmeyen magazin yıldızları arasında bulunan ünlü model Kim Kardashian, tatiline devam ediyor. Kardashian, tatil yaptığı anlardan fotoğraflarını da hayranlarına aktarıyor. Kardashian'ın yaptığı son paylaşımda, tanga bikinisiyle plaja indiği görüldü."
    #print(type(string.printable))
    tokens = tokenize_for_char_based(text, char_set=string.printable+"üÜiİöÖğĞşŞçÇ")
    print(tokens)
    
    