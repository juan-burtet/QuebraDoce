# import os

# base = "information/Resultados - TCC"

# folders = [os.path.join(base, o) for o in os.listdir(base) if os.path.isdir(os.path.join(base,o))]

# for fold in folders:
#     with open(base + "/1.txt", "a+") as f1, \
#             open(base + "/2.txt", "a+") as f2, \
#             open(base + "/3.txt", "a+") as f3:

#         # Arquivos de escrita
#         files = [f1, f2, f3]

#         for i in [1,2,3]:
#             filename = "%s/%d.txt" % (fold, i)

#             f = open(filename, "r+")
#             string = f.read()
            
#             files[i-1].write(string)
#             f.close()

#             pass
#         pass

#     pass

# import os

# base = "information/Resultados - TCC"

# with open(base + "/1.txt", "r+") as f1, \
#         open(base + "/2.txt", "r+") as f2, \
#         open(base + "/3.txt", "r+") as f3:

#     rewards = []
#     files = [f1, f2, f3]

#     for f in files:
#         lines = f.readlines()

#         data = {
#             "min": 1,
#             "max": 0,
#             "media": None,
#             "count": 0,
#             "wins": 0
#         }

#         r = 0
#         count = 0
#         for line in lines:
#             value = float(line)

#             if value == 1.0:
#                 data['wins'] += 1

#             if data["min"] > value:
#                 data['min'] = value
            
#             if data['max'] < value:
#                 data['max'] = value

#             r += value
#             count += 1

#         data['media'] = r/count
#         data['count'] = count

#         rewards.append(data)

# for r in rewards:
#     print(r)


import quebra_doce_bot as bot


maps = [
    "levels/75_75_points_protection_objective.csv",
    "levels/85_85_points_protection_objective.csv",
    "levels/95_95_points_protection_objective.csv"
]

for m in maps:

    ia = bot.QuebraDoceAI(file=m)
    print(ia.do_playouts(info=False, final=True))
