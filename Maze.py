from random import *
import random
class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height, width, empty):
        """
        Constructeur d'un labyrinthe de height cellules de haut
        et de width cellules de large
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height    = height
        self.width     = width
        self.neighbors = {(i, j): set() for i in range(height) for j in range(width)}
        if empty :
            for i in range(self.width):
                for b in range(self.height - 1):
                    self.neighbors[(b, i)].add((b + 1, i))
                    self.neighbors[(b + 1, i)].add((b, i))
            for b in range(self.height):
                for i in range(self.width - 1):
                    self.neighbors[(b, i)].add((b, i+1))
                    self.neighbors[(b, i+1)].add((b, i))


    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt

    def add_wall(self, c1, c2):
        """
        Ajoute un mur entre deux cellules voisines dans le labyrinthe.

        Arguments :
            c1 (tuple) : Coordonnée de la première cellule (ligne, colonne)
            c2 (tuple) : Coordonnée de la deuxième cellule (ligne, colonne)

        Retour :
            Rien.
        """
      # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
               0 <= c1[1] < self.width and \
               0 <= c2[0] < self.height and \
               0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:  # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2)  # on le retire
        if c1 in self.neighbors[c2]:  # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1)  # on le retire

    def remove_wall(self, c1, c2):
        """
        Retire un mur entre deux cellules voisines dans le labyrinthe.

        Arguments :
            c1 (tuple) : Coordonnée de la première cellule (ligne, colonne)
            c2 (tuple) : Coordonnée de la deuxième cellule (ligne, colonne)

        Retour :
            Rien
        """
        assert 0 <= c1[0] < self.height and \
               0 <= c1[1] < self.width and \
               0 <= c2[0] < self.height and \
               0 <= c2[1] < self.width, \
            f"Erreur lors de la supression d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        if c2 not in self.neighbors[c1]:
            self.neighbors[c1].add(c2)
        if c1 not in self.neighbors[c2]:
            self.neighbors[c2].add(c1)

    def get_walls(self):
        """
        Retourne une liste contenant les murs du labyrinthe.

        Argument :
            Aucun

        Retour :
          Une liste de tuples représentant les coordonnées des deux cellules séparées par un mur.
          Exemple du tuple : ((ligne1, colonne1), (ligne2, colonne2))
        """
        liste_murs=[]
        for i in range (self.width):
            for b in range (self.height-1):
                if (b,i) not in self.neighbors[(b+1,i)]:
                    liste_murs.append([(b,i),(b+1,i)])
        for b in range (self.height):
            for i in range (self.width-1):
                if (b,i) not in self.neighbors[(b,i+1)]:
                    liste_murs.append([(b,i),(b,i+1)])
        return liste_murs

    def fill(self):
        """
        Enlève tous les murs du labyrinthe afin de le remplir entièrement.

        Argument :
            Aucun

        Retour :
            Rien
        """
        for i in range(self.width):
            for b in range(self.height - 1):
                    self.add_wall((b, i), (b + 1, i))
        for b in range(self.height):
            for i in range(self.width - 1):
                    self.add_wall((b, i), (b, i + 1))

    def empty(self):
        """
        Supprime tous les murs du labyrinthe.

        Arguments :
            Aucun

        Retour :
            Aucun
        """
        for i in range(self.width):
            for b in range(self.height - 1):
                self.remove_wall((b, i), (b + 1, i))
        for b in range(self.height):
            for i in range(self.width - 1):
                self.remove_wall((b, i), (b, i + 1))

    def get_contiguous_cells(self,c):
        """
        Retourne la liste des cellules contigües à la cellule c (sans s'occuper des murs existants).

        Argument :
            c (tuple) : coordonnée de la cellule dont on veut connaître les voisines (ligne, colonne)

        Retour :
            liste_contigues (list) : liste des coordonnées des cellules voisines de la cellule passée en argument.
            Cette liste peut être vide si la cellule n'a pas de voisins
        """
        liste_contigues=[]
        if (c[0]+1,c[1]) in self.neighbors :
            liste_contigues.append((c[0]+1,c[1]))
        if (c[0]-1,c[1]) in self.neighbors :
            liste_contigues.append((c[0]-1,c[1]))
        if (c[0],c[1]+1) in self.neighbors :
            liste_contigues.append((c[0],c[1]+1))
        if (c[0],c[1]-1) in self.neighbors :
            liste_contigues.append((c[0],c[1]-1))
        return liste_contigues

    def get_reachable_cells(self,c) :
        """
        Retourne la liste des cellules accessibles (cellules contigües à c qui sont dans le voisinage de c)
        depuis la cellule c.

        Argument :
            c (tuple) : coordonnée de la cellule dont on veut connaître les voisines (ligne, colonne)

        Retour :
            liste_accessibles : Liste de tuples représentant les coordonnées des cellules accessibles
        """
        liste_accessibles=[]
        voisines=self.get_contiguous_cells(c)
        for i in range (len(voisines)):
            if voisines[i] in self.neighbors[c]:
                liste_accessibles.append(voisines[i])
        return liste_accessibles

    @classmethod
    def gen_btree(self,h, w):
        """
        Génère un labyrinthe à h lignes et w colonnes en utilisant l’algorithme de construction par arbre binaire.

        Explication de l'algorithme :
        On initie un labyrinthe plein. Ensuite, pour chaque cellule, on supprime aléatoirement le mur EST ou le mur SUD,
        attention s'il y a un seul mur, supprimer ce dernier, si aucun des deux : ne rien faire.

        Arguments :
            h (int) : nombre de ligne(s) du labyrinthe
            w (int) : nombre de colonne(s) du labyrinthe

        Retour :
            labyrinthe : labyrinthe modifié par l'algorithme de construction par arbre binaire
        """
        labyrinthe = Maze(h, w, empty = False)
        for cell in labyrinthe.neighbors :  #Parcours toutes les cellules du labyrinthe
            reachable = labyrinthe.get_reachable_cells(cell)    #Cellule autour (sauf si mur)
            contiguous = labyrinthe.get_contiguous_cells(cell)  #Cellule autour (même si mur)
            if (cell[0]+1,cell[1]) not in reachable and (cell[0]+1,cell[1]) in contiguous :
                if (cell[0], cell[1] + 1) not in reachable and (cell[0], cell[1] + 1) in contiguous and randint(0,1)==1:
                    labyrinthe.remove_wall(cell,(cell[0], cell[1] + 1))
                else :
                    labyrinthe.remove_wall(cell, (cell[0] + 1, cell[1]))
        return labyrinthe

    @classmethod
    def gen_sidewinder(self, h, w):
        """
        Génère un labyrinthe à h lignes et w colonnes en utilisant l'algorithme de construction de labyrinthe
        nommé Sidewinder.

        Explication de l'algorithme :
        L'algorithme consiste à partir d'un labyrinthe "plein", puis de procéder ligne par ligne, de l'OUEST à l'EST,
        en choisissant aléatoirement de casser le mur EST d'une cellule. Pour chaque séquence de cellules voisines
        (connectées) créée sur la ligne, on casse un mur SUD au hasard d'une de ces cellules
        (une séquence peut être constituée d'une seule cellule).

        Arguments:
            h (int) : nombre de ligne(s) du labyrinthe
            w (int) : nombre de colonne(s) du labyrinthe

        Retour:
            labyrinthe : labyrinthe modifié par l'algorithme de construction Sidewinder
        """
        labyrinthe = Maze(h, w, empty=False)
        for i in range(h - 1):
            seq = []
            for j in range(w - 1):
                seq.append((i, j))
                if randint(0, 1) == 1: # Pile = 1 / Face = 0
                    labyrinthe.remove_wall((i, j), (i, j + 1))
                else:
                    cell = seq[randint(0, len(seq)-1)]
                    labyrinthe.remove_wall(cell, (cell[0] + 1, cell[1]))
                    seq = []
            seq.append((i, w - 1))
            cell = seq[randint(0, len(seq)-1)]
            labyrinthe.remove_wall(cell, (cell[0] + 1, cell[1]))
        for j in range(w - 1):
            labyrinthe.remove_wall((h - 1, j), (h - 1, j + 1))
        return labyrinthe

    @classmethod
    def gen_fusion(self,h,w):
        """
        Génère un labyrinthe à h lignes et w colonnes en utilisant l'algorithme de fusion de chemins.

        Explication de l'algorithme :
        L'algorithme consiste à partir d'un labyrinthe "plein", puis à casser des murs au
        hasard en évitant de créer des cycles. Puisqu'un labyrinthe parfait est un arbre, et qu'un arbre à n sommets a
        exactement n-1 arêtes, il suffira d'abattre n-1 murs (soit (h-1) * w + (w-1) * h si h et w désignent
        respectivement le nombre de lignes et le nombre de colonnes). Pour éviter de créer des cycles, on utilise
        un mécanisme de labélisation des cellules (avec des entiers). Lorsqu'on casse un mur depuis une cellule,
        le label de la cellule "se propage" dans la zone découverte. Mais on n'ouvrira un mur que lorsque le label de
        la cellule courante est différent du label de la cellule qui est de l'autre côté du mur.

        Arguments :
            h (int) : nombre de ligne(s) du labyrinthe
            w (int) : nombre de colonne(s) du labyrinthe

        Retour :
            labyrinthe : labyrinthe modifié par l'algorithme de fusion de chemins
        """
        labyrinthe = Maze(h, w, empty=False)
        label={}
        ind=0
        for i in labyrinthe.neighbors : # Pour toutes les cellules du labyrinthe
            ind+=1
            label[i]=ind
        mur=labyrinthe.get_walls()
        random.shuffle(mur)
        for i in range (len(mur)):
            if label[mur[i][0]]!=label[mur[i][1]]:
                labyrinthe.remove_wall(mur[i][0],mur[i][1])
                labelCellule=label[mur[i][1]]
                for valeur in label:
                    if label[valeur] == labelCellule :
                        label[valeur]=label[mur[i][0]]
        return labyrinthe

    @classmethod
    def gen_exploration(self,h,w):
        """
        Génère un labyrinthe à h lignes et w colonnes en utilisant l'algorithme d'exploration exhaustive.

        Explication de l'algorithme :
        L'algorithme consiste à partir d'un labyrinthe "plein". On choisit une cellule au hasard dans le labyrinthe
        pour la marquer et l'ajouter dans une pile (list). Tant que cette liste n'est pas vide, on prend la cellule
        située en haut de la pile et on la retire. Si cette cellule possède des voisins qui n'ont pas encore été visités
        on la remet dans la pile. On choisit ensuite (au hasard) un de ces voisins (contigues).
        On va alors casser le mur entre la cellule (retirée de la pile) et son voisin choisi. Enfin, on marque la
        cellule voisine comme "visitée", puis on la remet dans la pile.

        Arguments :
            h (int) : nombre de ligne(s) du labyrinthe
            w (int) : nombre de colonne(s) du labyrinthe

        Retour :
            labyrinthe : labyrinthe modifié par l'algorithme d'exploration exhaustive
        """
        labyrinthe = Maze(h, w, empty=False)
        visite={}
        for i in labyrinthe.neighbors:
            # lettre N attribué aux cellules non visités et O pour les cellules visités
            visite[i] = "N"
        init=(randint(0,h-1),randint(0,w-1)) #On choisit une cellule au hasard
        visite[init]="O"
        pile=[init]
        while pile!=[]: #Tant que la pile n'est pas vide
            cell=pile.pop(-1) #.pop -> Enlève de la liste l'élément situé à la position indiquée et le renvoie en valeur de retour
            voisins=labyrinthe.get_contiguous_cells(cell) # Voisins (même si mûr)
            for i in range (len(voisins)):
                if visite[voisins[0]]=="N": #Si voisin non visité
                    voisins.append(voisins.pop(0))
                    if cell not in pile: # Si cellule n'est pas dans la pile
                        pile.append(cell)
                else :
                    voisins.pop(0)
            if voisins!=[]: #Si voisins n'est pas vide
                cellVoisine=voisins[randint(0,len(voisins)-1)]
                labyrinthe.remove_wall(cell,cellVoisine)
                visite[cellVoisine]="O"
                pile.append(cellVoisine)
        return labyrinthe

    @classmethod
    def gen_wilson (self,h,w):
        """
        Génère un labyrinthe à h lignes et w colonnes en utilisant l'algorithme de Wilson.

        Explication de l'algorithme :
        L'algorithme consiste à partir d'un labyrinthe "plein". On choisit une cellule au hasard dans le labyrinthe
        et on la marque. Tant qu'il reste des cellules non marquées : on choisit une cellule de départ au hasard, parmi
        les cellules non marquées. Puis, on effectue une marche aléatoire jusqu’à ce qu’une cellule marquée
        soit atteinte (en cas de boucle, si la tête du snake se mord la queue, « couper » la boucle formée
        [autrement dit, supprimer toutes étapes depuis le précédent passage]). Enfin, on marque chaque cellule du chemin
        et casser tous les murs rencontrés, jusqu’à la cellule marquée.

        Arguments :
            h (int) : nombre de ligne(s) du labyrinthe
            w (int) : nombre de colonne(s) du labyrinthe

        Retour :
            labyrinthe : labyrinthe modifié par l'algorithme de Wilson
        """
        labyrinthe = Maze(h, w, empty=False)
        visite = []
        for i in labyrinthe.neighbors: # Pour toutes les cellules du labyrinthe
            visite.append(i)
        visite.pop(randint(0, len(visite) - 1))
        cell = visite[randint(0,len(visite)-1)]
        parcours = [cell]
        cellPrece=cell
        while visite!=[]:
            voisins = labyrinthe.get_contiguous_cells(cell)
            if cellPrece!=cell :
                voisins.remove(cellPrece)
            cellPrece=cell
            cell=voisins[randint(0,len(voisins)-1)]
            if cell in parcours :
                parcours = [cell]
            elif cell not in visite:
                for i in range (len(parcours)-1):
                    labyrinthe.remove_wall(parcours[i],parcours[i+1])
                    visite.remove(parcours[i])
                labyrinthe.remove_wall(cell, parcours[-1])
                visite.remove(parcours[-1])
                if visite!=[]:
                    cell = visite[randint(0, len(visite) - 1)]
                    parcours = [cell]
                    cellPrece=cell
            else :
                parcours.append(cell)

        return labyrinthe

    def overlay(self, content=None):
        """
        Rendu en mode texte, sur la sortie standard, \
        d'un labyrinthe avec du contenu dans les cellules
        Argument:
            content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        Retour:
            string
        """
        if content is None:
            content = {(i, j): ' ' for i in range(self.height) for j in range(self.width)}
        else:
            # Python >=3.9
            # content = content | {(i, j): ' ' for i in range(
            #    self.height) for j in range(self.width) if (i,j) not in content}
            # Python <3.9
            new_content = {(i, j): ' ' for i in range(self.height) for j in range(self.width) if (i, j) not in content}
            content = {**content, **new_content}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width - 1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width - 1):
            txt += " " + content[(0, j)] + " ┃" if (0, j + 1) not in self.neighbors[(0, j)] else " " + content[
                (0, j)] + "  "
        txt += " " + content[(0, self.width - 1)] + " ┃\n"
        # Lignes normales
        for i in range(self.height - 1):
            txt += "┣"
            for j in range(self.width - 1):
                txt += "━━━╋" if (i + 1, j) not in self.neighbors[(i, j)] else "   ╋"
            txt += "━━━┫\n" if (i + 1, self.width - 1) not in self.neighbors[(i, self.width - 1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " " + content[(i + 1, j)] + " ┃" if (i + 1, j + 1) not in self.neighbors[(i + 1, j)] else " " + \
                                                                                                                 content[
                                                                                                                     (
                                                                                                                     i + 1,
                                                                                                                     j)] + "  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width - 1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt

    def solve_dfs(self, start, stop):
        """
        Calcule le parcours le plus court afin d'atteindre la cellule stop à partir de la cellule start.

        Explication de l'algorithme :
        On utilise ici un parcours en profondeur du labyrinthe. Dans l'initialisation, on choisit la cellule de départ D
        que l'on place dans une pile et que l'on marque. Ensuite on mémorise l'élément prédécesseur de D comme étant D.
        Tant qu'il reste des cellules non marquées : on prend la première cellule (c) de la pile. Si c correspond à
        la cellule A (ou arrivée), on met fin à l'algorithme. Sinon : pour chaque voisine de c, on vérifie si elle
        n'est pas marquée pour l'ajouter dans la pile et enfin mémoriser son prédecesseur comme étant c.

        Arguments :
            start (tuple): La cellule de départ
            stop (tuple): La cellule d'arrivée
        Retour :
            Nombre minimal de déplacements nécessaires pour aller de start à stop
        """
        parcours=[]
        marque=[start]
        predecesseurs={start:start}
        while marque!=[] :
            cell=marque.pop(-1)
            if cell==stop:
                marque=[]
            else :
                temp=self.get_reachable_cells(cell)
                for i in range (len(temp)):
                    if temp[i] not in marque and temp[i]!=predecesseurs[cell]:
                        marque.append(temp[i])
                        predecesseurs[temp[i]]=cell
        cell = stop
        while cell != start:
            parcours.append(cell)
            cell=predecesseurs[cell]
        return parcours

    def solve_bfs (self, start, stop):
        """
        Calcule le parcours le plus court afin d'atteindre la cellule stop à partir de la cellule start. Ici, on utilise
        un parcours en largeur, ce qui signifie que l'algorithme va trouver différents chemins mais on gardera le plus
        cours d'entre eux

        Arguments :
             start (tuple) : La cellule de départ
             stop (tuple) : La cellule d'arrivée
        Retour :
             Nombre minimal de déplacements nécessaires pour aller de start à stop
        """
        parcours = []
        marque = [start]
        predecesseurs = {start: start}
        while marque != []:
            cell = marque.pop(0)
            voisins = self.get_reachable_cells(cell)
            for i in range (len(voisins)):
                if voisins[i] not in marque and voisins[i] != predecesseurs[cell]:
                    marque.append(voisins[i])
                    predecesseurs[voisins[i]] = cell
        cell = stop
        while cell != start:
            parcours.append(cell)
            cell = predecesseurs[cell]
        return parcours

    def solve_rhr(self, start, stop):
        """
        Génère un chemin pour aller de la cellule start à la cellule stop. Ici, on utilise l'algorithme de la main droite
        qui suit la fameuse méthode pour qu'une personne perdue retrouve la sortie d'un labyrinthe : il faut toujours
        longer les murs situés du côté de notre main droite.

        Arguments :
             start (tuple) : La cellule de départ
             stop (tuple) : La cellule d'arrivée
        Retour :
             Nombre minimal de déplacements nécessaires pour aller de start à stop
        """
        parcours = []
        marque = [start]
        predecesseurs = {start: start}
        while marque != []:
            cell = marque.pop(0)
            if cell==stop :
                marque = []
            voisins = self.get_reachable_cells(cell)
            for i in range(len(voisins)):
                if voisins[i] not in marque and voisins[i] != predecesseurs[cell]:
                    marque.append(voisins[i])
                    predecesseurs[voisins[i]] = cell
        cell = stop
        while cell != start:
            parcours.append(cell)
            cell = predecesseurs[cell]
        return parcours

    def distance_geo(self,c1, c2):
        """
        Calcule la distance géodésique entree la cellule c1 et la cellule c2. Ici, on utilise la méthode "solve_dfs"
        définie au-dessus, on calcule donc la taille du parcours le plus cours trouvée par cette dernière. Attention ici
        on prend en compte les murs présent dans le labyrinthe !

        Arguments :
            c1 (tuple): Cellule 1
            c2 (tuple): Cellule 2
        Retour :
            Nombre minimal de déplacements nécessaires pour aller de c1 à c2
        """
        return len(self.solve_dfs(c1,c2))

    def distance_man(self,c1, c2):
        """
        Calcule la distance de Manhattan entre la cellule c1 et la cellule c2.

        Explication de la distance de Manhattan :
        La distance de Manhattan est le nombre de déplacements nécessaires pour aller de la cellule c2 à la cellule
        c1 si le labyrinthe était vide. On définit la distance par la formule suivante :
        d(A,B) = |xB - xA| + |yB - yA|.
        Arguments :
            c1 (tuple): Cellule 1
            c2 (tuple): Cellule 2
        Retour :
            Nombre minimal de déplacements nécessaires pour aller de c1 à c2
        """
        return (c2[0] - c1[0]) + (c2[1] - c1[1])