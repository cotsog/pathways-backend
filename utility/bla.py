import spacy
import scipy
from textacy.vsm import Vectorizer
import textacy.vsm
import sklearn.preprocessing

nlp = spacy.load('en')


doc1 = ('If you have an accident at work, get help '
        'right away. If you have a first aid attendant, '
        'call them or go to see them. Report the '
        'accident to your supervisor. If anyone '
        'witnessed (saw) the accident, you should '
        'ask them to report what they saw. You have '
        'to fill out a report form. The witness and '
        'supervisor need to sign it. If you need to see '
        'a doctor, take the accident report form with '
        'you. If you miss work because of your injury '
        'or sickness, call the WorkSafeBC claim line. '
        'Toll-free: 1 888 967-5377 (1 888 WORKERS)')

doc2 = ('If you have an accident at work, get help '
        'right away. If you have a first aid attendant, '
        'call them or go to see them. Report the '
        'accident to your supervisor.')

doc3 = 'This is an accidental test'

docs = [doc1, doc2, doc3]

spacy_docs = [nlp(doc) for doc in docs]
tokenized_docs = ([tok.lemma_ for tok in doc] for doc in spacy_docs)
vectorizer = Vectorizer(tf_type='linear', apply_idf=True, idf_type='smooth', apply_dl=False)
term_matrix = vectorizer.fit_transform(tokenized_docs)

print(vectorizer.vocabulary_terms)
print([word for word in spacy_docs[0]])
print(term_matrix.toarray())


def dupe(matrix):
    return scipy.sparse.csr_matrix(matrix)


def compute_cosine_doc_similarities(matrix):
    normalized_matrix = sklearn.preprocessing.normalize(matrix, axis=1)
    return normalized_matrix * normalized_matrix.T


def compute_cosine_term_similarities(matrix):
    normalized_matrix = sklearn.preprocessing.normalize(matrix, axis=0)
    return normalized_matrix.T * normalized_matrix


# term_matrix -> pass it through ANNOY (github.com/spotify/annoy) -- approximate nearest neighbours, oh yeah

doc_similarities = dupe(term_matrix).dot(dupe(term_matrix).transpose())
cosine_doc_similarities = compute_cosine_doc_similarities(dupe(term_matrix))
term_similarities = dupe(term_matrix).transpose().dot(dupe(term_matrix))
cosine_term_similarities = compute_cosine_term_similarities(dupe(term_matrix))

print('Doc similarities')
print(doc_similarities.toarray())
print('Cosine doc similarities')
print(cosine_doc_similarities.toarray())
print('Term similarities')
print(term_similarities.toarray())
print('Cosine term similarities')
print(cosine_term_similarities.toarray())
