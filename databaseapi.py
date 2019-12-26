from mongo import db

def GetUser(key):
    userTable = db.GetTable('Users')
    tar_user = userTable.find_one(key)
    return tar_user

def PutUser(val):
    userTable = db.GetTable('Users')
    userTable.insert_one(val)
    return
