import openai

# API OPENAI ================================================
def model_response(messages, openai_key, model='gpt-5-nano-2025-08-07', stream = False):
    openai.api_key = openai_key
    response = openai.responses.create(
        input=messages,
        model=model,
        stream=stream
    )
    return response