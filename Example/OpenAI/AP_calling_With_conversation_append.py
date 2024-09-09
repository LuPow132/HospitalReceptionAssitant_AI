from openai import OpenAI
import Key

client = OpenAI(api_key=Key.OPEN_AI_KEY)

conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
]

while True:
    # Get user input
    user_input = input("User: ")
    
    # Append user message to conversation
    conversation.append({"role": "user", "content": user_input})
    
    # Get the AI's response
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )
    
    # Append AI's response to conversation
    ai_response = completion.choices[0].message.content
    conversation.append({"role": "assistant", "content": ai_response})
    
    # Print the AI's response
    print(f'AI: {ai_response}')
