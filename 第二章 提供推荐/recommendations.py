import json
import os
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

# 一个涉及影评者及其对几部影片评分情况的字典
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}
           }


# 欧几里得距离
def sim_distance(prefs, u1, u2):
    si = {}
    # 找到两人的共同经历
    for item in prefs[u1]:
        if item in prefs[u2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    # 差值的平方累加
    sum_of_squares = sum(pow(prefs[u1][item] - prefs[u2][item], 2) for item in si)
    # 0-1
    return 1 / (1 + sqrt(sum_of_squares))


def sim_distance_np(prefs, u1, u2):
    v1 = []
    v2 = []
    # 找到两人的共同经历
    for item in prefs[u1]:
        if item in prefs[u2]:
            v1.append(prefs[u1][item])
            v2.append(prefs[u2][item])

    if len(v1) == 0:
        return 0
    nv1 = np.array(v1)
    nv2 = np.array(v2)
    d = np.linalg.norm(nv1 - nv2)
    # d = np.sqrt(np.sum(np.square(nv1 - nv2)))
    return 1 / (1 + d)


# 皮尔逊相关系数
def sim_pearson(prefs, u1, u2):
    si = {}
    # 找到两人的共同经历
    for item in prefs[u1]:
        if item in prefs[u2]:
            si[item] = 1
    n = len(si)
    # 没有共同之处 返回1
    if n == 0:
        return 1

    sum1 = sum(prefs[u1][item] for item in si)
    sum2 = sum(prefs[u2][item] for item in si)

    # 平方和
    sum1Sq = sum(pow(prefs[u1][item], 2) for item in si)
    sum2Sq = sum(pow(prefs[u2][item], 2) for item in si)

    # 乘积之和
    pSum = sum(prefs[u1][it] * prefs[u2][it] for it in si)

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0
    r = num / den
    return r


# 严格按照公式
def sim_pearson_standard(prefs, u1, u2):
    si = {}
    # 找到两人的共同经历
    for item in prefs[u1]:
        if item in prefs[u2]:
            si[item] = 1
    n = len(si)
    # 没有共同之处 返回1
    if n == 0:
        return 1

    # 均值
    m1 = sum([prefs[u1][item] for item in si]) / n
    m2 = sum([prefs[u2][item] for item in si]) / n

    # 协方差
    cov = sum([(prefs[u1][item] - m1) * (prefs[u2][item] - m2) for item in si])

    # 标准差
    sigma1 = sqrt(sum([pow((prefs[u1][item] - m1), 2) for item in si]))
    sigma2 = sqrt(sum([pow((prefs[u2][item] - m2), 2) for item in si]))

    den = sigma1 * sigma2
    if den == 0:
        return 0
    return cov / den


def sim_pearson_np(prefs, u1, u2):
    si = {}
    # 找到两人的共同经历
    for item in prefs[u1]:
        if item in prefs[u2]:
            si[item] = 1
    n = len(si)
    # 没有共同之处 返回1
    if n == 0:
        return 1

    v1 = [prefs[u1][item] for item in si]
    v2 = [prefs[u2][item] for item in si]
    nv1 = np.array(v1)
    nv2 = np.array(v2)
    return np.corrcoef(nv1, nv2)[0][1]


# 最相似n
def top_matches(prefs, u1, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, u1, u2), u2) for u2 in prefs if u2 != u1]
    scores.sort()
    scores.reverse()
    return scores[:n]


# 利用其他人评价值的加权平均，为指定用户提供推荐
def get_recommendations(prefs, u1, similarity=sim_pearson):
    totals = {}
    sim_sums = {}

    for u2 in prefs:
        if u2 == u1:
            continue
        sim = similarity(prefs, u1, u2)
        if sim <= 0:
            continue
        for item in prefs[u2]:
            if item not in prefs[u1] or prefs[u1][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[u2][item] * sim
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

    rankings = [(totals[item] / sim_sums[item], item) for item in totals]
    rankings.sort()
    rankings.reverse()
    return rankings[:5]


# 以被评价物为主体（如电影），汇总用户费评分
def transform_prefs(prefs):
    new = {}
    for u in prefs:
        for v in prefs[u]:
            new.setdefault(v, {})
            new[v][u] = prefs[u][v]
    return new


# 计算每个物品的最相似的10个物品
def calculate_similar_items(prefs, n=10, file_name=None):
    if file_name is not None:
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                user_dict = json.load(f)
                return user_dict

    result = {}
    item_prefs = transform_prefs(prefs)
    c = 0
    for item in item_prefs:
        c += 1
        if c % 100 == 0:
            print(c, len(item_prefs))
        scores = top_matches(item_prefs, u1=item, n=n, similarity=sim_pearson)
        result[item] = scores

    # 写入文件，避免重复计算
    if file_name is not None:
        with open(file_name, 'w') as outfile:
            json.dump(result, outfile)
    return result


# 物品相似度计算 sum(物品的评分 * 相似度) / sum(相似度)
def get_recommended_items(prefs, item_match, u):
    user_ratings = prefs[u]
    scores = {}
    total_sim = {}
    for (item, rating) in user_ratings.items():
        for (sim, item2) in item_match[item]:
            # 看过的电影跳过
            if item2 in user_ratings:
                continue
            scores.setdefault(item2, 0)
            scores[item2] += sim * rating
            # 全部相似度之和
            total_sim.setdefault(item2, 0)
            total_sim[item2] += sim
    rankings = [(score / total_sim[item], item) for item, score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


if __name__ == '__main__':
    # print(sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))
    # print(sim_distance_np(critics, 'Lisa Rose', 'Gene Seymour'))
    #
    # print(sim_pearson(critics, 'Lisa Rose', 'Gene Seymour'))
    # print(sim_pearson_standard(critics, 'Lisa Rose', 'Gene Seymour'))
    # print(sim_pearson_np(critics, 'Lisa Rose', 'Gene Seymour'))
    item_sim = calculate_similar_items(critics)
    print(item_sim)
    s = get_recommended_items(critics, item_sim, 'Toby')
    print(s)
