import sys
import keyboard

while True:
    record = keyboard.read_event()
    print("**")
    print(dir(record))
    print(record.__dict__)
    print('**')



