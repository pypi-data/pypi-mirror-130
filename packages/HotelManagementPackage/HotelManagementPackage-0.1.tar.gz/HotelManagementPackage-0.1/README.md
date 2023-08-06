# Hotel Management Package
Evelyn Sugihermanto
Anqi Li
---
We created a hotel management package to manage the services and people in the hotel. The package has two subpackages: Service and Person. 
## Subpackage 1: Service
---
The service sub package consist of 3 modules where each module is a class. The hotel service including the **room**, **restaurant**, and the **swimming pool** for children entertainment. The Room class is used to manage rooms in the hotel. The swimming_pool class is to manage the swimming pool in the hotel. The Restaurant class is to manage the restaurant in the hotel. 

###  (1) class Room
The room class is for managing the rooms in the hotel. It has the following 6 methods: 
- **\__init\__ : initialization for Room class.**
There are two attributes for the room class: **price**, which is the price for the room, and **availablenumber**, which is the available room number.
- **modifyprice : modify the room price**
There are many factors that would let the hotel manager directly change the room price, like holidays and seasons. This function is used to modify the price of the room, which is the the **price** attribute. (different from giving discounts) 
- **discountprice : discount the room price**
When the hotel manager want to give an discount offer, he/she can define the discount rate, and provide a discount price, which changes the the **price** attribute with the **discount rate** provided. If discount rate is minus, it will print a prompt "discount can't be negative".
- **reduceroomnumber : reduce number of room available if customer check in.**
When the customer checks in, the available room number will reduce. The **availablenumber** variable is going to be reduced by the value **reduceamount** passed in.  If reduction in room amount is greater than the current avaiable room number, it will print a prompt "not enough available room(s)".
-	**addroomnumber : add number of room available if customer check out.**
When the customer checks in, the available room number will increase. The **availablenumber** variable is going to be reduced by the value **addamount** passed in. 
-	**display : display the Room object.**
Display all the attributes of the room object: price and availablenumber.

###  (2) class swimming_pool

The swimming pool class is for managing the swimming pool for children in the hotel. It has the following 4 methods:
- **\__init\__: initialization for Swimming Pool class**
There are one attribute for the swimming_pool class, **price**, which is the ticket price for one entrance to the swimming pool.
- **modifyprice : modify the swimming pool price**
There are many factors that would influence the swimming pool price. In winter the price would go down and in summer the hotel manager may want to increase the price to gain more profits. This function is used to modify the price, which is the the **price** attribute. (different from giving discounts) 
- **discountprice : discount the swimming pool price**
When the hotel manager want to give an discount offer, he/she can define the discount rate, and provide a discount price,  which changes the the **price** attribute with the **discount** rate provided. If discount rate is less than 0, it will print a prompt "discount can't be negative".
- **display : display the Swimming Pool object**
Display the **price** attribute to show the current price of the swimming pool ticket.

###  (3) class Restaurant

The restaurant class is for managing the restaurant in the hotel. It has the following 4 methods: 
- **\__init\__ : initialization for Restaurant class.**
There are two attributes for the room class: **menu**, which includes the food and its price provided in the restaurant, and **employee**, which is the employees work in the restaurant. The menu is implemented with a dictionary, the key is food and the value is price of the food. The employee is implemented with a list. 
- **addfood : add food to restaurant menu.** 
When the hotel manager want to add food to the restaurant, he/she can use the function. The two value passed in is "food" and "price". The data will be added into the **menu** attribute, which is a dictionary.
- **addemployee : add employee who works at restaurant.**
The employee name is passed in, and the **employee** variable will be modified (the list will append the new item).
-	**display : display the Restaurant menu and employee.**
Display the attributes: the menu and the employees in a good format.

