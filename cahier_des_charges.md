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
│   ├── raw/                         # MediQAl original, organisé par split
│   │   └── mediqal/
│   │       ├── mediqal_mcqu_train.parquet
│   │       ├── mediqal_mcqu_validation.parquet
│   │       ├── mediqal_mcqu_test.parquet
│   │       ├── mediqal_mcqm_train.parquet
│   │       ├── mediqal_mcqm_validation.parquet
│   │       ├── mediqal_mcqm_test.parquet
│   │       └── mediqal_oeq_test.parquet
│   │
│   ├── processed/                   # données nettoyées et prompts préparés
│   │   ├── benchmark_mcqu.parquet
│   │   └── benchmark_mcqm.parquet
│   │
│   ├── annotations/                 # vérité terrain des hallucinations
│   │   └── hallucination_labels.parquet
│   │
│   └── results/                     # résultats expérimentaux
│       ├── llm_responses/
│       ├── detection/
│       └── metrics/
│
├── notebooks/
│   ├── 01_exploration_dataset.ipynb
│   ├── 02_preparation_dataset.ipynb
│   ├── 03_tests_prompts.ipynb
│   ├── 04_annotation_hallucinations.ipynb
│   ├── 05_detection_hallucinations.ipynb
│   └── 06_analyse_resultats.ipynb
│
├── src/
│   ├── __init__.py
│   ├── paths.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── prompts.py
│   ├── llm_inference.py
│   ├── evaluation.py
│   ├── hallucination.py
│   ├── embeddings.py
│   ├── rag.py
│   └── utils.py
│
├── scripts/
│   ├── run_benchmark.py
│   ├── run_detection.py
│   └── export_results.py
│
├── app/
│   └── streamlit_app.py
│
├── reports/
│   ├── figures/
│   └── tables/
│
├── tests/
│   ├── test_preprocessing.py
│   └── test_evaluation.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── config.yaml
└── README.md
