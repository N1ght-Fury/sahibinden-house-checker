import sqlite3

class User():

    def __init__(self,mail,stat,links):

        self.mail = mail
        self.stat = stat
        self.links = links

    def __str__(self):

        return ("\n-------------------\nMail: {}\nStat: {}\nLinks: {}\n-------------------").format(self.mail, self.stat, self.links)


class Database_User():

    def __init__(self):

        self.connect_database()

    def connect_database(self):

        self.connection = sqlite3.connect("Sahibinden.db")
        self.cursor = self.connection.cursor()

        query = "create table if not exists " \
                "Tbl_Mail (" \
                "Mail text," \
                "Stat boolean," \
                "Links text)"

        self.cursor.execute(query)
        self.connection.commit()

    def show_mails(self):

        query = "select * from tbl_mail"
        self.cursor.execute(query)
        total = self.cursor.fetchall()

        if (len(total) != 0):

            for i in total:
                info = User(i[0],i[1],i[2])
                print(info)

        else:
            print("\nNo user found on database.\n")


    def check_if_mail_exists(self,mail):

        query = "select * from tbl_mail where mail = @p1"
        self.cursor.execute(query,(mail,))

        user = self.cursor.fetchall()

        if (len(user) == 0):
            return 0
        else:
            return 1

    def add_mail(self,User):

        query = "insert into tbl_mail values (@p1,@p2,@p3)"
        self.cursor.execute(query,(User.mail,User.stat,User.links))
        self.connection.commit()

    def delete_mail(self,mail):
        
        query = "delete from tbl_mail where mail = @p1"
        self.cursor.execute(query,(mail,))
        self.connection.commit()

    def update_mail(self,ex_mail,new_mail):

        query = "update tbl_mail set mail = @p1 where mail = @p2"
        self.cursor.execute(query,(new_mail,ex_mail))
        self.connection.commit()

    def update_link(self,link,mail):
    	
        query = "update tbl_mail set links = @p1 where mail = @p2"
        self.cursor.execute(query,(link,mail,))
        self.connection.commit()

    def update_stat(self,mail,stat):

        query = "update tbl_mail set stat = @p1 where mail = @p2"
        self.cursor.execute(query,(stat,mail))
        self.connection.commit()

    def total_user(self):

        query = "select * from tbl_mail"
        self.cursor.execute(query)
        total = self.cursor.fetchall()

        if (len(total) == 0):
            return 0
        else:
            return len(total)

    def get_mails(self):

        query = "select * from tbl_mail where stat = 1"
        self.cursor.execute(query)
        user_list = self.cursor.fetchall()
        return user_list

    def get_link(self,mail):
        query = "select links from tbl_mail where mail = @p1"
        self.cursor.execute(query,(mail,))
        links = self.cursor.fetchall()
        return links
