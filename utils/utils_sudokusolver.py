from utils_sudoku import erstelle_sudoku, plotte
from copy import deepcopy

def initialisiere():
    eintraege = "123456789"
    liste = []
    for i in range(9):
        zeile = []
        for j in range(9):
            zeile.append(eintraege)
        liste.append(zeile)
    return liste

def einlesen(solver, sudoku_leer):
    s = deepcopy(solver)
    for i in range(9):
        for j in range(9):
            if sudoku_leer[i][j]!=" ":
                s[i][j] = sudoku_leer[i][j]
    return s

def plotte_solver(solver):
    s = deepcopy(solver)
    output = []
    for i in range(9):
        zeile = ""
        for j in range(9):
            eintrag = s[i][j]
            if len(eintrag)!=1:
                zeile = zeile+" "
            else:
                zeile = zeile+eintrag
        output.append(zeile)
    plotte(output)

def loesche_doppelte(solver):
    s = deepcopy(solver)
    for i in range(9):
        zeile = s[i]
        bekannte = ""
        for j in range(9):
            eintrag = zeile[j]
            if len(eintrag)==1:
                bekannte = bekannte+eintrag

        # Schritt 1: Finde Eintrag mit len(eintrag)>1
        for k in range(9):
            eintrag = zeile[k]
            if len(eintrag) != 1:

                # Schritt 2: Eliminiere alle "bekannte" aus "eintrag"
                for l in bekannte:
                    eintrag = eintrag.replace(str(l), "")

            # Schritt 3: Überschreibe Zeile s[i]
            s[i][k] = eintrag
    return s

def transponiere_solver(solver):
    s = deepcopy(solver)
    out = []
    for i in range(9):
        inner = []
        for j in range(9):
            inner.append(s[j][i])
        out.append(inner)
    return out

def loesche_spaltenweise(solver):
    s = deepcopy(solver)
    s = transponiere_solver(s)
    s = loesche_doppelte(s)
    s = transponiere_solver(s)
    return s

def loesche_3x3(solver):
    s = deepcopy(solver)
    bekannt = getblock(s)
    for i in range(9):
        for j in range(9):
            eintrag = s[i][j]
            if len(eintrag)>1:
                block_i = i//3
                block_j = j//3
                for zahl in bekannt[block_i][block_j]:
                    eintrag = eintrag.replace(zahl, "")
            s[i][j] = eintrag
    return s

def getblock(solver):
    s = deepcopy(solver)
    out = [["","",""],["","",""],["","",""]]
    for i in range(9):
        for j in range(9):
            eintrag = s[i][j]
            if len(eintrag)==1:
                block_i = i//3
                block_j = j//3
                out[block_i][block_j] = out[block_i][block_j]+eintrag
    return out

def loese(solver):
    s = deepcopy(solver)
    s_alt = None
    while s!=s_alt:
        s_alt = deepcopy(s)
        s = loesche_doppelte(s)
        s = loesche_spaltenweise(s)
        s = loesche_3x3(s)
    return s

def beseitige_zp(solver):
    s = deepcopy(solver)
    for i in range(9):
        zweier = []
        for j in range(9):
            if len(s[i][j])==2:
                zweier.append(s[i][j])
        if len(zweier)>1:
            loeschlist = []
            for h in range(0, len(zweier)-1):
                for k in range(h+1, len(zweier)):
                    if zweier[h]==zweier[k]:
                        loeschlist.append(zweier[h])
            if len(loeschlist)>0:
                for l in loeschlist:
                    for j in range(9):
                        if len(s[i][j])>1 and s[i][j]!=l:
                            s[i][j] = s[i][j].replace(l[0], "")
                            s[i][j] = s[i][j].replace(l[1], "")
    return s

def beseitige_zp_spalte(solver):
    s = deepcopy(solver)
    s = transponiere_solver(s)
    s = beseitige_zp(s)
    return transponiere_solver(s)

def beseitige_3x3_zp(solver):
    s = deepcopy(solver)
    s = block_zu_zeile(s)
    s = beseitige_zp(s)
    s = block_zu_zeile(s)
    return s

def block_zu_zeile(solver):
    s = deepcopy(solver)
    s_t = []

    for i in range(9):
        if i%3==0:
            s_t.append(s[i][:3])
            s_t.append(s[i][3:6])
            s_t.append(s[i][6:])
        else:
            if i%3==1:
                j = i
            else:
                j = i-1
            s_t[j-1].extend(s[i][:3])
            s_t[j].extend(s[i][3:6])
            s_t[j+1].extend(s[i][6:])
    return s_t

def loese(solver):
    s = deepcopy(solver)
    s_alt = None
    while s!=s_alt:
        s_alt = deepcopy(s)
        s = loesche_doppelte(s)
        s = loesche_spaltenweise(s)
        s = loesche_3x3(s)
        s = beseitige_zp(s)
        s = beseitige_zp_spalte(s)
        s = beseitige_3x3_zp(s)
    return s

def beseitige_3x3_zp(solver):
    s = deepcopy(solver)
    s = block_zu_zeile(s)
    s = beseitige_zp(s)
    s = block_zu_zeile(s)
    return s


def block_zu_zeile(solver):
    s = deepcopy(solver)
    s_t = []

    for i in range(9):
        if i%3==0:
            s_t.append(s[i][:3])
            s_t.append(s[i][3:6])
            s_t.append(s[i][6:])
        else:
            if i%3==1:
                j = i
            else:
                j = i-1
            #print(j)
            s_t[j-1].extend(s[i][:3])
            s_t[j].extend(s[i][3:6])
            s_t[j+1].extend(s[i][6:])
    return s_t

def brute_force(solver):
    #print("Starte brute_force")
    s = deepcopy(solver)
    s_test = deepcopy(s)
    s_geloest = deepcopy(s)
    for i in range(9):
        for j in range(9):
            s_test = deepcopy(s_geloest)
            kleinster = finde_kleinste(s_test)
            if len(s_test[i][j]) == kleinster:
                #print(s_test[i][j])
                s_test = deepcopy(s)
                eintrag = deepcopy(s_test[i][j])
                s_test[i][j] = eintrag[0]
                #print(s_test[i][j])
                s_geloest = loese(s_test)
                counter = 0
                while nicht_loesbar(s_geloest) and counter<kleinster-1:
                    counter += 1
                    s_test[i][j] = eintrag[counter]
                    s_geloest = loese(s_test)
                #print(f"starte mit {kleinster}")
                s_geloest = brute_force(s_geloest)
    return s_geloest

def finde_kleinste(solver):
    s = deepcopy(solver)
    kleinster = 10
    for i in range(9):
        for j in range(9):
            if len(s[i][j])<kleinster and len(s[i][j])>1:
                kleinster = len(s[i][j])
    return kleinster

def nicht_loesbar(solver):
    s = deepcopy(solver)
    return check_doppelt(s) or check_doppelt(transponiere_solver(s)) or check_doppelt(block_zu_zeile(s))

def check_doppelt(solver):
    s = deepcopy(solver)
    for i in range(9):
        zeichen = ""
        for j in range(9):
            if (len(s[i][j])==1 and s[i][j] in zeichen) or len(s[i][j])==0:
                #print(f"Doppelter in {i} {j}: {s[i][j]}, {zeichen}")
                return True
            else:
                zeichen += s[i][j]
    return False
