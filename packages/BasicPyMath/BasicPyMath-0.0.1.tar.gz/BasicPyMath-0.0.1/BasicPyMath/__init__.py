import math

def Add(num1, num2):
    return num1 + num2

def Subtract(num1, num2):
    return num1 - num2

def Multiply(num1, num2):
    return num1 * num2

def Divide(num1, num2):
    return num1 / num2

def Sqrt(num1):
    return math.sqrt(num1)

def Pow(Base, Exponent):
    ElevatedNum = 1
    Exponent += 1
    while Exponent >= 2:
        ElevatedNum = ElevatedNum * Base
        Exponent -= 1
    if (Exponent == 0):
        return 0
    else:
        return ElevatedNum

def Greater(num1, num2):
    if (num1 > num2):
        return num1
    elif (num2 > num1):
        return num2

def Less(num1, num2):
    if (num1 < num2):
        return num1
    elif (num2 < num1):
        return num2

def Equal(num1, num2):
    if (num1 == num2):
        return True
    elif (num1 != num2):
        return False

def Different(num1, num2):
    if (num1 != num2):
        return True
    elif (num1 == num2):
        return False

def FindHypotenuse(FirstCathetus, SecondCathetus):
    Hypotenuse = math.sqrt((FirstCathetus * FirstCathetus) - (SecondCathetus * SecondCathetus))
    return Hypotenuse

def FindCathetus(Cathetus, Hypotenuse):
    MissingCathetus = math.sqrt((Hypotenuse * 2) - (Cathetus * 2))
    return MissingCathetus

def SquareArea(sideLenght):
    return sideLenght * sideLenght

def RectangleArea(FirstSideLenght, SecondSideLenght):
    return FirstSideLenght * SecondSideLenght

def ParallelogramArea(FirstSideLenght, SecondSideLenght):
    return FirstSideLenght * SecondSideLenght

def TriangleArea(Base, Height):
    return (Base * Height) / 2

def TrapezoidArea(MajorBase, MinorBase, Height):
    return ((MajorBase + MinorBase) * Height) / 2

def RhombusArea(MajorDiagonal, MinorDiagonal):
    return (MajorDiagonal * MinorDiagonal) / 2

