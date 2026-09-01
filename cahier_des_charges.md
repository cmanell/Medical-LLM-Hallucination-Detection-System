# Évaluation et détection des hallucinations des grands modèles de langage sur des données médicales francophones

## Problématique : Les LLM peuvent générer des réponses médicales plausibles mais incorrectes. Comment mesurer et détecter automatiquement ces hallucinations dans un contexte médical francophone ?

### Objectifs:

- comparer plusieurs LLM ;
- mesurer les erreurs ;
- classifier les hallucinations ;
- développer un détecteur automatique.


# structure du projet

projet_llm_hallucinations/
│
├── data/
│   ├── raw/                 # données originales
│   ├── processed/           # données nettoyées
│   └── results/             # sorties expérimentales
│
├── notebooks/
│   ├── 01_exploration_dataset.ipynb
│   ├── 02_tests_prompts.ipynb
│   └── 03_analyse_resultats.ipynb
│
├── src/
│   ├── data_loader.py       # chargement datasets
│   ├── preprocessing.py     # nettoyage / formatage
│   ├── prompts.py           # templates de prompts
│   ├── llm_inference.py     # appels aux modèles
│   ├── evaluation.py        # accuracy, F1, scores
│   ├── hallucination.py     # détection hallucinations
│   ├── rag.py               # récupération documentaire si RAG
│   └── utils.py             # fonctions générales
│
├── scripts/
│   ├── run_benchmark.py
│   ├── run_detection.py
│   └── export_results.py
│
├── app/
│   └── streamlit_app.py     # interface finale éventuelle
│
├── reports/
│   ├── figures/
│   └── tables/
│
├── requirements.txt
├── config.yaml
└── README.md