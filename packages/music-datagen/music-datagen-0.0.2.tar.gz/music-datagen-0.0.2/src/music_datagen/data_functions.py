import random


def maskRandomly(tokens, maskRange, maskedToken = "x"):
    maskProb = random.uniform(maskRange[0], maskRange[1])
    return [random.choices([token, maskedToken], [1-maskProb, maskProb])[0] for token in tokens ]


def transposeRandomly(tokens, transposeRange):
    transposeAmount = random.randint(transposeRange[0], transposeRange[1])
    return [token+transposeAmount for token in tokens]


def maskIndex(tokens, index, maskedToken = "x"):
    tokens[index] = maskedToken
    return tokens



def test():
    print(maskRandomly([1,3,2,3,5,6,4,2,3], (0.10,0.20)))
    print(transposeRandomly([1,3,2,3,5,6,4,2,3], (-5,5)))
    print(maskIndex([1,3,2,3,5,6,4,2,3], 5))

if __name__ == "__main__":
    test()