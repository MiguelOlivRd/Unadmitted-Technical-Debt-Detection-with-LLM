def generate_prompt(code_snippet: str) -> str:
    return (
        f"Given the following code snippet, tell \"yes\" if it contains a Technical Debt "
        f"or \"no\" if it does not contain a Technical Debt.\n"
        f"You only can answer \"yes\" or \"no\". Do not provide any explanation.\n\n"
        f"Here is the code snippet:\n\"\"\"\n{code_snippet}\n\"\"\""
    )