def slicer(path):
    slicepath = "cuts"
    blurpath = "blurs"
    res = 5000              #The length of each snippet [ms]
    blursize = 6            #The number of snippets in a blur

    import pydub            #Enables the basics
    sound = pydub.AudioSegment.from_file(path)                              #opens the full recording as the sound variable
        sound = sound[len(sound) % res:]                                    #Removes excess length from the start to limit the files to a multiple of the resolution
        for n in range(1,(len(sound)//res)):
            snippet = sound[(n-1)*res:n*res]
            Nstr = str(n)
            for i in range(0,(len(str(len(sound)//res)))-len(str(n))):
                Nstr = "0"+str(Nstr)
            slicepath = slicepath+ str(Nstr) + ".wav"
            snippet.export(slicepath, format = "wav")

        for n in range(1,(len(sound)//res)-(blursize-1)):
            blur = sound[(n-1)*res:(n+(blursize-1))*res]
            Nstr = str(n)
            for i in range(0,(len(str(len(sound)//res)))-len(str(n))):
                Nstr = "0"+str(Nstr)
            blurpath = blurpath + str(Nstr) + ".wav"
            blur.export(blurpath, format = "wav")
