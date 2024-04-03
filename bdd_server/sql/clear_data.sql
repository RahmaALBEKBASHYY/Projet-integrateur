DELETE
FROM
    `categorie`
WHERE
    `idCategorie` > 0;


DELETE
FROM
    `joueur`
WHERE
    `idJoueur` > 0;

DELETE
FROM
    `partie`
WHERE
    `idPartie` > 0;


DELETE
FROM
    `question`
WHERE
    `idQuestion` > 0;


DELETE
FROM
    `questionjoueur`
WHERE
    `idQuestionJoueur` > 0;


DELETE
FROM
    `reponses`
WHERE
    `idReponses` > 0;


DELETE
FROM
    `pion`
WHERE
    `Joueur_idJoueur` > 0 or `Partie_idPartie` > 0 ;


DELETE
FROM
    `partie-has-question`
WHERE
    `Partie_idPartie` > 0 or `Partie_idPartie` > 0 ;


DELETE
FROM
    `reponsesjoueur`
WHERE
    `idReponsesJoueur` > 0;

DELETE
