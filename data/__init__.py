import pandas as pd
TurkishDataFrame = pd.read_pickle("./data/merged.gz", compression="gzip").fillna(" ")

def load_word2vec_model():
    import gensim
    Word2Vec_Model = gensim.models.Word2Vec.load("./data/word2vec_model/word2vec_gensim")
    Word2Vec_Model.wv.load_word2vec_format("./data/word2vec_model/word2vec_org",
                                        "./data/word2vec_model/vocabulary",
                                        binary=False)
    return Word2Vec_Model