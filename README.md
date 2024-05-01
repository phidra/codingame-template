Ce repo est un template servant à bootstrapper un [challenge codingame](https://www.codingame.com/contests/finished), tel que le [spring challenge 2022](https://www.codingame.com/contests/spring-challenge-2022).

Il contient du code réutilisable en python ou en rust, et des notes/conseils.

**Liens (privés) vers mes participations précédentes :**

- [codingame spring challenge 2021](https://github.com/phidra/codingame-spring-challenge-2021), ma découverte du competitive programming !
- [codingame spring challenge 2022](https://github.com/phidra/codingame-spring-challenge-2022), ma deuxième participation à un challenge, je finis dans le top 10% \o/
- [codingame fall challenge 2023](https://github.com/phidra/codingame-fall-challenge-2023), ma troisième participation, première en rust, je finis à 2.7% \o/

----


* [Faire un challenge en python](#faire-un-challenge-en-python)
* [Faire un challenge en rust](#faire-un-challenge-en-rust)
* [Notes et conseils sur le code](#notes-et-conseils-sur-le-code)
* [Notes et conseils indépendants du code](#notes-et-conseils-indépendants-du-code)

# Faire un challenge en python

Cf. [le README en python](./challenge_in_python/README.md).


# Faire un challenge en rust

Cf. [le README en rust](./challenge_in_rust/README.md).


# Notes et conseils sur le code

En vrac :

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

# Notes et conseils indépendants du code

En vrac :

- ne pas trop compter sur codingame le dernier soir : les serveurs sont chargés, et se faire ranker prend jusqu'à plusieurs heures (et même simplement tester son code dans l'IDE est lent)
- lorsque le jeu propose deux côtés, attention à tester le code dans les deux situations
- il faut un peu de temps pour s'habituer à l'interface, mais l'IDE permet de faire jouer n'importe qui contre n'importe qui, il suffit de sélectionner les joueurs :
    - notamment, en choisissant judicieusement la place de "code dans l'IDE", je peux choisir si je suis à gauche ou à droite du board
    - je peux également faire jouer mon IA actuelle contre mon IA précédente pour voir si elle est meilleure
- éviter de ne jouer que contre le boss de la league actuelle, sous peine d'overfitter ma stratégie à ses mouvements
- bien lire régulièrement les règles... ET LES LIRE ATTENTIVEMENT, en recherchant la p'tite bête ! (dans les deux challenges, j'ai "découvert" des spécificité des règles trop tardivement) (EDIT : un homme averti en vaut deux : en appliquant précautionneusement ce conseil, je n'ai rien "découvert" tardivement sur le troisième challenge `\o/` )
