import math

def main():
    run = True
    while run:
        print("""=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
                    [1]Hash
                    [2]Quit
=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=""")
        answer = input()
        if answer == "1":
            userInput = input("Please enter the string you would like to hash: ")
            result = handleHash(userInput)
            print(result)
        elif answer == "2":
            run = False
            exit()
        else:
            print("Please enter a valid option....")

def handleHash(userInput):
    result = []
    hashFunc = sha256(userInput)
    hashFunc.binConvert()
    hashFunc.generateConstants()
    for block in hashFunc.blocks:
        words = hashFunc.messageSchedule(block)
        result = hashFunc.compression(words, result)
    result = hashFunc.hexConvert(result)
    return result
        

class sha256():
    def __init__(self, userInput):
        self.str = userInput
        self.blocks = []
        self.constants = []

    def binConvert(self):
        binary = ""
        splitBin = ""
        count = 0
        arr = []
        for char in self.str:
            char = ord(char)
            char = bin(char)[2:].zfill(8)
            binary += char
        length = len(binary)
        binary += "1"
        blockNum = math.ceil((len(binary) + 64) / 512)
        binary = binary.ljust(512 * blockNum, "0")
        binary = binary[:-64]
        binary += bin(length)[2:].zfill(64)
        for bit in binary:
            if count % 512 == 0 and count >= 512:
                splitBin += f" {bit}"
            else:
                splitBin += bit
            count += 1
        self.blocks = splitBin.split()

    def rRotation(self, binary, rotNum):
        for i in range(rotNum):
            firstBit = binary[-1]
            binary = firstBit + binary[:-1]
        return binary
    def rShift(self, binary, shiNum):
        for i in range(shiNum):
            binary = "0" + binary[:-1]
        return binary
    def addition(self, binary1, binary2):
        result = ""
        carry = 0
        maxLen = max(len(binary1), len(binary2))
        binary1 = binary1.zfill(maxLen)
        binary2 = binary2.zfill(maxLen)
        for i in range(maxLen-1, -1, -1):
            r = carry
            if binary1[i] == "1":
                r += 1
            if binary2[i] == "1":
                r += 1
            if r % 2 == 1:
                result = "1" + result
            else:
                result = "0" + result
            if r < 2:
                carry = 0
            else:
                carry = 1
        if carry != 0:
            result = "1" + result
        result = int(result, 2) % (2 ** 32)
        result = bin(result)[2:].zfill(maxLen)
        return result
    def XOR(self, binary1, binary2):
        result = ""
        for i in range(len(binary1)):
            bit = int(binary1[i]) ^ int(binary2[i])
            result += str(bit)
        return result
            
    def lSigma0(self, x):
        result1 = self.rRotation(x, 7)
        result2 = self.rRotation(x, 18)
        result3 = self.rShift(x, 3)
        result4 = self.XOR(result1, result2)
        result5 = self.XOR(result4, result3)
        return result5
    def lSigma1(self, x):
        result1 = self.rRotation(x, 17)
        result2 = self.rRotation(x, 19)
        result3 = self.rShift(x, 10)
        result4 = self.XOR(result1, result2)
        result5 = self.XOR(result4, result3)
        return result5
    def uSigma0(self, x):
        result1 = self.rRotation(x, 2)
        result2 = self.rRotation(x, 13)
        result3 = self.rRotation(x, 22)
        result4 = self.XOR(result1, result2)
        result5 = self.XOR(result4, result3)
        return result5
    def uSigma1(self, x):
        result1 = self.rRotation(x, 6)
        result2 = self.rRotation(x, 11)
        result3 = self.rRotation(x, 25)
        result4 = self.XOR(result1, result2)
        result5 = self.XOR(result4, result3)
        return result5
    def choice(self, x, y, z):
        result = ""
        for i in range(len(x)):
            if x[i] == "1":
                result += y[i]
            else:
                result += z[i]
        return result
    def majority(self, x, y, z):
        result = ""
        for i in range(len(x)):
            count1 = 0
            count0 = 0
            if x[i] == "1":
                count1 += 1
            else:
                count0 += 1
            if y[i] == "1":
                count1 += 1
            else:
                count0 += 1
            if z[i] == "1":
                count1 += 1
            else:
                count0 += 1
            if count1 > count0:
                result += "1"
            else:
                result += "0"
        return result

    def generateConstants(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311]
        for prime in primes:
            constant = prime ** (1/3)
            constant = (constant - int(constant)) * (2 ** 32)
            constant = bin(int(constant))[2:].zfill(32)
            self.constants.append(constant)
    def messageSchedule(self, block):
        words = []
        bitCount = 0
        for i in range(16):
            words.append(block[bitCount:bitCount+32])
            bitCount += 32
        for i in range(48):
            index = i + 16
            word1 = words[index-2]
            word1 = self.lSigma1(word1)
            word2 = words[index-7]
            word3 = words[index-15]
            word3 = self.lSigma0(word3)
            word4 = words[index-16]
            newWord = self.addition(word1, word2)
            newWord = self.addition(newWord, word3)
            newWord = self.addition(newWord, word4)
            words.append(newWord)
        return words
    def compression(self, words, initialValues):
        arr = initialValues
        result = []
        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        if arr == []:
            for prime in primes:
                prime = prime ** (0.5)
                prime = (prime - int(prime)) * (2 ** 32)
                prime = bin(int(prime))[2:].zfill(32)
                arr.append(prime)
        a2, b2, c2, d2, e2, f2, g2, h2 = arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7]
        arr2 = arr
        for i in range(64):
            a, b, c, d, e, f, g, h = arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7]
            word = words[i]
            constant = self.constants[i]
            T1 = self.addition(self.uSigma1(e), self.choice(e, f, g))
            T1 = self.addition(T1, h)
            T1 = self.addition(T1, constant)
            T1 = self.addition(T1, word)
            T2 = self.addition(self.uSigma0(a), self.majority(a, b, c))
            arr.insert(0, self.addition(T1, T2))
            arr.pop()
            arr[4] = self.addition(arr[4], T1)
        a, b, c, d, e, f, g, h = arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7]
        result.append(self.addition(a2, a))
        result.append(self.addition(b2, b))
        result.append(self.addition(c2, c))
        result.append(self.addition(d2, d))
        result.append(self.addition(e2, e))
        result.append(self.addition(f2, f))
        result.append(self.addition(g2, g))
        result.append(self.addition(h2, h))
        return result

    def hexConvert(self, values):
        result = ""
        for value in values:
            value = int(value, 2)
            hexadecimal = self.hex(value)
            result += hexadecimal
        return result
    def hex(self, num):
        string = ""
        run = True
        while run:
            if num // 16 == 0:
                run = False
            remainder = num % 16
            if remainder == 10:
                remainder = "a"
            elif remainder == 11:
                remainder = "b"
            elif remainder == 12:
                remainder = "c"
            elif remainder == 13:
                remainder = "d"
            elif remainder == 14:
                remainder = "e"
            elif remainder == 15:
                remainder = "f"
            num //= 16
            string += str(remainder)
        string = string[::-1]
        return string
            
#main()
