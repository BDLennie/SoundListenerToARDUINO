from Listener import Listener
import asyncio

def main():
    listener = Listener()
    asyncio.run(listener.start())

if __name__ == '__main__':
    main()