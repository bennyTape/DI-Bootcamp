# Exercise 1: Pets
# Key Python Topics:
# Inheritance
# Class instantiation
# Lists
# Polymorphism
# Instructions:
# Use the provided Pets and Cat classes to create a Siamese breed, instantiate cat objects, and use the Pets class to manage them.
# See the example below, before diving in.

class Pets():
    def __init__(self, animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())

class Cat():
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'

class Bengal(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class Chartreux(Cat):
    def sing(self, sounds):
        return f'{sounds}'
        
class Siamese(Cat):
    pass

bengal_obj = Bengal("beng",3)
Chartreux =Chartreux("Chatr",2) 
Siam =  Siamese("Siam",2) 
all_cats = [bengal_obj,Chartreux,Siam ]


sara_pets = Pets(all_cats)
sara_pets.walk()






# Exercise 2: Dogs
# Goal: Create a Dog class with methods for barking, running speed, and fighting.
# Step 1: Create the Dog Class
# Create a class called Dog with name, age, and weight attributes.
# Implement a bark() method that returns “<dog_name> is barking”.
# Implement a run_speed() method that returns weight / age * 10.
# Implement a fight(other_dog) method that returns a string indicating which dog won the fight, based on run_speed * weight.
class Dog:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def bark(self):
        return f'{self.name} is barking'

    def run_speed(self):
        return self.weight / self.age * 10

    def fight(self, other_dog):
        my_power = self.run_speed() * self.weight
        other_power = other_dog.run_speed() * other_dog.weight

        if my_power > other_power:
            return f'{self.name} won the fight!'
        elif other_power > my_power:
            return f'{other_dog.name} won the fight!'
        else:
            return "It's a tie!"

# Step 2: Create dog instances
# Step 2: Create Dog Instances
# Create three instances of the Dog class with different names, ages, and weights.

dog1 = Dog('Rex',    5, 30)
dog2 = Dog('Buddy',  3, 20)
dog3 = Dog('Max',    4, 25)

# Step 3: Test Dog Methods
# Call the bark(), run_speed(), and fight() methods on the dog instances to test their functionality.

print(dog1.bark())
print(dog2.bark())
print(dog3.bark())

print(dog1.run_speed())
print(dog2.run_speed())
print(dog3.run_speed())

print(dog1.fight(dog2))
print(dog2.fight(dog3))
print(dog1.fight(dog3))








# Exercise 4: Family and Person Classes
# Goal:

# Practice working with classes and object interactions by modeling a family and its members.
# Step 1: Create the Person class
class Person:
    def __init__(self, first_name, age):
        self.first_name = first_name
        self.age = age
        self.last_name = ''

    def is_18(self):
        return self.age >= 18


# Step 2: Create the Family class
class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = []

    def born(self, first_name, age):
        new_person = Person(first_name, age)
        new_person.last_name = self.last_name
        self.members.append(new_person)
        print(f'Welcome to the family, {first_name} {self.last_name}!')

    def check_majority(self, first_name):
        for member in self.members:
            if member.first_name == first_name:
                if member.is_18():
                    print(f'You are over 18, your parents Jane and John accept that you will go out with your friends')
                else:
                    print(f'Sorry, you are not allowed to go out with your friends.')
                return
        print(f'{first_name} is not a member of the {self.last_name} family.')

    def family_presentation(self):
        print(f'\n--- The {self.last_name} Family ---')
        for member in self.members:
            print(f'  {member.first_name} {member.last_name}, Age: {member.age}')


# --- Test ---
my_family = Family('Smith')

my_family.born('Alice', 20)
my_family.born('Bob',   15)
my_family.born('Clara', 18)

my_family.family_presentation()

print()
my_family.check_majority('Alice')
my_family.check_majority('Bob')
my_family.check_majority('Clara')
my_family.check_majority('Dave')


