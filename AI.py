from groq import Groq


def aiProcess(command):
    client = Groq(
        api_key="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",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a virtual named jarvis skilled in general tasks like alexa and google cloud",
            },
            {"role": "user", "content": command}

        ],
        model="llama3-8b-8192",
    )

    return (chat_completion.choices[0].message.content)
