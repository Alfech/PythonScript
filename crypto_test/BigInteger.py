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
        NEGATIVE = -1
        POSITIVE = 1
        def __lt__(self, other):
            if isinstance(other, BigInteger.SIGN):
                return self.value < other.value
            return self < other

        def __le__(self, other):
            if isinstance(other, BigInteger.SIGN):
                return self.value <= other.value
            return self <= other

        def __gt__(self, other):
            if isinstance(other, BigInteger.SIGN):
                return self.value > other.value
            return self > other

        def __ge__(self, other):
            if isinstance(other, BigInteger.SIGN):
                return self.value >= other.value
            return self >= other


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
        if self.sign == BigInteger.SIGN.NEGATIVE:
            string = "-"
        
        if order == BigInteger.ORDER.BIGENDIAN:
            string += "".join(map(str, self.integer[::-1]))
        elif  order == BigInteger.ORDER.LITTLEENDIAN:
            string += "".join(map(str, self.integer))
        else:
            raise ValueError("You must provide a valid order.")
        
        return string


    def __str__(self) -> str:
        return self.to_string(order=BigInteger.ORDER.BIGENDIAN)

    def __repr__(self) -> str:
        return f"BigInteger('{self.__str__()}')"

    def get(self, index: int) -> int:
        return self.integer[index] if index < len(self) else None


    def __len__(self):
        return len(self.integer)


    def __neg__(self) -> 'BigInteger':
        """
        Unary minus operator.
        Returns a new BigInteger with the opposite sign.
        """
        new_sign = BigInteger.SIGN.NEGATIVE if self.sign == BigInteger.SIGN.POSITIVE else BigInteger.SIGN.POSITIVE
        return BigInteger(arrInteger=self.integer, sign=new_sign)
    

    def __add__(self, other: 'BigInteger') -> 'BigInteger':
        """
        Perform addition of two BigIntegers.
        Returns a new BigInteger as the result.
        """
        if not isinstance(other, BigInteger):
            raise TypeError("Unsupported operand type for +: '{}' and '{}'".format(type(self).__name__, type(other).__name__))
        
        
        if self.sign == other.sign:
            result_sign = self.sign
            result_integer = []
            carry = 0
        
            for i in range(max(len(self), len(other))):
                val1 = self.get(i) if i < len(self) else 0
                val2 = other.get(i) if i < len(other) else 0
                addition = val1 + val2 + carry
                result_integer.append(addition % 10)
                carry = addition // 10

            if carry:
                result_integer.append(carry)
        else:
            return self - (-other)
        
        return BigInteger(arrInteger=result_integer, sign=result_sign)
    

    def __sub__(self, other: 'BigInteger') -> 'BigInteger':
        """
        Perform substraction of two BigIntegers.
        Returns a new BigInteger as the result.
        """

        if not isinstance(other, BigInteger):
            raise TypeError("Unsupported operand type for -: '{}' and '{}'".format(type(self).__name__, type(other).__name__))


        if self.sign != other.sign:
            return self + (-other)

        compare = BigInteger._compare(self, other)
        if compare == 0:
            return BigInteger(0)
        
        result_sign = self.sign if compare > 0 else BigInteger.SIGN.NEGATIVE if self.sign == BigInteger.SIGN.POSITIVE else BigInteger.SIGN.POSITIVE
        a, b = (self, other) if compare > 0 else (other, self)
            
        result_integer = []
        borrow = 0

        for i in range(max(len(a), len(b))):
            val1 = a.get(i) if i < len(a) else 0
            val2 = b.get(i) if i < len(b) else 0
            diff = val1 - val2 - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            result_integer.append(diff)


        while len(result_integer) > 1 and result_integer[-1] == 0:
            result_integer.pop()
            
        return BigInteger(arrInteger=result_integer, sign=result_sign)


    @staticmethod
    def compare(a: 'BigInteger', b: 'BigInteger') -> int:
        """
        Static method to compare two BigIntegers.

        Params:
            a (BigInteger) : A BigInteger
            b (BigInteger) : A BigInteger

        return:
            1 if a > b
            0 if a = b
            -1 if a < b
        """

        if a.sign > b.sign:
            return 1
        
        elif a.sign < b.sign:
            return -1
        
        else:
            comparison = BigInteger._compare(a, b)
            return comparison if a.sign == b.sign == BigInteger.SIGN.POSITIVE else -comparison


    @staticmethod
    def _compare(a: 'BigInteger', b: 'BigInteger') -> int:
        """
        Static method to compare two BigIntegers (ignoring signs).

        O(k), where k is the lenght of the BigInteger. The worst case happens when we test equality between twos numbers where k is big.

        Params:
            a (BigInteger) : A BigInteger
            v (BigInteger) : A BigInteger

        return:
            1 if a > b
            0 if a = b
            -1 if a < b
        """
        if len(a) > len(b):
            return 1
        
        elif len(a) < len(b):
            return -1
        
        elif len(a) == len(b):
            for i,j in zip(reversed(a.integer), reversed(b.integer)):
                if i > j:
                    return 1
                elif i < j:
                    return -1
            return 0




