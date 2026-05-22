#Gross Salary in Variables

salary=float(input("input salary income:"))


if  salary>=0 and salary <=-1:
    print("invalid")

if  salary>=200 and salary <=5999:
    print("150.00")
    
elif salary >=6000 and salary<=7999:
    print("300.00")

elif salary >=8000 and salary <=11999:
    print("400.00") 
    

elif salary >=12000 and salary <=14999:
    print("500.00") 

elif salary >=15000 and salary <=19999:
    print("600.00") 

elif salary >=20000 and salary <=24999:
    print("750.00") 

elif salary >=25000 and salary <=29999:
    print("850.00") 

elif salary >=30000 and salary <=49999:
    print("1000.00") 

elif salary >=50000 and salary <=99999:
    print("1500.00") 

elif salary >=100000 and salary <=100000000:
    print("20000.00") 

else:
    print("invalid")    
