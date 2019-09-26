import random

FILE_PATH = "proguard-words.pro"
MAX_COUNT = 4000


def randomName(length=3):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    name = []
    for i in range(length):
        index = random.randint(0, len(chars) - 1)
        name.append(chars[index])
    return ''.join(name)


with open(FILE_PATH, 'w') as fp:
    length = 2
    names = set()
    retryCount = 0
    for i in range(MAX_COUNT):
        name = randomName(length)
        while name in names:
            for retry in range(3):
                name = randomName(length)
            if name in names:
                length+=1

        fp.write(name+"\n")
        names.add(name)

