"""Module pour la matiere Math de la Decision.

:authors:
    - Guillaume CLEMENT
    - Adrien ALEXANDRE
    - Arthur LEBLANC
"""

import csv
import sys


class Repartition:
    """Util classe pour calculer toutes les repartitions et/ou les compter."""

    @staticmethod
    def nombres_possibles_groupes(nb_eleves):
        """Return the number of possible groups (min and max) for nb_eleves person.

        :param nb_eleves: nombre d'eleves
        :type nb_eleves: int
        :return : Nombre minimum et maximum de groupes (de 2 ou 3 personnes)
        :rtype : [int, int]
        """
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

    @staticmethod
    def repartition_nombre_groupes(nb_etu, nb_groupes):
        """Donne une configuration de groupe.

        nb_groupes doit etre entre le minimum et le maximum de nombres_possibles_groupes(nb_etu_max)
        .. seealso:: nombres_possibles_groupes

        :param nb_groupes: nombre de groupes a former (de 2 ou 3 eleves)
        :type nb_groupes: int
        :param nb_etu: nombre d'eleves
        :type nb_etu: int
        :return : Nombre de groupes de 2 et de groupes de 3 respectivement
        :rtype : [int, int]
        """
        if nb_etu % 2 == 0:
            rep = [nb_etu / 2, 0]
            while rep[0] + rep[1] > nb_groupes:
                rep[0] = rep[0] - 3
                rep[1] = rep[1] + 2
            return rep
        tmp = Repartition.repartition_nombre_groupes(nb_etu - 3, nb_groupes - 1)
        tmp[1] = tmp[1] + 1
        return tmp

    @staticmethod
    def compter_repartitions_config(nbr_grps_2, nbr_grps_3):
        """Etant donnée une configuration, donne le nombre de répartitions de cette configuration.

        .. seealso:: compter_repartitions

        :param nbr_grps_2: nombre de groupes de 2 eleves
        :type nbr_grps_2: int
        :param nbr_grps_3: nombre de groupes de 3 eleves
        :type nbr_grps_3: int
        :return: nombre de répartitions de (nbr_grps_2 + nbr_grps_3) eleves
                 dans nbr_grps_2 groupes de 2 et nbr_grps_3 groupes de 3
        :rtype: int
        """
        if nbr_grps_2 <= 1 and nbr_grps_3 <= 0:
            return 1
        if nbr_grps_2 <= 0 and nbr_grps_3 <= 1:
            return 1
        nb_etu = (nbr_grps_2 * 2 + nbr_grps_3 * 3)
        if nbr_grps_2 > 0 and nbr_grps_3 > 0:
            small = Repartition.compter_repartitions_config(nbr_grps_2 - 1, nbr_grps_3)
            small *= (nb_etu - 1)
            big = Repartition.compter_repartitions_config(nbr_grps_2, nbr_grps_3 - 1)
            big *= (nb_etu - 1) * (nb_etu - 2) / 2
            return small + big
        if nbr_grps_2 > 0:
            repart_inter = Repartition.compter_repartitions_config(nbr_grps_2 - 1, nbr_grps_3)
            return (nb_etu - 1) * repart_inter
        repart_inter = Repartition.compter_repartitions_config(nbr_grps_2, nbr_grps_3 - 1)
        return ((nb_etu - 1) * (nb_etu - 2) / 2) * repart_inter

    @staticmethod
    def compter_repartitions(nb_etu):
        """Donne le nombre de repartitions de nb_etu_max etudiants.

        .. seealso:: compter_repartitions_config

        :param nb_etu: nombre d'étudiants
        :type nb_etu: int
        :return: nombre de repartitions de nbr_etu eleves
        :rtype: int
        """
        nbr_grps_possibles = Repartition.nombres_possibles_groupes(nb_etu)
        nbr_grps_max = nbr_grps_possibles[0]
        nbr_grps_min = nbr_grps_possibles[1]
        repartition_tmp = Repartition.repartition_nombre_groupes(nb_etu, nbr_grps_max)
        nbr_grps = repartition_tmp[0] + repartition_tmp[1]
        somme = 0
        while nbr_grps >= nbr_grps_min:
            inc = Repartition.compter_repartitions_config(repartition_tmp[0], repartition_tmp[1])
            somme = somme + inc
            repartition_tmp[0] = repartition_tmp[0] - 3
            repartition_tmp[1] = repartition_tmp[1] + 2
            nbr_grps = repartition_tmp[0] + repartition_tmp[1]
        return somme

    @staticmethod
    def repartitions_config(set_eleves, config):
        """ Donne les repartitions possibles des set_eleves etudiants dans config.

        2 * config[0] + 3 * config[1] == len(set_eleves)
        .. seealso:: toutes_repartitions

        :param set_eleves: ensemble des id des étudiants à repartir
        :type set_eleves: [str]
        :param config: nombre de groupe de 2 et de groupes de 3 à répartir les etudiants
        :type config: [int, int]
        :return: Toutes les de répartitions de len(set_eleves) eleves
                dans config[0] groupes de 2 et config[1] groupes de 3
        :rtype: [[[str]]]
        """
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
                res_temp = Repartition.repartitions_config(set_temp2, [config[0] - 1, config[1]])
                for temp in res_temp:
                    temp.append([eleve, eleve2])
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
                        res_temp = Repartition.repartitions_config(set_temp3, config_temp)
                        for temp in res_temp:
                            temp.append([eleve, eleve2, eleve3])
                        ret.extend(res_temp)
        return ret

    @staticmethod
    def toutes_repartitions(set_eleves):
        """Donne les repartitions possibles des set_eleves.

        .. seealso:: repartitions_config

        :param set_eleves: ensemble des id des étudiants à repartir
        :type set_eleves: [str]
        :return: Toutes les de répartitions de len(set_eleves) eleves possibles
        :rtype: [[[str]]]
        """
        if len(set_eleves) < 2:
            return []
        nbr_grps_possibles = Repartition.nombres_possibles_groupes(len(set_eleves))
        nbr_grps_max = nbr_grps_possibles[0]
        nbr_grps_min = nbr_grps_possibles[1]
        repartitions = Repartition.repartition_nombre_groupes(len(set_eleves), nbr_grps_max)
        nbr_grps = repartitions[0] + repartitions[1]
        ret = []
        while nbr_grps >= nbr_grps_min:
            ret.extend(Repartition.repartitions_config(set_eleves, repartitions))
            repartitions[0] = repartitions[0] - 3
            repartitions[1] = repartitions[1] + 2
            nbr_grps = repartitions[0] + repartitions[1]
        return ret

    @staticmethod
    def format(repart):
        """Formatte une repartition en cvs string.

        :param repart: une repartition d'etudiants
        :type repart: [[str]]
        :return: string formatte
        :rtype: str
        """
        form = []
        symbol = " "
        for group in repart:
            form.append(symbol.join(group))
        return form


