import csv
import sys

EXT = ""

NLIMIT = -1

ARGUMENT = "reel"

for arg0 in sys.argv:
    # Remove the "-" to just keep what is behind
    if arg0.find("--arg=") != -1:
        ARGUMENT = arg0[6:]
    elif arg0.find("--ext=") != -1:
        EXT = arg0[6:]
    elif arg0.find("--number=") != -1:
        NLIMIT = int(arg0[9:])


# Util classe pour calculer toutes les repartitions et/ou les compter
class Repartition:

    # Return the number of possible groups for n person
    # données: n : Int : nombre d'eleves
    # Resultat : [Int, Int] Nombre minimum et maximum de groupes (de 2 ou 3 personnes)
    @staticmethod
    def nombres_possibles_groupes(nb_eleves):
        if nb_eleves <= 1:
            return [0, 0]
        if nb_eleves % 6 == 0:
            return [nb_eleves / 2, nb_eleves / 3]
        if nb_eleves % 2 != 0:
            tmp = Repartition.nombres_possibles_groupes(nb_eleves - 3)
            tmp[1] = tmp[1] + 1
            tmp[0] = tmp[0] + 1
            return tmp
        tmp = Repartition.nombres_possibles_groupes(nb_eleves - 2)
        tmp[1] = tmp[1] + 1
        tmp[0] = tmp[0] + 1
        return tmp

    # Données: nb_eleves  : nombre d'eleves
    #         nb_groupes : nombre de groupes a former (de 2 ou 3 eleves)
    # pre: Le nb_groupes doit etre entre le minimum et le maximum de nombre_groupes(nb_eleves)
    # Resultat : [Int, Int] : Nombre de groupes de 2 et de groupes de 3 respectivement
    @staticmethod
    def repartition_nombre_groupes(nb_etu, nb_groupes):
        if nb_etu % 2 == 0:
            rep = [nb_etu / 2, 0]
            while rep[0] + rep[1] > nb_groupes:
                rep[0] = rep[0] - 3
                rep[1] = rep[1] + 2
            return rep
        tmp = Repartition.repartition_nombre_groupes(nb_etu - 3, nb_groupes - 1)
        tmp[1] = tmp[1] + 1
        return tmp

    # Donnees: nbr_grps_2 : nombre de groupes de 2 eleves
    #         nbr_grps_3 : nombre de groupes de 3 eleves
    # Resultat : Int, nombre de répartitions de (nbr_grps_2 + nbr_grps_3) eleves
    #            dans nbr_grps_2 groupes de 2 et nbr_grps_3 groupes de 3
    @staticmethod
    def compter_repartitions_fixe(nbr_grps_2, nbr_grps_3):
        if nbr_grps_2 <= 1 and nbr_grps_3 <= 0:
            return 1
        if nbr_grps_2 <= 0 and nbr_grps_3 <= 1:
            return 1
        nb_etu = (nbr_grps_2 * 2 + nbr_grps_3 * 3)
        if nbr_grps_2 > 0 and nbr_grps_3 > 0:
            small = Repartition.compter_repartitions_fixe(nbr_grps_2 - 1, nbr_grps_3)
            small *= (nb_etu - 1)
            big = Repartition.compter_repartitions_fixe(nbr_grps_2, nbr_grps_3 - 1)
            big *= (nb_etu - 1) * (nb_etu - 2) / 2
            return small + big
        if nbr_grps_2 > 0:
            return (nb_etu - 1) * Repartition.compter_repartitions_fixe(nbr_grps_2 - 1, nbr_grps_3)
        repart_inter = Repartition.compter_repartitions_fixe(nbr_grps_2, nbr_grps_3 - 1)
        return ((nb_etu - 1) * (nb_etu - 2) / 2) * repart_inter

    # Donnees: nbr_etu : nombre d'étudiants
    # Resultat : Int, nombre de repartitions de nbr_etu eleves
    @staticmethod
    def compter_repartitions(nb_etu):
        nbr_grps_possibles = Repartition.nombres_possibles_groupes(nb_etu)
        nbr_grps_max = nbr_grps_possibles[0]
        nbr_grps_min = nbr_grps_possibles[1]
        repartition_tmp = Repartition.repartition_nombre_groupes(nb_etu, nbr_grps_max)
        nbr_grps = repartition_tmp[0] + repartition_tmp[1]
        somme = 0
        while nbr_grps >= nbr_grps_min:
            inc = Repartition.compter_repartitions_fixe(repartition_tmp[0], repartition_tmp[1])
            somme = somme + inc
            repartition_tmp[0] = repartition_tmp[0] - 3
            repartition_tmp[1] = repartition_tmp[1] + 2
            nbr_grps = repartition_tmp[0] + repartition_tmp[1]
        return somme

    # Donnees:
    #   set_eleves : ensemble des id des étudiants à repartir
    #   config : [Int, Int] : nombre de groupe de 2 et de groupes de 3 à répartir les etudiants
    # pre :
    #   2 * config[0] + 3 * config[1] == len(set_eleves)
    # Resultat :
    #   Toutes les de répartitions de len(set_eleves) eleves
    #   dans config[0] groupes de 2 et config[1] groupes de 3
    @staticmethod
    def repartitions_fixes(set_eleves, config):
        set_temp = set_eleves.copy()
        if config[0] <= 1 and config[1] <= 0:
            return [[[set_temp.pop(), set_temp.pop()]]]
        if config[0] <= 0 and config[1] <= 1:
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
                        config_temp = [config[0], config[1] - 1]
                        res_temp = Repartition.repartitions_fixes(set_temp3, config_temp)
                        for i in range(0, len(res_temp)):
                            res_temp[i].append([eleve, eleve2, eleve3])
                        ret.extend(res_temp)
        return ret

    # Donnees: set_eleves : ensemble des id des étudiants à repartir
    # Resultat : Toutes les de répartitions de len(set_eleves) eleves possibles
    @staticmethod
    def toutes_repartitions(set_eleves):
        if len(set_eleves) < 2:
            return []
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

    @staticmethod
    def format(repart):
        form = str(repart).replace("', '", " ").replace("'], ['", ",")
        return form.replace("[", "").replace("]", "").replace("'", "")


