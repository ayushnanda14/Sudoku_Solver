import json
f = open("sudoku-hard.csv", "r")

lines = f.readlines()
instances = []


def difficulty(lis):
    cnt = 0
    for i in lis:
        if i == 0:
            cnt += 1
    print(cnt)
    if cnt <= 46:
        return "easy"
    elif cnt <= 49:
        return "medium"
    else:
        return "hard"


Max, Min = -1, 9
for line in range(1, 1000):
    tmp = list(lines[line].split(","))
    instances.append([tmp[1], tmp[4]])
    Max = max(Max, float(tmp[4]))
    Min = min(Min, float(tmp[4]))

f2 = open("instances.txt", "w")

data = {}
data["easy"] = []
data["medium"] = []
data["hard"] = []
print(Max, Min)
for string in instances:
    ls = []
    # print(string)
    rng = Max - Min
    for ch in string[0]:
        if ch == '.':
            ls.append(0)
        else:
            ls.append(int(ch))
    print(difficulty(ls))
    if float(string[1]) <= rng // 3:
        data['easy'].append(ls)
    elif float(string[1]) <= rng * 2 // 3:
        data['medium'].append(ls)
    else:
        data['hard'].append(ls)

N = 10
data["easy"] = data["easy"][:N]
data["medium"] = data["medium"][:N]
data["hard"] = data["hard"][:N]
jsonString = json.dumps(data)

f2.write(jsonString)

# f = open("sudoku-3m.csv","r")

# lines = f.readlines()
# instances = []

# def difficulty(lis):
#     cnt = 0
#     for i in lis:
#         if i == 0:
#             cnt+=1
#     # print(cnt)
#     if cnt <= 46:
#         return "easy"
#     elif cnt<=49:
#         return "medium"
#     else:
#         return "hard"
# Max,Min = -1,9    
# for line in range(1,1000):
#     tmp = list(lines[line].split(","))
#     instances.append([tmp[1],tmp[4]])
#     Max = max(Max,float(tmp[4]))
#     Min = min(Min,float(tmp[4]))

# f2 = open("instances.txt","w")

# data = {}
# data["easy"] = []
# data["medium"] = []
# data["hard"] = []
# print(Max,Min)
# for string in instances:
#     ls = []
#     # print(string)
#     rng = Max - Min
#     for ch in string[0]:
#         if ch == '.':
#             ls.append(0)
#         else:
#             ls.append(int(ch))
#     print(difficulty(ls))
#     if float(string[1]) <= rng // 3:
#         data['easy'].append(ls)
#     elif float(string[1]) <= rng * 2 // 3:
#         data['medium'].append(ls)
#     else:
#         data['hard'].append(ls)

# N = 10
# data["easy"] = data["easy"][:N]
# data["medium"] = data["medium"][:N]
# data["hard"] = data["hard"][:N]
# import json
# jsonString = json.dumps(data)

# f2.write(jsonString)
