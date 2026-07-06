import asyncio
import websockets
import json
import serial
import time
import serial.tools.list_ports

class Listener:
    def __init__(self):
        self.last_state = None
        self.arduino = None

        poorten = serial.tools.list_ports.comports()
        for poort in poorten:
            if "Arduino" in poort.description or "USB" in poort.description or "Serial" in poort.description:
                try:
                    print(f"Arduino herkent op {poort.device}. Verbinden...")
                    self.arduino = serial.Serial(poort.device,9600,timeout=.1)
                    time.sleep(2)
                    break
                except serial.SerialException:
                    continue

    def __del__(self):
        try:
            self.arduino.close()
        except serial.SerialException:
            pass

    async def handler(self, ws):
        async for msg in ws:
            data = json.loads(msg)
            current = data["isPlaying"]

            if current != self.last_state:
                self.last_state = current
                print("STATE CHANGE:", current)
                try:
                    await self.stuurData()
                except serial.SerialException as e:
                    print(f"ERROR: {e}")


    async def start(self):
        print("WebSocket server gestart op ws://localhost:8765")
        async with websockets.serve(self.handler,"localhost",8765):
            await asyncio.Future() # run forever

    async def stuurData(self):
        self.arduino.write(bytes(str(self.last_state),"utf-8"))
