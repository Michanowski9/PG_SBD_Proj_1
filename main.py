import os
import getch
from DiskManager import DiskManager, TapeManager
from Utils import Sorter, PrintFile

def PrintMenu():
    os.system('clear')
    print("\t\tMENU")
    print("\t[1] Print Input File")
    print("\t[2] Print Output File")
    print("\t[3] Sort")
    print("\t[4] Sort step by step")
    print("\t[5] Stats")

    print("\t[Q] Exit")
    print()

#dm = DiskManager()
#tape_1_manager = TapeManager(dm, "Out/out")
#while True:
#    record = tape_1_manager.GetNextRecord()
#    print(record)
#    if record is None:
#        break
#getch.getch()

def tests():
    sorter = Sorter(debug=True)
    sorter.SortFile("Out/out")

def main_loop():
    running = True
    while running:
        PrintMenu()
        choosen_option = getch.getch()
        match choosen_option.lower():
            case '1':
                print("Input File:")
                PrintFile("Out/out")
            case '2':
                print("Output File:")
                PrintFile("tape_3")
            case '3':
                print("Sorting File")
                sorter = Sorter()
                sorter.SortFile("Out/out")
                pass
            case '4':
                print("Sorting step by step")
                sorter = Sorter(debug=True)
                sorter.SortFile("Out/out")
                pass
            case '5':
                pass
            case '6':
                pass
            case 'q':
                running = False
                break
        print("\npress any button to continue")
        getch.getch()


tests()

#GenerateExampleFile(filename,20)
#SortFile("Out/out")
