import sqlite3

#creation de la base de donnee courses 

call = sqlite3.connect("courses.db") 

# creation de la table users 

call.execute("""
                create table if not exists users(
             idUser integer primary key autoincrement ,
             fullNames varchar(50),
             fuctionUser varchar(15) default 'student' , 
             phoneUser varchar(15),
             passwordUser varchar(30),
             dateRegister timestamp default current_timestamp 
             
             )
""")

## information par defaut 
#call.execute("insert into users(fullNames,fuctionUser,passwordUser) values('nila','admin','nila')")

call.commit()