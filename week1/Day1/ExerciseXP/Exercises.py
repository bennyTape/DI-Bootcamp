#Exercice 1
#Instructions
# Print the following output using one line of code:
# Hello world
# Hello world
# Hello world
# Hello world
print("Hello World\nHello World\nHello World\nHello World")



#Exercice 2
# Instructions
# Write code that calculates the result of:
# (99^3)*8 (meaning 99 to the power of 3, times 8).
result = (99**3)*8
print(result)




#Exercice 3
# Instructions
# Predict the output of the following code snippets:
# Coment what is your guess, then run the code and compare
# Example:
# >>> 15 < 8 #False
5 < 3 #False
3==3  #True
3=="3" #False
"3"> 3 #TypeError: '>' not supported between instances of 'str' and 'int'
"Hello" == "hello" #False


#Exercice 4
# Instructions
# Create a variable called computer_brand which value is the brand name of your computer.
# Using the computer_brand variable, print a sentence that states the following:
# "I have a <computer_brand> computer."
import platform
computer_brand  = platform.node()
print(f"I have a { computer_brand} computer")



#Exercice 5
# Instructions
# Create a variable called name, and set it’s value to your name.
# Create a variable called age, and set it’s value to your age.
# Create a variable called shoe_size, and set it’s value to your shoe size.
# Create a variable called info and set it’s value to an interesting sentence about yourself. The sentence must contain all the variables created in parts 1, 2, and 3.
# Have your code print the info message.
# Run your code.
name ="TAPE KOFFI ISAAC"
age = 20
shoe_size =44
info =f"My name is {name} i am {age} yo an my shoe size is {shoe_size}."
print(info)



#Exercice 6
# Instructions
# Create two variables, a and b.
# Each variable’s value should be a number.
# If a is bigger than b, have your code print "Hello World".
a =15
b =24
if a > b:
    print("Hello World")



#Exercice 7
# Instructions
# Write code that asks the user for a number and determines whether this number is odd or even.
a= input("enter a number ")
if int(a)%2 ==0:
    print("your number is even")
else:
    print("your number is odd")



#Exercice 8
# Instructions
# Write code that asks the user for their name and determines whether or not you have the same name. Print out a funny message based on the outcome.
my_name= "TAPE"
user_name = input("What is your name ?")
if user_name.upper() == my_name:
    print("Well !! we have the same name!")
else :
    print("Unfortunatly your name is deferent of mine !")



#Exercice 9
# Instructions
# Write code that will ask the user for their height in centimeters.
# If they are over 145 cm, print a message that states they are tall enough to ride.
# If they are not tall enough, print a message that says they need to grow some more to ride.
height = input("what is your height (in cm )?")
if int(height) > 145:
    print("they are tall enough to ride")
else:
    print("they need to grow some more to ride")