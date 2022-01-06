## Notes: Lecture 2 Python

## Python
Powerful, interpreted language, easy to build things quickly  
print("Hello, world!"), save to hello.py  
>python hello.py ->Hello, world!  


## Variables
Dynamically-typed language, variables are not declared with a type  
Variable types: int, float, complex, str, bool, NoneType, etc.  
name = input("Name: ")  print("Hello, " + name), save to name.py  
>python name.py  
->Name: Dave  
->Hello, Dave   


## Formatting Strings
name.py with fstrings:  
name = input("Name: ") /n print(f"Hello, {name}!"), save name.py  
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
name="Dave"  
>print(name[0]) ->D 
>print(name[0:2]) ->Da  

Lists: ordered, mutable, allows duplicates  
fruit = ["apple", "banana", "watermelon"]  
>print(fruit) ->["apple", "banana", "watermelon"]  
>print(fruit[2]) ->watermelon  
>fruit.append("cherry")  
>fruit.sort()  
>print(fruit[2]) ->cherry

Tuples: ordered, immutable, allows duplicates  
pointcoordinates = (12.2, -4, 1.8)  

Sets: ordered, elements can be added/removed, unique (no duplicates)  
create an empty set: s = set()  
add/rem some elements: s.add(1) s.add(2) s.add(3) s.add(1) s.remove(3)  
>print(s) ->{1,2}  
>print(len(s)) ->2  

Loops: for loops and while loops  

## Functions


## Modules


## Object-Oriented Programming


## Functional Programming


## Exceptions