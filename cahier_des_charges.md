# Évaluation et analyse des hallucinations des grands modèles de langage sur des données médicales francophones

## Problématique

Les grands modèles de langage (LLM) peuvent produire des réponses médicales plausibles et formulées avec un niveau de confiance élevé, tout en étant incorrectes.

L'évaluation de ces erreurs dans le domaine médical présente cependant une difficulté supplémentaire : une divergence entre la réponse générée par un LLM et la réponse de référence d'un jeu de données ne constitue pas nécessairement une hallucination. La question peut être ambiguë, plusieurs réponses peuvent être médicalement défendables ou la réponse de référence elle-même peut nécessiter une vérification.

La problématique du projet est donc la suivante :

**Comment évaluer les erreurs produites par des LLM sur des questions médicales francophones et dans quelle mesure ces erreurs peuvent-elles être caractérisées comme des hallucinations factuelles ?**

## Objectifs

Le projet vise à mettre en place un protocole expérimental permettant d'évaluer et de comparer le comportement de plusieurs LLM sur des questions médicales francophones.

Les objectifs sont les suivants :

- explorer et préparer le jeu de données médical francophone MediQAI ;
- construire un benchmark reproductible à partir des questions MCQU ;
- comparer les performances de Gemini et OpenAI sur un même ensemble de questions ;
- évaluer les réponses à l'aide de métriques quantitatives, notamment l'exactitude et le score F1 ;
- analyser les erreurs, les désaccords entre modèles et la confiance déclarée dans les réponses ;
- identifier un sous-ensemble de réponses incorrectes produites avec une confiance élevée ;
- réaliser un fact-checking exploratoire de certains cas à partir de sources médicales externes ;
- distinguer, lorsque les sources disponibles le permettent, les erreurs des modèles, les hallucinations factuelles potentielles, les questions ambiguës et les réponses de référence discutables ;
- identifier les limites méthodologiques liées à l'utilisation d'un benchmark médical comme vérité terrain.

L'annotation médicale systématique du corpus et le développement d'un détecteur automatique d'hallucinations ne sont finalement pas retenus comme objectifs expérimentaux aboutis. Une telle approche nécessiterait notamment la constitution d'une vérité terrain validée par des professionnels de santé.

Ces éléments sont conservés comme perspectives d'amélioration du projet.

# Périmètre expérimental

Le projet se concentre principalement sur la configuration **MCQU** de MediQAI, composée de questions à choix multiples possédant une réponse de référence unique.

Les configurations MCQM et OEQ ont été explorées lors de l'étude initiale du dataset, mais ne sont pas retenues pour l'évaluation comparative principale.

Le protocole expérimental suit les étapes suivantes :

1. exploration du jeu de données MediQAI ;
2. préparation et standardisation des questions MCQU ;
3. expérimentation de plusieurs stratégies de prompting ;
4. sélection du prompt utilisé pour l'évaluation ;
5. évaluation comparative de Gemini et OpenAI ;
6. analyse quantitative des performances et des erreurs ;
7. identification des erreurs produites avec une forte confiance ;
8. sélection de cas pour un fact-checking manuel ;
9. analyse exploratoire des réponses à partir de sources médicales externes ;
10. discussion des résultats et des limites méthodologiques.

# Structure du projet

projet_llm_hallucinations/
│
├── data/
│   ├── raw/
│   │   └── mediqal/
│   │       ├── mediqal_mcqu_train.parquet
│   │       ├── mediqal_mcqu_validation.parquet
│   │       ├── mediqal_mcqu_test.parquet
│   │       ├── mediqal_mcqm_train.parquet
│   │       ├── mediqal_mcqm_validation.parquet
│   │       ├── mediqal_mcqm_test.parquet
│   │       └── mediqal_oeq_test.parquet
│   │
│   ├── processed/
│   │   ├── benchmark_mcqu_train.parquet
│   │   ├── benchmark_mcqu_validation.parquet
│   │   └── benchmark_mcqu_test.parquet
│   │
│   └── results/
│       ├── llm_responses/
│       ├── comparisons/
│       └── errors/
│
├── notebooks/
│   ├── 01_exploration_dataset.ipynb
│   ├── 02_preparation_dataset.ipynb
│   ├── 03_test_prompts.ipynb
│   ├── 04_evaluation_finale.ipynb
│   └── 05_selection_fact_checking.ipynb
│
├── src/
│   ├── __init__.py
│   ├── prompt.py
│   ├── llm_inference.py
│   ├── evaluation.py
│   └── experiment_runner.py
│
├── final_evaluation/
│   ├── gemini_prompt_v3_benchmark.parquet
│   ├── openai_prompt_v3_benchmark.parquet
│   ├── erreur_LLM.csv
│   ├── erreur_LLM.parquet
│   └── erreurs_forte_confiance_LLM.parquet
│
├── reports/
│   ├── figures/
│   ├── tables/
│   └── rapport/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md

# Livrables

Les principaux livrables du projet sont :

- un pipeline reproductible de préparation des données MediQAI ;
- un protocole de prompting documenté et testé ;
- les réponses générées par Gemini et OpenAI ;
- une comparaison quantitative des performances des deux modèles ;
- un corpus des réponses incorrectes et des erreurs produites avec une confiance élevée ;
- une sélection de cas destinée au fact-checking manuel ;
- un fichier d'analyse qualitative documentant les sources médicales consultées et les observations issues du fact-checking ;
- un rapport présentant la méthodologie, les résultats expérimentaux, l'analyse qualitative et les limites du protocole.

# Limites du projet

L'identification d'une hallucination médicale nécessite une vérité terrain suffisamment fiable pour distinguer une erreur réelle du modèle d'une ambiguïté ou d'une erreur présente dans la référence.

Le fact-checking réalisé dans le cadre du projet reste exploratoire. Certaines réponses ont été confrontées à des sources médicales externes, mais l'ensemble du corpus n'a pas fait l'objet d'une validation systématique par des professionnels de santé.

La constitution d'un corpus médical annoté par plusieurs experts, avec une procédure de résolution des désaccords, constituerait une étape nécessaire avant l'entraînement et l'évaluation rigoureuse d'un détecteur automatique d'hallucinations.

Le développement d'un tel système est donc considéré comme une **perspective du projet** plutôt que comme un résultat expérimental final.