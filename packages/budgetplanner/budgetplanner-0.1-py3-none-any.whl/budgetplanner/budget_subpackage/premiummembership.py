from .basicmembership import BasicMembership
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
#import freemembership

class PremiumMembership(BasicMembership):
    __ideal_labels=["Groceries","Travel","Shopping","Restaurant","Others"]
    __ideal_values=[4,2,3,1,1]
    __percentage_list=[10,20,25]

    def __init__(self):
        super().__init__()

    def get_whole_data(self):
        return self.__whole_data

    def expenditure_chart(self,monthly_allowance):  
        try:      
            monthly_allowance=int(monthly_allowance)
            data=self.user_expenditure_data()
            expenditure_allowance_percentage=data.iloc[0].values*100/monthly_allowance            
            ideal_data= pd.DataFrame([PremiumMembership.__ideal_values],columns=PremiumMembership.__ideal_labels)
            labels=data.columns
            new_labels=[x if x in PremiumMembership.__ideal_labels else "Others" for x in labels]
            new_data=pd.DataFrame([data.iloc[0].values,expenditure_allowance_percentage],columns=new_labels)
            whole_data= pd.concat([new_data,ideal_data])
            self.__whole_data=whole_data.fillna(0)        
            whole_labels=self.__whole_data.columns 
            fig = go.Figure(data=[
                go.Bar(name='Actual', x=whole_labels, y=self.__whole_data.iloc[1].values),
                go.Bar(name='Ideal', x=whole_labels, y=self.__whole_data.iloc[2].values)
            ])        
            fig.update_layout(barmode='group')
            #fig.show()   
        except ValueError:
            print("Invalid value")
        

    def analysis_and_suggestion(self,monthly_allowance):  
        try:
            monthly_allowance=int(monthly_allowance)
            self.expenditure_chart(monthly_allowance)      
            diff_percentages=self.__whole_data.iloc[1].values-self.__whole_data.iloc[2].values
            whole_labels=self.__whole_data.columns
            top_three_areas=sorted(zip(diff_percentages, whole_labels), reverse=True)[:3]        
            expenditure_diff,Areas=list(zip(*sorted(zip(diff_percentages, whole_labels), reverse=True)[:3]))
            savings_per_month=[]
            print("Based on your profile, our recommendation are the following. Choose the one that is most appropriate for you")
            for ind1 in range(0,len(PremiumMembership.__percentage_list)):
                sum_savings=0
                print(ind1+1,"--------------------------------------------------------------------------------")
                for ind2 in range(0,len(expenditure_diff)):
                    per=PremiumMembership.__percentage_list[ind1]
                    diff=expenditure_diff[ind2]                
                    curr_expenditure_amount=self.__whole_data.loc[0,Areas[ind2]].values[0]
                    
                    new_expense=round((1-0.01*per)*curr_expenditure_amount)
                    new_savings=round(0.01*per*curr_expenditure_amount)
                    sum_savings+=new_savings
                    
                    print("Reduce the expenditure on {} from {} to {} thus savings {} per month".format(Areas[ind2],curr_expenditure_amount,new_expense,new_savings))
                savings_per_month.append(sum_savings)
            option=int(input("Enter an option to know about the reward points and expected annual savings goal"))        
            reward=self.rewards_calculator(option,savings_per_month[option-1])   
            print(reward)
            print("Your expected annual savings is {} !!!!".format(savings_per_month[option-1]*12))        
            return savings_per_month[option-1]*12
        except ValueError:
            print("Invalid value")
        except IndexError:
            print("Invalid index")
    
    def rewards_calculator(self, option, savings):    
        reward=""
        if(option==1):
            reward="Gift coupon to Starbucks and McDonalds worth {} per month".format(0.015*savings)
        elif(option==2):
            reward="{} off of your next purchase on hudson bay with unlimited validity ".format(0.15*savings)
        elif(option==3):
            reward="50% off of your membership for the next year"
        return reward   
        

