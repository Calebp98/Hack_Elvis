def Analysis(data):
    n = 0
    timestamps = []
    for frame in data:
        n +=1                       #/////  These are just dummy logic
        if frame[0] > 0:            #/////
            timestamps.append(n)    #/////
    return (timestamps)