# classe wrapper autour des données du csv à lire (pour les avis des étudiants)
class EtuPreferences:
    tab = []

    etu_map = {}

    avis_map = {'TB': 5, 'B': 4, 'AB': 3, 'P': 2, 'I': 1, 'AR': 0}

    avis_ret = {5: 'TB', 4: 'B', 3: 'AB', 2: 'P', 1: 'I', 0: 'AR'}

    # ouvre le fichier de préférences désigné par l'extension et stocke les données
    def __init__(self, extension):

        preferences_csv_path = "../DONNEES/preferences" + extension + ".csv"
        try:
            with open(preferences_csv_path, newline='') as pref_file:
                result_reader = csv.reader(pref_file, delimiter=',', quotechar='"',
                                           quoting=csv.QUOTE_MINIMAL)
                for row in result_reader:
                    self.tab.append(row)
                pref_file.close()
        except IOError:
            pref_file.close()
            print("IOERROR lors de la lecture du CSV")
            sys.exit(1)

        for i in range(1, len(self.tab[0])):
            self.etu_map[self.tab[0][i]] = i

    # Donne le rang de l'étudiant dans les données (car c'est une matrice carrée a diagonale == -1)
    def get_place(self, num_etu):
        return self.etu_map[num_etu]

    # Donne l'avis de l'etudiant source sur l'etudiant cible
    def get_avis(self, num_etu_source, num_etu_cible):
        return self.tab[self.get_place(num_etu_source)][self.get_place(num_etu_cible)]

    # Données :
    #   self : preferences étudiants
    #   repart : une répartition valide d'étudiants
    # pre :
    #   tout les étudiants de repart font bien partie de self
    # Resultat :
    #   tout les avis d'etudiants sur d'autres étudiants de leurs groupes, triées, sous 2 forme :
    #   une de int (pour comparaison / comptage), l'autre de String (pour affichage)
    #   [["AB",...],[3,...]]
    # post :
    #   len(avis[0]) == len(avis[1])
    #   pour tout i entre 0 et len(avis[0]), avis[0][i] == avis_ret[avis[1][i]]
    def get_avis_repartition(self, repart):
        avis_value = []
        for group in repart:
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


# Classe comprenant une répartition et des infos à son sujets (avis, médiane, ...)
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
        return 1