## Subpackage 2: Person
---
The person sub package consist of 3 modules which include **employee**, **customers** (adults), and **children**. Each module is a class and is used to manage the type of person in a hotel. The Employee class is to manage employees who work for the hotel. Customers class is to manage adult customers who stay at the hotel. Children class is to manage the children of adult customers, if any, who stay at the hotel. The Children class inherits some of the property from the Customers class.
###  (1) class Employee
The employee module contains Employee class that is used to create instance of employee objects that works for the hotel. In this module, the hotel management can modify the employee's salary, add bonus to an employee's salary, and display the employee information. This module contain the following 6 methods:
- **\__init\__ : initialization for Employee class.**
This method is used to initialize the Employee class. There are five attributes for the Employee class: First, **name**, which is the name of the employee. Second, **age**, which is the age of the employee. Third, **workhour**, which is the number of hours an employee worked. Fourth, **salary**, which is the employee's salary. Fifth, **hourlyrate** is the employee's salary per hour worked.
- **add_work_salary : add salary and workhour to employee.**
This method is used to add the number of hours worked for each employee object and the salary for the number of hours worked.
- **add_bonus : add bonus to employee**
This method is used to add bonus to an employee. For instance, if they have worked overtime or worked over during peak season such as new year.
- **reduce_salary : reduce salary of employee**
This methos is used to reduce the salary of an employee. For instance, if the employee is late to work or is absence from work. If reduction in salary is greater than the current salary, it will print a prompt "salary can't be negative".
-	**display : display the Employee object.**
Display all the attributes of the employee object: name, age, hourlyrate, workhour, and salary.

###  (2) class Customers
The class customer is used to manage the customers in the hotel. It has the following 4 methods:
- **\__init\__ : initialization for customers class.**
There are four attributes for the room class: **name**, which is the name of the customer; **age**, which is the age of the customer; **durationday**, which is how many days the customer stayed in the hotel; and **bill**, which is bill the customer should pay. The default value for the **bill** is 0.
- **addbill : charge service fee to customer’s bill.**
The function is used to charge the service fee to the customer's bill. The data **amount** is passed in and the **bill** attribute would be modified by adding the new service fee amount.
- **reducebill : reduce customer’s bill (e.g. cancellation)**
The function is used to reduce the service fee to the customer's bill. Sometimes customers order something but then cancelled the order. Then the service fee should also be cancelled. The data **amount** is passed in and the **bill** attribute would be modified by minusing the cancelled service fee amount. If reduction in bill is greater than the current bill, it will print a prompt "bill can't be negative".
- **display : display the customer object**
Display all the attributes of the customer object: name, age, length of duration, and also the bill amount.

###  (3) class Children
The class customer is used to manage all the **children** customers in the hotel. It is set as a **sub class** of the class **Customers**. It has the following 5 methods:
- **\__init\__ : initialization for Children class.**
There are five attributes for the room class. The first four attributes (**name, age, bill, durationday**) are inherit attributes from the Customer class. It has one its own attribute **pooltime**, because only the children can go to the children swimming pool. The pool time is how many times the child entered the swimming pool.
- **add_children_pool_time : add number of time pool is entered.**
This function is used to add the number of time the children entered the swimming pool. The data **time** is passed in and the **pooltime** variable is modified by adding the **time** value.
- **add_bill : charge service fee to customer’s bill**
The function tooks advantage of inheriting the addbill function of the parent class **Customers**. It is used to charge the service fee to the customer's bill. The data **amount** is passed in and the **bill** attribute would be modified by adding the new service fee amount.
- **reduce_bill : reduce customer’s bill (e.g. cancellation)**
The function tooks advantage of inheriting the reducebill function of the parent class **Customers**. The function is used to reduce the service fee to the customer's bill. Sometimes customers order something but then cancelled the order. Then the service fee should also be cancelled. The data **amount** is passed in and the **bill** attribute would be modified by minusing the cancelled service fee amount. If reduction in bill is greater than the current bill, it will print a prompt "bill can't be negative".
- **display : display the children object**
Display all the attributes of the children object: name, age, length of duration, bill amount, and pooltime.

