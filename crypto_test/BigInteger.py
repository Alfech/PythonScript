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
            return False

        def __le__(self, other):
            if isinstance(other, BigInteger.SIGN):
                return self.value <= other.value
            return False

        def __gt__(self, other):
            if isinstance(other, BigInteger.SIGN):
                return self.value > other.value
            return False

        def __ge__(self, other):
            if isinstance(other, BigInteger.SIGN):
                return self.value >= other.value
            return False

        def __eq__(self, other):
            if isinstance(other, BigInteger.SIGN):
                return self.value == other.value
            return False


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
            if integer == 0:
                self.integer = [0]
            else:
                while integer > 0:
                    self.integer.append(integer%10)
                    integer //=10

        elif arrInteger is not None:
            self.integer = arrInteger

        elif filePath is not None:
            with open(filePath, 'r') as file:
                for line in file:
                    for c in line:
                        if c.isdigit():
                            self.integer.append(int(c))
                            
        else:
            raise ValueError("You must provide an integer an array of integer or a file path storing a BigInteger")

        if order == BigInteger.ORDER.BIGENDIAN:
            self.integer.reverse()


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


    def __lt__(self, other):
        if isinstance(other, BigInteger):
            return BigInteger.compare(self, other) == -1
        return False

    def __le__(self, other):
        if isinstance(other, BigInteger):
            return BigInteger.compare(self, other) <= 0
        return False

    def __gt__(self, other):
        if isinstance(other, BigInteger):
            return BigInteger.compare(self, other) == 1
        return False

    def __ge__(self, other):
        if isinstance(other, BigInteger):
            return BigInteger.compare(self, other) >= 0
        return False

    def __eq__(self, other):
        if isinstance(other, BigInteger):
            return BigInteger.compare(self, other) == 0
        return False


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