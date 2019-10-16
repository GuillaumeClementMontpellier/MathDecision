import csv
import sys

ext = ""

nlimit = -1

argument = "reel"

for arg in sys.argv:
    # Remove the "-" to just keep what is behind
    if arg == "-a" or arg == "--all":
        argument = "exhaustif"
    elif arg == "-r" or arg == "--real":
        argument = "reel"
    elif arg.find("--ext=") != -1:
        ext = arg[6:]
    elif arg.find("--number=") != -1:
        nlimit = int(arg[9:])


class Repartition:

    # Return the number of possible groups for n person
    # données: n : Int : nombre d'eleves
    # Resultat : [Int, Int] Nombre minimum et maximum de groupes (de 2 ou 3 personnes)
    @staticmethod
    def nombres_possibles_groupes(n):
        if n <= 1:
            return [0, 0]
        elif n % 6 == 0:
            return [n / 2, n / 3]
        elif n % 2 != 0:
            tmp = Repartition.nombres_possibles_groupes(n - 3)
            tmp[1] = tmp[1] + 1
            tmp[0] = tmp[0] + 1
            return tmp
        else:
            tmp = Repartition.nombres_possibles_groupes(n - 2)
            tmp[1] = tmp[1] + 1
            tmp[0] = tmp[0] + 1
            return tmp

    # Données: nb_eleves  : nombre d'eleves
    #         nb_groupes : nombre de groupes a former (de 2 ou 3 eleves)
    # Le nb_groupes doit etre entre le minimum et le maximum de nombre_groupes(nb_eleves)
    # Resultat : [Int, Int] : Nombre de groupes de 2 et de groupes de 3 respectivement
    @staticmethod
    def repartition_nombre_groupes(nb_etu, nb_groupes):
        if nb_etu % 2 == 0:
            rep = [nb_etu / 2, 0]
            while rep[0] + rep[1] > nb_groupes:
                rep[0] = rep[0] - 3
                rep[1] = rep[1] + 2
            return rep
        else:
            tmp = Repartition.repartition_nombre_groupes(nb_etu - 3, nb_groupes - 1)
            tmp[1] = tmp[1] + 1
            return tmp

    # Donnees: nbr_grps_2 : nombre de groupes de 2 eleves
    #         nbr_grps_3 : nombre de groupes de 3 eleves
    # Resultat : Int, nombre d'enumerations de (nbr_grps_2 + nbr_grps_3) eleves
    # dans nbr_grps_2 groupes de 2 et nbr_grps_3 groupes de 3
    @staticmethod
    def compter_repartitions_fixe(nbr_grps_2, nbr_grps_3):
        if nbr_grps_2 <= 1 and nbr_grps_3 <= 0:
            return 1
        elif nbr_grps_2 <= 0 and nbr_grps_3 <= 1:
            return 1
        nb_etu = (nbr_grps_2 * 2 + nbr_grps_3 * 3)
        if nbr_grps_2 > 0 and nbr_grps_3 > 0:
            small = ((nb_etu - 1) * Repartition.compter_repartitions_fixe(nbr_grps_2 - 1, nbr_grps_3))
            big = (((nb_etu - 1) * (nb_etu - 2) / 2) * Repartition.compter_repartitions_fixe(nbr_grps_2,
                                                                                             nbr_grps_3 - 1))
            return small + big
        elif nbr_grps_2 > 0:
            return (nb_etu - 1) * Repartition.compter_repartitions_fixe(nbr_grps_2 - 1, nbr_grps_3)
        else:
            return ((nb_etu - 1) * (nb_etu - 2) / 2) * Repartition.compter_repartitions_fixe(nbr_grps_2,
                                                                                             nbr_grps_3 - 1)

    @staticmethod
    def compter_repartitions(nb_etu):
        nbr_grps_possibles = Repartition.nombres_possibles_groupes(nb_etu)
        nbr_grps_max = nbr_grps_possibles[0]
        nbr_grps_min = nbr_grps_possibles[1]
        repartition_tmp = Repartition.repartition_nombre_groupes(nb_etu, nbr_grps_max)
        nbr_grps = repartition_tmp[0] + repartition_tmp[1]
        somme = 0
        while nbr_grps >= nbr_grps_min:
            somme = somme + Repartition.compter_repartitions_fixe(repartition_tmp[0], repartition_tmp[1])
            repartition_tmp[0] = repartition_tmp[0] - 3
            repartition_tmp[1] = repartition_tmp[1] + 2
            nbr_grps = repartition_tmp[0] + repartition_tmp[1]
        return somme

    #
    @staticmethod
    def repartitions_fixes(set_eleves, config):
        set_temp = set_eleves.copy()
        if config[0] <= 1 and config[1] <= 0:
            return [[[set_temp.pop(), set_temp.pop()]]]
        elif config[0] <= 0 and config[1] <= 1:
            return [[[set_temp.pop(), set_temp.pop(), set_temp.pop()]]]
        eleve = set_temp.pop()
        ret = []
        if config[0] > 0:
            for eleve2 in set_temp:
                set_temp2 = set_temp.copy()
                set_temp2.remove(eleve2)
                res_temp = Repartition.repartitions_fixes(set_temp2, [config[0] - 1, config[1]])
                for i in range(0, len(res_temp)):
                    res_temp[i].append([eleve, eleve2])
                ret.extend(res_temp)
        if config[1] > 0:
            for eleve2 in set_temp:
                set_temp2 = set_temp.copy()
                set_temp2.remove(eleve2)
                for eleve3 in set_temp2:
                    if eleve2 < eleve3:
                        set_temp3 = set_temp2.copy()
                        set_temp3.remove(eleve3)
                        res_temp = Repartition.repartitions_fixes(set_temp3, [config[0], config[1] - 1])
                        for i in range(0, len(res_temp)):
                            res_temp[i].append([eleve, eleve2, eleve3])
                        ret.extend(res_temp)
        return ret

    # Prends un set d'eleves, renvoie un tableau de tableaux de tableaux (un tableau de tableaux == une enumeration)
    #
    @staticmethod
    def toutes_repartitions(set_eleves):
        if len(set_eleves) < 2:
            return []
        else:
            nbr_grps_possibles = Repartition.nombres_possibles_groupes(len(set_eleves))
            nbr_grps_max = nbr_grps_possibles[0]
            nbr_grps_min = nbr_grps_possibles[1]
            repartitions = Repartition.repartition_nombre_groupes(len(set_eleves), nbr_grps_max)
            nbr_grps = repartitions[0] + repartitions[1]
            ret = []
            while nbr_grps >= nbr_grps_min:
                ret.extend(Repartition.repartitions_fixes(set_eleves, repartitions))
                repartitions[0] = repartitions[0] - 3
                repartitions[1] = repartitions[1] + 2
                nbr_grps = repartitions[0] + repartitions[1]
            return ret


