import sqlite3

#creation de la base de donnee courses 

call = sqlite3.connect("nila.db") 

# creation de la table users 

call.execute("""
             create table if not exists users(
             idUser integer primary key autoincrement ,
             fullNames varchar(50),
             fuctionUser varchar(15) default 'student' , 
             phoneUser varchar(15),
             passwordUser varchar(30),
             postNom varchar(30) ,
             emailUser varchar(30),
             dateRegister timestamp default current_timestamp , 
             statut char(3) default 'non'
             
             )
""")


#add 



## information par defaut 
call.execute("insert into users(fullNames,fuctionUser,passwordUser,emailUser) values('nila','admin','nila' ,'nila@gmail.com')")

# table module 
call.execute("create table if not exists modules(idModule integer primary key autoincrement , libelleModule varchar(30))")



call.commit()