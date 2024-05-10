# 课后习题
import json
import os

import recommendations as r


# tanimoto分值
def sim_tanimoto(l1, l2):
    union = len(set(l1) | (set(l2)))
    intersection = len(set(l1) & set(l2))
    if union == 0:
        return 0
    return intersection / union


# 计算相似的用户 top5
def calculate_similar_users(prefs, file_name='./user_sims.json'):
    if file_name is not None:
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                user_dict = json.load(f)
                return user_dict

    similar_users = {}
    for u in prefs:
        top5 = r.top_matches(prefs, u)
        top5_items = [(score, uid) for (score, uid) in top5 if score > 0]
        similar_users[u] = top5_items

    if file_name is not None:
        with open(file_name, 'w') as outfile:
            json.dump(similar_users, outfile)

    return similar_users


def get_recommendations(prefs, u1):
    totals = {}
    sim_sums = {}

    # 从已经计算好的相似用户中取
    sim_users = calculate_similar_users(prefs)
    for (sim, u2) in sim_users[u1]:
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


if __name__ == '__main__':
    l1 = [1, 2, 2, 1, 3, 4]
    l2 = [3, 4, 5, 6]
    # print(sim_tanimoto(l1, l2))

    # calculate_similar_users(r.critics)
    print(get_recommendations(r.critics, 'Toby'))
