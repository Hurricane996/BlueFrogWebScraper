####################################IMPORTS#####################################
import os
import copy
import pymysql
###################################CONSTANTS####################################
default_connection_data={
     "host":"localhost",
     "user":os.getlogin(),
     "password":"password",
     "db":"db"
}
####################################GLOBALS#####################################
connection=None
############################INITIALIZATION FUNCTIONS############################
def load_connection_data(file):
    connection_data={}

    try:
        with open("user_data","r") as f:
            # using f.read().split() instead of f.readlines() to filter "\n"
            for line in f.read().split("\n"):
                kvpair=line.split("=")
                if not len(kvpair)==2:
                    continue
                if kvpair[0] in ["host","user","password","db"]:
                    connection_data[kvpair[0]]=kvpair[1]
        for key in default_connection_data.keys():
            if key not in connection_data.keys():
                print "\033[31mKey " + key + " not found in user_data. Using default value\033[0m"
                connection_data[key]=default_connection_variables[key]
    except IOError:
        print "\033[31m user_data not found. Using default values\033[0m"
        connection_data=copy.copy(default_connection_data)
    return connection_data

def connect(connection_data):
    global connection
    connection_data["cursorclass"]=pymysql.cursors.DictCursor
    connection = pymysql.connect(**connection_data)

def initialize(file="user_data"):
    connect(load_connection_data(file))
###########################DATABASE MODIFYING METHODS###########################
def add_website(site_name):
    try:
        with connection.cursor() as cur:
            sql = "INSERT INTO `sites` (`name`) VALUES (%s)"
            cur.execute(sql,(site_name,))
    except pymysql.err.IntegrityError:
        pass 
    else:
        connection.commit()

def add_page(page_name,site_name,parent_page=None):
    with connection.cursor() as cur:
        sql="SELECT `id` FROM `sites` WHERE `name`=%s"
        cur.execute(sql,(site_name,))
        res=cur.fetchone()
        if res == None:
            add_website(site_name)
            cur.execute(sql,(site_name,))
            res=cur.fetchone()
        site_id=res["id"]
        if(parent_page==None):
            parent_page_id=None
        else:
            sql="SELECT `id` FROM `pages` WHERE `site_id`=%s AND `page_name`=%s"
            cur.execute(sql,(site_id,parent_page))
            res=cur.fetchone()
            if res == None:
                add_page(parent_page,site_name)
                cur.execute(sql,(site_id,parent_page))
                res=cur.fetchone()
            parent_page_id=res["id"]
        sql = "INSERT INTO `pages` (`site_id`,`page_name`,`parent_page_id`) VALUES (%s,%s,%s)"
        cur.execute(sql,(site_id,page_name,parent_page_id))
        connection.commit() 
