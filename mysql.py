
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
def get_website(site_name):
    with connection.cursor() as cur:
        sql = "SELECT `id` FROM `sites` WHERE `name`=%s"
        cur.execute(sql,(site_name,))
        res=cur.fetchone()
        if not res:
            add_website(site_name)
            return get_website(site_name)
        return res["id"]
def add_website(site_name):
    try:
        with connection.cursor() as cur:
            sql = "INSERT INTO `sites` (`name`) VALUES (%s)"
            cur.execute(sql,(site_name,))
    except pymysql.err.IntegrityError:
        pass 
    else:
        connection.commit()




def get_page(site_name,page_name):
    with connection.cursor() as cur:
        site_id=get_website(site_name)
        sql="SELECT `id` FROM `pages` WHERE `site_id`=%s AND `page_name`=%s"
        cur.execute(sql,(site_id,page_name))
        res=cur.fetchone()
        if not res:
            add_page(page_name,site_name)
            return get_page(site_name,page_name)
        return res["id"]
def add_page(page_name,site_name,parent_page=None):
    with connection.cursor() as cur:
        site_id=get_website(site_name)    
        if(parent_page==None):
            parent_page_id=None
        else:
            parent_page_id=get_page(site_name,parent_page)
        sql = "INSERT INTO `pages` (`site_id`,`page_name`,`parent_page_id`) VALUES (%s,%s,%s)"
        cur.execute(sql,(site_id,page_name,parent_page_id))
        connection.commit() 
def page_exists(site_name,page_name):
    with connection.cursor() as cur:
        site_id=get_website(site_name)
        sql="SELECT `id` FROM `pages` WHERE `site_id`=%s AND `page_name`=%s"
        cur.execute(sql,(site_id,page_name))
        res=cur.fetchone()
        return res != None




def get_module(module_name):
    with connection.cursor() as cur:
        sql="SELECT `id` FROM `modules` WHERE `name`=%s"
        cur.execute(sql,module_name)
        res=cur.fetchone()
        return res["id"]





def insert_site_data(site_name,module_name,data):
    try:
        with connection.cursor() as cur:
            sql="SELECT `id` FROM `sites` WHERE `name`=%s"
            site_id=get_website(site_name)
            module_id=get_module(module_name)
            sql="INSERT INTO `site_module_results` (`site_id`,`module_id`,`data`,`date_updated`) VALUES (%s,%s,%s,NOW())"
            cur.execute(sql,(site_id,module_id,data))
            connection.commit()
    except Exception as e:print e





def insert_page_data(site_name,page_name,module_name,data):
    with connection.cursor() as cur:
        site_id=get_website(site_name)
        page_id=get_page(site_name,page_name) 
        module_id=get_module(module_name)
        sql="INSERT INTO `page_module_results` (`page_id`,`site_id`,`module_id`,`data`,`date_updated`) VALUES (%s,%s,%s,%s,NOW())"
        cur.execute(sql,(page_id,site_id,module_id,data))
        connection.commit()
