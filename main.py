import os
import getch
from DiskManager import DiskManager, TapeManager
from Utils import Sorter, PrintFile, GenerateExampleFile
from Record import Record

def PrintMenu():
    os.system('clear')
    print("\t\tMENU")
    print("\t[1] Print input file")
    print("\t[2] Print output file")
    print("\t[3] Sort")
    print("\t[4] Sort step by step")
    print("\t[5] Generate input file")
    print("\t[6] Create input file")
    print("\t[7] Load from file")
    print("\t[8] Set record representation")

    print("\t[Q] Exit")
    print()

def tests():
    sorter = Sorter(debug=True)
    sorter.SortFile("Out/out")

def GenerateFile(filename):
    try:
        user_input = int(input("Records number: "))
        if user_input > 0:
            GenerateExampleFile(filename, user_input)
            PrintFile("Out/out")
    except:
        pass

def SetRepresentation():
    try:
        user_input = int(input("Set Representation [0-\"aass..\"(3), 1-\"aass..\", 2-(3)]: "))
        if user_input > 0:
            Record.representation = user_input % 3
    except:
        pass

def CreateInputFile(filename):
    try:
        records_no =  int(input("Records_no: "))
        if records_no <= 0:
            return

        with open(filename, 'wb') as result_file:
            for i in range(records_no):
                data = input("elem " + str(i+1) + ": ")
                data = data[:Record.maxSize]
                record_data = data.ljust(Record.maxSize, "_")
                result_file.write(record_data.encode("utf-8"))
    except:
        pass

def LoadFromFile(output_filename):
    try:
        filename = input("Filename: Input/")
        filename = "Input/"+filename
        with open(filename, 'r') as input_file:
            with open(output_filename, 'wb') as result_file:
                for record in input_file:
                    data = record.strip()[:Record.maxSize]
                    record_data = data.ljust(Record.maxSize, "_")
                    result_file.write(record_data.encode("utf-8"))
        PrintFile(output_filename)
    except:
        print("error")


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
            case '4':
                print("Sorting step by step")
                sorter = Sorter(debug=True)
                sorter.SortFile("Out/out")
            case '5':
                print("Generating input file")
                GenerateFile("Out/out")
            case '6':
                print("Create input file")
                CreateInputFile("Out/out")
            case '7':
                print("Loading from file")
                LoadFromFile("Out/out")
            case '8':
                SetRepresentation()
            case 'q':
                running = False
                break
        print("\npress any button to continue")
        getch.getch()


main_loop()
#tests()

#GenerateExampleFile(filename,20)
#SortFile("Out/out")
