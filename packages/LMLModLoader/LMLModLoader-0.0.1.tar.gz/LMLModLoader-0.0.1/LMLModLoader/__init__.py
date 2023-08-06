import os

def register_mods(path):
    modsPath = os.getenv('USERPROFILE')+"\\LoudML"
    for s in os.listdir(modsPath):
        modPath = modsPath + "\\" + s
        for line in open(modpath):
            l = line.split()
            if l[0] == "setScene":
                open(f"{path}\\{l[1]}.txt","w").write(" ".join(l[2:]).replace('"',''))



        
