# Ask the user for their birthdate (specify the format, for example: DD/MM/YYYY).
# Display a little cake as seen below:
actual_year = 2026
actual_month = 5
actual_day = 20
nb1 = input("enter the day of your birthday : ")
nb2 = input("enter the month of your birthday : ")
nb3 = input("enter the year of your birthday ")

age_aprox = actual_year - int(nb3)

if int(nb2) < actual_month :
    age = age_aprox

elif int(nb2) == actual_month:
    if int(nb1) <= actual_day:
        age = age_aprox
    
    else : 
        age = age_aprox -1

else:
    age = age_aprox -1


age_str = str(age)

nb_candles = int(age_str[len(age_str)-1])

f=""
for i in range(nb_candles):
    f+="i"


print(f"    __{f}__\n |:H:a:p:p:y:|\n__|___________|__\n|^^^^^^^^^^^^^^^^^|\n|:B:i:r:t:h:d:a:y:|\n|                 |\n~~~~~~~~~~~~~~~~~~~")