class CSVdata:
    tab = []

    avis_map = {'TB': 5, 'B': 4, 'AB': 3, 'P': 2, 'I': 1, 'AR': 0}

    avis_ret = {5: 'TB', 4: 'B', 3: 'AB', 2: 'P', 1: 'I', 0: 'AR'}

    def __init__(self):

        preferences_csv_path = "../DONNEES/preferences" + ext + ".csv"
        try:
            with open(preferences_csv_path, newline='') as pref_file:
                result_reader = csv.reader(pref_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in result_reader:
                    self.tab.append(row)
                pref_file.close()
        except IOError:
            print("IOERROR lors de la lecture du CSV")
            sys.exit(1)

    def get_place(self, num_etu):
        for i in range(len(self.tab)):
            if num_etu == self.tab[0][i]:
                return i

    def get_avis(self, num_etu_source, num_etu_cible):
        return self.tab[self.get_place(num_etu_source)][self.get_place(num_etu_cible)]

    def get_avis_repartition(self, repartitions):
        avis_value = []
        for group in repartitions:
            for etu in group:
                autres_etu = group.copy()
                autres_etu.remove(etu)
                for etu2 in autres_etu:
                    avis_value.append(self.avis_map[self.get_avis(etu, etu2)])
        avis_value.sort()
        avis_string = []
        for i in avis_value:
            avis_string.append(self.avis_ret[i])
        return [avis_string, avis_value]

    def get_liste_etus(self, nb_etu):
        return self.tab[0][1:1 + nb_etu]


class RepartitionStat:
    repart = []
    avis = []
    nb_avis = []
    rang_med = -1
    pourc_inf = -1
    pourc_sup = -1

    def __init__(self, _repart, data_promo):

        self.repart = _repart
        self.avis = data_promo.get_avis_repartition(self.repart)
        self.rang_med = int(len(self.avis[0]) / 2)
        med_num = self.avis[1][self.rang_med]

        nb_inf = 0
        while nb_inf < len(self.avis[0]) and self.avis[1][nb_inf] < med_num:
            nb_inf += 1
        self.pourc_inf = 100 * nb_inf / float(len(self.avis[0]))

        nb_sup = 0
        while nb_sup < len(self.avis[0]) and self.avis[1][len(self.avis[0]) - nb_sup - 1] > med_num:
            nb_sup += 1
        self.pourc_sup = 100 * nb_sup / float(len(self.avis[0]))

        self.nb_avis = [0, 0, 0, 0, 0, 0]
        for val in self.avis[1]:
            self.nb_avis[val] += 1

    def med_string(self):
        return self.avis[0][self.rang_med]

    def med_val(self):
        return self.avis[1][self.rang_med]

    def signe(self):
        if self.pourc_inf > self.pourc_sup:
            return -1
        else:
            return 1


class EnsembleRepartition:
    reparts = []

    def __init__(self, repartitions, data_avis):
        for re in repartitions:
            self.reparts.append(RepartitionStat(re, data_avis))

    def max_med(self):
        max_med = -1
        top = []
        for s in self.reparts:
            if s.med_val() > max_med:
                top = []
                max_med = s.med_val()
                top.append(s)
            elif s.med_val() == max_med:
                top.append(s)
        return top

    def max_signe(self):
        repart_max = self.max_med()
        signe = -1
        top = []
        for t in repart_max:
            if t.signe() == 1:  # Si on a plus de mention strict sup a la mediane
                if signe == -1:
                    signe = 1
                    top = []
                top.append(t)
            elif signe == -1:
                top.append(t)
        return [top, signe]

    def max_score(self):
        [repart_max, signe] = self.max_signe()
        top = []
        if signe == -1:  # cas mediane est un moins
            min_inf = repart_max[0].pourc_inf
            for r in repart_max:
                if r.pourc_inf < min_inf:
                    top = [r]
                    min_inf = r.pourc_inf
                elif r.pourc_inf == min_inf:
                    top.append(r)
        else:  # cas mediane est un plus
            max_sup = repart_max[0].pourc_sup
            for r in repart_max:
                if r.pourc_sup > max_sup:
                    top = [r]
                    max_sup = r.pourc_sup
                elif r.pourc_sup == max_sup:
                    top.append(r)
        return [top, signe]

    def min_pire(self):
        removed = []
        top = self.reparts.copy()
        rep = top.copy()
        to_remove = 0
        while rep:
            top = rep.copy()
            removed = []
            for t in top:
                if t.nb_avis[to_remove] > 0:
                    rep.remove(t)
                    removed.append(t)
            to_remove += 1
        to_remove -= 1
        # removed n'est pas vide et contient toutes les répartitions r telles que:
        #   pour tout n < to_remove, r.nb_avis[n] == 0
        #   r.nb_avis[to_remove] > 0
        # On veut alors garder tout ceux qui ont le nb_avis[to_remove] minimum
        min_nb_avis = removed[0].nb_avis[to_remove]
        for r in removed:
            if r.nb_avis[to_remove] < min_nb_avis:
                min_nb_avis = r.nb_avis[to_remove]
        top = []
        for r in removed:
            if r.nb_avis[to_remove] == min_nb_avis:
                top.append(r)
        return [top, to_remove, min_nb_avis]


data = CSVdata()

nb_eleves_max = 10

liste_etus = data.get_liste_etus(nb_eleves_max)

reparts = Repartition.toutes_repartitions(liste_etus)

stat = EnsembleRepartition(reparts, data)

# Donne le tableau de toutes les répartitions au meilleur score selon le systeme d'election (et leurs stats)
# Pas le bon objectif
# output = stat.max_score()[0]

best_reparts = stat.min_pire()

output = best_reparts[0]

#for o in output:
#    print(o.repart, "\n", o.avis[0], "\n")

#print(best_reparts[2], data.avis_ret[best_reparts[1]])

# Ecrire dans 'ACL.csv'

resultat_path = "ACL.csv"

with open(resultat_path, mode="w+", newline="") as result_file:
    result_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for out in output:
        formattedRepartition = str(out.repart).replace("', '", " ").replace("'], ['", ",") \
            .replace("[", "").replace("]", "").replace("'", "")
        result_writer.writerow([formattedRepartition])

    result_file.close()
