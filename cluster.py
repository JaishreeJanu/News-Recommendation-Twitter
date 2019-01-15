from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import csv
import pandas as pd


#source = pd.read_csv('THexplains_tweets.csv',sep = '|', encoding = 'latin-1')

documents = []

with open('timesofindia_tweets.csv', 'rb') as f:
	reader = csv.reader(f, delimiter='|')
	for row in reader:
		documents.extend([row[3]])




#print(documents)

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

true_k = 7
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print "Cluster %d:" % i,
    for ind in order_centroids[i, :10]:
        print ' %s' % terms[ind],
    print 
