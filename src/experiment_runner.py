

import time
import pandas as pd


result_columns = [
    "sample_id",
    "model_name",
    "model_version",
    "prompt_version",
    "prompt_text",
    "temperature",
    "raw_response",
    "predicted_letter",
    "generated_justification",
    "declared_confidence",
    "response_format_valid",
    "reference_letter",
    "is_correct",
    "latency_seconds",
    "generation_error",
]



def run_experiment_batch(
    experiments,
    runner,
    model_name,
    output_path,
    pause_seconds=1,
):
    if output_path.exists():
        saved_results = pd.read_parquet(output_path)
        results = saved_results.to_dict(orient="records")
        completed_sample_ids = set(saved_results["sample_id"])
    else:
        results = []
        completed_sample_ids = set()

    pending = experiments.loc[
        ~experiments["sample_id"].isin(completed_sample_ids)
    ]

    print("Déjà terminées :", len(completed_sample_ids))
    print("À exécuter :", len(pending))

    for number, (_, experiment_row) in enumerate(
        pending.iterrows(),
        start=1,
    ):
        print(
            f"[{number}/{len(pending)}] "
            f"{experiment_row['sample_id']}"
        )

        result = runner(
            experiment_row=experiment_row,
            model_name=model_name,
        )
        results.append(result)

        pd.DataFrame(results)[result_columns].to_parquet(
            output_path,
            index=False,
        )

        print(
            "Prédiction :", result["predicted_letter"],
            "| Référence :", result["reference_letter"],
            "| Correcte :", result["is_correct"],
            "| Erreur :", result["generation_error"],
        )
        time.sleep(pause_seconds)

    return pd.DataFrame(results)[result_columns]