import random

def bewerte(feld):
    k = [feld[3*i:3*i+3] for i in range(3)]
    #print(*k, sep="\n")
    lose = -1
    win = 1
    # bewerte Zeilen
    for i in range(3):
        score = 0
        for j in range(3):
            score += 1 if k[i][j]=="O" else 0
            score -= 1 if k[i][j]=="X" else 0
        if score==3:
            return True, lose
        if score==-3:
            return True, win
    # bewerte Spalten
    for i in range(3):
        score = 0
        for j in range(3):
            score += 1 if k[j][i]=="O" else 0
            score -= 1 if k[j][i]=="X" else 0
        if score==3:
            return True, lose
        if score==-3:
            return True, win
    # bewerte Diag
    score = 0
    for i in range(3):
        score += 1 if k[i][i]=="O" else 0
        score -= 1 if k[i][i]=="X" else 0
    if score==3:
        return True, lose
    if score==-3:
        return True, win
    score = 0
    for i in range(3):
        score += 1 if k[i][-i-1]=="O" else 0
        score -= 1 if k[i][-i-1]=="X" else 0
    if score==3:
        return True, lose
    if score==-3:
        return True, win
    freelist = [i for i in range(9) if feld[i]==" "]
    if len(freelist)==0:
        return True, 0
    return False, 0

def minimax(curDepth, feld, maxturn):
    #print(feld)
    fertig, score = bewerte(feld)
    freelist = [i for i in range(9) if feld[i]==" "]
    #print(freelist, fertig, score)
    if fertig:
        return score#*(8-curDepth)

    if maxturn:
        s = -100
        for idx in freelist:
            feld[idx] = "X"
            s = max(s, minimax(curDepth+1, feld, False))
            feld[idx] = " "
    else:
        s = 100
        for idx in freelist:
            feld[idx] = "O"
            s = min(s, minimax(curDepth+1, feld, True))
            feld[idx] = " "
    return s

def get_movelist(feld):
    scorelist = []
    freelist = [i for i in range(9) if feld[i]==" "]
    #print(freelist)
    for idx in freelist:
        s = minimax(0, feld, True)
        #print(idx, s)
        scorelist.append([idx, s])
    return scorelist

def permute(liste):
    out = []
    n = len(liste)
    for i in range(len(liste)):
        z = int(random.random()*(n-i))
        out.append(liste[z])
        liste[z] = liste[-(i+1)]
    return out


def next_move(feld):
    bestScore = -1e10
    freelist = permute([i for i in range(9) if feld[i]==" "])
    for idx in freelist:
        feld[idx] = "X"
        score = minimax(0, feld, False)
        if score>bestScore:
            bestScore = score
            bestidx = idx
        feld[idx] = " "
    return bestidx
