from datetime import datetime

print("Days between two dates.")
print("="*50)

# User input
first_date_str = input("Enter first date MM-DD-YYYY: ")
second_date_str = input("Enter second date MM-Day-YYYY: ")
print("="*50)

# Creating date objects (year, month, day)
date_1 = datetime(int(first_date_str[6:]), 
                        int(first_date_str[:2]), 
                              int(first_date_str[3:5]) )
date_2 = datetime(int(second_date_str[6:]), 
                        int(second_date_str[:2]), 
                              int(second_date_str[3:5]) )
# Calculating days apart
days_apart = abs((date_1 - date_2)).days

# Displaying info
print( "{} and {} are {} days apart.".format(first_date_str, second_date_str, days_apart))