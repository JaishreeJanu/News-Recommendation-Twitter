from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import csv
import pandas as pd
from nltk.corpus import wordnet
from googletrans import Translator


#source = pd.read_csv('THexplains_tweets.csv',sep = '|', encoding = 'latin-1')

documents = []

t = open("translated_tweets.csv",'a')

with open('sample_tweet.csv', 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		#print(row)
		b = "".join(str(a) for a in row)
		translator = Translator()
		lists = translator.translate(b)
		
		#print(lists)
		
		print(lists.text)
		writer = csv.writer(t)
		writer.writerow([lists.text])
		#print(lists)
		documents.extend([lists.text])



print"****Documents ARRAY*****"
print(documents)

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

true_k = 4
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print "Cluster %d:" % i,
    for ind in order_centroids[i, :6]:
        print ' %s' % terms[ind],
    print 
