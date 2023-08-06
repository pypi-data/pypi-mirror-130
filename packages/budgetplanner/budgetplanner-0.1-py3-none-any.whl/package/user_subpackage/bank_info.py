class password:

    def __init__(self,userid,password):
        self.userid = userid
        self.password = password
    def update(self,newuserid, newpassword):
        self.userid = newuserid
        self.password = newpassword
        return self.userid,self.password

    def show(self):
        print('userid: {} password: {}'.format(self.userid,self.password))

    def delete(self):
        self.userid = ''
        self.password = ''
        return self.userid,self.password
 