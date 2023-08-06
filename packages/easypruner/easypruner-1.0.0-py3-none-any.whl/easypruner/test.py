a = [1,2,3,0,2,0,1,0]

for index, i in enumerate(a):
    print(index)
    if i==0:
        print(index)
        print(a)
        del(a[index])
        print(a)
