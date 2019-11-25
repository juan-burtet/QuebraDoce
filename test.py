# import quebra_doce_bot as ia

# level = "levels/75_75_points_protection_objective.csv"
# FILE = level
# print("----------")
# print("%s -> %d" % (FILE, 1))
# print("----------")

# x = []
# times = []
# with open("tests/rewards_for_simulations.csv", "w+") as f:
#     f.write("Rodada,10,25,50,100,250,500,\n")
#     for i in range(10):
#         f.write("%d," % i)
#         print(i, "-> ", end="")
#         for n in [10, 25, 50, 100, 250, 500]:
#             bot = ia.QuebraDoceAI(file=level)
#             y = bot.do_playouts(n=n, n_moves=1, info=False, final=False)
#             f.write("%.3f," % y[0])
#             if i == 0:
#                 times.append(y[1])

#             print("- %.3f - " % y[0], end="")
#         f.write("\n")
#         print("")

# print(times)

