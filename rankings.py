import matplotlib.pyplot as plt

# Season 1
o1Sy = [0, 26830, 52755, 78360, 103790]
o1Ay = [0, 23390, 45115, 66335, 87395]
o1By = [0, 19810, 36470, 52250, 68595]
o1Cy = [0, 13131, 18345, 21755, 25105]

# Season 2

o2Sy = [0, 28400, 55841, 83090, 110170]
o2Ay = [0, 25760, 49685, 73510, 97098]
o2By = [0, 22748, 41880, 60950, 80175]
o2Cy = [0, 16491, 23040, 31160, 37800]

# Season 3

x = [0, 1, 2, 3, 4]
Sy = [0, 29160, 57500, 85460, 113267]
Ay = [0, 26310, 50880, 74890, 98485]
By = [0, 22400, 39650, 55520, 73000]
Cy = [0, 12435, 17225, 20390, 22740]


# x = x[:-1]
# Sy = Sy[:-1]
# Ay = Ay[:-1]
# By = By[:-1]
# Cy = Cy[:-1]


def variation(y):
    return (y[-1] - y[-2]) / (y[-2] - y[-3])


def tomorrow(name, y, t):
    var = 0
    count = 0
    print(y)
    for i in range(len(y), 2, -1):
        var += variation(y[:i])
        count += 1
    var /= count
    # print(name + ":", y, "Average increase:", format(y[-1] / (len(y) - 1), "6,.0f"))
    next_day = y[-1] + ((y[-1] / (len(y) - 1)) * var)

    print("{}: {:7,.0f}".format(name, next_day))
    return [next_day]


def tomorrow2(name, y, oy):
    index = len(y)
    tom = (y[-1] / oy[index - 1]) * oy[index]
    print("{}: {:>7,.0f}".format(name, tom))
    return [tom]


def calc_next():
    global x
    global Sy
    global Ay
    global By
    global Cy
    x += [x[-1] + 1]
    Sy += tomorrow("S", Sy, o2Sy)
    Ay += tomorrow("A", Ay, o2Ay)
    By += tomorrow("B", By, o2By)
    Cy += tomorrow("C", Cy, o2Cy)


calc_next()

plt.plot(x, Sy, "b-", x, Ay, "g-", x, By, "y-", x, Cy, "r-")
plt.ylabel('Points')
plt.xlabel('Day')
plt.axis([0, 5.5, 0, Sy[-1] + 5000])
plt.grid(True)


def annotate(y):
    for a, b in zip(x, y):
        plt.text(a + .05, b - 3000, "{:.0f}".format(b))


annotate(Sy)
annotate(Ay)
annotate(By)
annotate(Cy)

plt.show()
