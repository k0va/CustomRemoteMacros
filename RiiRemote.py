from pykodi import get_kodi_connection, Kodi
from evdev import ecodes, UInput
import asyncio
import evdev
import psutil
import threading

def deviceName():
    return "123 COM Smart Control Consumer Control"

def findDeviceByName(deviceName):
    devices = evdev.list_devices()
    for path in devices:
        device = evdev.InputDevice(path);
        if (deviceName == device.name):
            print(device)
            break
    return device

async def connectToKodi():
     kc = get_kodi_connection(host="127.0.0.1", port=8080, ws_port=None, username="", password="")
     await kc.connect()
     kodi = Kodi(kc)
     retVal = (kodi, kc)
     return retVal
     
def createDevice():
    deviceItem = findDeviceByName(deviceName())
    device = evdev.InputDevice(deviceItem.path)
    return device

async def previous(kodi):
    try:
        await kodi.previous_track()
    except:
        pass
async def next(kodi):
    try:
        await kodi.next_track()
    except:
        pass

async def playpause(kodi):
    try:
        await kodi.play_pause()
    except:
        pass

async def stop(kodi):
    try:
        await kodi.stop()                   
    except:
        pass

async def catchEvents():

    kodi, kc = await connectToKodi()
    device = createDevice()
    ui = UInput.from_device(device, name='SIMDev')
    device.grab()
    try:
        for event in device.read_loop():
            if (event.code == ecodes.KEY_PLAYPAUSE):
                if (event.value == 0):
                    await playpause(kodi)
            if (event.code == ecodes.KEY_NEXTSONG):
                if (event.value == 0):
                    await next(kodi)                   
            if (event.code == ecodes.KEY_PREVIOUSSONG):
                if (event.value == 0):
                    await previous(kodi)
            if (event.code == ecodes.KEY_SEARCH):
                if (event.value == 0):
                    await stop(kodi)
            else:
                ui.write(event.type, event.code, event.value)
            #print(evdev.categorize(event))


    finally:
        try:
            await kc.close()
        except:
            print("Failed to close!")
        try:
             device.ungrab()
        except:
            print("Failed to close2!")


def main():
    event = threading.Event()
    while (True):
        kodiIsRunning = "kodi" in (p.name() for p in psutil.process_iter())
        if kodiIsRunning:
            print("starting")
#            try:
            asyncio.run(catchEvents())
#            except:
#                pass
            print("end")
            event.wait(10)
        else:
            event.wait(1)
            print("Waiting")


if __name__ == '__main__':
    main()

