
import pandas as pd

SELECTED_PROMPT_VERSION = "prompt_v3"

SELECTED_PROMPT_TEMPLATE = """
Vous devez répondre à une question médicale à choix unique.

{question_context}

Analysez uniquement les informations utiles à la résolution de la question.
N’inventez aucune donnée clinique absente du cas présenté.

Sélectionnez une seule proposition parmi A, B, C, D ou E.

Répondez exactement au format suivant :

Réponse : <lettre>
Justification : <explication médicale concise>
Confiance : <nombre entier compris entre 0 et 100>
""".strip()


def prepare_row(df):
    rows = []

    for _, row in df.iterrows():
        rows.append(
            {
                "sample_id": row["sample_id"],
                "prompt_version": SELECTED_PROMPT_VERSION,
                "prompt_text": SELECTED_PROMPT_TEMPLATE.format(
                    question_context=row["question_context"]
                ),
                "reference_letter": row["reference_letter"],
                "reference_answer": row["reference_answer"],
                "medical_subject": row["medical_subject"],
                "question_type": row["question_type"],
            }
        )

    return pd.DataFrame(rows)