import sqlite3

class House():

    def __init__(self,house_link,title,price,m2,date,neighborhood,room,img):
        self.house_link = house_link
        self.title = title
        self.price = price
        self.m2 = m2
        self.date = date
        self.neighborhood = neighborhood
        self.room = room
        self.img = img

class Database_Post():

    def __init__(self):

        self.connect_database()

    def connect_database(self):

        self.connection = sqlite3.connect("Sahibinden.db")
        self.cursor = self.connection.cursor()

        query = "create table if not exists " \
                "Tbl_Posts (" \
                "Link text," \
                "Title text," \
                "Price text," \
                "M2 text," \
                "Date text," \
                "Neighborhood text," \
                "Room text," \
                "Img text);" \
                "create table if not exists " \
                "Tbl_Posts_Backup (" \
                "Link text," \
                "Title text," \
                "Price text," \
                "M2 text," \
                "Date text," \
                "Neighborhood text," \
                "Room text," \
                "Img text);" \

        self.cursor.executescript(query)
        self.connection.commit()

    def check_if_house_exists(self,link):

        query = "select * from Tbl_Posts where Link = @p1"
        self.cursor.execute(query,(link,))
        posts = self.cursor.fetchall()

        if (len(posts) == 0):
            return 0

        else:
            return 1

    def add_house(self,House,backup=False):

        if (backup):
            query = "insert into Tbl_Posts_Backup values (@p1,@p2,@p3,@p4,@p5,@p6,@p7,@p8)"
        else:
            query = "insert into Tbl_Posts values (@p1,@p2,@p3,@p4,@p5,@p6,@p7,@p8)"
        self.cursor.execute(query,(House.house_link,House.title,House.price,House.m2,House.date,House.neighborhood,House.room,House.img))
        self.connection.commit()

    def clear_posts(self,day):

        query = "delete from tbl_posts where date like '%" + day + "%'"
        self.cursor.execute(query)
        self.connection.commit()
