#bankingOOP

import mysql.connector, sys
class DepositError(BaseException): pass

class WithDrawError(Exception): pass

class InsuffFundsError(BaseException): pass

class WrongNumberError(Exception): pass

class IncorrectPinError(BaseException): pass

class UserWantsToExit(BaseException): pass

class Banking:
    
    def __init__(self):
        self.conn= mysql.connector.connect(host='localhost', user= 'user', password= 'password', database= 'database_name')
        self.cursor= self.conn.cursor()


    def atmmenu(self):
        print("-"*50)
        print("\tA T M  S E R V I C E ")
        print("-"*50)
        print("\tChoose a Number")
        print("-"*50)
        print("\t1. Deposit")
        print("\t2. Withdraw")
        print("\t3. Check Balance")
        print("\t4. Fund Transfer")
        print("\t5. Exit")
        self.choice= int(input("Enter Operation Number: "))
        return self.choice

    def ac_pin_verify(self):
        self.acno= int(input("Account Number: "))
        query= "SELECT * FROM account WHERE acno= {}".format(self.acno)
        self.cursor.execute(query)
        self.ac_info= list(self.cursor.fetchall()[0])
        if len(self.ac_info)==0:
            print("Invalid Account Number: ")
        else:
            self.pswd= int(input("Password: "))
            if self.pswd==self.ac_info[3]:
                return True
            else:
                return False
        
    
    def deposit(self):
        #Banking.ac_pin_verify()
        if Banking.ac_pin_verify(self)== True:
            amt= float(input("Enter Deposit Amount: "))
            if amt<=0:
                raise DepositError
            else:
                self.ac_info[2]+= amt 
                upd_query= "UPDATE account SET bal = {} WHERE acno= {}".format(self.ac_info[2], self.acno)
                self.cursor.execute(upd_query)
                print("Your account has been credited with INR {}".format(amt))
                print("Your Current Account Balance is INR {}".format(self.ac_info[2]))
                self.conn.commit()
        else:
            raise IncorrectPinError



    def WithDraw(self):
        if Banking.ac_pin_verify(self)== True:
            wamt= float(input("Enter Withdraw Amount: "))
            if wamt<=0:
                raise WithDrawError
            elif (wamt > self.ac_info[2]):
                raise InsuffFundsError
            else:
                self.ac_info[2]= self.ac_info[2] - wamt
                upd_query= "UPDATE account SET bal= {} WHERE acno = {}".format(self.ac_info[2], self.acno)
                self.cursor.execute(upd_query)
                self.conn.commit()
                print("Your account has been debited with INR {}".format(wamt))
                print("Your Current Account Balance is INR {}".format(self.ac_info[2]))
        else:
            raise IncorrectPinError

    def CheckBal(self):
        if Banking.ac_pin_verify(self)==True:
            print("Your Current Account Balance is {}".format(self.ac_info[2]))
        else:
            raise IncorrectPinError
    
    def FundTransfer(self):
        if Banking.ac_pin_verify(self)== True:
            self.rec_acno= int(input("Receiver's account number: "))
            if self.acno== self.rec_acno:
                print("Transfer can't be made to the same account.")
            else:
                self.cursor.execute("SELECT * FROM account where acno= %d"%self.rec_acno)
                rec_lst= list(self.cursor.fetchall()[0])
                if len(rec_lst)!=0:
                    amount= float(input("Enter amount: "))
                    if amount>0:
                        if amount<float(self.ac_info[2]):
                            self.ac_info[2]= self.ac_info[2]- amount
                            rec_lst[2]= rec_lst[2]+ amount
                            upd_giver= "UPDATE account SET bal = %f where acno= %d"%(self.ac_info[2], self.acno)
                            self.cursor.execute(upd_giver)
                            upd_receiver= "UPDATE account SET bal = %f where acno= %d"%(rec_lst[2], self.rec_acno)
                            self.cursor.execute(upd_receiver)
                            s_query= "SELECT * FROM account WHERE acno= {}".format(self.rec_acno)
                            self.cursor.execute(s_query)
                            self.cursor.fetchall()
                            self.conn.commit()
                            print("Your transaction is completed.")
                            ch=input("Enter n/N to exit. Any other button to continue.")
                            if ch.upper()=='N':
                                sys.exit()
                        else:
                            print("Insufficient Funds.")
                    else:
                        print("Can't Transfer Negative Amount")

    def Exit(self):
        pass
            
class BankingMain(Banking):
    def __init__(self):
        Banking.__init__(self)

    def BankingMain(self):
        menu= BankingMain.atmmenu(self)
        if menu==1:
            Banking.deposit(self)
        elif menu==2:
            Banking.WithDraw(self)
        elif menu==3:
            Banking.CheckBal(self)
        elif menu==4:
            Banking.FundTransfer(self)
        elif menu==5:
            sys.exit()
        else:
            print("Check The Value You Have Entered.")

    def BankRun(self):
        while True:
            try:
                BankingMain().BankingMain()
            except IncorrectPinError:
                print("Insufficient Funds.")
            except ValueError:
                print("Please Check The Value You Have Entered")
                ch=input("Enter n/N to exit. Any other button to continue.")
                if ch.upper()=='N':
                    sys.exit()
            except DepositError:
                print("Please Chcek Amount Entered.")
            except WithDrawError:
                print("Please Chcek Amount Entered") 
            except IndexError:
                print("Check Account Number.")

if __name__=='__main__':
    bankob= BankingMain()
    bankob.BankRun()

