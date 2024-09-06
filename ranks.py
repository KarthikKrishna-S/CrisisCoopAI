def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if (arr[j][2]/arr[j][1]) > (arr[j+1][2]/arr[j+1][1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


data = []

with open("output.txt", "w+") as f1:
    for i in f1.readlines:
        data.append(i)

localities = {
    "edapally": [0, 0],
    "kalamassery": [0, 0]
}

for i in data:
    localities[i][0] = localities[i][0] + i[1]
    localities[i][1] = localities[i][1] + i[2]

for i in localities:
    localities[i][2] = localities[i][1]/localities[i][0]

ranks = bubbleSort(list(localities))

with open("ranks.txt", "w") as f2:
    f2.writelines(ranks)