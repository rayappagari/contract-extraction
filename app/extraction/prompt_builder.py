from pathlib import Path


PROMPTS_DIR = Path(__file__).parents[2] / "prompts"


def load_prompt(prompt_file: str) -> str:
    path = PROMPTS_DIR / prompt_file
    return path.read_text(encoding="utf-8")


def build_extraction_prompt(contract_text: str, prompt_file: str = "contract_extraction_v2.md") -> tuple[str, str]:
    system_prompt = load_prompt(prompt_file)
    user_message = f"<contract>\n{contract_text}\n</contract>\n\nExtract all fields as specified."
    return system_prompt, user_message


def build_amendment_prompt(original_text: str, amendment_text: str) -> tuple[str, str]:
    system_prompt = load_prompt("amendment_prompt.md")
    user_message = (
        f"<original_contract>\n{original_text}\n</original_contract>\n\n"
        f"<amendment>\n{amendment_text}\n</amendment>\n\nIdentify and extract all changes."
    )
    return system_prompt, user_message
