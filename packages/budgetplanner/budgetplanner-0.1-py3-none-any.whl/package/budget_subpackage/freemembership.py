import plotly.graph_objects as go

class FreeMemberShip:
    def __init__(self,user_budget) :
        self.__user_budget=user_budget
        self.__balance=0
    
    
    def get_user_budget(self):
        return self.__user_budget

    def get_balance(self):
        return self.__balance

    def set_balance(self,balance):
        self.__balance=balance
    
    def show_budget_chart(self):
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = self.__balance,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Budget Goal", 'font': {'size': 24}},
            delta = {'reference': self.__user_budget, 'increasing': {'color': "RebeccaPurple"}},
            gauge = {
                'axis': {'range': [None, self.__user_budget], 'tickwidth': 1, 'tickcolor': "RebeccaPurple"},
                'bar': {'color': "deepskyblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, self.__user_budget/3], 'color': 'cyan'},
                    {'range': [self.__user_budget/3, (2*self.__user_budget/3)], 'color': 'royalblue'},
                    {'range': [(2*self.__user_budget/3), (3*self.__user_budget/3)], 'color': 'darkblue'}],
                }))

        fig.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})
        #fig.show()
        
        

    def add_amount(self,amount):
        self.__balance+=amount        
        self.show_budget_chart()  
            
        

    def withdraw_amount(self,amount):
        curr_balance=self.__balance-amount
        if(curr_balance<0):
            return "Please enter lesser amount"
        else:
            self.__balance=curr_balance   
            self.show_budget_chart()
            return self.__balance                  

     
