
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
