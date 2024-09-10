from openai import OpenAI
import json
import Key

client = OpenAI(api_key=Key.OPEN_AI_KEY)

conversation = [
    {"role": "system", "content": "You are a hospital receptionist anime girl. Your job is to assist patient in Thai. You work at BUU hospital"},
]

function_descriptions = [
    {
        "name": "make_an_appointment",
        "description": "Make an appointment based on information user give",
        "parameters": {
            "type": "object",
            "properties": {
                "Height": {
                    "type": "string",
                    "description": "Height in cm",
                },
                "Weight": {
                    "type": "string",
                    "description": "Weight in kg",
                },
                "Symptoms": {
                    "type": "string",
                    "description": "Symptoms of what user feel",
                },
            },
            "required": ["Height", "Weight","Symptoms"],
        },
    }
]

while True:
    # Get user input
    user_input = input("User: ")
    
    # Append user message to conversation
    conversation.append({"role": "user", "content": user_input})
    
    # Get the AI's response
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation,
        functions=function_descriptions,
        function_call="auto",  # specify the function call
    )
    
    # Append AI's response to conversation
    ai_response = completion
    conversation.append({"role": "assistant", "content": ai_response.choices[0].message.content})
    
    # Print the AI's response
    print(f'AI: {ai_response.choices[0].message.content}')
    print(f'Function{ai_response.choices[0].message.function_call}')
    if(ai_response.choices[0].message.function_call != None):
        parameter = json.loads(ai_response.choices[0].message.function_call.arguments)
        height = int(parameter["Height"])
        weight = float(parameter["Weight"])
        symptoms = parameter["Symptoms"]
        print(f'parameter{height,weight,symptoms}')
