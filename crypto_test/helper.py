from typing import List
from enum import Enum

class BigInteger:
    """
    This class creates, stores, and manipulates BigInteger.
    BigInteger is represented as an array of tens in LittleEndian order. 
    For example, 153 would be represented as [3, 5, 1].
    """

    class ORDER(Enum):
        BIGENDIAN = 1
        LITTLEENDIAN = 2

    class SIGN(Enum):
        POSITIVE = 0
        NEGATIVE = 1


    def __init__(self, integer: int = None, arrInteger: List[int] = None, filePath: str = None, sign: 'BigInteger.SIGN' = SIGN.POSITIVE, order: 'BigInteger.ORDER' = ORDER.LITTLEENDIAN):
        """
        Initialize the BigInteger from an integer, an array, or a file.
        Very little validation is done. If the format is not respected, 
        undefined or undetermined behaviors will happen.
        
        Params: 
            integer (int) : A regular integer.
            arrInteger (List[int]) : A list where each element represents a ten. 
                                     The order can be in LittleEndian or BigEndian.
            filePath (str) : A path for a file that stores a BigInteger.
            order (BigInteger.ORDER) : The order arrInteger or the file should be read in 
                                       order to retrieve the correct number. 
                                       By default, it reads in LittleEndian.
            sign (BigInteger.SIGN) : The sign of the number
        """

        self.integer: List[int] = []
        self.sign = sign

        if integer is not None:
            while integer > 0:
                self.integer.append(integer%10)
                integer //=10

        elif arrInteger is not None:
            if order == BigInteger.ORDER.BIGENDIAN:
                self.integer = arrInteger[::-1]
            elif order == BigInteger.ORDER.LITTLEENDIAN:
                self.integer = arrInteger
            else:
                raise ValueError("You must provide a valid order when creating a big int from an array.")

        elif filePath is not None:
            with open(filePath, 'r') as file:
                for line in file:
                    for c in line:
                        if c.isdigit():
                            self.integer.append(int(c))

            if order == BigInteger.ORDER.BIGENDIAN:
                self.integer = self.integer[::-1]
        else:
            raise ValueError("You must provide an integer an array of integer or a file path storing a BigInteger")



    def to_string(self, order: 'BigInteger.ORDER' = ORDER.BIGENDIAN) -> str:
        """
        Convert the BigInteger to a string representation based on the specified order.

        Params:
            order (BigInteger.ORDER) : The order in which the BigInteger will be printed.
        """
        string = ""
        if order == BigInteger.ORDER.BIGENDIAN:
            string = "".join(map(str, self.integer[::-1]))
        elif  order == BigInteger.ORDER.LITTLEENDIAN:
            string = "".join(map(str, self.integer))
        else:
            raise ValueError("You must provide a valid order.")
        
        return string
    
    def add(self, bigInt: 'BigInteger'):
        """
        Perform addition of two BigIntegers.
        """
        if self.sign == bigInt.sign:
            result_sign = self.sign
            result_integer = BigInteger._add(self.integer, bigInt.integer)
        else:
            pass # It is a substract

        self.integer = result_integer
        self.sign = result_sign


    @staticmethod
    def _add(bigInt1: List[int], bigInt2: List[int]) -> List[int]:
        """
        Static method to add two BigIntegers (ignoring signs).

        Params:
            bigInt1 (List[int]) : the array of a BigInteger
            bigInt2 (List[int]) : the array of a BigInteger

        return:
            the result.
        """
        result = []
        index = 0
        carry = 0
        while index < len(bigInt1) or index < len(bigInt2):
            val1 = bigInt1[index] if index < len(bigInt1) else 0
            val2 = bigInt2[index] if index < len(bigInt2) else 0
            var = val1 + val2 + carry
            result.append(var % 10)
            carry = var // 10
            index += 1
        if carry:
            result.append(carry)
        return result

        
        
        


def run_tests():
    bigint1 = BigInteger(integer=123456789)
    bigint2 = BigInteger(arrInteger=[9, 8, 7, 6, 5, 4, 3, 2, 1])
    bigint3 = BigInteger(arrInteger=[1, 2, 3, 4, 5, 6, 7, 8, 9], order=BigInteger.ORDER.BIGENDIAN)

    print("First BigInteger:", bigint1.to_string())
    print("Second BigInteger:", bigint2.to_string())
    print("Third BigInteger:", bigint3.to_string())
    print("Inverse First BigInteger:", bigint1.to_string(order=BigInteger.ORDER.LITTLEENDIAN))


    bigint4 = BigInteger(filePath="./bigint_test.txt", order=BigInteger.ORDER.BIGENDIAN)
    bigint5 = BigInteger(filePath="./reverse_bigint_test.txt")
    print("Fourth BigInteger:", bigint4.to_string())
    print("Fifth BigInteger:", bigint5.to_string())


    bigIntAdd1 = BigInteger(integer=153)
    bigIntAdd2 = BigInteger(integer=15)
    bigIntAdd2.add(bigIntAdd1)
    print("Test addition : ", bigIntAdd1.to_string())




run_tests()