def run_tests():
    # bigint1 = BigInteger(integer=123456789)
    # bigint2 = BigInteger(arrInteger=[9, 8, 7, 6, 5, 4, 3, 2, 1])
    # bigint3 = BigInteger(arrInteger=[1, 2, 3, 4, 5, 6, 7, 8, 9], order=BigInteger.ORDER.BIGENDIAN)

    # print("First BigInteger:", bigint1.to_string())
    # print("Second BigInteger:", bigint2.to_string())
    # print("Third BigInteger:", bigint3.to_string())
    # print("Inverse First BigInteger:", bigint1.to_string(order=BigInteger.ORDER.LITTLEENDIAN))

    # bigint4 = BigInteger(filePath="./bigint_test.txt", order=BigInteger.ORDER.BIGENDIAN)
    # bigint5 = BigInteger(filePath="./reverse_bigint_test.txt")
    # print("Fourth BigInteger:", bigint4.to_string())
    # print("Fifth BigInteger:", bigint5.to_string())

    # bigIntCompare1 = BigInteger(integer=153)
    # bigIntCompare2 = BigInteger(integer=15)
    # print("Test Compare 1 : ", BigInteger.compare(bigIntCompare1, bigIntCompare2))

    # bigIntCompare3 = BigInteger(integer=153, sign=BigInteger.SIGN.NEGATIVE)
    # bigIntCompare4 = BigInteger(integer=15, sign=BigInteger.SIGN.NEGATIVE)
    # print("Test compare 2 : ", BigInteger.compare(bigIntCompare3, bigIntCompare4))

    # bigIntCompare5 = BigInteger(integer=153)
    # bigIntCompare6 = BigInteger(integer=15, sign=BigInteger.SIGN.NEGATIVE)
    # print("Test compare 3 : ", BigInteger.compare(bigIntCompare5, bigIntCompare6))

    # bigIntCompare7 = BigInteger(integer=153, sign=BigInteger.SIGN.NEGATIVE)
    # bigIntCompare8 = BigInteger(integer=15)
    # print("Test compare 4 : ", BigInteger.compare(bigIntCompare7, bigIntCompare8))

    # bigIntCompare9 = BigInteger(integer=153)
    # bigIntCompare10 = BigInteger(integer=154)
    # print("Test compare 5 : ", BigInteger.compare(bigIntCompare9, bigIntCompare10))

    # bigIntCompare11 = BigInteger(integer=153)
    # bigIntCompare12 = BigInteger(integer=153)
    # print("Test compare 6 : ", BigInteger.compare(bigIntCompare11, bigIntCompare12))

    # bigIntCompare13 = BigInteger(integer=153, sign=BigInteger.SIGN.NEGATIVE)
    # bigIntCompare14 = BigInteger(integer=154, sign=BigInteger.SIGN.NEGATIVE)
    # print("Test compare 7 : ", BigInteger.compare(bigIntCompare13, bigIntCompare14))

    # bigIntCompare15 = BigInteger(integer=153, sign=BigInteger.SIGN.NEGATIVE)
    # bigIntCompare16 = BigInteger(integer=153, sign=BigInteger.SIGN.NEGATIVE)
    # print("Test compare 8 : ", BigInteger.compare(bigIntCompare15, bigIntCompare16))


    bigIntAdd1 = BigInteger(integer=236)
    bigIntAdd2 = BigInteger(integer=79)
    print("{} + {} = {}".format(bigIntAdd1, bigIntAdd2, bigIntAdd1 + bigIntAdd2))

    bigIntAdd3 = BigInteger(integer=236, sign=BigInteger.SIGN.NEGATIVE)
    bigIntAdd4 = BigInteger(integer=79, sign=BigInteger.SIGN.NEGATIVE)
    print("{} + {} = {}".format(bigIntAdd3, bigIntAdd4, bigIntAdd3 + bigIntAdd4))

    bigIntAdd5 = BigInteger(integer=236, sign=BigInteger.SIGN.NEGATIVE)
    bigIntAdd6 = BigInteger(integer=79)
    print("{} + {} = {}".format(bigIntAdd5, bigIntAdd6, bigIntAdd5 + bigIntAdd6))

    bigIntAdd7 = BigInteger(integer=236)
    bigIntAdd8 = BigInteger(integer=79, sign=BigInteger.SIGN.NEGATIVE)
    print("{} + {} = {}".format(bigIntAdd7, bigIntAdd8, bigIntAdd7 + bigIntAdd8))

    bigIntSub1 = BigInteger(integer=236)
    bigIntSub2 = BigInteger(integer=79)
    print("{} - {} = {}".format(bigIntSub1, bigIntSub2, bigIntSub1 - bigIntSub2)) # 157

    bigIntSub3 = BigInteger(integer=236, sign=BigInteger.SIGN.NEGATIVE)
    bigIntSub4 = BigInteger(integer=79, sign=BigInteger.SIGN.NEGATIVE)
    print("{} - {} = {}".format(bigIntSub3, bigIntSub4, bigIntSub3 - bigIntSub4)) #-157

    bigIntSub5 = BigInteger(integer=236, sign=BigInteger.SIGN.NEGATIVE)
    bigIntSub6 = BigInteger(integer=79)
    print("{} - {} = {}".format(bigIntSub5, bigIntSub6, bigIntSub5 - bigIntSub6))  # -315

    bigIntSub7 = BigInteger(integer=236)
    bigIntSub8 = BigInteger(integer=79, sign=BigInteger.SIGN.NEGATIVE)
    print("{} - {} = {}".format(bigIntSub7, bigIntSub8, bigIntSub7 - bigIntSub8)) # 315

    bigIntSub9 = BigInteger(integer=79)
    bigIntSub10 = BigInteger(integer=236)
    print("{} - {} = {}".format(bigIntSub9, bigIntSub10, bigIntSub9 - bigIntSub10)) # -157
    
    bigIntSub11 = BigInteger(integer=79, sign=BigInteger.SIGN.NEGATIVE)
    bigIntSub12 = BigInteger(integer=236, sign=BigInteger.SIGN.NEGATIVE)
    print("{} - {} = {}".format(bigIntSub11, bigIntSub12, bigIntSub11 - bigIntSub12)) # 157

    bigIntSub13 = BigInteger(integer=10)
    bigIntSub14 = BigInteger(integer=9)
    print("{} - {} = {}".format(bigIntSub13, bigIntSub14, bigIntSub13 - bigIntSub14)) # 1

run_tests()