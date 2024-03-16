import os
from typing import Final
from llama_cpp import Llama
from dotenv import load_dotenv


# LOAD ENV
load_dotenv()

BOT_NAME: Final[(str | None)] = os.getenv('BOT_NAME')
BOT_INSTRUCT: Final[(str | None)] = os.getenv('BOT_INSTRUCT')
BOT_MODEL_PATH: Final[(str | None)] = os.getenv('BOT_MODEL_PATH')

assert BOT_NAME is not None
assert BOT_INSTRUCT is not None
assert BOT_MODEL_PATH is not None


# LLM SETUP
llm = Llama(
    model_path=BOT_MODEL_PATH,
    n_ctx=1024,
    verbose=False
)


def get_response(username: str, message: str) -> str:
    try:
        prompt = f'''<|im_start|>system\n{BOT_INSTRUCT}.\nYou are chatting through Discord with the user {username}.<|im_end|>\n<|im_start|>user\n{message}<|im_end|>\n<|im_start|>assistant\n'''

        completion = llm.create_completion(
                prompt=prompt,
                stop=['<|im_end|>'],
                max_tokens=200,
                top_k=10,
                temperature=0,
        )

        assert isinstance(completion, dict)

        response = completion['choices'][0]['text'].strip()
        finish_reason = completion['choices'][0]['finish_reason']

        print(f'{BOT_NAME}: {response}')
        print(f'finish_reason: {finish_reason}')
        
        assert response != ''
        if finish_reason == 'length':
            response += ' [truncated]'

        return response

    except Exception as e:
        print(e)
        return f'Sorry {username}, there was a problem with my AI 🥺'
