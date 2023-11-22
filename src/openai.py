from src.entities import MessageEntities


def get_tools():
    """Helper function to return the tools to make available for OpenAI."""

    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_pii_entities",
                "description": "Extract any PII related entities found in the message(s). If there are none found, return an empty list for each type.",
                "parameters": MessageEntities.model_json_schema(),
            },
        }
    ]
    return tools