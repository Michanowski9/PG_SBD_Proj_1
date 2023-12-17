import random
import string
from colorama import Fore, Style
import os

from Record import IsAGreaterThanB, Record, GetRepeatingLettersNumber
from DiskManager import DiskManager, TapeManager

def GenerateExampleFile(filename, records_no, padding_char="_"):
    with open(filename, 'wb') as result_file:
        for _ in range(records_no):
            record_data = GenerateRandomRecord().data.ljust(Record.maxSize, padding_char)
            result_file.write(record_data.encode("utf-8"))


def GenerateRandomRecord():
    length = random.randint(1, Record.maxSize)
    result = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    return Record(result)



def PrintFile(filename):
    print("\t",end="")
    with open(filename, 'rb') as input_file:
        records = []
        record_data = input_file.read(Record.maxSize)
        while record_data:
            records.append(Record(record_data.decode("utf-8")))
            record_data = input_file.read(Record.maxSize)

        for id in range(len(records)):
            if id > 0 and IsAGreaterThanB(records[id-1], records[id]):
                print(f"{Fore.RED}|{Style.RESET_ALL}", end=" ")
            print(records[id],end=" ")
            #print(GetRepeatingLettersNumber(records[id].data),end=" ")
            #print()
        print()

class Sorter:
    def __init__(self, debug=False) -> None:
        self.disk_manager = DiskManager()
        self.debug = debug
        self.merges = 0
        self.splits = 0

    def LoadFileToTapes(self,filename="tape_3"):
        self.splits += 1

        try:
            os.remove("tape_1")
            os.remove("tape_2")
        except OSError:
            pass

        last_record = None

        current_tape = 1
        input_tape = TapeManager(self.disk_manager, filename)

        out_tape = { 1:TapeManager(self.disk_manager, "tape_1"), 2:TapeManager(self.disk_manager, "tape_2")}

        record = input_tape.GetNextRecord()
        last_record = None
        while record:
            if last_record is None:
                last_record = record
            elif IsAGreaterThanB(last_record, record):
                current_tape = 1 if current_tape == 2 else 2

            out_tape[current_tape].WriteNextRecord(record)
            last_record = record
            record = input_tape.GetNextRecord()

        for _, tape in out_tape.items():
            tape.ForceWrite()


    def MergeTwoTapesIntoOneTape(self):
        self.merges += 1
        try:
            os.remove("tape_3")
        except OSError:
            pass

        tapes = { 1:TapeManager(self.disk_manager, "tape_1"), 2:TapeManager(self.disk_manager, "tape_2")}
        out_tape = TapeManager(self.disk_manager, "tape_3")

        record_tape = {1:tapes[1].GetNextRecord(), 2:tapes[2].GetNextRecord()}

        last_record = { 1:None, 2:None }

        is_file_sorted = True
        while True:
            if IsAGreaterThanB(last_record[1], record_tape[1]) or IsAGreaterThanB(last_record[1], record_tape[1]):
                is_file_sorted = False

            if record_tape[1] is None and record_tape[2] is None:
                break

            if record_tape[1] is None:
                out_tape.WriteNextRecord(record_tape[2])
                record_tape[2] = tapes[2].GetNextRecord()
            elif record_tape[2] is None:
                out_tape.WriteNextRecord(record_tape[1])
                record_tape[1] = tapes[1].GetNextRecord()
            else:
                if last_record[2] is None and IsAGreaterThanB(record_tape[1], record_tape[2]):
                    out_tape.WriteNextRecord(record_tape[2])
                    last_record[2] = record_tape[2]
                    record_tape[2] = tapes[2].GetNextRecord()
                elif last_record[1] is None:
                    out_tape.WriteNextRecord(record_tape[1])
                    last_record[1] = record_tape[1]
                    record_tape[1] = tapes[1].GetNextRecord()
                elif not IsAGreaterThanB(last_record[2],record_tape[2]) and IsAGreaterThanB(record_tape[1], record_tape[2]):
                    out_tape.WriteNextRecord(record_tape[2])
                    last_record[2] = record_tape[2]
                    record_tape[2] = tapes[2].GetNextRecord()
                elif not IsAGreaterThanB(last_record[1],record_tape[1]):
                    out_tape.WriteNextRecord(record_tape[1])
                    last_record[1] = record_tape[1]
                    record_tape[1] = tapes[1].GetNextRecord()
                elif IsAGreaterThanB(last_record[2],record_tape[2]) and IsAGreaterThanB(last_record[1],record_tape[1]):
                    last_record = {1:None, 2:None}

        out_tape.ForceWrite()

        return is_file_sorted


    def SortFile(self, filename):
        print("Input:")
        PrintFile(filename)
        if self.debug:
            print("\n\n")

        is_file_sorted = False

        is_file_sorted = self.LoadFileToTapes(filename)

        self.PrintTapesIfDebug()

        while True:
            is_file_sorted = self.MergeTwoTapesIntoOneTape()
            self.PrintTapeIfDebug()
            if is_file_sorted:
                break
            self.LoadFileToTapes()
            self.PrintTapesIfDebug()

        print("\n")
        print("Output:")
        PrintFile("tape_3")
        print("\n")
        self.PrintStats()


    def PrintStats(self):
        print(f"Reads:\t{self.disk_manager.reads}")
        print(f"Writes:\t{self.disk_manager.writes}")
        print(f"R+W:\t{self.disk_manager.writes + self.disk_manager.reads}")

        print(f"Splits:\t{self.splits}")
        print(f"Merges:\t{self.merges}")


    def PrintTapesIfDebug(self):
        if self.debug:
            print("t1: ",end="")
            PrintFile("tape_1")
            print("t2: ",end="")
            PrintFile("tape_2")
            print()


    def PrintTapeIfDebug(self):
        if self.debug:
            print("t3: ",end="")
            PrintFile("tape_3")
            print()

