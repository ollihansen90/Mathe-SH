from random import randint

bauer = 1 # 1
springer = 2 # 3
laeufer = 3 # 3
turm = 4 # 5
dame = 5 # 9
koenig = 6 # 1000
leer = 0
figuren = ["\u2659", "\u2659","\u2658","\u2657","\u2656","\u2655","\u2654","\u265A","\u265B","\u265C","\u265D","\u265E","\u265F"]
wertigkeit = [0, 1, 3, 3, 5, 9, 1000]

def flip_pos(pos):
    """
    Funktion, die das Brett dreht.
    Args:
        pos: Position des Feldes
    Returns:
        Position des Feldes nach Drehung

    Beispiel:
        "D4" wird zu "D5"
        "D5" wird zu "D4"
    """
    # Rxc7+  -> rest = Rx, pos = c7 -> Rxc2
    # g8=Q
    rest = ""
    ende = ""
    pos = pos.replace("+", "")
    if "=" in pos:
        ende = pos[-2:]
        pos = pos[:-2]
    if len(pos)>2:
        rest = pos[:-2]
        pos = pos[-2:]
    pos = pos[0]+str(9-int(pos[1]))
    return rest+pos+ende

def get_index(pos):
    """
    Funktion, die eine Position in Koordinaten übersetzt.
    Args:
        pos: Position des Feldes
    Returns:
        Liste [Zeile, Spalte]
    Beispiel:
        "D4" wird zu [3,4]
    """
    pos = pos.upper()
    assert pos[0] in "ABCDEFGH" and pos[1] in "12345678", pos+" ist keine gültige Position."

    counter = 0
    for buchstabe in "ABCDEFGH":
        if buchstabe==pos[0]:
            break
        counter += 1

    liste = [8-int(pos[1]), counter]
    return liste

class Spielfeld():
    """
    Klasse, die das Spielbrett repräsentiert.
    """
    def __init__(self):
        """
        Konstruktor, der das Spielbrett erstellt.
        """
        #self.feld = None
        self.reset()

    def reset(self):
        """
        Setzt das Spielfeld auf Anfang zurück.
        """
        self.feld = [
            [-turm, -springer, -laeufer, -dame, -koenig, -laeufer, -springer, -turm],
            [-bauer, -bauer, -bauer, -bauer, -bauer, -bauer, -bauer, -bauer],
            [leer, leer, leer, leer, leer, leer, leer, leer],
            [leer, leer, leer, leer, leer, leer, leer, leer],
            [leer, leer, leer, leer, leer, leer, leer, leer],
            [leer, leer, leer, leer, leer, leer, leer, leer],
            [bauer, bauer, bauer, bauer, bauer, bauer, bauer, bauer],
            [turm, springer, laeufer, dame, koenig, laeufer, springer, turm]
        ]

    def male(self):
        """
        Gibt das Spielfeld auf der Konsole aus.
        """
        output = ''
        bg = ["\x1b[47m", "\x1b[107m"]
        leer_farbe = ["\x1b[37m", "\x1b[97m"]
        counter = 0
        for reihe in self.feld:
            counter += 1
            for feld in reihe:
                if feld == 0:
                    output += bg[counter%2]+leer_farbe[counter%2]+figuren[feld]
                else:
                    output += bg[counter%2]+"\x1b[30m"+figuren[feld]
                counter += 1
            output += '\n'
        output += "\x1b[0m"
        print(output)

    def __getitem__(self, pos):
        """
        Gibt an, was auf einem Feld steht.
        Args:
            pos: Position des Feldes
        Returns:
            Figurenwert
        Beispiel:
            "D2" wird zu 1
        """
        liste = get_index(pos)
        return self.feld[liste[0]][liste[1]]

    def __setitem__(self, pos, value):
        """
        Setzt das Feld auf einen neuen Wert.
        Args:
            pos: Position des Feldes
            value: neuer Wert
        """
        liste = get_index(pos)
        self.feld[liste[0]][liste[1]] = value

    def flip(self):
        """
        Flippt das Spielfeld.
        """
        self.feld = self.feld[::-1]

    def invertiere(self):
        """
        Invertiert das Spielfeld.
        """
        self.flip()
        for i in range(8):
            for j in range(8):
                self.feld[i][j] = -self.feld[i][j]

