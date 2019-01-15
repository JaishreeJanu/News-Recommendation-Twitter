import pandas as pd

trends_cols = ['topic', 'articles']
trending_topics = pd.read_csv('trendingRecommendations.csv', sep='|', names=trends_cols,encoding='latin-1')
#print(trending_topics)

trending_news = trending_topics.articles
#print(trending_news)

rec_cols = ['user_id', 'articles']
rec_articles = pd.read_csv('finalRecommendations.csv', sep='|', names=rec_cols,encoding='latin-1')
#print(rec_articles)

user_id = input('Enter user id : ')

rec_df = pd.DataFrame(rec_articles)
user_articles = rec_df.loc[rec_df['user_id'] == user_id]

print("\n------RECOMMENDED FOR YOU--------")
articles = ""

for article in user_articles.articles:
    #print(article)
    article = article.split(',')

for a in article:
    print(a)

print()

aa  = set()

print("-----------TRENDING------------")
for t in trending_news:
    #print("news")
    #print(t)
    tt = t.split(',')
    aa.update(tt)

for xy in aa:
    if xy!='0':
        print(xy)

#print(trending_topics)



