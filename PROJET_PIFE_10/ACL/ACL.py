import csv

ext = "IG4MD"

# Return the number of possible groups for n person
# données: n : Int : nombre d'eleves
# Resultat : [Int, Int] Nombre minimum et maximum de groupes (de 2 ou 3 personnes)
def nombres_possibles_groupes(n):
    if n <= 1:
        return [0, 0]
    elif n % 6 == 0:
        return [n / 2, n / 3]
    elif n % 2 != 0:
        tmp = nombres_possibles_groupes(n - 3)
        tmp[1] = tmp[1] + 1
        tmp[0] = tmp[0] + 1
        return tmp
    else:
        tmp = nombres_possibles_groupes(n - 2)
        tmp[1] = tmp[1] + 1
        tmp[0] = tmp[0] + 1
        return tmp


#Données: nb_eleves  : nombre d'eleves
#         nb_groupes : nombre de groupes a former (de 2 ou 3 eleves)
#Le nb_groupes doit etre entre le minimum et le maximum de nombre_groupes(nb_eleves)
#Resultat : [Int, Int] : Nombre de groupes de 2 et de groupes de 3 respectivement
def repartition_nombre_groupes(nb_eleves,nb_groupes):
    if nb_eleves % 2 == 0:
        res = [nb_eleves / 2, 0]
        while res[0] + res[1] > nb_groupes:
            res[0] = res[0] - 3
            res[1] = res[1] + 2
        return res
    else:
        tmp =  repartition_nombre_groupes(nb_eleves - 3 , nb_groupes - 1)
        tmp[1] = tmp[1] + 1
        return tmp

#Donnees: nbr_grps_2 : nombre de groupes de 2 eleves
#         nbr_grps_3 : nombre de groupes de 3 eleves
#Resultat : Int, nombre d'enumerations de (nbr_grps_2 + nbr_grps_3) eleves dans nbr_grps_2 groupes de 2 et nbr_grps_3 groupes de 3
def compter_enumerations_fixe(nbr_grps_2, nbr_grps_3):
    if nbr_grps_2 <= 1 and nbr_grps_3 <= 0:
        return 1
    elif nbr_grps_2 <= 0 and nbr_grps_3 <= 1:
        return 1
    nb_eleves = (nbr_grps_2 * 2 + nbr_grps_3 * 3)
    if nbr_grps_2 > 0 and nbr_grps_3 > 0:
        small = ( ( nb_eleves - 1) * compter_enumerations_fixe(nbr_grps_2 - 1, nbr_grps_3))
        big = ((( nb_eleves - 1) * ( nb_eleves - 2 )/ 2) * compter_enumerations_fixe(nbr_grps_2 , nbr_grps_3 - 1))
        return small + big
    elif nbr_grps_2 > 0:
        return ( ( nb_eleves - 1) * compter_enumerations_fixe(nbr_grps_2 - 1, nbr_grps_3))
    else :
        return ( ( ( nb_eleves - 1) * ( nb_eleves - 2 )/ 2) * compter_enumerations_fixe(nbr_grps_2 , nbr_grps_3 - 1))


def compter_enumerations(nb_eleves):
    nbr_grps_possibles = nombres_possibles_groupes(nb_eleves)
    nbr_grps_max = nbr_grps_possibles[0]
    nbr_grps_min = nbr_grps_possibles[1]
    repartition = repartition_nombre_groupes(nb_eleves, nbr_grps_max)
    nbr_grps = repartition[0] + repartition[1]
    sum = 0
    while nbr_grps >= nbr_grps_min:
        sum = sum + compter_enumerations_fixe(repartition[0] , repartition[1])
        repartition[0] = repartition[0] - 3
        repartition[1] = repartition[1] + 2
        nbr_grps = repartition[0] + repartition[1]
    return sum

#
def enumerations_fixes(set_eleves, repartition):
    set_temp = set_eleves.copy()
    if repartition[0] <= 1 and repartition[1] <= 0:
        return [[[set_temp.pop(), set_temp.pop()]]]
    elif repartition[0] <= 0 and repartition[1] <= 1:
        return [[[set_temp.pop(), set_temp.pop(), set_temp.pop()]]]
    eleve = set_temp.pop()
    res = []
    if repartition[0] > 0:
        for eleve2 in set_temp:
            set_temp2 = set_temp.copy()
            set_temp2.remove(eleve2)
            res_temp = enumerations_fixes(set_temp2, [repartition[0] - 1, repartition[1]])
            for i in range(0, len(res_temp)):
                res_temp[i].append([eleve, eleve2])
            res.extend(res_temp)
    if repartition[1] > 0:
        for eleve2 in set_temp:
            set_temp2 = set_temp.copy()
            set_temp2.remove(eleve2)
            for eleve3 in set_temp2:
                if eleve2 < eleve3:
                    set_temp3 = set_temp2.copy()
                    set_temp3.remove(eleve3)
                    res_temp = enumerations_fixes(set_temp3, [repartition[0], repartition[1] - 1])
                    for i in range(0, len(res_temp)):
                        res_temp[i].append([eleve, eleve2, eleve3])
                    res.extend(res_temp)
    return res


