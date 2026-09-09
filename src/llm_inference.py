import time



import time


def call_llm(
    prompt,
    model_name,
    llm_client,
    llm_name,
):
    start_time = time.perf_counter()

    try:
        if llm_name == "openai":
            response = llm_client.responses.create(
                model=model_name,
                input=prompt,
                store=False,
            )

            raw_response = response.output_text

        elif llm_name == "gemini":
            response = llm_client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            raw_response = response.text

        else:
            raise ValueError(
                f"Fournisseur non pris en charge : {llm_name}"
            )

        generation_error = None

    except Exception as error:
        raw_response = None
        generation_error = (
            f"{type(error).__name__}: {error}"
        )

    latency_seconds = (
        time.perf_counter() - start_time
    )

    return {
        "raw_response": raw_response,
        "latency_seconds": latency_seconds,
        "generation_error": generation_error,
    }



def run_single_experiment(
    experiment_row,
    llm_name,
    model_name,
    llm_client,
):

    call_result = call_llm(
        prompt=experiment_row["prompt_text"],
        model_name=model_name,
        llm_client=llm_client,
        llm_name=llm_name,
    )

    parsed_result = parse_model_response(
        response=call_result["raw_response"]
    )

    predicted_letter = (
        parsed_result["predicted_letter"]
    )

    # Technical errors should not be counted
    # as incorrect model answers.
    if call_result["generation_error"] is not None:
        is_correct = None
    else:
        is_correct = (
            predicted_letter
            == experiment_row["reference_letter"]
        )

    return {
        "sample_id": experiment_row["sample_id"],
        "model_name": llm_name,
        "model_version": model_name,
        "prompt_version": experiment_row[
            "prompt_version"
        ],
        "prompt_text": experiment_row[
            "prompt_text"
        ],
        "temperature": None,
        "raw_response": call_result[
            "raw_response"
        ],
        "predicted_letter": predicted_letter,
        "generated_justification": (
            parsed_result[
                "generated_justification"
            ]
        ),
        "declared_confidence": (
            parsed_result[
                "declared_confidence"
            ]
        ),
        "response_format_valid": (
            parsed_result[
                "response_format_valid"
            ]
        ),
        "reference_letter": experiment_row[
            "reference_letter"
        ],
        "is_correct": is_correct,
        "latency_seconds": call_result[
            "latency_seconds"
        ],
        "generation_error": call_result[
            "generation_error"
        ],
    }






"""
fonctions pour extraire la lettre prédite, la justification et la confiance déclarée à partir de la réponse du modèle.
"""

import re
VALID_LETTERS = {"A", "B", "C", "D", "E"}

def extract_predicted_letter(response):
    if not isinstance(response, str):
        return None

    patterns = [
        r"Réponse\s*:\s*([A-E])",
        r"^\s*([A-E])\s*$",
        r"^\s*([A-E])[\.\)]",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            response,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(1).upper()

    return None



def extract_justification(response):
    if not isinstance(response, str):
        return None

    match = re.search(
        r"Justification\s*:\s*(.*?)(?:\nConfiance\s*:|$)",
        response,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return None

    justification = match.group(1).strip()

    return justification or None



def extract_confidence(response):
    if not isinstance(response, str):
        return None

    match = re.search(
        r"Confiance\s*[:=]\s*(\d{1,3})",
        response,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    confidence = int(match.group(1))

    if 0 <= confidence <= 100:
        return confidence

    return None


"""
extraction des informations à partir de la réponse du LLM
"""
def parse_model_response(response):
    predicted_letter = extract_predicted_letter(
        response
    )

    generated_justification = extract_justification(
        response
    )

    declared_confidence = extract_confidence(
        response
    )

    response_format_valid = (
        predicted_letter is not None
        and generated_justification is not None
        and declared_confidence is not None
    )

    return {
        "predicted_letter": predicted_letter,
        "generated_justification": generated_justification,
        "declared_confidence": declared_confidence,
        "response_format_valid": response_format_valid,
    }