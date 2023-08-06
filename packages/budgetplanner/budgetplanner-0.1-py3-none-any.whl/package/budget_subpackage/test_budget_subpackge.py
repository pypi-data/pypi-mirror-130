from .freemembership import FreeMemberShip
from .basicmembership import BasicMembership
from .premiummembership import PremiumMembership
from ..user_subpackage.personal_info import personal_info as ps
from ..user_subpackage.service import Service

#import ..user_subpackage.personal_info.personal_info as ps

def testing_budget():    
    print("Hello, we are thrilled to have you with us. We hope to make your life easier by managing your piggy bank for you :) To begin with, we would love to know more about you. Please fill in the following details")
    user_name=input("What is your name?  ")
    user_age=int(input("{}, what is your age?  ".format(user_name)))
    user_email=input("We would love to be in touch with you. What is your email?    ")
    user_income=int(input("Enter your yearly income for us to start managing your finances  "))
    person1 = ps(user_name,user_age,user_email,user_income)
    #person1=ps("Maddy",26,"madggy@gmail.com",120000)
    service1=Service()
    print("PS: Remember that you can add and withdraw money from your piggy bank. We have the following services for you    ")
    service1.list()  
    flag=True
    while flag:  
        user_service_choice=int(input("Choose the appropriate service to know more  "))
        service1.show(user_service_choice)
        more=input("Curious about any other service listed? Enter yes or no ")
        if(more=="no"):
            flag=False    
    user_select_service=int(input("Select the appropriate service   "))
    service1.choice(user_select_service)    

    if(service1.getChoice()==1):
        user_budget=int(input("Enter your goal budget   "))
        free_mem1=FreeMemberShip(user_budget)
        amount=int(input("Enter amount to add   "))
        free_mem1.add_amount(amount)        

    elif(service1.getChoice()==2):
        print("Please enter variable expenditure in user_data excel file. I would call insurances as fixed expenditure that cannot be avoided at all costs  ")
        done=input("Ping me an yes when you are done    ")
        basic_mem1=BasicMembership()
        annual=basic_mem1.analysis_and_suggestion(person1.income/12)
        free_mem2 =FreeMemberShip(annual)
        amount=int(input("Enter amount to add   "))
        free_mem2.add_amount(amount)

    elif(service1.getChoice()==3):
        print("Please enter variable expenditure in user_data excel file. I would call insurances as fixed expenditure that cannot be avoided at all costs  ")
        done=input("Ping me an yes when you are done    ")
        premium_mem1=PremiumMembership()
        annual=premium_mem1.analysis_and_suggestion(person1.income/12)
        free_mem3=FreeMemberShip(annual)
        amount=int(input("Enter amount to add   "))
        free_mem3.add_amount(amount)
    else:
        print("Sorry! Try again. Please choice appropriate service  ")

