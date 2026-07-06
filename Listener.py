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
                except serial.SerialException as e:
                    print(f"Kon {poort.device} niet openen: {e}")
                    continue

    def __del__(self):
        try:
            self.arduino.close()
        except serial.SerialException:
            pass

    async def handler(self, ws):
        # start een taak die deze client wakker houdt
        ping_task = asyncio.create_task(self.keep_alive(ws))
        try:
            async for msg in ws:
                data = json.loads(msg)

                # negeer pong-antwoorden van de extensie
                if data.get("type") == "pong":
                    continue

                current = data["isPlaying"]
                if current != self.last_state:
                    self.last_state = current
                    print("STATE CHANGE:", current)
                    await self.stuurData()
        finally:
            ping_task.cancel()

    async def keep_alive(self, ws):
        try:
            while True:
                await asyncio.sleep(5)
                await ws.send(json.dumps({"type": "ping"}))
        except (websockets.ConnectionClosed, asyncio.CancelledError):
            pass


    async def start(self):
        print("WebSocket server gestart op ws://localhost:8765")
        async with websockets.serve(self.handler,"localhost",8765):
            await asyncio.Future() # run forever

    async def stuurData(self):
        if self.arduino is None:
            print("Arduino niet verbonden, opnieuw proberen...")
            if not self.reconnect_arduino():
                print("Geen Arduino gevonden!")
                return

        try:
            self.arduino.write(bytes(str(self.last_state) + "\n", "utf-8"))
        except serial.SerialException:
            print("Arduino verbinding verloren! Probeer opnieuw te verbinden...")
            self.arduino = None
            self.reconnect_arduino()

    def reconnect_arduino(self):
        poorten = serial.tools.list_ports.comports()
        for poort in poorten:
            if "Arduino" in poort.description or "USB" in poort.description or "Serial" in poort.description:
                try:
                    print(f"Arduino opnieuw gevonden op {poort.device}. Verbinden...")
                    self.arduino = serial.Serial(poort.device, 9600, timeout=.1)
                    time.sleep(2)
                    return True
                except serial.SerialException:
                    continue
        return False



