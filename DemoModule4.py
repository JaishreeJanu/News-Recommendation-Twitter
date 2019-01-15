import pandas as pd
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import operator #for sorting
import collections


#Tuning Parameters
max_article_count = 2 #maximum number of articles to be recommended user-item based
limit = 5   #maximum number of Hybrid recommendations
default_user_pofile = "social" #Default category to be recommended
threshold_score = 0.05  #threshold score trending for news article


def generate_recommendations(user,similar_users,rec,writer,news):
    rec_df = pd.DataFrame(rec)
    user_articles = rec_df.loc[rec_df['user_id'] == user]

    news_df = pd.DataFrame(news)
    print("User = ", user, " , ")
    print("Similar Users = ", similar_users, " ")
    print()

    articles = user_articles.articles

    dict1 = {}
    for article in articles:
        #print(article)
        a = article.split('[')
        a = a[1].split(']')
        a = a[0].split(',')
        #print("a = ",a[0])
        for ab in a:
            score = 0.7
            if ab!='':
                #print(ab, "is the article id. char at pos 0 is",ab[0])
                if ab[0]==' ':
                    ab = ab[1:]
                #print(ab, "is the article id. char at pos 0 is", ab[0])
                dict1[ab] = score

    #print(dict1)
    denominator = similar_users.__len__()
    #print(denominator)

    for user2 in similar_users:  #chh
        user_articles = rec_df.loc[rec_df['user_id'] == user2] #chh

        articles = user_articles.articles
        for article in articles:
            # print(article)
            a = article.split('[')
            a = a[1].split(']')
            a = a[0].split(',')
            for ab in a:
                if ab != '':
                    if ab[0]==' ':
                        ab = ab[1:]
                    if ab in dict1.keys():
                        dict1[ab] = dict1[ab] + 0.3/denominator
                    else:
                        dict1[ab] = 0.3/denominator

    print(dict1)

    dictionary = collections.namedtuple('recommendations', 'score news_id')
    best = sorted([dictionary(v, k) for (k, v) in dict1.items()], reverse=True)
    print(best)
    num_of_recommendations = best.__len__()
    #print(num_of_recommendations)

    rec_articles = "" #chh

    for i in range(num_of_recommendations):
        rec = best[i]
        #print(rec.news_id, "  ", rec.score)
        newsid = rec.news_id
        #print(newsid)

        rec_news_id = news_df.loc[news_df['news_id'] == int(newsid) ]
        #print(rec_news_id.news_link)

        count= 0


        for n in rec_news_id.news_link:
            count = count + 1
            #rec_articles.extend([n])
            rec_articles = rec_articles + "," + n    #chh
            if count>limit:
                break

        #rec_articles.extend([rec.news_id])
    if rec_articles != "":
        if rec_articles[0] == ',':
            rec_articles = rec_articles[1:]
        writer.writerow([user,rec_articles])
        print(rec_articles)
    else:
        writer.writerow([user,'0'])


def get_user_profile(user,profiles):
    profiles_df = pd.DataFrame(profiles)
    profile = profiles_df.loc[profiles_df['user_id'] == user]
    #print("PROFILE = ", profile.categories)
    for prof in profile.categories:
        return prof
    return default_user_pofile   #default value

def get_similar_users(user,profile,profiles):
    profiles_df = pd.DataFrame(profiles)
    similar_users = profiles_df.loc[profiles_df['categories'] == profile]
    #print("similar users : ", similar_users)
    result = []
    for user2 in similar_users.user_id:
        if user2!=user:
            result.extend([user2])
    return result


