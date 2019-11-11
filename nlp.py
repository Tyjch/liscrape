from textacy.corpus import Corpus
from textacy.ke import scake

corpus = Corpus.load('en', 'data/corpus')

for doc in corpus:
    kt = scake(
        doc,
        normalize=None,
        include_pos=('NOUN', 'PROPN'),
        topn=0.5
    )

    kt = filter(lambda x: x[0][0].isupper(), kt)
    print()

    for term in kt:
        print(term[0])