# Aggregat de RepartitionStat, qui peut donc calculer le meilleur selon l'objectif
class EnsembleRepartition:
    reparts = []

    def __init__(self, repartitions, data_avis):
        for choice in repartitions:
            self.reparts.append(RepartitionStat(choice, data_avis))

    def max_med(self):
        max_med = -1
        top = []
        for choice in self.reparts:
            if choice.med_val() > max_med:
                top = []
                max_med = choice.med_val()
                top.append(choice)
            elif choice.med_val() == max_med:
                top.append(choice)
        return top

    def max_signe(self):
        repart_max = self.max_med()
        signe = -1
        top = []
        for choice in repart_max:
            if choice.signe() == 1:  # Si on a plus de mention strict sup a la mediane
                if signe == -1:
                    signe = 1
                    top = []
                top.append(choice)
            elif signe == -1:
                top.append(choice)
        return [top, signe]

    def max_score(self):
        [repart_max, signe] = self.max_signe()
        top = []
        if signe == -1:  # cas mediane est un moins
            min_inf = repart_max[0].pourc_inf
            for choice in repart_max:
                if choice.pourc_inf < min_inf:
                    top = [choice]
                    min_inf = choice.pourc_inf
                elif choice.pourc_inf == min_inf:
                    top.append(choice)
        else:  # cas mediane est un plus
            max_sup = repart_max[0].pourc_sup
            for choice in repart_max:
                if choice.pourc_sup > max_sup:
                    top = [choice]
                    max_sup = choice.pourc_sup
                elif choice.pourc_sup == max_sup:
                    top.append(choice)
        return [top, signe]

    def min_pire(self):
        removed = []
        top = self.reparts.copy()
        rep = top.copy()
        to_remove = 0
        while rep:
            top = rep.copy()
            removed = []
            for choice in top:
                if choice.nb_avis[to_remove] > 0:
                    rep.remove(choice)
                    removed.append(choice)
            to_remove += 1
        to_remove -= 1
        # removed n'est pas vide et contient toutes les répartitions r telles que:
        #   pour tout n < to_remove, r.nb_avis[n] == 0
        #   r.nb_avis[to_remove] > 0
        # On veut alors garder tout ceux qui ont le nb_avis[to_remove] minimum
        min_nb_avis = removed[0].nb_avis[to_remove]
        for choice in removed:
            if choice.nb_avis[to_remove] < min_nb_avis:
                min_nb_avis = choice.nb_avis[to_remove]
        top = []
        for choice in removed:
            if choice.nb_avis[to_remove] == min_nb_avis:
                top.append(choice)
        return [top, to_remove, min_nb_avis]


def main(extension, nb_limit, arg):
    # Execution du prog :
    data = EtuPreferences(extension)

    nb_eleves_max = 10

    liste_etus = data.get_liste_etus(nb_eleves_max)

    best_reparts = []

    def opti(plist_etus, data_prefs):
        return [[]]

    if arg == "exhaustif":
        # Operation la plus chère
        stat = EnsembleRepartition(Repartition.toutes_repartitions(liste_etus), data)

        # Donne le tableau de toutes les répartitions au
        # meilleur score selon le systeme d'election (et leurs stats)
        # Pas le bon objectif
        # best_reparts = stat.max_score()

        best_reparts = stat.min_pire()
    else:
        # si arg est réél
        # best_reparts = opti(liste_etus, data)

        # TODO : Changer a methode opti
        stat = EnsembleRepartition(Repartition.toutes_repartitions(liste_etus), data)
        best_reparts = stat.min_pire()

    output = []

    for choice in best_reparts[0]:
        formatted = Repartition.format(choice.repart)
        output.append(formatted)

    if nb_limit != -1:
        if NLIMIT < len(output):
            output = output[:nb_limit]
            output.append("ACL, encore d'autres")

    # Ecrire dans 'ACL.csv'

    resultat_path = "ACL.csv"

    with open(resultat_path, mode="w+", newline="") as result_file:
        result_writer = csv.writer(result_file, delimiter=';', quotechar='"',
                                   quoting=csv.QUOTE_MINIMAL)

        for out in output:
            result_writer.writerow([out])

    result_file.close()


main(EXT, NLIMIT, ARGUMENT)
