**TODO** = extraire un template à partir de [mon code pour le fall challenge 2023](https://github.com/phidra/codingame-fall-challenge-2023).

Notes sur un minifier rust :

- ça a l'air d'être assez compliqué d'accéder à l'AST, il n'y a pas de façon standard+simple de faire
- du coup, j'abandonne l'idée de faire propre, et j'en reste sur ma version hacky manuelle (qui exclut certains trucs)
- je peux l'améliorer (alphabet plus grand, notamment + commande rust pour aller plus vite qu'en bash)
- l'un des trucs qui fait gagner le plus de place est le join des lignes (suppression des trailing spaces), mais ça nécessite un code sans commentaires de fin de ligne
- du coup, ces outils pour supprimer les commentaires sont à explorer :
    - https://docs.rs/comment-strip/latest/comment_strip/
    - https://github.com/gorilskij/no-comment
    - https://crates.io/crates/no-comment
    - https://crates.io/crates/comment-strip
- ce qu'il me faudrait in fine, c'est un merger/minifier en one-shot (et qui peut prendre un fichier d'exclusion)
- forker le cargo-merger ?


