#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

echo "Ce script agrège les différents fichiers de code en un seul fichier."

TMPFILE=$(mktemp) || exit 1
echo "Le temporary file agrégeant le code est : $TMPFILE"

FLAKE8_FORMATTING_ERRORS="E1,W1,E2,W2,E3,W3,E4,W4,E5"
FLAKE8_DUPLICATED_IMPORTS_ERROR="F811"

echo "" > "$TMPFILE"
for f in \
    TOMERGE_logging.py \
    TOMERGE_board.py \
    TOMERGE_game.py \
    TOMERGE_ai.py \
    main_code.py
do
    # on vérifie chaque fichier avant concaténation, pour donner la localisation des erreurs dans le source :
    # (mais à ce stade, on se fiche des erreurs de formattage)
    flake8 "$f" --extend-ignore="$FLAKE8_FORMATTING_ERRORS"
    mypy "$f"
    {
        grep -E -v -e "from TOMERGE_" -e "if TYPE_CHECKING" -e '^ *#' -e '^ *$' "$f"
    } >> "$TMPFILE"
done

# copie dans le press-papier :
< "$TMPFILE" xclip -selection c

echo "Le contenu agrégé est placé dans le presse-papiers"
echo ""

# on vérifie aussi l'ensemble du fichier concaténé

trap 'on_error' ERR
on_error() {
    RED='\033[0;31m'
    REGULAR='\033[0m'
    BOLD=$(tput bold)
    NORMAL=$(tput sgr0)
    echo ""
    # affichage très visible, pour être sûr de ne pas louper les erreurs :
    echo -e "${RED}${BOLD}ATTENTION ATTENTION ATTENTION : il y a eu des erreurs mypy ou flake8${REGULAR}${NORMAL} !"
}

flake8 "$TMPFILE" --extend-ignore="$FLAKE8_FORMATTING_ERRORS","$FLAKE8_DUPLICATED_IMPORTS_ERROR"
mypy "$TMPFILE"
