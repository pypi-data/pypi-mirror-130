# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

class personal_info:
    def __init__(self,userid,age = 0,email = "",income = 0):
        self.userid = userid
        self.age = age
        self.email = email
        self.income = income
        
    def show(self):
        print('Userid:{} Age:{} Email:{} Income:{}'.format(self.userid,self.age,self.email,self.income))

    def update(self,newuserid,newage,newemail,newincome):
        self.userid = newuserid
        self.age = newage
        self.email = newemail
        self.income = newincome
    def delete(self):
        self.userid = ''
        self.age = ''
        self.email = ''
        self.income = ''


