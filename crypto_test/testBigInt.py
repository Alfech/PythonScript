import unittest
from BigInteger import BigInteger

class testBigInt(unittest.TestCase):

    def test_BigIntegerCreationLittleEndian(self):
        test_cases = [
            (BigInteger(integer=123456789), "123456789"),
            (BigInteger(arrInteger=[9, 8, 7, 6, 5, 4, 3, 2, 1]), "123456789"),
            (BigInteger(arrInteger=[1, 2, 3, 4, 5, 6, 7, 8, 9]), "987654321"),
            (BigInteger(filePath="./bigint_test.txt"), "987654321987654321"),
            (BigInteger(filePath="./reverse_bigint_test.txt"), "123456789123456789")
        ]

        for bigInt, expected in test_cases:
            self.assertEqual(bigInt.to_string(), expected)


    def test_BigIntegerCreationBigEndian(self):
        test_cases = [
            (BigInteger(integer=123456789, order=BigInteger.ORDER.BIGENDIAN), "987654321"),
            (BigInteger(arrInteger=[9, 8, 7, 6, 5, 4, 3, 2, 1], order=BigInteger.ORDER.BIGENDIAN), "987654321"),
            (BigInteger(arrInteger=[1, 2, 3, 4, 5, 6, 7, 8, 9], order=BigInteger.ORDER.BIGENDIAN), "123456789"),
            (BigInteger(filePath="./bigint_test.txt", order=BigInteger.ORDER.BIGENDIAN), "123456789123456789"),
            (BigInteger(filePath="./reverse_bigint_test.txt", order=BigInteger.ORDER.BIGENDIAN), "987654321987654321")
        ]

        for bigInt, expected in test_cases:
            self.assertEqual(bigInt.to_string(), expected)


    def test_BigIntegertoStringLittleEndian(self):
        test_cases = [
            (BigInteger(integer=123456789), "987654321"),
            (BigInteger(arrInteger=[9, 8, 7, 6, 5, 4, 3, 2, 1]), "987654321"),
            (BigInteger(arrInteger=[1, 2, 3, 4, 5, 6, 7, 8, 9]), "123456789"),
            (BigInteger(filePath="./bigint_test.txt"), "123456789123456789"),
            (BigInteger(filePath="./reverse_bigint_test.txt"), "987654321987654321"),
            (BigInteger(integer=123456789, order=BigInteger.ORDER.BIGENDIAN), "123456789"),
            (BigInteger(arrInteger=[9, 8, 7, 6, 5, 4, 3, 2, 1], order=BigInteger.ORDER.BIGENDIAN), "123456789"),
            (BigInteger(arrInteger=[1, 2, 3, 4, 5, 6, 7, 8, 9], order=BigInteger.ORDER.BIGENDIAN), "987654321"),
            (BigInteger(filePath="./bigint_test.txt", order=BigInteger.ORDER.BIGENDIAN), "987654321987654321"),
            (BigInteger(filePath="./reverse_bigint_test.txt", order=BigInteger.ORDER.BIGENDIAN), "123456789123456789")
        ]

        for bigInt, expected in test_cases:
            self.assertEqual(bigInt.to_string(BigInteger.ORDER.LITTLEENDIAN), expected)


    def test_BigIntegerCompare(self):
        test_cases = [
            (BigInteger(integer=153), BigInteger(integer=15), 1),
            (BigInteger(integer=153, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=15, sign=BigInteger.SIGN.NEGATIVE), -1),
            (BigInteger(integer=153), BigInteger(integer=15, sign=BigInteger.SIGN.NEGATIVE), 1), 
            (BigInteger(integer=153, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=15), -1),
            (BigInteger(integer=153), BigInteger(integer=154), -1),
            (BigInteger(integer=153), BigInteger(integer=153), 0),
            (BigInteger(integer=987654321987654321), BigInteger(integer=987654321987654320), 1),
            (BigInteger(integer=987654321987654321), BigInteger(integer=987654321987654321), 0),
        ]

        for bigint1, bigint2, expected in test_cases:
            with self.subTest(bigint1=bigint1, bigint2=bigint2):
                self.assertEqual(BigInteger.compare(bigint1, bigint2), expected)


    def test_bigIntegerAdd(self):
        test_cases = [
            (BigInteger(integer=236), BigInteger(integer=79), BigInteger(integer=315)),
            (BigInteger(integer=236, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=79, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=315, sign=BigInteger.SIGN.NEGATIVE)),
            (BigInteger(integer=236, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=79), BigInteger(integer=157, sign=BigInteger.SIGN.NEGATIVE)),
            (BigInteger(integer=236), BigInteger(integer=79, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=157)),
        ]

        for bigint1, bigint2, expected in test_cases:
            with self.subTest(bigint1=bigint1, bigint2=bigint2):
                self.assertEqual(bigint1 + bigint2, expected)


    def test_bigIntegerSub(self):
        test_cases = [
            (BigInteger(integer=236), BigInteger(integer=79), BigInteger(integer=157)),
            (BigInteger(integer=236, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=79, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=157, sign=BigInteger.SIGN.NEGATIVE)),
            (BigInteger(integer=236, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=79), BigInteger(integer=315, sign=BigInteger.SIGN.NEGATIVE)),
            (BigInteger(integer=236), BigInteger(integer=79, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=315)),
            (BigInteger(integer=79), BigInteger(integer=236), BigInteger(integer=157, sign=BigInteger.SIGN.NEGATIVE)),
            (BigInteger(integer=79, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=236, sign=BigInteger.SIGN.NEGATIVE), BigInteger(integer=157)),
            (BigInteger(integer=10), BigInteger(integer=9), BigInteger(integer=1)),
            (BigInteger(integer=9), BigInteger(integer=10), BigInteger(integer=1, sign=BigInteger.SIGN.NEGATIVE)),
        ]

        for bigint1, bigint2, expected in test_cases:
            with self.subTest(bigint1=bigint1, bigint2=bigint2):
                self.assertEqual(bigint1 - bigint2, expected)


if __name__ == '__main__':
    unittest.main()