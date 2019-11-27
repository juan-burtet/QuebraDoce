import quebra_doce_bot as ia

level = "levels/75_75_points_protection_objective.csv"
FILE = level
print("----------")
print("%s -> %d" % (FILE, 1))
print("----------")

x = []
times = []

    
for i in range(10):
    print(i, "-> ", end="")
    for n in [500]:
        bot = ia.QuebraDoceAI(file=level)
        y = bot.do_playouts(n=n, n_moves=1, info=False, final=True)
        
        if i == 0:
            times.append(y[1])

        print("- %.3f - " % y[0], end="")
    print("")

print(times)

