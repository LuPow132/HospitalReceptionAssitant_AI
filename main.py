import json
import pyvts
import time
import random
import websockets
import Key
import csv
import asyncio
import edge_tts
import os
import threading
import speech_recognition as sr
from openai import OpenAI
from playsound import playsound

plugin_info = {
    "plugin_name": "Hospital Reception",
    "developer": "LuPow132",
    "authentication_token_path": "./token.txt"
}

csvDB = "Output/appointment.csv"
rows = []

VOICE = "th-TH-PremwadeeNeural"
OUTPUT_FILE = "Output/output.mp4"

client = OpenAI(api_key=Key.OPEN_AI_KEY)

conversation = [
    {"role": "system", "content": "You are a friendly hospital receptionist anime girl who want to make everyone happy. Your job is to assist patient about giving basic information or making an appointment in User languages. You work at Burapha University Hospital. Burapha University Hospital Information: Located in Chonburi, on Burapha University campus. It’s a teaching hospital offering outpatient, inpatient services, and emergency care. Departments: OPD, ER, Radiology, Dental – 1st Floor,Internal Medicine, Pediatrics – 2nd Floor,OB-GYN – 3rd Floor,Surgery – 4th Floor"},
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

def write_subtitle(filename, content):
    with open(filename, 'w',encoding="utf-8") as file:
        file.write(content)


async def connect_and_authenticate(vts):
    await vts.connect()
    await vts.request_authenticate_token()  # get token
    await vts.request_authenticate()  # use token

async def send_request_with_retry(vts, request, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await vts.request(request)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"WebSocket connection closed with error: {e}. Retrying {attempt + 1}/{max_retries}...")
            await asyncio.sleep(5)  # Wait before retrying
            await connect_and_authenticate(vts)
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return

async def setup_vts(vts):
    try:
        await connect_and_authenticate(vts)

        plugin_parameter_face_lean_rot = "PI_FACE_lean_rot"
        plugin_parameter_face_lean_X = "PI_FACE_lean_X"
        await send_request_with_retry(vts, vts.vts_request.requestCustomParameter(plugin_parameter_face_lean_rot, max=30, min=30, default_value=0))
        await send_request_with_retry(vts, vts.vts_request.requestCustomParameter(plugin_parameter_face_lean_X, max=30, min=30, default_value=0))

    finally:
        await vts.close()

    return vts

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
    queue_number = appointment_avaliable()
    if(queue_number < 20):
        #make appointment
        content = ID_Card_Info
        content.append(str(height))
        content.append(str(weight))
        content.append(str(Symtomps))
        print(f'Data to write:{content}')
        write_csv(content)
        text = f"ทำการลงทะเบียนนัดลงระบบเรียบร้อยคะ\n ลำดับคิวของท่านคือ {queue_number} คะ\n ขอบคุณที่ใช้บริการคะ"
        write_subtitle("subtitle.txt",text)
    else:
        text = "ขออภัยคะ ตอนนี้คิวเต็มแล้วคะ ลองติดต่อฝ่ายเวชระเบียนดูนะคะ"
        write_subtitle("subtitle.txt",text)
    print(text)
    asyncio.run(generate_audio(text))

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
        return csvreader.line_num

def write_csv(content):
    with open(csvDB, 'a', encoding="utf8", newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the data as a new row (content is wrapped in another list)
        csvwriter.writerow(content)
def reset_conversation():
    global conversation
    conversation = [
    {"role": "system", "content": "You are a friendly hospital receptionist anime girl who want to make everyone happy. Your job is to assist patient about giving basic information or making an appointment in User languages. You work at Burapha University Hospital. Burapha University Hospital Information: Located in Chonburi, on Burapha University campus. It’s a teaching hospital offering outpatient, inpatient services, and emergency care. Departments: OPD, ER, Radiology, Dental – 1st Floor,Internal Medicine, Pediatrics – 2nd Floor,OB-GYN – 3rd Floor,Surgery – 4th Floor"},
]

def chatBot(recognizer):
    while True:
        with sr.Microphone(device_index=1) as source:
            print("Listening...")
            audio = recognizer.listen(source)  # Listen for speech

        try:
            # Use Google Web Speech API to recognize Thai speech (supports Thai)
            print("Recognizing speech...")
            text = recognizer.recognize_google(audio, language="th-TH")  # Thai language code
            print(f"You said: {text}")
            user_input = text
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

            if ai_response.choices[0].message.function_call is not None:
                if ai_response.choices[0].message.function_call.name == "make_an_appointment":
                    parameter = json.loads(ai_response.choices[0].message.function_call.arguments)
                    height = int(parameter["height"])
                    weight = float(parameter["weight"])
                    symptoms = parameter["symptoms"]
                    make_an_appointment(height, weight, symptoms)
                    reset_conversation()
            else:
                write_subtitle("subtitle.txt",ai_response.choices[0].message.content)
                asyncio.run(generate_audio(ai_response.choices[0].message.content))

        except sr.UnknownValueError:
            text = "ขอโทษนะคะ ฉันได้ยินไม่ชัดคะ รบกวนพูดอีกครั้งได้ไหมคะ"
            print(text)
            asyncio.run(generate_audio(text))
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

async def vts_move(vts):
    while True:
        try:
            await connect_and_authenticate(vts)
            time.sleep(round(random.uniform(1, 5), 1))
            lean_rot = random.randint(-10, 10)
            lean_X = random.randint(-20, 20)
            plugin_parameter_face_lean_rot = "PI_FACE_lean_rot"
            plugin_parameter_face_lean_X = "PI_FACE_lean_X"
            await send_request_with_retry(vts, vts.vts_request.requestSetParameterValue(plugin_parameter_face_lean_rot, lean_rot))
            await send_request_with_retry(vts, vts.vts_request.requestSetParameterValue(plugin_parameter_face_lean_X, lean_X))

            print(f'Ping with data {lean_rot}, {lean_X} at {time.time()}')
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"WebSocket connection closed with error: {e}. Reconnecting...")
            await asyncio.sleep(5)  # Wait before attempting to reconnect
        except Exception as e:
            print(f"An error occurred: {e}")
            break

async def setup_vts():
    global vts
    vts = pyvts.vts(plugin_info=plugin_info)
    try:
        await connect_and_authenticate(vts)

        plugin_parameter_face_lean_rot = "PI_FACE_lean_rot"
        plugin_parameter_face_lean_X = "PI_FACE_lean_X"
        await send_request_with_retry(vts, vts.vts_request.requestCustomParameter(plugin_parameter_face_lean_rot, max=30, min=30, default_value=0))
        await send_request_with_retry(vts, vts.vts_request.requestCustomParameter(plugin_parameter_face_lean_X, max=30, min=30, default_value=0))

    finally:
        await vts.close()

recognizer = sr.Recognizer()

asyncio.run(setup_vts())

with sr.Microphone(device_index=1) as source:
    print("Adjusting for ambient noise... Please wait.")
    recognizer.adjust_for_ambient_noise(source)  # Adjust based on the surrounding noise level


# Create the threads without calling the functions
x = threading.Thread(target=chatBot, args=(recognizer,))
y = threading.Thread(target=lambda: asyncio.run(vts_move(vts)))

# Start the threads
x.start()
y.start()

# Wait for both threads to complete
x.join()
y.join()
