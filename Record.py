

class Record:
    maxSize = 30
    def __init__(self, data) -> None:
        if len(data) > self.maxSize:
            print("to long")
            data = data[:self.maxSize]
        self.data = data

    def __repr__(self) -> str:
        #return "\"" + self.data + "\""
        return str(GetRepeatingLettersNumber(self.data))
        return "\"" + self.data + "\"" + str(GetRepeatingLettersNumber(self.data))


def IsAGreaterThanB(a, b):
    if a is None:
        return None
    if b is None:
        return None

    a_lettersNo = GetRepeatingLettersNumber(a.data)
    b_lettersNo = GetRepeatingLettersNumber(b.data)

    if a_lettersNo > b_lettersNo:
        return True
    if a_lettersNo < b_lettersNo:
        return False
    return None

    for index in range(max(len(a_lettersNo), len(b_lettersNo))):
        if index >= len(a_lettersNo):
            return False
        elif index >= len(b_lettersNo):
            return True
        elif index < len(a_lettersNo) and index < len(b_lettersNo):
            if a_lettersNo[index] > b_lettersNo[index]:
                return True
            elif a_lettersNo[index] < b_lettersNo[index]:
                return False


def GetRepeatingLettersNumber(record):
    letter_count = {}
    for letter in record.replace('_', ''):
        letter_count[letter] = letter_count.get(letter, 0) + 1
    #print(letter_count)
    return sum(1 for count in letter_count.values() if count > 1)
    return sum(count for count in letter_count.values() if count > 1)

    letters = {}
    for letter in record:
        if letter in letters:
            letters[letter] += 1
        else:
            letters[letter] = 1
    result = []
    for letter, count in letters.items():
        result.append(count)

    result.sort(reverse=True)
    return result
