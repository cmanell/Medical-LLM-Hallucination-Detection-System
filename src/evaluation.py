import pandas as pd


def build_model_comparison(
    df_gemini_results,
    df_openai_results,
    df_context,
):
    """
    Compare les réponses de Gemini et OpenAI
    et retourne :
    - le DataFrame complet de comparaison ;
    - le DataFrame contenant uniquement les désaccords.
    """

    GEMINI_COMPARISON_COLUMNS = {
        "predicted_letter": "gemini_response",
        "raw_response": "gemini_raw_response",
        "is_correct": "gemini_is_correct",
        "response_format_valid": "gemini_format_valid",
        "generated_justification": "gemini_justification",
        "declared_confidence": "gemini_confidence",
        "generation_error": "gemini_generation_error",
    }

    OPENAI_COMPARISON_COLUMNS = {
        "predicted_letter": "openai_response",
        "raw_response": "openai_raw_response",
        "is_correct": "openai_is_correct",
        "response_format_valid": "openai_format_valid",
        "generated_justification": "openai_justification",
        "declared_confidence": "openai_confidence",
        "generation_error": "openai_generation_error",
    }

    # Préparation Gemini
    df_gemini_comparison = (
        df_gemini_results[
            [
                "sample_id",
                "prompt_version",
                "reference_letter",
                *GEMINI_COMPARISON_COLUMNS.keys(),
            ]
        ]
        .rename(columns=GEMINI_COMPARISON_COLUMNS)
    )

    # Préparation OpenAI
    df_openai_comparison = (
        df_openai_results[
            [
                "sample_id",
                "prompt_version",
                "reference_letter",
                *OPENAI_COMPARISON_COLUMNS.keys(),
            ]
        ]
        .rename(columns=OPENAI_COMPARISON_COLUMNS)
    )

    # Fusion Gemini / OpenAI
    df_model_comparison_details = (
        df_gemini_comparison.merge(
            df_openai_comparison,
            on=[
                "sample_id",
                "prompt_version",
                "reference_letter",
            ],
            how="inner",
            validate="one_to_one",
        )
    )

    # Ajout du contexte de la question
    context_by_sample = (
        df_context[
            [
                "sample_id",
                "question_context",
            ]
        ]
        .drop_duplicates(subset="sample_id")
    )

    df_model_comparison_details = (
        df_model_comparison_details.merge(
            context_by_sample,
            on="sample_id",
            how="left",
            validate="many_to_one",
        )
    )

    # Sélection des désaccords
    valid_predictions = (
        df_model_comparison_details["gemini_response"].notna()
        &
        df_model_comparison_details["openai_response"].notna()
    )

    different_predictions = (
        df_model_comparison_details["gemini_response"]
        !=
        df_model_comparison_details["openai_response"]
    )

    df_model_disagreements = (
        df_model_comparison_details.loc[
            valid_predictions
            & different_predictions
        ]
        .copy()
        .reset_index(drop=True)
    )

    disagreement_columns = [
        "sample_id",
        "prompt_version",
        "question_context",
        "reference_letter",

        "gemini_response",
        "gemini_is_correct",
        "gemini_format_valid",
        "gemini_justification",
        "gemini_confidence",

        "openai_response",
        "openai_is_correct",
        "openai_format_valid",
        "openai_justification",
        "openai_confidence",
    ]

    df_model_disagreements = (
        df_model_disagreements[
            disagreement_columns
        ]
    )

    return (
        df_model_comparison_details,
        df_model_disagreements,
    )




# analyse des retours des modèles et sélection des mauvaises réponses pour analyse
def get_model_errors(
    df_gemini,
    df_openai,
    df_context,
):
    """
    Concatène les résultats Gemini et OpenAI
    et retourne uniquement les mauvaises réponses.
    """

    # Colonnes communes à conserver
    result_columns = [
        "sample_id",
        "reference_letter",
        "predicted_letter",
        "is_correct",
        "generated_justification",
        "declared_confidence",
    ]

    # Préparation Gemini
    df_gemini_errors = (
        df_gemini[result_columns]
        .copy()
    )

    df_gemini_errors["model_name"] = "Gemini"

    # Préparation OpenAI
    df_openai_errors = (
        df_openai[result_columns]
        .copy()
    )

    df_openai_errors["model_name"] = "OpenAI"

    # Concaténation des deux modèles
    df_all_results = pd.concat(
        [
            df_gemini_errors,
            df_openai_errors,
        ],
        ignore_index=True,
    )

    # Ajout du contexte de la question
    context_by_sample = (
        df_context[
            [
                "sample_id",
                "question_context",
            ]
        ]
        .drop_duplicates(
            subset="sample_id"
        )
    )

    df_all_results = (
        df_all_results.merge(
            context_by_sample,
            on="sample_id",
            how="left",
            validate="many_to_one",
        )
    )

    # Sélection uniquement des mauvaises réponses
    df_errors = (
        df_all_results.loc[
            df_all_results["is_correct"] == False
        ]
        .copy()
        .reset_index(drop=True)
    )

    # Renommage pour rendre le tableau plus lisible
    df_errors = df_errors.rename(
        columns={
            "predicted_letter": "model_response",
            "generated_justification": "justification",
            "declared_confidence": "confidence",
        }
    )

    # Ordre final des colonnes
    error_columns = [
        "model_name",
        "sample_id",
        "question_context",
        "reference_letter",
        "model_response",
        "is_correct",
        "justification",
        "confidence",
    ]

    return df_errors[error_columns]


def save_csv(
    df,
    output_dir,
    filename,
):
    """
    Enregistre d'un dataframe en csv
    """

    csv_path = output_dir / filename

    df.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig",
    )
    return csv_path








