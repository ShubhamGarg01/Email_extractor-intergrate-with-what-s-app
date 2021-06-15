import imaplib
import os
import email, getpass
import sys
import json
import pandas as pd
import pywhatkit as kit
from datetime import datetime
import os

class GmailFinin():
    def helloWorld(self):
        print("\nHello I'm here to help you")

    def initializeVariables(self):
        self.usr = ""
        self.pwd = ""
        self.mail = object
        self.mailbox = ""
        self.mailCount = 0
        self.destFolder = ""
        self.data = []
        self.ids = []
        self.idsList = []

    def getLogin(self):
        print("\nPlease enter your Gmail login details below.")
        self.usr = input("Email: ")
        # self.pwd = input("Password: ")
        self.pwd = getpass.getpass("Enter your password --> ")

    def attemptLogin(self):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        if self.mail.login(self.usr, self.pwd):
            print("\nLogon SUCCESSFUL")
            return True
        else:
            print("\nLogon FAILED")
            return False

    def checkIfUsersWantsToContinue(self):
        print("\nWe have found "+str(self.mailCount)+" emails in the mailbox "+self.mailbox+".")
        return True        
        
    def selectMailbox(self):
        # self.mailbox = input("\nPlease type the name of the mailbox you want to extract, e.g. Inbox: ")
        self.mailbox = "Inbox"
        bin_count = self.mail.select(self.mailbox)[1]
        self.mailCount = int(bin_count[0].decode("utf-8"))
        return True if self.mailCount > 0 else False
    def get_mostnew_email(self,messages):
        
        ids = messages[0]  
        id_list = ids.split()  
        latest_ten_email_id = id_list[-10:]  
        keys = map(int, latest_ten_email_id)
        news_keys = sorted(keys, reverse=True)
        str_keys = [str(e) for e in news_keys]

        return  str_keys

    def searchThroughMailbox(self):
        type, self.data = self.mail.search(None, "ALL")
        self.data=self.data[::-1]
        # self.data = self.get_mostnew_email(self.data)
        self.ids = self.data[0]
        self.idsList = self.ids.split()

    def parseEmails(self):
        jsonOutput = {}
        for anEmail in self.data[0].split()[::-1]:
            type, self.data = self.mail.fetch(anEmail, '(UID RFC822)')
            raw = self.data[0][1]
            try:
                raw_str = raw.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    raw_str = raw.decode("ISO-8859-1") # ANSI support
                except UnicodeDecodeError:
                    try:
                        raw_str = raw.decode("ascii") # ASCII ?
                    except UnicodeDecodeError:
                        pass
                        
            msg = email.message_from_string(raw_str)

            jsonOutput['subject'] = msg['subject']
            jsonOutput['from'] = msg['from']
            jsonOutput['date'] = msg['date']
            raw = self.data[0][0]
            raw_str = raw.decode("utf-8")


            uid = raw_str.split()[2]
            # Body #
            try:
                if msg.is_multipart():
                    for part in msg.walk():
                        partType = part.get_content_type()
                        ## Get Body ##
                        if partType == "text/plain" and "attachment" not in part:
                            jsonOutput['body'] = part.get_payload()
                            key,companyemail='Payment ID','support@instamojo.com'
                            values=['ID' ,'Email','number','Name']
                            lst=[]
                            if (key and companyemail) in jsonOutput['body']:
                                for i in range(len(jsonOutput['body'].split())):
                                    print(jsonOutput['body'])
                                    if jsonOutput['body'].split()[i] in values:
                                        if jsonOutput['body'].split()[i]=='Name':
                                            s,c='',1
                                            while(c):
                                                if jsonOutput['body'].split()[i+c]=='Email':
                                                    lst.append(s)
                                                    break
                                                else:
                                                    s+=jsonOutput['body'].split()[i+c]+' '
                                                    c+=1
                                        else:
                                            jsonOutput['body'].split()[i]
                                            lst.append(jsonOutput['body'].split()[i+1])
                            # file=pd.read_csv('data.csv')
                            if lst:
                                df=pd.DataFrame([lst])
                                try:
                                    print(lst[0] ,'he', pd.read_csv('data.csv', index=False)[['ID']] )
                                    if lst[0] in pd.read_csv('data.csv').ID:
                                        exit(0)

                                    if not lst[0] in pd.read_csv('data.csv').ID:
                                        df.to_csv('data.csv',index=False,header=['ID','Name','Email','number'])
                                except:
                                    df.to_csv('data.csv',index=False,header=['ID','Name','Email','number'])

    
                else:
                    jsonOutput['body'] = msg.get_payload(decode=True).decode("utf-8") # Non-multipart email, perhaps no attachments or just text.
                    jsonOutput['body'] = msg.get_payload()
            except:
                pass

    def __init__(self):
        self.initializeVariables()
        self.helloWorld()
        self.getLogin()
        if self.attemptLogin():
            not self.selectMailbox() and sys.exit()
        else:
            sys.exit()
        not self.checkIfUsersWantsToContinue() and sys.exit()
        self.searchThroughMailbox()
        self.parseEmails()
        #
        if os.path.isfile("data.csv"):
            df=pd.read_csv('data.csv')
            data=df[['number','ID','Name','Email']]
            time = datetime.now()
            for i,j in df.iterrows():
                number_temp,Name_temp,ID_temp,Email_temp=j['number'],j['Name'],j['ID'],j['Email']
                msg='Hello {},\n Your transation is successful and your transation ID is {}\n We have also sent the payment receipt to {} Please Check !!'.format(Name_temp,ID_temp,Email_temp)
                if len(str(number_temp))==11:
                    kit.sendwhatmsg(f"+91-{int(str(number_temp)[1:])}",msg,time.hour,time.minute+1,10)
                else:
                    kit.sendwhatmsg(f"+91-{number_temp}",msg,time.hour,time.minute+1,10)
                

if __name__ == "__main__":
    run = GmailFinin()
