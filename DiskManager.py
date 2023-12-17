
from Record import Record

class DiskManager:
    blockSize = 3
    def __init__(self) -> None:
        self.reads = 0
        self.writes = 0
        pass

    def ReadBlock(self, filename, position=0):
        self.reads += 1
        with open(filename, 'rb') as input_file:
            input_file.seek(position)
            data = input_file.read(self.blockSize * Record.maxSize)
            result = []
            for i in range(0, len(data), Record.maxSize):
                result.append(Record(data[i : i + Record.maxSize].decode("utf-8")))
            return result

    def WriteBlock(self, filename, block):
        self.writes += 1
        data = ''.join([record.data for record in block])
        with open(filename, 'ab') as output_file:
            output_file.write(data.encode("utf-8"))

class TapeManager:
    def __init__(self, disk_manager, filename) -> None:
        self.disk_manager = disk_manager
        self.filename = filename
        self.position = 0
        self.block = []
        self.out_block = []

    def GetNextRecord(self):
        if self.block == []:
            print("read block " + self.filename +" " + str(self.position))
            self.block = self.disk_manager.ReadBlock(self.filename, self.position)
            print(self.block)
            self.position += DiskManager.blockSize * Record.maxSize

        if self.block == []:
            print("none")
            return None

        result = self.block[0]
        self.block.pop(0)
        return result

    def WriteNextRecord(self, record):
        self.out_block.append(record)
        if len(self.out_block) == DiskManager.blockSize:
            #print("write block")
            self.disk_manager.WriteBlock(self.filename, self.out_block)
            self.out_block.clear()

    def ForceWrite(self):
        #print("write block")
        self.disk_manager.WriteBlock(self.filename, self.out_block)
        self.out_block.clear()