# Prends un set d'eleves, renvoie un tableau de tableaux de tableaux (un tableau de tableaux == une enumeration)
#
def enumerations(set_eleves):
    if len(set_eleves) < 2:
        return []
    else:
        nbr_grps_possibles = nombres_possibles_groupes(len(set_eleves))
        nbr_grps_max = nbr_grps_possibles[0]
        nbr_grps_min = nbr_grps_possibles[1]
        repartition = repartition_nombre_groupes(len(set_eleves), nbr_grps_max)
        nbr_grps = repartition[0] + repartition[1]
        res = []
        while nbr_grps >= nbr_grps_min:
            res.extend(enumerations_fixes(set_eleves, repartition))
            repartition[0] = repartition[0] - 3
            repartition[1] = repartition[1] + 2
            nbr_grps = repartition[0] + repartition[1]
        return res


class CSVdata:
    tab = []

    avisMap = {}

    avisRet = {}

    def __init__(self):
        self.avisMap['TB'] = 5
        self.avisMap['B'] = 4
        self.avisMap['AB'] = 3
        self.avisMap['P'] = 2
        self.avisMap['I'] = 1
        self.avisMap['AR'] = 0

        self.avisRet[5] = 'TB'
        self.avisRet[4] = 'B'
        self.avisRet[3] = 'AB'
        self.avisRet[2] = 'P'
        self.avisRet[1] = 'I'
        self.avisRet[0] = 'AR'

        preferences_csv_path = "../DONNEES/preferences" + ext + ".csv"
        try:
            with open(preferences_csv_path, newline='') as pref_file:
                result_reader = csv.reader(pref_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)                
                for row in result_reader:
                    self.tab.append(row)
                pref_file.close()
        except IOError: pass


    def getPlace(self, numEtu):
        for i in range(len(self.tab)):
            if numEtu == self.tab[0][i]:
                return i

    def getAvis(self, numEtuSource, numEtuCible):
        return self.tab[ self.getPlace(numEtuSource) ][self.getPlace(numEtuCible)]

    def getAvisRepartition(self, repartition):
        avisRepartition = []
        for group in repartition:
            for etu in group:
                autreEtu = group.copy()
                autreEtu.remove(etu)
                for etu2 in autreEtu:
                    avisRepartition.append(self.avisMap[self.getAvis(etu,etu2)])
        avisRepartition.sort()
        avis = []
        for i in avisRepartition:
            avis.append(self.avisRet[i])
        return [avis, avisRepartition]


data = CSVdata()

nb_eleves = 11

liste_etus = data.tab[0][1: 1 + nb_eleves]

reparts = enumerations(liste_etus)

stat = []

for r in reparts:
    avis = data.getAvisRepartition(r)
    rangMed = (int) (len(avis[0]) / 2)
    med = avis[0][rangMed]
    medNum = avis[1][rangMed]

    #print(avis[0])
    #print("Mediane : " + med)

    nbInf = 0
    while nbInf < len(avis[0]) and avis[1][nbInf] < medNum :
        nbInf += 1
    #print("nb inf : " + str(nbInf))
    pourcNbInf = nbInf / (float) (len(avis[0]))
    #print(pourcNbInf) 

    nbSup = 0
    while nbSup >= 0 and avis[1][ len(avis[0]) - nbSup - 1 ] > medNum :
        nbSup += 1
    #print("nb sup : " + str(nbSup))
    pourcNbSup = nbSup / (float) (len(avis[0]))
    #print(pourcNbSup)

    stat.append([r, med, pourcNbInf * 100, pourcNbSup * 100, avis, medNum])

#for s in stat:
#    print(s[0])
#    print("                                           ", s[4][0])
#    print(s[1], s[2], s[3])
#    print()

# Choix de celui avec la median max
max = 0
top = []
for s in stat:
    if s[5] > max :
        top = []
        max = s[5]
        top.append(s)
    elif s[5] == max: 
        top.append(s)

#print(len(top))

#Choix des plus / moins
signe = 0
res = []
for t in top:
    if t[3] - t[2] > 0: # Si on a plus de mention strict sup a la mediane
        if signe == 0:
            signe = 1
            res = []
        res.append(t)
    elif signe == 0:
        res.append(t)

#print(signe, len(res))

#Choix du meilleur poucentage
fin = []
if signe == 0: # cas mediane est un moins
    minInf = res[0][2]
    for r in res:
        if r[2] < minInf:
            fin = []
            fin.append(r)
            minInf = r[2]
        elif r[2] == minInf:
            fin.append(r)
else : #cas mediane est un plus
    maxSup = 0
    for r in res:
        if r[2] > maxSup:
            fin = []
            fin.append(r)
            maxSup = r[2]
        elif r[2] == maxSup:
            fin.append(r)

#for f in fin:
#    print(f)

#print(liste_etus)


#Ecrire dans 'ACL'+ext+'.csv'

# Construct the resultat path
resultat_path = "ACL.csv"

with open(resultat_path, mode="w+", newline="") as result_file:

    result_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for repartition in stat:
        formattedRepartition = str(repartition[0]).replace("', '", " ").replace("'], ['", ",").replace("[", "").replace("]", "").replace("'", "")
        row = [repartition[1], formattedRepartition]
        result_writer.writerow(row)
    
    result_writer.writerow("")

    for repartition in fin:
        formattedRepartition = str(repartition[0]).replace("', '", " ").replace("'], ['", ",").replace("[", "").replace("]", "").replace("'", "")
        result_writer.writerow(formattedRepartition)

    result_file.close()
