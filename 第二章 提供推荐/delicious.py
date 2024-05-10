import json
import os
import random
import recommendations as r

# 30个用户
users = ['张伟', '王芳', '李娜', '刘强', '张敏', '王伟', '李静', '王秀英', '张静', '王勇', '李明', '张丽', '王敏',
         '李军', '张磊', '王强', '李杰', '王霞', '张涛', '王艳', '李磊', '张娟', '王平', '李婷', '张艳', '王超',
         '李秀英', '张宇', '王浩', '李娟']

def generate_data():
    file_name = "delicious-data/delicious_user_dict.json"
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            user_dict = json.load(f)
            return user_dict

    user_dict = {}
    links = []
    for line in open('delicious-data/links.txt'):
        links.append(line.strip())

    user_dict = {}
    for u in users:
        user_dict.setdefault(u, {})
        for i in range(random.randint(5, 20)):
            link = random.choice(links)
            if link not in user_dict[u]:
                user_dict[u][link] = 1.0

    for ratings in user_dict.values():
        for l in links:
            if l not in ratings:
                ratings[l] = 0.0

    with open(file_name, 'w') as outfile:
        json.dump(user_dict, outfile)

    return user_dict


if __name__ == '__main__':
    ud = generate_data()
    r = r.top_matches(ud, '王超', similarity=r.sim_pearson_np)
    print(r)
