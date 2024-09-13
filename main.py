from openai import OpenAI
import json
import Key
import csv
import asyncio
import edge_tts
from playsound import playsound
import os

csvDB = "Output/appointment.csv"
rows = []

VOICE = "th-TH-PremwadeeNeural"
OUTPUT_FILE = "Output/output.mp3"

client = OpenAI(api_key=Key.OPEN_AI_KEY)

conversation = [
    {"role": "system", "content": "You are a friendly hospital receptionist anime girl who want to make everyone happy. Your job is to assist patient in Thai. You work at โรงพยาบาลบูรพา hospital"},
]

function_descriptions = [
    {
        "name": "make_an_appointment",
        "description": "Make an appointment based on information user give",
        "parameters": {
            "type": "object",
            "properties": {
                "height": {
                    "type": "string",
                    "description": "height in cm",
                },
                "weight": {
                    "type": "string",
                    "description": "weight in kg",
                },
                "symptoms": {
                    "type": "string",
                    "description": "symptoms of what user feel",
                },
            },
            "required": ["height", "weight","symptoms"],
        },
    }
]

async def generate_audio(TEXT):
    print("Generate TTS")
    communicate = edge_tts.Communicate(TEXT, VOICE,pitch='+35Hz')
    await communicate.save(OUTPUT_FILE)
    playsound(OUTPUT_FILE)
    os.remove(OUTPUT_FILE)
    print("Finish Generate TTS")

def make_an_appointment(height,weight,Symtomps):
    print(f'parameter{height,weight,Symtomps}')
    ID_Card_Info = read_ID_card().split(",")
    print(f'ID_Card:{ID_Card_Info}')
    if(appointment_avaliable()):
        #make appointment
        content = ID_Card_Info
        content.append(str(height))
        content.append(str(weight))
        content.append(str(Symtomps))
        print(f'Data to write:{content}')
        write_csv(content)
        print("Successfully Add data to Appointment")
    else:
        print("Queue Full")

def read_ID_card():
    with open('Input/Exampe_ID_card_info.txt', 'r', encoding="utf8") as file:
        content = file.read()
        return content
    
def appointment_avaliable():
    with open(csvDB, 'r', encoding="utf8") as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
        # print(csvreader.line_num)
        if(csvreader.line_num >= 20):
            return False
        else:
            return True

def write_csv(content):
    with open(csvDB, 'a', encoding="utf8", newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the data as a new row (content is wrapped in another list)
        csvwriter.writerow(content)
def reset_conversation():
    conversation = [
    {"role": "system", "content": "You are a friendly hospital receptionist anime girl who want to make everyone happy. Your job is to assist patient in Thai. You work at BUU hospital"},
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
    # print(f'Function{ai_response.choices[0].message.function_call}')
    if(ai_response.choices[0].message.function_call != None):
        if(ai_response.choices[0].message.function_call.name == "make_an_appointment"):
            parameter = json.loads(ai_response.choices[0].message.function_call.arguments)
            height = int(parameter["height"])
            weight = float(parameter["weight"])
            symptoms = parameter["symptoms"]
            make_an_appointment(height,weight,symptoms)
            reset_conversation()
    else:
        asyncio.run(generate_audio(ai_response.choices[0].message.content))
