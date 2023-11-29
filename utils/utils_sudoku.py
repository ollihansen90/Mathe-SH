from random import randint, shuffle, random

def sudoku2list(text):
    return text.split("\n")

def plotte(sudoku):
    print("+"+9*"---+")
    i = 0
    for zeile in sudoku:
        z = "| "
        j = 0
        for zeichen in zeile:
            if j%3==2:
                z += zeichen+" | "
            else:
                z = z+zeichen+"   "
            j += 1
        print(z)
        if i%3==2:
            print(9*"+---"+"+")
        else:
            print(9*"+   "+"+")
        i += 1
        

def generiere_indizes(n=10, minwert=0, maxwert=80):
    assert minwert<maxwert, "minwert muss kleiner als maxwert sein"
    out = []
    # Schritt 1: Erstelle eine Liste mit den Werten von minwert bis maxwert
    liste = list(range(minwert, maxwert+1))
    #shuffle(liste)
    #out = liste[:n]

    for i in range(n):
        # Schritt 2: Ziehe eine Zufallszahl z von 0 bis len(liste)
        z = randint(0, len(liste)-1-i)
        # Schritt 3: Speichere liste[z] in out
        out.append(liste[z])
        # Schritt 4: Überschreibe liste[z] mit liste[-1]
        liste[z] = liste[-1-i]
        #print(liste)
        # Schritt 5: Wiederhole 2 und 3 und 4 (dieses Mal mit z von 0 bis len(liste)-i) n mal
    return out

def loesche_wert(sudoku, idx):
    s = sudoku.copy()
    zeile = idx//9
    spalte = idx%9
    s[zeile] = s[zeile].replace(s[zeile][spalte], " ")
    return s

def loesche_werte(sudoku, n=40):
    s = sudoku.copy()
    indizes = generiere_indizes(n, 0, 80)
    for idx in indizes:
        s = loesche_wert(s, idx)
    return s

def tausche_werte(sudoku):
    s = sudoku.copy()
    indizes = generiere_indizes(9,1,9)
    #print(indizes)
    temp = indizes[0]
    for i in range(len(s)):
        s[i] = s[i].replace(str(temp), "x")

    for j in range(1, 9):
        erster = indizes[j]
        nullter = indizes[j-1]
        for i in range(len(s)):
            s[i] = s[i].replace(str(erster), str(nullter))

    for i in range(len(s)):
        s[i] = s[i].replace("x", str(indizes[-1]))
    return s

def transponiere(sudoku):
    s = sudoku.copy()
    out = []
    for j in range(9):
        zeilentext = ""
        for i in range(9):
            zeilentext+= s[i][j]
        out.append(zeilentext)
    return out


def generiere_tauschindizes():
    out = []
    blockidc = generiere_indizes(3,0,2)
    for idx in blockidc:
        out.extend(generiere_indizes(3, idx*3+0, idx*3+2))
        #out += (generiere_indizes(3, idx*3+0, idx*3+2))
    return out

def sudoku_anordnen(sudoku, idc):
    s = sudoku.copy()
    out = []
    for idx in idc:
        out.append(s[idx])
    return out

def erstelle_sudoku(p=50):
    sudoku_string = """534678912
672195348
198342567
859761423
426853791
713924856
961537284
287419635
345286179""".split("\n")
    s = sudoku_string.copy()
    s = tausche_werte(s)
    s = sudoku_anordnen(s, generiere_tauschindizes())
    s = transponiere(s)
    s = sudoku_anordnen(s, generiere_tauschindizes())
    if random()>0.5:
        s = transponiere(s)
    s = loesche_werte(s, p)
    return s

if __name__=="__main__":
    plotte(erstelle_sudoku())
