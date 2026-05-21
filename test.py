
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


