import os
from typing import Final
from llama_cpp import Llama
from dotenv import load_dotenv


# LOAD ENV
load_dotenv()

LLM_NAME: Final[(str | None)] = os.getenv('LLM_NAME')
LLM_INSTRUCT: Final[(str | None)] = os.getenv('LLM_INSTRUCT')
LLM_MODEL_PATH: Final[(str | None)] = os.getenv('LLM_MODEL_PATH')

assert LLM_NAME is not None
assert LLM_INSTRUCT is not None
assert LLM_MODEL_PATH is not None


# LLM SETUP
llm = Llama(
    model_path=LLM_MODEL_PATH,
    n_ctx=1024,
    verbose=False
)


def get_response(username: str, user_input: str) -> str:
    try:
        prompt = f"<|prompt|>{LLM_INSTRUCT}</s>\n" \
                 f"<|prompt|>Here is what {username} says: {user_input}</s>\n" \
                  "<|answer|>"

        completion = llm.create_completion(
            prompt=prompt,
            stop=['</s>'],
            max_tokens=None,
            repeat_penalty=1.18,
            temperature=0.3
        )

        assert isinstance(completion, dict)

        response = completion['choices'][0]['text'].strip()
        finish_reason = completion['choices'][0]['finish_reason']

        print(f'{LLM_NAME}: {response}')
        print(f'finish_reason: {finish_reason}')
        
        assert response != ''
        if finish_reason == 'length':
            response += ' [truncated]'

        return response

    except Exception as e:
        print(e)
        return f'Sorry {username}, there was a problem with my AI 🥺'
