# Translation code

Ce projet à pour objectif de traduire des données **anglais** en **malagasy**.

## Liens des données

**Eli5**: https://huggingface.co/datasets/sentence-transformers/eli5

**Sentence Compression**: https://huggingface.co/datasets/sentence-transformers/sentence-compression

**Squad**: https://huggingface.co/datasets/sentence-transformers/squad

**Wikihow**: https://huggingface.co/datasets/sentence-transformers/wikihow

## Scripts sh

Les fichiers **sh** contenu dans le dossier **scripts_sh** permet de lancer la traduction pour chaque lien cité plus haut.

Chaque script sh appelle le fichier **translate.py**. Ce dernier contient le code qui fait la tâche de traduction.

## Requirements

Les modules nécéssaires qui s'installent dans chaque script sh lors de son execution.

## Executer un script sh

Dans le dossier **translation**, avant d'executer un script sh, donner celui-ci le droit d'execution.

Par exemple le script **eli5.sh** :

1. Droit d'execution : **chmod +x scripts_sh/eli5.sh**
2. Execution : **./scripts_sh/eli5.sh**

Ainsi la traduction des données **Eli5** se lance.

## Lancement des autres scripts

Dans le dossier **translation** :

*  **Sentence Compression** :
    *  chmod +x scripts_sh/sentence_compression.sh
    *  ./scripts_sh/sentence_compression.sh

*  **Squad** :
    *  chmod +x scripts_sh/squad.sh
    *  ./scripts_sh/squad.sh
 
*  **Wikihow** :
    *  chmod +x scripts_sh/wikihow.sh
    *  ./scripts_sh/wikihow.sh

## Sorties des données traduites

Les données traduites sont stockées dans la plateforme weights and biases sous mon compte dans un projet différent chaque script sh.

## Les arguments dans le code **translate.py**

![Capture d’écran du 2025-03-31 15-07-54](https://github.com/user-attachments/assets/b35cf6a5-a9a8-42e9-b17e-59e4953465e0)

**--input** : Lien des données fourni dans la plateforme Hugging Face en format pandas.

**--column1** : Première colonne correspondant au format de données.

**--column2** : Deuxième colonne correspandant au format de données.

**--weave_output** : Nom du projet dans la plateforme **wandb** où les données tradutes y sont stockées.

**--batch_size** : Valeur recommendée entre 8 à 32 y compris, exemple 8, 16, 32. Augmenter selon la puissance du GPU, pour un GPU assez puissant la valeur 16 ou 32 est idéale.

**--chunk_size** : Seuil de données traduites à publier dans la plateforme **wandb**. Exemple 50, puis 50 ligne données a été traduites, le seuil 50 est atteint donc les 50 lignes données traduites seront publiées dans la plateforme **wandb**.

**--range_begin** : L'indice pour commencer la traduction

**--range_end** : L'indice pour finir la traduction