def article_recommender(df,all_users,news):
    news_df = pd.DataFrame(news)
    with open('newsIdRecommendations.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['user_id', 'articles'])
        for user in all_users:
            count = 1

            user_specific_recommendation_threshold = 0

            df2 = df.loc[(df['user_id'] == user) & df['similarity_score'] > user_specific_recommendation_threshold]
            #print("----------DATA FRAME FOR USER -----------")
            #print(df2)
            df2_size = df2.size/4
            #print("--------DATA FRAME END---------------")
            #print("Articles recommended to ", user, " : ")

            news_ids = df2['news_id']
            articles = []



            for news_id in news_ids:
                df3 = news_df.loc[news_df['news_id'] == news_id]
                #print(df3['news_link'])

                articles.extend(df3['news_id'])
                count = count + 1
                if count>max_article_count:
                    break


            #print(articles)
            writer.writerow([user, articles])



def similarityScore(vara, varb):
    documents = (vara, varb)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    cs = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    return cs[0][1]


#User File
users_cols = ['user_id', 'tweet_id', 'tweet', 'summary', 'date']
users = pd.read_csv('users.csv', sep='|', names=users_cols,encoding='latin-1')
#print(users.shape)
#print(users.head())

#print("------USER FILE END-----")

#News File
news_cols = ['news_id', 'news_link', 'summary', 'date']
news = pd.read_csv('news.csv', sep='|', names=news_cols,encoding='latin-1')
#print(news.shape)
#print(news.head())

#print("-------------NEWS FILE END----------------")


#Extract Fields For Calculating Similarity
news_summary = news.summary
tweet_summary = users.summary
#print(news_summary)
#print(tweet_summary)
#print("------------SUMMARY END-----------")


#Generating Similarity Score between tweet and news article
with open('similarity.csv', 'w') as csvfile:   #a means append, w means write from beginning
    fieldnames = ['user_id', 'tweet_id','news_id','similarity_score']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    tweet_index = 0

    for t in tweet_summary:
        news_index = 0
        for n in news_summary:
            score=similarityScore(t,n)
            uid = (users.user_id)[tweet_index]
            tid = (users.tweet_id)[tweet_index]
            nid = (news.news_id)[news_index]
            writer.writerow({'user_id': uid, 'tweet_id': tid,'news_id':nid, 'similarity_score': score})
            news_index = news_index + 1
        tweet_index = tweet_index + 1

#print("--------END OF WRITING TO SIMILARITY FILE----------")




#Article Recommendation
similarity = pd.read_csv('similarity.csv', sep=',',encoding='latin-1')
#print(similarity.shape)
#print(similarity.head())

#print("--------------SIMILARITY FILE-----------")

all_users = set(users.user_id)   #chh
df = pd.DataFrame(similarity)
df = df.groupby(['user_id']).apply(lambda x: x.sort_values(['similarity_score'], ascending = False)).reset_index(drop=True)
#print(df)
#print("---------------GROUPED AND SORTED SIMILARITY FILE-----------")


#Recommend 2 Articles
#print("---------RECOMMEND ARTICLES-----------")
article_recommender(df,all_users,news)

#Fetch articles for trending topics
trending_topics_cols = ['topics']
trending_topics = pd.read_csv('trendingTopics.csv', sep=',',names=trending_topics_cols,encoding='latin-1')  #chh
#print(trending_topics)


#print("------------TRENDING TOPICS------------")

with open('trendingRecommendations.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='|')
    for t in trending_topics.topics:
        #print(t)
        articles = "" #chh
        #articles = []
        #print(news.summary.size)
        for news_index in range(news.summary.size):
            #print((news.summary)[news_index])
            score = similarityScore(t,(news.summary)[news_index])
            if score>=threshold_score:
                articles = articles + ","  + (news.news_link)[news_index]
                #articles.extend([(news.news_link)[news_index]])
        if articles!='':
            if articles[0] == ',':
                articles = articles[1:]

        if articles=="":
            articles = "0"
        writer.writerow([t,articles])

#print("-------VERIFYING PROFILING----------")

#Finding Similar Users
profiles = pd.read_csv('userProfile.csv', sep='|',encoding='latin-1')
#print(profiles)
rec = pd.read_csv('newsIdRecommendations.csv', sep='|',encoding='latin-1')
#print(rec)

with open('finalRecommendations.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='|')

    #print("--------------------------------------------------")
    for i in range(profiles.user_id.size):      #chh
        user = (profiles.user_id)[i]            #chh
        #print(user)
        profile = get_user_profile(user,profiles)
        similar_users = get_similar_users(user,profile,profiles)
        #print(similar_users)
        #print()
        #print("---RECOMMENDATIONS-----")
        generate_recommendations(user,similar_users,rec,writer,news)