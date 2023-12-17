import random
import string
from colorama import Fore, Style
import os

from Record import IsAGreaterThanB, Record, GetRepeatingLettersNumber
from DiskManager import DiskManager

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
        tapes = []
        tapes.append([])
        tapes.append([])

        try:
            os.remove("tape_1")
            os.remove("tape_2")
        except OSError:
            pass

        last_record = None

        position = 0
        current_tape = 0
        block = self.disk_manager.ReadBlock(filename, position)
        while block:
            for record in block:
                if last_record is None:
                    tapes[current_tape].append(record)

                else:
                    if not IsAGreaterThanB(last_record, record):
                        tapes[current_tape].append(record)
                    else:
                        current_tape = 0 if current_tape == 1 else 1
                        tapes[current_tape].append(record)
                last_record = record

                for i, tape in enumerate(tapes, start=1):
                    if len(tape) > DiskManager.blockSize:
                        self.disk_manager.WriteBlock("tape_" + str(i), tape)
                        tape.clear()


            if len(block) < DiskManager.blockSize:
                break
            position += len(block) * Record.maxSize
            block = self.disk_manager.ReadBlock(filename, position)

        for i, tape in enumerate(tapes, start=1):
            self.disk_manager.WriteBlock("tape_" + str(i), tape)
            tape.clear()

    def MergeTwoTapesIntoOneTape(self):
        self.merges += 1
        try:
            os.remove("tape_3")
        except OSError:
            pass

        tapes = { 1:self.disk_manager.ReadBlock("tape_1"), 2:self.disk_manager.ReadBlock("tape_2") }
        tapes_last_record = { 1:None, 2:None }
        tapes_position = { 1:0, 2:0}
        tapes_empty = {1:False, 2:False}

        out_block = []
        is_file_sorted = True
        while True:

            if tapes_empty[1] and tapes[1] == []:
                out_block.append(tapes[2][0])
                tapes[2].pop(0)
            elif tapes_empty[2] and tapes[2] == []:
                out_block.append(tapes[1][0])
                tapes[1].pop(0)

            else:
                if IsAGreaterThanB(tapes_last_record[1],tapes[1][0]) and IsAGreaterThanB(tapes_last_record[2],tapes[2][0]):
                    is_file_sorted = False
                    tapes_last_record = { 1:None, 2:None }

                if IsAGreaterThanB(tapes_last_record[1],tapes[1][0]):
                    out_block.append(tapes[2][0])
                    tapes_last_record[2] = tapes[2][0]
                    tapes[2].pop(0)

                elif IsAGreaterThanB(tapes_last_record[2],tapes[2][0]) or IsAGreaterThanB(tapes[2][0], tapes[1][0]):
                    out_block.append(tapes[1][0])
                    tapes_last_record[1] = tapes[1][0]
                    tapes[1].pop(0)

                else:
                    out_block.append(tapes[2][0])
                    tapes_last_record[2] = tapes[2][0]
                    tapes[2].pop(0)

            if len(out_block) >= DiskManager.blockSize:
                self.disk_manager.WriteBlock("tape_3", out_block)
                out_block.clear()

            for tape_id, _ in enumerate(tapes, start=1):
                if not tapes_empty[tape_id] and len(tapes[tape_id]) == 0:
                    tapes_position[tape_id] += DiskManager.blockSize * Record.maxSize
                    tapes[tape_id] = self.disk_manager.ReadBlock("tape_" + str(tape_id), tapes_position[tape_id])
                    if len(tapes[tape_id]) < DiskManager.blockSize:
                        tapes_empty[tape_id] = True
            if tapes_empty[1] and tapes[1] == [] and tapes_empty[2] and tapes[2] == []:
                if len(out_block) > 0:
                    self.disk_manager.WriteBlock("tape_3", out_block)
                break
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

