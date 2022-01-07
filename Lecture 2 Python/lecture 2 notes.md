## Notes: Lecture 2 Python

## Python
Powerful, interpreted language, easy to build things quickly  
```print("Hello, world!")```, save to hello.py  
>python hello.py  
->Hello, world!  


## Variables
Dynamically-typed language, variables are not declared with a type  
Variable types: int, float, complex, str, bool, NoneType, etc.  
```name = input("Name: ") print("Hello, " + name)```  , save to name.py  
>python name.py  
->Name: Dave  
->Hello, Dave   


## Formatting Strings
name.py with fstrings:  
```name = input("Name: ") print(f"Hello, {name}!")```, save name.py  
>python name.py  
->Name: Dave  
->Hello, Dave! 

## Conditions
if conditionA:  
    expression1  
elif (conditionB OR (conditionC AND conditionD):  
    expression2  
else:  
    expression3  

shorthand: expression1 if conditionA else expression2  


## Sequences and Loops
Sequences are either mutable or immutable (aka, elements are editable or not),
ordered or not, and unique or not (aka allows element duplicates)  
Sequence types: strings, lists, tuples, sets, dicts  

Strings: ordered, immutable, allows duplicates  
>name="Dave"  
>print(name[0]) ->D  
>print(name[0:2]) ->Da  

Lists: ordered, mutable, allows duplicates  
>fruits = ["apple", "banana", "watermelon"]  
>print(fruits)  
->["apple", "banana", "watermelon"]  

>print(fruits[2])  
->watermelon  

>fruits.append("cherry")  
>fruits.sort()  
>print(fruits[2])  
->cherry

Tuples: ordered, immutable, allows duplicates  
```pointcoordinates = (12.2, -4, 1.8)```  

Sets: ordered, elements can be added/removed, unique (no duplicates)  
create an empty set:  
>s = set()  

add/rem some elements:  
>s.add(1) s.add(2) s.add(3) s.add(1) s.remove(3)  

>print(s) ->{1,2}  
>print(len(s)) ->2  

Dictionaries (Dicts): unordered*, mutable, allows duplicate values (not keys)  
*Note: as of python 3.6, default is OrderedDicts, which keep the key:value
insertion order:
https://stackoverflow.com/questions/39980323/are-dictionaries-ordered-in-python-3-6/39980744#39980744
  
>foods = {"fruit": "apple", "spinach": "vegetable", "grain": "bread"}  
>print(foods["fruit"])  
->Apple  
>foods["meat"] = "chicken"  

```food.clear()```: deletes all elements from food  
```food.items()```: returns a list of the dict's keys  
```food.values()```: returns a list of all the dict's values  
```food.setdefault(key, value)```: returns the value of a key if it exists, otherwise
inserts the key:value pair

Loops: For loops and While loops  
>for i in [0, 1, 2, 3, 4, 5]:  
->prints 0 through 5  

>for i in range(6):  
->prints 0 through 5  

>while i<6:  
->prints 0 through 6, and increments i+=1 each loop  

>for fruit in fruits:  
->apple ->banana ->cherry ->watermelon


## Functions
```def square(x):```  
&emsp;```return x * x```  
>square(3)  
->9  


## Modules
put ```square(x)``` into a new file ```functions.py```, then use ```squares.py``` with:  
```from functions import square```, then use ```square()``` in code, or,  
```import functions```, then use ```functions.square()``` in code  
Many modules available to use  

## Object-Oriented Programming
A style of programming centered on objects that store information and perform
actions.  
A class is a template to create a new data type with associated functions  
Functions in a class are called methods  
```class point():```  
&emsp;```def __init__(self, x, y):```  
&emsp;&emsp;```self.x = x```  
&emsp;&emsp;```self.y = y```  
&emsp;```def distance(self, x, y):```  
&emsp;&emsp;```return( sqrt( square(x)+square(y)))```  

>p = point(3, 4)  
>print(p.x, p.y, p.distance())  
->3 4 5  


## Functional Programming  
A style of programming centered on functions, where functions are treated as
values like any other variable. They can be passed in and returned by other
functions.    

Wrapper: A function that can modify another function. Applied using symbol
```@```  
see decorators.py


Lambda expressions: 1-line expressions to create a function  
Takes the form: ```lambda arg1 arg2 argN: expression to return```  

comparing a regular function sum() to its lambda  
```def sum(x, y):```  
&emsp;```return x+y```  
as a lambda: ```lambda x, y: x+y```  


## Exceptions  
Dealing with things that go wrong  
List of exceptions: https://docs.python.org/3/library/exceptions.html#exception-hierarchy  
Catching exceptions:  
```try:``` run some block of code  
```except:``` if there is an exception in the ```try``` block, run this code  
```else:``` if there are no exceptions in the ```try``` block, run this code  
```finally:``` either way, afterwards, run this code  
```else``` and ```finally``` can be used for logging errors or for making
functions severable, so even if part of a function fails, the rest will work  