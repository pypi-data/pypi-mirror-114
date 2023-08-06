import os
import asyncio
import time

def launch():
    # if exeInput is None:
    #     InputError = "ERROR: Input not found.."

    #     return print(InputError)

    exeInput = input("File Location(Do not include .EXE inside dirName):\n")
    exeInput2 = input('Exe Name(Do not include .exe inside fileName):\n')
    exe = exeInput.lower()
    exe2 = exeInput2.lower()
    time.sleep(1.5)
    print('\nRunning..')
    time.sleep(1.5)
    print('Successful!')
    os.startfile(exe + "\\" + exe2 + ".exe")