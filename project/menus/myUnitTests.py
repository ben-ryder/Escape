#Adam Hamilton-Sutherland
#My example Unit Tests
import unittest

#My functions that will be tested===========================

#flips the bool given to its opposite
def flip(boolToFlip):
    return not boolToFlip

#averages the 2 numbers given
def average(num1, num2):
    return (num1 + num2)/2

#finds the nth number in the fibonacci sequence using recursion and memoization.
foundNums = {0:0, 1:1}
def fib(n):
    if n in foundNums:
        return foundNums[n]
    else:
        num = fib(n-1) + fib(n-2)
        foundNums[n] = num
        return num

#unit tests==================================================
class MyTests(unittest.TestCase):
    def setUp(self):
        pass
    
    #tests the flip function I wrote
    def test_flip(self):
        self.assertEqual(flip(False), True)
    
    def test_flip2(self):
        self.assertEqual(flip(True), False)

    #tests the average function I wrote
    def test_average(self):
        self.assertEqual(average(10,10), 10)

    def test_average2(self):
        self.assertEqual(average(15,25), 20)

    def test_average3(self):
        self.assertEqual(average(30,50), 40)
    
    def test_average4(self):
        self.assertEqual(average(130,60), 95)

    def test_average5(self):
        self.assertEqual(average(100003,47.8), 50025.4)

    #tests the fib function I wrote
    def test_fib(self):
        self.assertEqual(fib(3), 2)

    def test_fib2(self):
        self.assertEqual(fib(4), 3)
    
    def test_fib3(self):
        self.assertEqual(fib(5), 5)

    def test_fib4(self):
        self.assertEqual(fib(6), 8)

    def test_fib5(self):
        self.assertEqual(fib(7), 13)

if __name__ == "__main__":
    unittest.main()
