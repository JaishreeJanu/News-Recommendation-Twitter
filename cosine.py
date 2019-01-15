import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def similarityScore(vara, varb):
    documents = (vara, varb)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    cs = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    #print()
    #print()
    #print(vara)
    #print(varb)
    print("COSINE SIMILARITY : ",cs[0][1])
    set_1 = set(vara)
    set_2 = set(varb)
    n = len(set_1.intersection(set_2))
    sim = n / float(len(set_1.union(set_2)))
    print("jaccard : ", sim)
    return cs[0][1]



with open('THexplains_tweets.csv', 'rb') as f:
		reader = csv.reader(f, delimiter='|')
		
		'''for row in reader:
			doc1 = row[3]
			print "doc1"
			print(doc1)
			break'''

with open('timesofindia_tweets.csv', 'rb') as f:
		reader = csv.reader(f, delimiter='|')
		for row in reader:
			doc2 = row[3]
			print "doc2"
			print(doc2)
			similarityScore(doc1,doc2)
			
