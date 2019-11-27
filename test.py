import statistics as st

filename = "tests/rewards_for_simulations.csv"

labels = [10, 25, 50, 100, 250, 500]

data = {
    i:[] for i in labels
}

with open(filename, "r+") as f:
    lines = f.readlines()

    for i, line in enumerate(lines):
        if i == 0:
            continue

        info = line.split(",")

        info = info[1:]

        for i, a in enumerate(info):
            data[labels[i]].append(float(a))

            pass

    pass

print("Desvio padrão para cada simulação:")
for key, value in data.items():
    dp = st.stdev(value)
    print("%s: %f" % (key, dp))
