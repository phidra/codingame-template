* [How to use](#how-to-use)
* [Contenu du repo](#contenu-du-repo)
   * [merge and copy](#merge-and-copy)
   * [sticky logs](#sticky-logs)
   * [perfs et mesure du temps d'exécution](#perfs-et-mesure-du-temps-dexécution)
   * [reste à faire](#reste-à-faire)


# How to use

- créer un repo pour le nouveau challenge
- y copier-coller le contenu du template (y compris les fichiers cachés comme `.gitignore` et `.pre-commit-config.yaml`)
- mettre à jour le readme
- connaître la version de python utilisée par le moteur codingame :
    ```python
    import sys
    print(sys.version_info)
    ```
- adapter la version de python dans la config pre-commit :
- définir un virtualenv pyenv + installer les outils :
    ```sh
    pyenv install 3.9.12
    pyenv virtualenv 3.9.12 codingame-spring-2022
    pyenv local codingame-spring-2022
    python -m pip install -r requirements.txt
    ```
- adapter le code de parsing des inputs, et les notes, et au boulot !

# Contenu du repo

En vrac, ce repo contient :

- config : `.gitignore`, `.pre-commit-config.yaml`, `setup.cfg`, ...
- le script `check_merge_and_copy.sh` pour pouvoir coder dans des fichiers séparés tout en ne soumettant qu'un unique fichier de code
- un squelette basique de code =
    - `TOMERGE_board.py` = un squelette de classe pour stocker l'état du jeu
    - `TOMERGE_game.py` = un moteur simple qui joue des tours en boucle infinie, où chaque tour :
        - parse les inputs sur `stdin`
        - mets à jour le board
        - décide quoi faire
        - produit la sortie correspondante sur `stdout`
    - `TOMERGE_ai.py` = le code choisissant quoi faire à chaque tour, appliquant plusieurs stratégies successives, jusqu'à ce que toutes les actions requises aient été choisies
    - `TOMERGE_logging.py` = des fonctions de logging, notamment pour logger les perfs
- des notes

Attention que j'ai fait quelques modifs **après** le dernier challenge sans les tester → il y aura sans doute des petits trucs à fixer avant de pouvoir utiliser ce repo.

Le reste de cette section donne quelques détails supplémentaires.

## merge and copy

**Pourquoi ?**

Parce que l'interface codingame n'accepte qu'un unique programme, mais que je préfère coder en splittant mon code.

**Comment ?**

Le script `check_merge_and_copy.sh` est un gros `cat` de certains fichiers déclarés statiquement, dans l'ordre dans lesquels ils sont déclarés. Quelques précisions :

- les fichiers python doivent être déclarés dans l'ordre qui va bien pour que dans le fichier concaténé, au moment où on utilise une dépendance, celle-ci existe
- quand je crée un nouveau fichier, ne pas oublier de l'ajouter au script :-)
- le script supprime donc tout import de fichier dont le nom commence par `TOMERGE_` (et d'autres trucs inutiles)
- par simplicité, il est donc obligatoire qu'un import de `TOMERGE_` tienne sur une seule ligne. Si nécessaire, désactiver le formatter sur ces imports :
    ```python
    # this line will be replaced by the code merger -> do not reformat them :
    # fmt: off
    from TOMERGE_game import a, very, long, line, of, multiple, imports, that, would, normally, be, splitted, on, several, lines
    # fmt: on
    ```
- pour éviter de ne détecter les erreurs que dans l'IDE codingame (pour lequel la boucle de rétroaction est assez lente), le script fait également des checks flake8 et mypy

## sticky logs

`TOMERGE_logging.py` contient de quoi logger des infos éphémères, mais également des logs qui restent jusqu'à la fin de la partie : les **sticky-logs**.

Le principe est de sticky-logger un évènement qui nous intéresse mais qui ne se produit pas tout le temps, et de n'avoir qu'à jeter un oeil à l'état en fin de partie pour détecter immédiatement si l'évènement s'est produit ou non dans la game actuelle.

## perfs et mesure du temps d'exécution

Les deux challenges auxquels j'ai participés imposaient une limite sur le temps maximal qu'on peut prendre avant de produire un output.

Il y a donc un peu de code sur ce sujet :

- une fonction de log spécifique `perflog` pour logger les temps d'exécution
- un décorateur utilisant `perflog` pour logger le temps d'exécution des fonctions décorées
- un context-manager utilisant `perflog` pour logger le temps d'exécution de son contenu

Ne pas hésiter à les utiliser partout en baseline, car la fonction ne fait rien par défaut ; il suffit alors d'activer le switch pour débugger les perfs, ou des boucles infinies.

**ATTENTION** : il y a un caveat sur le temps d'exécution = si on on mesure le temps complet d'un tour, on trouve régulièrement des temps faramineux (dépassant parfois largement la limite imposée). J'ai pu constater que c'est le parsing du premier input qui prend du temps : je suppose qu'on mesure en fait le temps nécessaire au moteur codingame pour calculer l'état du tour suivant.

## reste à faire

Il y a pas mal de trucs utiles que je pourrais ajouter à ce template, par exemple logger préventivement _pourquoi_ j'ai choisi d'effectuer tell ou telle action à chaque tour, que je n'aurais plus qu'à activer pour débugger les situations où mes bots se comportent de façon inattendue, ou encore utiliser `pytest` pour tester des fonctions bas-niveau indépendantes du moteur du jeu.

Autre truc potentiellement intéressant : dans les deux challenges que j'ai faits, mes heuristiques ont eu besoin d'exprimer une sélection complexe d'objets, du style :

> si j'ai un héros adverse dans ma base, qu'il est plus proche de mon core que mes défenseurs, et qu'il a des araignées à portée de wind, alors je le wind-out avec le défenseur le plus proche

Mieux vaut alors mutualiser les mécanismes de sélection d'objets, pour exprimer ça avec quelque chose comme :

```python
def STRAT_wind_out_dangerous_enemies(
    board: Board,
    current_turn: int,
    sticky_logs: List[str],
) -> None:
    dangerous_enemies = board.heroes.select(
        is_enemy,
        is_in_my_base,
        is_closer_to_my_core_than_me,
        can_wind_spiders,
    )
    dangerous_enemy = closest_to_my_core(dangerous_enemies)
    if not dangerous_enemy:
        # je n'ai pas d'ennemis dangereux dans ma base
        # cette stratégie choisit donc de ne rien faire
        # elle délègue aux stratégies suivantes :
        return

    my_defenders = board.heroes.select(
        is_mine,
        has_no_action,
        is_in_my_base,
    )
    defender = closest(my_defenders, dangerous_enemy)
    if not defender:
        # je n'ai pas de défenseur de libre
        # elle délègue aux stratégies suivantes :
        return

    defender.wind_out(dangerous_enemy)
```

Le principe est de :

- créer des filtres adaptés aux problématiques du challenge, e.g. `is_in_my_base`, et les utiliser pour faire des sélection intuitives
- créer des _pickers_ qui choisissent un élément donné dans une sélection selon un critère adapté aux problématiques du challenge, e.g. `closest_to_my_core`

Le code que j'avais dans [le premier challenge](https://github.com/phidra/codingame-spring-challenge-2021) était plus avancé sur ce sujet -> à sortir proprement dans ce ce template.

