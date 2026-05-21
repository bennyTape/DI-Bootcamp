# Exercise 1: Converting Lists into Dictionaries
# Key Python Topics:
# Creating dictionaries
# Zip function or dictionary comprehension
# Instructions
# You are given two lists. Convert them into a dictionary where the first list contains the keys and the second list contains the corresponding values.
keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]
diction ={}
for i in range(len(keys)):
    diction[keys[i]] = values[i]
# diction = {keys[0]:values[0],}
print(diction)





# Exercise 2 
# Instructions
# Write a program that calculates the total cost of movie tickets for a family based on their ages.
# Family members’ ages are stored in a dictionary.
# The ticket pricing rules are as follows:
# Under 3 years old: Free
# 3 to 12 years old: $10
# Over 12 years old: $15
# Family Data:
family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}
total =0
for x,y in family.items():
    total+=y
    if y < 3:
        print(x + " : Free")
    elif y < 12:
        print(x+ " : $10")
    else:
        print(x+ " : $15")
print("The total coast is"+str(total))





#  Exercise 3: Zara
# Key Python Topics:
# Creating dictionaries
# Accessing and modifying dictionary elements
# Dictionary methods like .pop() and .update()
# Instructions
# Create and manipulate a dictionary that contains information about the Zara brand.
# instructions
# Create and manipulate a dictionary that contains information about the Zara brand.
# Brand Information:

# name: Zara
# creation_date: 1975
# creator_name: Amancio Ortega Gaona
# type_of_clothes: men, women, children, home
# international_competitors: Gap, H&M, Benetton
# number_stores: 7000
# major_color: 
#     France: blue, 
#     Spain: red, 
#     US: pink, green
# Create a dictionary called brand with the provided data.
# Modify and access the dictionary as follows:
# Change the value of number_stores to 2.
# Print a sentence describing Zara’s clients using the type_of_clothes key.
# Add a new key country_creation with the value Spain.
# Check if international_competitors exists and, if so, add “Desigual” to the list.
# Delete the creation_date key.
# Print the last item in international_competitors.
# Print the major colors in the US.
# Print the number of keys in the dictionary.
# Print all keys of the dictionary.

brand = {'name':'Zara',
           
           'creation_date' : '1975',

           'creator_name':'Amancio Ortega Gaona',
           
           'type_of_clothes':['men','women','children','home'],

           'international_competitors' : ['Gap','H&M','Benetton'],

           'number_stores':'7000',

           'major_color':
                {
                    'France':'blue',
                    'Spain':'red',
                    'US': ['pink','green']
                }    
           }
brand['number_stores'] ='2'
print("The different type of clothes are: "+brand['type_of_clothes'][0]+' '+brand['type_of_clothes'][1]+' '+brand['type_of_clothes'][2]+' '+brand['type_of_clothes'][3])
brand['country_creation'] ='Spain'

if 'international_competitors' in brand:
    brand['international_competitors'].append('Desigual')
del brand['creation_date']

print(brand['international_competitors'][-1])
#major color in the US
print(brand['major_color']['US'])
#number of keys and all keys
nb_key =0
for i in brand:
    nb_key+=1
    print(i)
print('the number of keys is '+ str(nb_key))







#  Exercise 4 : Some Geography
# Goal: Create a function that describes a city and its country.
# Key Python Topics:
# Functions with multiple parameters
# Default parameter values
# String formatting
# Step 1: Define a Function with Parameters
# Define a function named describe_city().
# This function should accept two parameters: city and country.
# Give the country parameter a default value, such as “Unknown”.
# Step 2: Print a Message
# Inside the function, set up the code to display a sentence like “ is in “.
# Replace <city> and <country> with the parameter values.
# Step 3: Call the Function
# Call the describe_city() function with different city and country combinations.
# Try calling it with and without providing the country argument to see the default value in action.
# Example: describe_city("Reykjavik", "Iceland") and describe_city("Paris").
def describe_city(city, country ='Unknown'):
    print(f"{city} is in {country}")

describe_city("Abidjan","Côte d'ivoire")  
describe_city("Cotonou","Bénin")
describe_city("sao tomé")




import random
# Exercise 5 : Random
# Goal: Create a function that generates random numbers and compares them.
# Key Python Topics:
# random module
# random.randint() function
# Conditional statements (if, else)
def my_function(nb):
    rd_nb = random.randint(1,100)

    if int(nb) == rd_nb :
        print("fail message and display both numbers")
    else:
        print("the two numbers are differents")
my_function(28)





# Exercise 6 : Let’s create some personalized shirts !
# Goal: Create a function to describe a shirt’s size and message, with default values.
# Key Python Topics:
# Functions with parameters and default values
# Keyword arguments
def make_shirt(size ="large",text="I love Python"):
    print("The size of the shirt is "+size +" and the text is " +text)

make_shirt("M"," Size M ")

make_shirt(text="large shirt")
make_shirt(size="medium")
make_shirt(size="very large",text="very large size")





# Exercise 7 : Temperature Advice
# Goal: Generate a random temperature and provide advice based on the temperature range.
# Key Python Topics:
# Functions
# Conditionals (if / elif)
# Random numbers
# Floating-point numbers (Bonus)
# Handling seasons (Bonus)
import random
def get_random_temp():
     return random.randint(-10,40)

def main():
    temp = get_random_temp()
    print(f"The temperature right now is {temp} degrees Celsius.")
    if temp < 0 :
          print("Brrr, that’s freezing! Wear some extra layers today.")
    elif temp < 16 :
            print("Quite chilly! Don’t forget your coat.")
    elif temp < 23 :
           print("Nice weather.")
    elif temp < 32:
          print("A bit warm, stay hydrated.")
    else:
          print("It’s really hot! Stay cool.")




# Exercise 8: Pizza Toppings
# Key Python Topics:
# Loops
# Lists
# String formatting
# Instructions:
# Write a loop that asks the user to enter pizza toppings one by one.
# Stop the loop when the user types 'quit'.
# For each topping entered, print:
# "Adding [topping] to your pizza."
# After exiting the loop, print all the toppings and the total cost of the pizza.
# The base price is $10, and each topping adds $2.50.
base_price =10
pizza =[]
while True:
    response = input("enter a topping")
    if response == "quit":
        break
    print(f"Adding {response} to your pizza")
    pizza.append(response)
    base_price+=2.5

print(f"the amount is {base_price}")












