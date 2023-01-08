# nlp_sentiment_analysis_movie_comments
--------------------------------------

Modèle NLP pour analyser les commentaires de films postés par les spectateurs pour indiquer s'ils sont positifs ou négatifs.

- Data : CSV comprenant les commentaires scrapés
- Img : Images pour Wordclouds
- Modules : Code de webscraping, Test en console du modèle (input par user)
- Notebooks : Contient le preprocessing, les wordclouds des commentaires selon les catégories et les tests modèles;  
- Website : Application web pour tester en ligne les commentaires que l'user entre.

Pour faire fonctionner: 
- installer l'environnement avec les librairies >> requirements.txt (pip install -r requirements.txt)
- aller jusqu'au dossier website dans la console et lancer la commande : flask run
- cliquer sur le lien dans la console

--------------------------------------

Pistes d'amélioration :

- Clean du code CSS (en vrac actuellement)
- Ajout de la fonction scrap sur le site
- Ajout de la consultation de la base de données comprenant : Nom du film, Commentaire du spectateur, Résultat Analyse (Thumb Up or Down)
- Ajout d'une catégorie neutre pour les commentaires mitigés
