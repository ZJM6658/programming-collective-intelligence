import pandas as pd
import recommendations as r

# 这种方式不好，如果中间字段有分隔符，就会有问题了
# def load_movie_lens(path='./movieLens-latest-small'):
#     movies = {}
#     for line in open(path + "/movies.csv"):
#         if line.startswith('movieId'):
#             continue
#         (id, title) = line.strip().split(',')[0:2]
#         movies[id] = title
#
#     prefs = {}
#     for line in open(path + "/ratings.csv"):
#         # 跳过第一行表头
#         if line.startswith('userId'):
#             continue
#         (user, movieId, rating) = line.strip().split(',')[0:3]
#         prefs.setdefault(user, {})
#         prefs[user][movies[movieId]] = float(rating)
#     return prefs


# 使用pandas读取csv
def load_movies_lens_pd(path='./movieLens-latest-small'):
    df = pd.read_csv(path + "/movies.csv", header=0)
    movies = {}
    for idx, data in df.iterrows():
        id = data['movieId']
        title = data['title']
        movies[id] = title

    prefs = {}
    df2 = pd.read_csv(path + "/ratings.csv", header=0)
    for idx, data in df2.iterrows():
        user = int(data['userId'])
        movie_id = data['movieId']
        rating = data['rating']
        prefs.setdefault(user, {})
        prefs[user][movies[movie_id]] = float(rating)

    return prefs


if __name__ == '__main__':
    # pf = load_movie_lens()
    pf = load_movies_lens_pd()
    print(pf[87])

    item_sim = r.calculate_similar_items(pf, n=20, file_name="./movie_sims.json")
    s = r.get_recommended_items(pf, item_sim, 87)[0:30]
    print(s)
