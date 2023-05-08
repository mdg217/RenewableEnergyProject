l = [2, 5, 3, 6]
ind = [i for i in range(len(l))] # oppure ind = list(range(len(l)))
new_ind = sorted(ind, key=lambda i: l[i])
new_l = [l[i] for i in new_ind]

print(new_l)