def links(pos):
    """
    Bewegt nach links.
    Args:
        pos: Position des Feldes
    Returns:
        Position des Feldes nach links
    Beispiel:
        "D2" wird zu "C2"
    """
    if not pos:
        return False
    zeile = pos[1]
    spalte = pos[0]
    spalte_neu = ord(spalte)-1
    if spalte_neu>=65:
        return chr(spalte_neu)+zeile
    else:
        return False

def rechts(pos):
    """
    Bewegt nach rechts.
    Args:
        pos: Position des Feldes
    Returns:
        Position des Feldes nach rechts
    Beispiel:
        "D2" wird zu "E2"
    """
    if not pos:
        return False
    zeile = pos[1]
    spalte = pos[0]
    spalte_neu = ord(spalte)+1
    if spalte_neu<=72:
        return chr(spalte_neu)+zeile
    else:
        return False

def vor(pos):
    """
    Bewegt nach vorne.
    Args:
        pos: Position des Feldes
    Returns:
        Position des Feldes nach vorne
    Beispiel:
        "D2" wird zu "D3"
    """
    if not pos:
        return False
    zeile = pos[1]
    spalte = pos[0]
    zeile_neu = int(pos[1])+1
    if zeile_neu<=8:
        return spalte+str(zeile_neu)
    else:
        return False

def zurueck(pos):
    """
    Bewegt nach hinten.
    Args:
        pos: Position des Feldes
    Returns:
        Position des Feldes nach hinten
    Beispiel:
        "D2" wird zu "D1"
    """
    if not pos:
        return False
    zeile = pos[1]
    spalte = pos[0]
    zeile_neu = int(pos[1])-1
    if zeile_neu>=1:
        return spalte+str(zeile_neu)
    else:
        return False

def bewege_bauer(schachbrett, pos, pos_neu=None):
    """
    Bewegt einen Bauern auf bestimmter Position zu neuer Position.
    Args:
        pos: Position des Feldes
        pos_neu: Position des Feldes nach dem Zug

    """
    assert abs(schachbrett[pos])==bauer, "Hier steht kein Bauer."

    schachbrett[pos] = leer
    if pos_neu is None:
        pos_neu = get_bewegung_bauer(schachbrett, pos)
        pos_neu = pos_neu[randint(0,len(pos_neu)-1)]
    if pos_neu[-1]==8:
        schachbrett[pos_neu] = dame
    else:
        schachbrett[pos_neu] = bauer

def bewege_springer(schachbrett, pos, pos_neu=None):
    """
    Bewegt einen Springer auf bestimmter Position zu neuer Position.
    Args:
        pos: Position des Feldes
        pos_neu: Position des Feldes nach dem Zug
    """
    assert abs(schachbrett[pos])==springer, "Hier steht kein Springer."

    schachbrett[pos] = leer
    if pos_neu is None:
        pos_neu = get_bewegung_springer(schachbrett, pos)
        pos_neu = pos_neu[randint(0,len(pos_neu)-1)]
    schachbrett[pos_neu] = springer

def bewege_turm(schachbrett, pos, pos_neu=None):
    # Checkliste: Ist da Bauer? Kann er sich bewegen?
    assert abs(schachbrett[pos])==turm, "Hier steht kein Turm."

    schachbrett[pos] = leer
    if pos_neu is None:
        pos_neu = get_bewegung_turm(schachbrett, pos)
        pos_neu = pos_neu[randint(0,len(pos_neu)-1)]
    schachbrett[pos_neu] = turm

def bewege_laeufer(schachbrett, pos, pos_neu=None):
    # Checkliste: Ist da Bauer? Kann er sich bewegen?
    assert abs(schachbrett[pos])==laeufer, "Hier steht kein Läufer."

    schachbrett[pos] = leer
    if pos_neu is None:
        pos_neu = get_bewegung_laeufer(schachbrett, pos)
        pos_neu = pos_neu[randint(0,len(pos_neu)-1)]
    schachbrett[pos_neu] = laeufer

def bewege_dame(schachbrett, pos, pos_neu=None):
    # Checkliste: Ist da Bauer? Kann er sich bewegen?
    assert abs(schachbrett[pos])==dame, "Hier steht keine Dame."

    schachbrett[pos] = leer
    if pos_neu is None:
        pos_neu = get_bewegung_dame(schachbrett, pos)
        pos_neu = pos_neu[randint(0,len(pos_neu)-1)]
    schachbrett[pos_neu] = dame

