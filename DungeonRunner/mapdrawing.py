m = [[0 for x in range(20)] for x in range(15)]
sy = 0
sx = 10
m[sy][sx] = 1

ey = 14
ex = 2
m[ey][ex] = 2

vd = ey - (sy + 1)
hd = ex - sx
hd *= 1

previous = [sy, sx]

while hd > 0 or vd > 0:
    if hd == 0:
        for x in range(vd):
            m[previous[0] + 1][previous[1]] = 3
            previous[0] += 1
            vd -= 1
    elif vd == 0:
        for x in range(hd):
            m[previous[0]][previous[1] - 1] = 3
            # this is assuming end is to the left of start
            previous[1] -= 1
            hd -= 1
    else:
        m[previous[0] + 1][previous[1]] = 3
        previous[0] += 1
        vd -= 1

for i, row in enumerate(m):
    print(i, ' '.join(str(row)))
