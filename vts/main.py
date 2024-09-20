import asyncio
import pyvts
import time
import random
import websockets

plugin_info = {
    "plugin_name": "Hospital Reception",
    "developer": "LuPow132",
    "authentication_token_path": "./token.txt"
}

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
    return None

async def main():
    vts = pyvts.vts(plugin_info=plugin_info)
    try:
        await connect_and_authenticate(vts)

        plugin_parameter_face_lean_rot = "PI_FACE_lean_rot"
        plugin_parameter_face_lean_X = "PI_FACE_lean_X"
        await send_request_with_retry(vts, vts.vts_request.requestCustomParameter(plugin_parameter_face_lean_rot, max=30, min=30, default_value=0))
        await send_request_with_retry(vts, vts.vts_request.requestCustomParameter(plugin_parameter_face_lean_X, max=30, min=30, default_value=0))

        while True:
            try:
                await connect_and_authenticate(vts)
                time.sleep(round(random.uniform(1, 5), 1))
                lean_rot = random.randint(-10, 10)
                lean_X = random.randint(-20, 20)
                await send_request_with_retry(vts, vts.vts_request.requestSetParameterValue(plugin_parameter_face_lean_rot, lean_rot))
                await send_request_with_retry(vts, vts.vts_request.requestSetParameterValue(plugin_parameter_face_lean_X, lean_X))

                print(f'Ping with data {lean_rot}, {lean_X} at {time.time()}')
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"WebSocket connection closed with error: {e}. Reconnecting...")
                await asyncio.sleep(5)  # Wait before attempting to reconnect
            except Exception as e:
                print(f"An error occurred: {e}")
                break
    finally:
        await vts.close()

if __name__ == "__main__":
    asyncio.run(main())