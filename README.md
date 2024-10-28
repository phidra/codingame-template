Ce repo est mon template me servant à bootstrapper un [challenge codingame](https://www.codingame.com/contests/finished), tel que le [spring challenge 2022](https://www.codingame.com/contests/spring-challenge-2022).

Il contient du code réutilisable en python ou en rust, et des notes/conseils.

**Liens (privés) vers mes participations précédentes :**

- [codingame spring challenge 2021](https://github.com/phidra/codingame-spring-challenge-2021), ma découverte du competitive programming !
- [codingame spring challenge 2022](https://github.com/phidra/codingame-spring-challenge-2022), ma deuxième participation à un challenge, je finis dans le top 10% \o/
- [codingame fall challenge 2023](https://github.com/phidra/codingame-fall-challenge-2023), ma troisième participation, première en rust, je finis à 2.7% \o/

----


* [Faire un challenge en python](#faire-un-challenge-en-python)
* [Faire un challenge en rust](#faire-un-challenge-en-rust)
* [Notes et conseils](#notes-et-conseils)
   * [Lors des deux premiers challenges en python](#lors-des-deux-premiers-challenges-en-python)
   * [Lors du troisième challenge en rust](#lors-du-troisième-challenge-en-rust)


# Faire un challenge en python

Cf. [le README en python](./challenge_in_python/README.md).


# Faire un challenge en rust

Cf. [le README en rust](./challenge_in_rust/README.md).


# Notes et conseils

## Lors des deux premiers challenges en python

**En vrac, sur le code :**

- le contenu du repo python est très orienté vers :
    - du turn-based qui, à chaque tour, lit l'état sur `stdin`, et écrit les commandes sur `stdout`, car les deux seuls challenges que j'ai faits suivaient ce modèle
    - des heuristiques (plutôt que des algos basés sur la simulation, comme minimax ou monte-carlo tree search), car c'est ce que j'ai fait sur les deux challenges
    - du python, car c'est ce que j'ai utilisé (mais je switcherai sans doute en C++ si j'essaye des simus)
- ne tenir que très peu compte du squelette d'IA proposée par codingame (juste pour le parsing des inputs, et encore...)
- si besoin, ne pas hésiter à précalculer des trucs lourds que je peux connaître statiquement (e.g. un tableau de distance)...
- ... mais rester pragmatique et ne penser optimisation QUE si je suis confronté à des soucis de perf : ne pas hésiter à coder sous-optimalement si l'optimal est plus complexe à mettre en oeuvre.
- l'esprit est assez différent du dev dans le cadre du boulot, pour lequel la maintenabilité et l'évolutivité sont des critères majeurs : ici, surtout en fin de compétition, les trade-offs penchent en faveur du quick-and-dirty si le code reste lisible
- d'ailleurs, en fin de challenge, tout s'accélère, et je n'ai plus le temps de faire des refactos...
    - il faut bien prendre le temps de définir les types et fonctions de base de façon expressive au début et milieu de challenge
    - l'objectif visé par les refactos = ce que j'utilise beaucoup s'exprime de façon intuitive et expressive
    - l'intérêt est de pouvoir exprimer clairement ce que je veux faire (plutôt que comment le faire)
- d'ailleurs, vu qu'on les manipule tout le temps, bien choisir les noms associés aux problématiques du challenge, et privilégier les noms très courts s'ils ne perdent pas en expressivité :
    - `foe` plutôt que `enemy_hero`
    - `mob` plutôt que `monster`
    - `commando` plutôt que `troublemaker`
- python permet certes de coder de façon très expressive, mais vue la lenteur de la boucle de rétroaction (il faut des dizaines de secondes pour copier-coller son IA dans l'IDE codingame, lancer un run, et voir le résultat) il faut **impérativement** type-annoter tout le code, et flake8+mypy avant de balancer son code dans l'IDE codingame
- pour éviter les soucis, mieux vaut connaître et utiliser exactement la même version de python que le moteur codingame (pyenv FTW)
- heuristiques vs. simulation ? (e.g. sur le spring-challenge 2022, je ne maîtrisais pas assez les simus, j'ai perdu un peu de temps à les essayer, pour finalement rester sur les heuristiques) À noter que rien n'interdit de faire les deux : [ce mec l'a fait pour le spring challenge 2022](https://forum.codingame.com/t/spring-challenge-2022-feedbacks-strategies/195736/5), par exemple
- ce qui marche pas mal pour les heuristiques = appliquer des stratégies séquentiellement :
    - j'ai 3 héros auxquels il faut attribuer des actions
    - l'heuristique la plus prioritaire (e.g. shielder un héros allié actuellement contrôlé par l'ennemi) s'applique en premier
    - cette première heuristique peut soit décider d'attribuer une action à des héros, soit décider de ne rien faire, et déléguer la décision aux stratégies suivantes
    - la deuxième plus prioritaire (e.g. attaquer les mobs dans ma base) s'applique. S'il ne reste plus de héros auxquels attribuer des actions, elle failfast, sinon, elle fait son taf
    - cette deuxième heuristique décide elle aussi d'attribuer une action, ou de déléguer le boulot aux stratégies suivantes
    - etc.
    - la toute dernière stratégie est une stratégie fallback qui s'assure qu'aucun héros ne reste sans action
    - je peux aussi avoir des heuristiques en post-processing (e.g. si j'ai décidé de taper sur un mob M1, et que je peux être plus optimal en tapant à la fois sur M1 et sur M2, alors je le fais)

**En vrac, indépendant du code :**

- ne pas trop compter sur codingame le dernier soir : les serveurs sont chargés, et se faire ranker prend jusqu'à plusieurs heures (et même simplement tester son code dans l'IDE est lent)
- lorsque le jeu propose deux côtés, attention à tester le code dans les deux situations
- il faut un peu de temps pour s'habituer à l'interface, mais l'IDE permet de faire jouer n'importe qui contre n'importe qui, il suffit de sélectionner les joueurs :
    - notamment, en choisissant judicieusement la place de "code dans l'IDE", je peux choisir si je suis à gauche ou à droite du board
    - je peux également faire jouer mon IA actuelle contre mon IA précédente pour voir si elle est meilleure
- éviter de ne jouer que contre le boss de la league actuelle, sous peine d'overfitter ma stratégie à ses mouvements
- bien lire régulièrement les règles... ET LES LIRE ATTENTIVEMENT, en recherchant la p'tite bête ! (dans les deux challenges, j'ai "découvert" des spécificité des règles trop tardivement) (EDIT : un homme averti en vaut deux : en appliquant précautionneusement ce conseil, je n'ai rien "découvert" tardivement sur le troisième challenge `\o/` )
- poser une journée de congé vers la fin du jeu ? :-P

## Lors du troisième challenge en rust

- Si le jeu s'y prête, il sera toujours symétrique → en profiter ! (e.g. si je détecte un ugly à telle position, alors il y en avait un autre en miroir)
- Ce qui a bien marché :
    - ménage réguliers dans le notes pour distinguer les sujets
    - sortir de mes notes principales tout ce qui n'est pas en rapport avec des idées d'implémentation
        - (j'aurais même dû sortir dans des notes secondaires les notes de futures participations)
    - noter les sujets de perfs plutôt que les faire (vu qu'au final, j'ai eu besoin d'en faire... aucun)
        - EDIT : a posteriori, j'ai un avis encore plus radical : je n'ai JAMAIS besoin de faire des optimisations (qui sont donc toutes trop early) à la seule exception de si je fais des simulations (car dans ce cas, l'explosion combinatoire plombe les perfs)
    - regarder des bons bots jouer pour avoir des bonnes idées (c'est là où j'ai vu qu'on pouvait contourner les uglies)
- Attention : les irritants et erreurs de design reviennent me hanter en fin de challenge...
    - du coup, certains refactos non-seulement clarifient le code, mais en plus me font gagner du temps (et éviter des bugs), tout en réduisant la taille du code
    - la difficulté est de trancher entre le bon et le mauvais refacto (mauvais = qui n'en vaut pas la peine + fait trop tôt / bon = qui fait gagner du temps au final)
    - il faut trouver l'équilibre entre :
        - coder correctement trop tard (et se retrouver obligé de faire des refactos quand tout s'accélère la dernière semaine)
        - coder correctement trop tôt (et perdre du temps à faire du code clean, mais en se trompant de design car ma connaissance du jeu, de mes besoins, et des bonnes abstractions est insuffisante)
- Taille du code : j'ai perdu beaucoup de temps du challenge à améliorer incrémentalement la minification de code...
    - Avec ma façon de modéliser les choses, la taille du code devient vraiment une limitation, ça s'est vérifié à chaque challenge
    - Normalement, avec la dernière version de mon minifier rust, ça devrait passer crème même avec un gros code
    - C'est un peu custom car je hardcode des noms de variables à ne pas renommer
    - Je pourrais le généraliser (mais je pense que le jeu n'en vaut pas la chandelle) :
        1. en ne renommant pas les variables (les espaces et commentaires font déjà gagner du temps)
        2. en renommant les variables de plus de 10 caractères, je suis à peu près certain de ne pas interférer avec la stdlib.
    - **attention** : ne pas tenir compte de la limite officielle des 100k caractères car l'IDE refuse parfois des codes de moins de 100k caractères (et ça évolue même en cours de challenge !) : viser plutôt 85k
- Coder le moteur du jeu servira probablement → à faire tôt, avec des inputs simples.
    - dans la même veine : passer un peu de temps à **analyser** le moteur du jeu pour en comprendre les mécaniques fines est important
- Pour la prochaine fois, si je code le moteur du jeu, considérer que la boucle principale suit une approche fonctionnelle (plutôt que de considérer qu'elle mute un état = l'état du jeu) :
    - prend les paramètres du jeu en entrée (ici : drônes, actions, monsters, fishes)
    - produit d'autres paramètres de jeu en entrée (ici : drônes, monsters, fishes)
    - note : rester très agnostique sur ce qu'on reçoit en entrée, car le simulateur pourra être utilisé dans des conditions différentes des conditions "normales" (e.g. je ne passe qu'un unique drône en entrée pour simuler le scare des fishes, alors qu'habituellement, il y en a 4)
    - ça permet d'utiliser le moteur du jeu dans un moteur de simulation
- Organisation des tours de jeux = un point crucial qui m'a fait défaut dans les challenges précédents :
    - comprendre ce qui se passe AVANT et APRES un tour, et comprendre le lien avec ce qui est affiché à l'écran
    - pour ce challenge (et à mon avis pour les précédents et suivants aussi), le fonctionnement est un peu contre-intuitif, les actions du jeu sont décidées AVANT le tour :
        - le déplacement des monstres et fish est déjà décidé au moment où le tour de jeu commence, et il est envoyé au joueur comme input-state
        - le joueur choisit SES déplacements à partir de l'input
        - le moteur applique les déplacements de tout le monde : monstres, fish, drônes :
        - une fois tout le monde déplacé (les monstres et fish à partir de ce qui était déjà décidé avant le tour, et le joueur à partir de ses actions décidées pendant le tour), le moteur calcule le déplacement des monstres et créatures qui sera pris en compte au tour suivant
    - ce qui est contre-intuitif : à un tour donné, le comportement des monstres et fishes NE DÉPEND PAS de mes actions ! Les monstres et fishes ne réagissent à mes mouvements qu'au tour suivant.
    - Autre point important à comprendre : quand on positionne l'IHM du jeu sur un tour T, l'état affiché est celui à la fin des déplacements du tour T (i.e. après avoir bougé mes drônes tels que je l'ai demandé au tour T)

**Conseils généraux sur la stratégie globale :**

- Ce qu'il faut BEAUCOUP faire = regarder des matchs pour analyser les défaites de mon bot contre les autres bots. Attention : il faut distinguer deux choses :
    - regarder un match en particulier pour analyser UN comportement en particulier, et le débugger ou l'améliorer
    - regarder toute une série de défaites pour essayer de trouver les points les plus prioritaires à améliorer, voire les classer aussi en fonction de s'ils sont faciles à coder
- [Cette page](https://meritis.fr/codingame-spring-challenge-2022-les-best-practices-pour-etre-au-top/) donne une idée intéressante, à mieux formuler :
    > Difficile de garder la motivation encore et toujours jusqu’à la dernière minute malgré les échecs répétitifs et les soirées passées à coder dans le vent. Surtout quand, en parallèle, vous voyez votre classement baisser. Mais il faut garder la tête froide, car il suffit d’une seule bonne idée parmi des dizaines d’échecs pour vous faire gagner énormément de place.
    - NDM : c'est acceptable de "perdre" beaucoup de temps sans gagner de places si c'est pour mettre en oeuvre un "moyen" de mettre en place des stratégies, mais beaucoup moins pour une unique stratégie en particulier au gain incertain.
    - par exemple, c'est intéressant de passer plusieurs jours à développer du code pour être capable d'effrayer les poissons en général, mais pas de passer plusieurs jours à peaufiner le fait d'effrayer les poissons juste pour le début de game
    - autre exemple : c'est intéressant d'investir du code pour analyse le game-state en terme de "qui gagne quoi comme points bonus en fonction de qui sauvegarde ses scans", mais pas de passer plusieurs jours sur l'unique stratégie "je veux sauvegarder mes scans dans telle situation"
- Autre bonne idée [dans la même page](https://meritis.fr/codingame-spring-challenge-2022-les-best-practices-pour-etre-au-top/) :
    > Petit à petit, on peut construire une sorte de boîte à outil de calcul en dehors de l’algorithme.
    - NDM = c'est bien l'idée : il faut que je distingue :
        - d'un côté le code qui calcule des infos sur le jeu, ou qui effectue des actions (i.e. qui met en oeuvre des intentions)
        - de l'autre la vraie IA = le code qui utilise ces infos et ces actionneurs pour mettre en place une IA
- Très important à noter : _la compréhension du jeu et de ce qui permet de gagner évolue vraiment au fur et à mesure du challenge_ :
    - e.g. une fois que je sais farmer les poissons, éviter les monstres, et rapporter mes scans, je finis par comprendre que ce qui fait gagner, c'est de rapporter ses scans au bon moment
    - du coup je peux mettre en place des tactiques pour ça
    - conséquence : au début du challenge, il est plus important d'investir du temps dans "quelque chose PERMETTANT la mise en place de stratégies", plutôt que dans le peaufinage d'UNE stratégie en particulier
- Note a posteriori : dans le challenge, il y avait un pré-requis indispensable et pas si facile = éviter les monstres.
    -c'était presque binaire : soit tu sais éviter les uglies et tu peux faire le challenge en avançant dans les leagues, soit tu ne sais pas et tu resteras bloqué dans une des premières leagues
    -je généralise : si dans un challenge, il y a une **skill "barrière"** comme celle-ci, il faut l'adresser rapidement dans le challenge
- _Good enough_ est le meilleur compromis possible : ne pas hésiter à approximer des cercles par des carrés, à ne pas traiter du mieux possible, etc.
    - je vais plus loin : comme je ne sais que rarement si une idée est bonne / facile à mettre en œuvre, il FAUT rechercher activement des raccourcis à prendre permettant de tester l'idée
- Si je veux viser la ligue légendaire, le premier jour de l'ouverture est mon meilleur créneau.
- Les premiers jours du challenge, me contenter d'avoir un board correct.

# cg-brutaltester

J'avais commencé à utiliser [cg-brutaltester](https://github.com/dreignier/cg-brutaltester) = un tool java pour pouvoir faire jouer ses IA en local. Mes notes sont [ici](https://github.com/phidra/notes/blob/main/structured/competitive_programming/codingame_brutaltester.md), et j'ai des notes de reprise dans mon frigo.

Ça me permettrait plein de choses, et notamment de faire des refactos en étant sûr d'être iso !