class EtuPreferences:
    """Classe wrapper autour des données du csv à lire (pour les avis des étudiants)."""
    tab = []

    etu_map = {}

    avis_map = {'TB': 5, 'B': 4, 'AB': 3, 'P': 2, 'I': 1, 'AR': 0}

    avis_ret = {5: 'TB', 4: 'B', 3: 'AB', 2: 'P', 1: 'I', 0: 'AR'}

    def __init__(self, extension):
        """ Ouvre le fichier de préférences désigné par l'extension et stocke les données.

        :param extension: extension du fichier csv des preferences
        :type extension: str
        """
        # Read from the csv
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
        # Crée table de correspondance entre etu et position
        for i in range(1, len(self.tab[0])):
            self.etu_map[self.tab[0][i]] = i

    def get_place(self, id_etu):
        """Donne le rang de l'étudiant dans les données.

        :param id_etu: designation de l'etudiant
        :type id_etu: str
        :return: place dans la matrice
        :rtype: int
        """
        return self.etu_map[id_etu]

    def get_avis(self, id_etu_source, id_etu_cible):
        """Donne l'avis de l'etudiant source sur l'etudiant cible.

        :param id_etu_source: Juge de la relation
        :type id_etu_source: str
        :param id_etu_cible: Victime de la Relation
        :type id_etu_cible: str
        :return: avis de source sur cible
        :rtype: str
        """
        return self.tab[self.get_place(id_etu_source)][self.get_place(id_etu_cible)]

    def get_avis_repartition(self, repart):
        """Donne 2 tableaux trie d'avis.

        :Pre:
            Tout les étudiants de repart font bien partie des données

        :param repart: une répartition valide d'étudiants
        :type repart: [[str]]
        :return: tout les avis d'etudiants sur d'autres
                 étudiants de leurs groupes, triées, sous 2 forme :
                 une de int (pour comparaison / comptage),
                 l'autre de String (pour affichage)
        :rtype: [[str], [int]]

        :Post:
            len(avis[0]) == len(avis[1])
            Pour tout i entre 0 et len(avis[0]), avis[0][i] == avis_ret[avis[1][i]]
        """
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

    def get_liste_etus(self, nb_etu_max):
        """Donne la liste des etudiants des données.

        :param nb_etu_max: nombre max d'etudiants
        :type nb_etu_max: int
        :return: liste des etudiants
        :rtype: [str]
        """
        if nb_etu_max < 0:
            nb_etu_max = 0
        return self.tab[0][1:1 + nb_etu_max]


