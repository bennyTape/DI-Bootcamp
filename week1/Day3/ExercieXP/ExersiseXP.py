
#Exercice1
# Instructions:
# Use the provided Cat class to create three cat objects. Then, create a function to find the oldest cat and print its details.
class Cat:
    def __init__(self, cat_name, cat_age):
        self.name = cat_name
        self.age = cat_age
    def __str__(self):
        return f"the cat is {self.name} and hit age is {self.age}"
cat1 = Cat("miaous", 2)
cat2 = Cat("milou", 3)
cat3 = Cat("tigger",1)

def find_oldest_cat(cat1, cat2, cat3):
    if cat1.age > cat2.age and cat1.age > cat3.age :
        return cat1
    elif cat2.age > cat1.age and cat2.age > cat3.age :
        return cat2
    else:
        return cat3
print(find_oldest_cat(cat1,cat2, cat3))






# Exercise 2 : Dogs
# Instructions:
# Create a Dog class with methods for barking and jumping. Instantiate dog objects, call their methods, and compare their sizes.
class Dog:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def bark(self):
        print(f"{self.name} goes woof!")

    def jump(self):
        print(f"{self.name} jump { self.height} cm high!")
        
davids_dog = Dog('davids', 120)
sarahs_dog = Dog('sarahs', 80)

print(davids_dog.bark())
print(davids_dog.jump())

print(sarahs_dog.bark())
print(sarahs_dog.height())

if sarahs_dog.height < davids_dog.height:
    print(f"{sarahs_dog.name} heigts upper ")
else:
    print(f"{davids_dog.name} heigts upper")



# Exercise 3 : Who’s the song producer?
# Goal: Create a Song class to represent song lyrics and print them.
# Create a Song class with a method to print song lyrics line by line.
class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics

    def sing_me_a_song(self):
         for i in self.lyrics:
             print(i)

stairway = Song(["There’s a lady who's sure", "all that glitters is gold", "and she’s buying a stairway to heaven"])
stairway.sing_me_a_song()   




# Exercise 4 : Afternoon at the Zoo
# Goal:

# Create a Zoo class to manage animals. The class should allow adding animals, displaying them, selling them, and organizing them into alphabetical groups.


class Zoo:
    def __init__(self, zoo_name):
        self.animals = []
    def add_animal(self,new_animal):
        if new_animal in self.animals:
            pass
        else:
          self.animals.append(new_animal)
    def get_animals(self):
        for animal in self.animals:
            print(animal)
    
    def sell_animal(self,animal_sold):
        if animal_sold in self.animals:
            self.animals.remove(animal_sold)

    def sort_animals(self):
       self.animals.sort()
       diction = {}
       for i in self.animals:
           i.capitalize()
           if i[0] in diction.keys():
               if i in diction[i[0]]:
                   pass
               else:
                  diction[i[0]].append(i)      
           else:
               diction[i[0]] = [i]
       print(diction)

brooklyn_safari = Zoo("Brooklyn Safari")

# Step 3: Use the Zoo methods
brooklyn_safari.add_animal("Giraffe")
brooklyn_safari.add_animal("Bear")
brooklyn_safari.add_animal("Baboon")
brooklyn_safari.add_animal("Cougar")
brooklyn_safari.add_animal("Cougar")
brooklyn_safari.add_animal('Zebra')
brooklyn_safari.add_animal('Cat')
brooklyn_safari.sort_animals()

print(brooklyn_safari.animals)




    
