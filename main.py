from fastapi import FastAPI,status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError,jwt
from datetime import timedelta,datetime
import mysql.connector
import json
from typing import Optional

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
security=HTTPBearer()

Secret_Key='This_is_a_developmental_test_key'
Algorithm='HS256'
Time_to_expire=30

def create_access_token(data: dict):
        token_data=data.copy()
        expiration_time=datetime.now()+timedelta(minutes=Time_to_expire)
        token_data.update({"exp":expiration_time})
        encoded_token=jwt.encode(token_data,Secret_Key,algorithm=Algorithm)
        return encoded_token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, Secret_Key, algorithms=[Algorithm])
        username: str = payload.get("user_name")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    return token_data

def get_curr_user(token: str = Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",headers={"WWW-authenticate":"bearer"})
    token=verify_access_token(token,credentials_exception)
    return token

app = FastAPI()

class user(BaseModel):
    username:str
    password:str
    email:str
    id: Optional[int]

class group(BaseModel):
    name: str
    id:Optional[int]
    region:str

class post(BaseModel):
    title:str
    id:Optional[int]
    text:str
    creator_id:int

class grp_participants(BaseModel):
    group_id:int
    user_id:int

class grp_posts(BaseModel):
    group_id:int
    post_id:int
    
while True:
    try:
        conn=mysql.connector.connect(host='localhost',database='blog_prod',user='root',password='',port=3306)
        cursor= conn.cursor()
        print("Successful Connection")
        break
    except Exception as error:
        print("error:",error)

@app.get("/")
def read_root():
    return {"Hello": "World"}

#login_method
@app.post("/login")
def login(user_creds:OAuth2PasswordRequestForm = Depends()):
    prov_username=user_creds.username
    cursor.execute("select user.password from user where username=%s",(prov_username,))
    stored_password=cursor.fetchone()[0]
    if (stored_password==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with name {prov_username} was not found.")
    else:
        if not (stored_password==user_creds.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
        at=create_access_token({"user_name":user_creds.username})
        return ({"access_token":at,"token_type":"bearer"})

#user table
@app.get("/Users")
def get_users():
    cursor.execute("select * from user order by ID")
    users=cursor.fetchall()
    return({"users":users})

@app.get("/Users/{id}")
def get_users_by_id(id:int):
    cursor.execute("Select * from user where id = %s",(id,))
    user = cursor.fetchone()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} was not found.")
    return({"user":user})

@app.post("/Users")
def create_user(user: user):
    q='''INSERT INTO user(Username,Email,Password) values (%s,%s,%s)'''
    a=(user.username,user.email,user.password)
    cursor.execute(q,a)
    conn.commit()

#group table
@app.get("/Groups")
def get_groups():
    cursor.execute("select * from groups order by ID")
    groups=cursor.fetchall()
    return({"groups":groups})

@app.post("/Groups")
def create_group(group: group,curr_user:int = Depends(get_curr_user)):
    q='''INSERT INTO groups(Name, Region) values (%s,%s)'''
    a=(group.name,group.region)
    cursor.execute(q,a)
    conn.commit()

@app.get("/Groups/{id}")
def get_groups_by_id(id:int):
    cursor.execute("Select * from groups where id = %s",(id,))
    group = cursor.fetchone()
    if group == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"group with id {id} was not found.")
    return({"group":group})

@app.delete("/Groups/{id}")
def delete_group_by_id(id:int,curr_user:int = Depends(get_curr_user)):
    cursor.execute("Select * from groups where id = %s",(id,))
    group = cursor.fetchone()
    if group == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"group with id {id} was not found.")
    cursor.execute("Delete from groups where id = %s",(id,))
    conn.commit()
    return({"group deleted":group})

#posts table
@app.get("/Posts")
def get_posts():
    cursor.execute("select * from posts order by ID")
    posts=cursor.fetchall()
    return({"posts":posts})

@app.post("/Posts")
def create_posts(post: post,curr_user:int = Depends(get_curr_user)):
    q='''INSERT INTO posts(title,text,Creator_ID) values (%s,%s,%s)'''
    a=(post.title,post.text,post.creator_id)
    cursor.execute(q,a)
    conn.commit()

@app.get("/Posts/{id}")
def get_users_by_id(id:int):
    cursor.execute("Select * from posts where id = %s",(id,))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found.")
    return({"post":post})

@app.delete("/Posts/{id}")
def delete_posts_by_id(id:int,curr_user:int = Depends(get_curr_user)):
    cursor.execute("Select * from posts where id = %s",(id,))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"group with id {id} was not found.")
    cursor.execute("Delete from post where id = %s",(id,))
    conn.commit()
    return({"post deleted":post})

#group participants table
@app.get("/group_participants")
def get_group_participants():
    cursor.execute("select * from group_participants")
    participants=cursor.fetchall()
    return({"participants":participants})

@app.post("/group_participants")
def create_group_participants(grp_participants:grp_participants):
    q='''INSERT INTO group_participants(group_id,participant_id) values(%s,%s)'''
    a=(grp_participants.group_id,grp_participants.user_id)
    cursor.execute(q,a)
    conn.commit()

#group posts table
@app.get("/group_posts")
def get_group_posts():
    cursor.execute("select * from group_posts")
    grp_posts=cursor.fetchall()
    return({"grp_posts":grp_posts})

@app.post("/group_posts")
def create_group_posts(grp_posts:grp_posts):
    q='''INSERT INTO group_posts(group_id,post_id) values(%s,%s)'''
    a=(grp_posts.group_id,grp_posts.post_id)
    cursor.execute(q,a)
    conn.commit()