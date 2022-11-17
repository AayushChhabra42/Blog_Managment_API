import mysql.connector 

while True:
    try:
        conn=mysql.connector.connect(host='localhost',database='blog_prod',user='root',password='',port=3306)
        cursor= conn.cursor()
        print("Successful Connection")
        break
    except Exception as error:
        print("error:",error)

#creating tables
cursor.execute("CREATE TABLE user (Username varchar(50) NOT NULL,Email varchar(255) NOT NULL,Password varchar(16) NOT NULL,Joined_at date NOT NULL DEFAULT current_timestamp(),ID int(6) NOT NULL AUTO_INCREMENT,PRIMARY KEY (ID))")
cursor.execute("CREATE TABLE groups (Name varchar(200) NOT NULL,ID int(6) NOT NULL AUTO_INCREMENT,Region varchar(6) NOT NULL,Created_at date NOT NULL DEFAULT current_timestamp(),PRIMARY KEY(ID))")
cursor.execute("CREATE TABLE posts (Title varchar(300) NOT NULL,ID int(6) NOT NULL AUTO_INCREMENT,Text text NOT NULL,Creator_ID int(6) NOT NULL,PRIMARY KEY (ID),FOREIGN KEY (Creator_ID) REFERENCES user(ID))")
cursor.execute("CREATE TABLE group_participants (Group_ID int(6) NOT NULL,Participant_ID int(6) NOT NULL,PRIMARY KEY (Group_ID,Participant_ID),FOREIGN KEY (Group_ID) REFERENCES groups(ID),FOREIGN KEY (Participant_ID) REFERENCES user(ID))")
cursor.execute("CREATE TABLE group_posts (Group_ID int(6) NOT NULL,Post_ID int(6) NOT NULL,PRIMARY KEY (Group_ID,Post_ID),FOREIGN KEY (Group_ID) REFERENCES groups (ID),FOREIGN KEY (Post_ID) REFERENCES posts (ID))")

#trigger create
cursor.execute("CREATE TRIGGER group_participants_auto_ins AFTER INSERT ON group_posts FOR EACH ROW BEGIN DECLARE test int(6);SELECT posts.creator_id into test from posts,group_posts where posts.ID=new.post_id limit 1; insert into group_participants(Group_ID,Participant_ID) VALUES(new.group_id,test); END")

#insertion queries
#groups
cursor.execute("INSERT INTO `groups` (`Name`, `ID`, `Region`, `Created_at`) VALUES('GRP1', 200000, 'ASIA', '2022-11-09'),('GRP2', 200001, 'ASIA', '2022-11-09');")
#users
cursor.execute("INSERT INTO `user` (`Username`, `Email`, `Password`, `Joined_at`, `ID`) VALUES('Aayush', 'tt@test.com', 'Pass123', '2022-11-09', 100000),('Chaitanya01', 'te2@test.com', '123456789', '2022-11-09', 100001);")
#posts
cursor.execute("INSERT INTO `posts` (`Title`, `ID`, `Text`, `Creator_ID`) VALUES ('This is the first post', 300000, 'this is content contained by the first post', 100000)")
#group_posts
cursor.execute("INSERT INTO `group_posts` (`Group_ID`, `Post_ID`) VALUES(200000, 300000)")
conn.commit()