class RepartitionStat:
    """Classe comprenant une répartition et des infos à son sujet (avis, médiane, ...)."""

    repart = []
    avis = []
    nb_avis = []
    rang_med = -1
    pourc_inf = -1
    pourc_sup = -1

    def __init__(self, repart, data_promo):
        """Analyse les stats selon la promo.

        :param repart: une repartition a analyser
        :type repart: [[str]]
        :param data_promo: un ensemble de references
        :type data_promo: EtuPreferences
        """

        self.repart = repart
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
        """Donne la mediane sous forme de str."""
        return self.avis[0][self.rang_med]

    def med_val(self):
        """Donne la mediane sous forme de int."""
        return self.avis[1][self.rang_med]

    def signe(self):
        """Donne le signe selon le systeme de vote."""
        if self.pourc_inf > self.pourc_sup:
            return -1
        return 1


class EnsembleRepartition:
    """Aggregat de RepartitionStat, qui peut donc calculer le meilleur selon l'objectif."""
    reparts = []

    def __init__(self, repartitions, data_avis):
        """Analyse un ensemble de repartition.

        :param repartitions: ensemble de repartition
        :type repartitions: [[[str]]]
        :param data_avis: avis de la promo
        :type data_avis: EtuPreferences
        """
        for choice in repartitions:
            self.reparts.append(RepartitionStat(choice, data_avis))

    def max_med(self):
        """Donne les repartitions avec les meilleures medianes

        :return: ensemble de RepartitionStat
        :rtype: [RepartitionStat]
        """
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
        """Donne les repartitions avec les meilleures medianes et signe

        :return: ensemble de RepartitionStat
        :rtype: [RepartitionStat]
        """
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
        """Donne les repartitions avec les meilleures scores

        :return: ensemble de RepartitionStat
        :rtype: [RepartitionStat]
        """
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
        """Donne les repartitions avec le moins de mauvais votes (meuilleurs)

        Par exemple, [TB, TB, AB] > [B, B, AB] > [B, B, AB, AB] > [TB, TB, P]

        :return: ensemble de RepartitionStat
        :rtype: [RepartitionStat]
        """
        reparts = self.reparts
        to_remove = -1
        while to_remove < 4:  # 5 represente TB
            to_remove += 1
            min_to_remove = reparts[0].nb_avis[to_remove]
            top = []
            for choice in reparts:
                if choice.nb_avis[to_remove] < min_to_remove:
                    min_to_remove = choice.nb_avis[to_remove]
                    top = [choice]
                elif choice.nb_avis[to_remove] == min_to_remove:
                    top.append(choice)
            reparts = top
        # Important : reparts ne sera jamais vide !!
        return [reparts]


def calculate_best(preferences, how, group_name, nb_max_enum):
    """Calcule les meilleures repartitions (et les limite si besoin)"""
    nb_eleves_max = 10
    liste_etus = preferences.get_liste_etus(nb_eleves_max)
    if how == "exhaustif":
        # Operation la plus chère
        stat = EnsembleRepartition(Repartition.toutes_repartitions(liste_etus), preferences)

        # Donne le tableau de toutes les répartitions au
        # meilleur score selon le systeme d'election (et leurs stats)
        # Pas le bon objectif : best_reparts = stat.max_score()
        best_reparts = stat.min_pire()
    else:  # si arg est réél
        # TODO : Changer methode à graphe !!
        stat = EnsembleRepartition(Repartition.toutes_repartitions(liste_etus), preferences)
        best_reparts = stat.min_pire()
    if nb_max_enum != -1:
        if nb_max_enum < len(best_reparts):
            best_reparts = best_reparts[:nb_max_enum]
            best_reparts.append(group_name + ", encore d'autres")
    return best_reparts


def write_to_csv(reparts, group_name):
    """Ecrit les repartitions dans un fichier csv."""
    # formatte les repartitions
    result = []
    for best in reparts[0]:
        formatted = Repartition.format(best.repart)
        result.append(formatted)
    # Ecrire dans 'ACL.csv'
    resultat_path = group_name + ".csv"
    with open(resultat_path, mode="w+", newline="") as result_file:
        result_writer = csv.writer(result_file, delimiter=';', quotechar='"',
                                   quoting=csv.QUOTE_MINIMAL)
        for solution in result:
            result_writer.writerow(solution)

    result_file.close()

# =========================================================
# ================== Execution du script ==================
# =========================================================


# ================== Parse les arguments ==================


EXT = "IG4MD"

NLIMIT = -1

ARGUMENT = "reel"

GROUP = "ACL"

for arg0 in sys.argv:
    if arg0.find("--arg=") != -1:
        ARGUMENT = arg0[6:]
    elif arg0.find("--ext=") != -1:
        EXT = arg0[6:]
    elif arg0.find("--number=") != -1:
        NLIMIT = int(arg0[9:])


# ================== Extraction données ===================


DATA = EtuPreferences(EXT)


# ====================== Algorithme =======================


OUTPUT = calculate_best(DATA, ARGUMENT, GROUP, NLIMIT)


# ======================== Output =========================


write_to_csv(OUTPUT, GROUP)
