def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    # TODO Embedding
    # TODO Load context
    # TODO Promt engineering
    # TODO Get response from LLM

    if 'hello' in lowered:
        return 'Hey hey!'
    elif 'how are you' in lowered:
        return 'I feel great and you?'
    elif 'bye' in lowered:
        return 'See ya!'
    else:
        return 'Sorry, could you repeat that?'