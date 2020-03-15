def Analysis(data):
    timestamps = []
    total = [0,0,0,0,0,0,0,0,0,0]
    for frame in data:
        n = 0
        for point in frame:
            print(n)
            total[n] += point
            n +=1
    maximum=0
    index = 0
    for i,value in enumerate(total):
        if value>maximum:
            maximum=value
            index=i
    highflag = 0
    N = 0
    for frame in data:
        normal = True
        for i,point in enumerate(frame):
            if i != index:
                if point > frame[index]:
                    normal = False
                    if highflag <1:
                        highflag = 3
                        timestamps.append(N+1)
        if normal:
            highflag -= 1
        N +=1
                
    return (timestamps)

#print(Analysis([[1,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,1,0,0]]))