def bewege_koenig(schachbrett, pos, pos_neu=None):
    # Checkliste: Ist da Bauer? Kann er sich bewegen?
    assert abs(schachbrett[pos])==koenig, "Hier steht kein König."

    schachbrett[pos] = leer
    if pos_neu is None:
        pos_neu = get_bewegung_koenig(schachbrett, pos)
        pos_neu = pos_neu[randint(0,len(pos_neu)-1)]
    schachbrett[pos_neu] = koenig

def get_bewegung_dame(schachbrett, pos):
    return get_bewegung_laeufer(schachbrett, pos)+get_bewegung_turm(schachbrett, pos)

def get_bewegung_koenig(schachbrett, pos):
    output = []
    figur = schachbrett[pos]
    # Springe 1 nach vorne
    pos_neu = vor(pos)
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    # Springe 1 nach vorne rechts
    pos_neu = vor(rechts(pos))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    # Springe 1 nach vorne links
    pos_neu = vor(links(pos))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    # Springe 1 nach rechts
    pos_neu = rechts(pos)
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    # Springe 1 nach hinten rechts
    pos_neu = rechts(zurueck(pos))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    # Springe 1 nach hinten
    pos_neu = zurueck(pos)
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    # Springe 1 nach hinten links
    pos_neu = zurueck(links(pos))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    # Springe 1 nach links
    pos_neu = links(pos)
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)

    # TODO: Rochade
    return output

def get_bewegung_bauer(schachbrett, pos):
    output = []
    figur = schachbrett[pos]
    # Springe 1 nach vorne
    pos_neu = vor(pos)
    if schachbrett[pos_neu]==leer and pos_neu:
        output.append(pos_neu)
    # Springe 2 nach vorne, falls du dich noch nicht bewegt hast
    pos_neu = vor(vor(pos))
    if pos[1]=="2" and len(output)==1 and schachbrett[pos_neu]==leer:
        output.append(pos_neu)
    # Springe 1 diagonal nach vorne, falls da ein Gegner sitzt
    # Oben rechts von B2 ist C3
    pos_neu = rechts(vor(pos))
    if pos_neu and figur*schachbrett[pos_neu]<0:
        output.append(pos_neu)
    pos_neu = links(vor(pos))
    if pos_neu and figur*schachbrett[pos_neu]<0:
        output.append(pos_neu)
    # TODO: En Passant
    return output

def get_bewegung_turm(schachbrett, pos):
    output = []
    figur = schachbrett[pos]
    # vor
    pos_neu = vor(pos)
    while pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
        if figur*schachbrett[pos_neu]<0:
            break
        pos_neu = vor(pos_neu)

    # links
    pos_neu = links(pos)
    while pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
        if figur*schachbrett[pos_neu]<0:
            break
        pos_neu = links(pos_neu)

    # rechts
    pos_neu = rechts(pos)
    while pos_neu and ((schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0)):
        output.append(pos_neu)
        if figur*schachbrett[pos_neu]<0:
            break
        pos_neu = rechts(pos_neu)

    # zurueck
    pos_neu = zurueck(pos)
    while pos_neu and ((schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0)):
        output.append(pos_neu)
        if figur*schachbrett[pos_neu]<0:
            break
        pos_neu = zurueck(pos_neu)

    # TODO: Rochade
    return output

def get_bewegung_laeufer(schachbrett, pos):
    output = []
    figur = schachbrett[pos]
    # diagonal rechts vor
    pos_neu = rechts(vor(pos))
    while pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        #print("diagonal rechts vor", pos_neu)
        output.append(pos_neu)
        if figur*schachbrett[pos_neu]<0:
            break
        pos_neu = rechts(vor(pos_neu))

    # diagonal links vor
    pos_neu = vor(links(pos))
    while pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        #print("diagonal links vor",pos_neu)
        output.append(pos_neu)
        if figur*schachbrett[pos_neu]<0:
            break
        pos_neu = vor(links(pos_neu))

    # diagonal links zurück
    pos_neu = links(zurueck(pos))
    while pos_neu and ((schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0)):
        #print("diagonal links zurück",pos_neu)
        output.append(pos_neu)
        if figur*schachbrett[pos_neu]<0:
            break
        pos_neu = links(zurueck(pos_neu))

    # diagonal rechts zurück
    pos_neu = rechts(zurueck(pos))
    while pos_neu and ((schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0)):
        #print("diagonal rechts zurück",pos_neu)
        output.append(pos_neu)
        if figur*schachbrett[pos_neu]<0:
            break
        pos_neu = rechts(zurueck(pos_neu))

    return output

