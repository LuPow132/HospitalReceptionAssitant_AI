from openai import OpenAI
import Key

client = OpenAI(api_key=Key.OPEN_AI_KEY)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Hello Who are you"
        }
    ]
)

print(completion.choices[0].message.content)
