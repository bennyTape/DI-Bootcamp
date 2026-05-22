# exercise 1 : Geometry
# Instructions
# Write a class called Circle that receives a radius as an argument (default is 1.0).
# Write two instance methods to compute perimeter and area.
# Write a method that prints the geometrical definition of a circle.

class circle:
    def __init__(self,radius=10):
        self.radius = radius

    def perimeter(self):
        return 2*(3.14)*self.radius
    
    def geo_def(self):
        print(f"circle of radius {self.radius}")
    

cercle1=  circle(10)
cercle2=  circle(20)




# Exercise 2 : Custom List Class
# Instructions
# Create a class called MyList, the class should receive a list of letters.
# Add a method that returns the reversed list.
# Add a method that returns the sorted list.
# Bonus : Create a method that generates a second list with the same length as mylist. The list should be constructed with random numbers. (use list comprehension).


class MyList:
    def reverse_list(self, letter_list):
       return letter_list.reverse()
    

    