def get_bewegung_springer(schachbrett, pos):
    output = []
    figur = schachbrett[pos]
    pos_neu = rechts(vor(vor(pos)))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    pos_neu = links(vor(vor(pos)))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    pos_neu = rechts(rechts(vor(pos)))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    pos_neu = rechts(rechts(zurueck(pos)))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    pos_neu = rechts(zurueck(zurueck(pos)))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    pos_neu = links(zurueck(zurueck(pos)))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    pos_neu = links(links(zurueck(pos)))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    pos_neu = links(links(vor(pos)))
    if pos_neu and (schachbrett[pos_neu]==leer or figur*schachbrett[pos_neu]<0):
        output.append(pos_neu)
    return output

def rochade(schachbrett, z):
    """
    Macht eine Rochade.
    Args:
        schachbrett: Spielfeld
        z: Richtung
    """
    # O-O-O
    # O-O
    if z=="O-O": # Kurze Rochade
        bewege_koenig(schachbrett, "E1", "G1")
        bewege_turm(schachbrett, "H1", "F1")
    elif z=="O-O-O": # Lange Rochade
        bewege_koenig(schachbrett, "E1", "C1")
        bewege_turm(schachbrett, "A1", "D1")

def get_alle_bewegungen(schachbrett):
    """
    Funktion, die alle Bewegungen bestimmt.
    Args:
        schachbrett: Spielfeld
    """
    bewegungsfunc = [
            lambda x: [z.lower() for z in get_bewegung_bauer(schachbrett,x)],
            lambda x: ["N" + z.lower() for z in get_bewegung_springer(schachbrett,x)],
            lambda x: ["B" + z.lower() for z in get_bewegung_laeufer(schachbrett,x)],
            lambda x: ["R" + z.lower() for z in get_bewegung_turm(schachbrett,x)],
            lambda x: ["Q" + z.lower() for z in get_bewegung_dame(schachbrett,x)],
            lambda x: ["K" + z.lower() for z in get_bewegung_koenig(schachbrett,x)]
        ]
    output = []
    for i in range(8):
        for j in range(8):
            figur = schachbrett.feld[i][j]
            if figur>0:
                output.extend(bewegungsfunc[figur-1]("ABCDEFGH"[j]+str(8-i)))
    return output

def zug(schachbrett, z):
    #print(z)
    if z[0]=="O":
        return rochade(schachbrett, z)
    if z[0].upper()!=z[0]:
        figur = bauer
        pos_neu = z.upper()
        get_bewegung = get_bewegung_bauer
        bewege = bewege_bauer
    elif z[0]=="K":
        figur = koenig
        pos_neu = z.upper()[-2:]
        get_bewegung = get_bewegung_koenig
        bewege = bewege_koenig
    elif z[0]=="N":
        figur = springer
        pos_neu = z.upper()[-2:]
        get_bewegung = get_bewegung_springer
        bewege = bewege_springer
    elif z[0]=="R":
        figur = turm
        pos_neu = z.upper()[-2:]
        get_bewegung = get_bewegung_turm
        bewege = bewege_turm
    elif z[0]=="B":
        figur = laeufer
        pos_neu = z.upper()[-2:]
        get_bewegung = get_bewegung_laeufer
        bewege = bewege_laeufer
    elif z[0]=="Q":
        figur = dame
        pos_neu = z.upper()[-2:]
        get_bewegung = get_bewegung_dame
        bewege = bewege_dame

    for i in range(8):
        for j in range(8):
            if schachbrett.feld[i][j]==figur:
                b = get_bewegung(schachbrett, "ABCDEFGH"[j]+str(8-i))#, "ABCDEFGH"[j]+str(8-i)
                if pos_neu in b:
                    return bewege(schachbrett, "ABCDEFGH"[j]+str(8-i), pos_neu)
    print("Ungültiger Zug.")
    return False


