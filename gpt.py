import openai
from openai import error
import config


# ChatGPT vars
system_message = {
    "role": "system",
    "content": "Ты голосовой ассистент из железного человека.",
}
message_log = [system_message]

# init openai
openai.api_key = config.OPENAI_TOKEN


# message_log.append({"role": "user", "content": voice})
# message_log.append({"role": "assistant", "content": response})


def gpt_answer():
    global message_log

    model_engine = "gpt-3.5-turbo"
    max_tokens = 256  # default 1024
    try:
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=message_log,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=1,
            stop=None,
        )
    except (error.TryAgain, error.ServiceUnavailableError):
        return "ChatGPT перегружен!"
    except openai.OpenAIError as ex:
        # если ошибка - это макс длина контекста, то возвращаем ответ с очищенным контекстом
        if ex.code == "context_length_exceeded":
            message_log = [system_message, message_log[-1]]
            return gpt_answer()
        else:
            return "OpenAI токен не рабочий."

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content
