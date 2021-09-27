CREATE DATABASE FOODDBa;
USE FOODDBa;



CREATE TABLE CUSTOMERINFO (
	CUSTOMERID INT (10) AUTO_INCREMENT PRIMARY KEY,
	FIRSTNAME CHAR (20) NOT NULL,
	LASTNAME CHAR (20) NOT NULL,
	ADDRESS VARCHAR (50) NOT NULL,
	EMAIL VARCHAR (50) NOT NULL,
	DOB DATE NOT NULL,
	REGDATE DATE NOT NULL,
	GENDER CHAR (1) NOT NULL
) ENGINE = INNODB ;

CREATE TABLE RESTAURANT(
	RESTAURANTNAME VARCHAR (30) NOT NULL PRIMARY KEY,
	LPDelivery INT (3) NOT NULL DEFAULT 1,
	LPDPickup INT (3) NOT NULL DEFAULT 1
) ENGINE = INNODB ;

CREATE TABLE RESTAURANTLOCATION(
	RESTAURANTNAME VARCHAR (30) NOT NULL,
	LOCATION VARCHAR (50) NOT NULL,
	FOREIGN KEY (RESTAURANTNAME) REFERENCES RESTAURANT (RESTAURANTNAME)
) ENGINE = INNODB ;


CREATE TABLE LOYALTY (
	RESTAURANTNAME VARCHAR (30) NOT NULL,
	POINTS INT (10) NOT NULL,
	CUSTOMERID INT (10) NOT NULL,
	FOREIGN KEY (RESTAURANTNAME) REFERENCES RESTAURANT (RESTAURANTNAME),
	FOREIGN KEY (CUSTOMERID) REFERENCES CUSTOMERINFO (CUSTOMERID)
) ENGINE = INNODB ;


CREATE TABLE MOBILE (
	CUSTOMERID INT (10) NOT NULL,
	MOBILENUMBER INT (40) NOT NULL PRIMARY KEY,
	FOREIGN KEY (CUSTOMERID) REFERENCES CUSTOMERINFO (CUSTOMERID)
) ENGINE = INNODB ;

CREATE TABLE CARD (
	CARDTYPE VARCHAR (20) NOT NULL PRIMARY KEY
) ENGINE = INNODB ;

CREATE TABLE SAVEDCARD (
    CUSTOMERID INT (10) NOT NULL,
    CARDTYPE VARCHAR (20) NOT NULL,
	CARDHOLDERNAME CHAR (40) NOT NULL,
    CARDNUMBER VARCHAR (20) NOT NULL PRIMARY KEY,
    EXPIRYDATE DATE NOT NULL,
    ADDRESS VARCHAR (50) NOT NULL,
	FOREIGN KEY (CUSTOMERID) REFERENCES CUSTOMERINFO (CUSTOMERID),
    FOREIGN KEY (CARDTYPE) REFERENCES CARD (CARDTYPE)
) ENGINE = INNODB ;

CREATE TABLE CUSTOMERORDER (
	ORDERNUMBER INT (100) AUTO_INCREMENT PRIMARY KEY,
	CUSTOMERID INT (10) NOT NULL,
	ORDERDATE DATE NOT NULL, 
	Value INT (50) NOT NULL DEFAULT 0,
	FULFILLED BOOLEAN DEFAULT 0
) ENGINE = INNODB ;

CREATE TABLE PRODUCT (
    PRODUCTID INT (100) AUTO_INCREMENT PRIMARY KEY ,
    RESTAURANTNAME VARCHAR (30) NOT NULL ,
    PRODUCTNAME VARCHAR (50) NOT NULL,
	PRODUCTPRICE FLOAT (50) NOT NULL,
    FOREIGN KEY (RESTAURANTNAME) REFERENCES RESTAURANT (RESTAURANTNAME)
) ENGINE = INNODB ;

CREATE TABLE ORDERINFO (
	ORDERNUMBER INT (100) NOT NULL,
	PRODUCTID INT (100) NOT NULL,
	Quantity int(10) default 1 ,
	PRIMARY KEY (ORDERNUMBER, PRODUCTID) ,
	FOREIGN KEY (ORDERNUMBER) REFERENCES CUSTOMERORDER (ORDERNUMBER),
	FOREIGN KEY (PRODUCTID) REFERENCES PRODUCT (PRODUCTID)
	
) ENGINE = INNODB ;

CREATE TABLE Voucher(
	Code VARCHAR (30) NOT NULL PRIMARY KEY,
	Value INT (50) NOT NULL NOT NULL,
	RESTAURANTNAME VARCHAR (30) NOT NULL,
	 FOREIGN KEY (RESTAURANTNAME) REFERENCES RESTAURANT (RESTAURANTNAME)

) ENGINE = INNODB ;




insert into customerinfo values(null,
'Ishaq',
'Burgah',
'burger ville',
'IshaqForBurger@gmail.com',
'1993-10-6',
'2007-03-23',
'O');

insert into customerinfo values(null,
'Depressed',
'Panda',
'Nowhere',
'SadPanda@gmail.com',
'1995-11-9',
'2007-03-22',
'M');


insert into customerinfo values(null,
'Angry',
'Bear',
'Forest',
'DepressedSalmonHelper@gmail.com',
'1996-01-2',
'2007-03-21',
'M');


insert into customerinfo values(null,
'Death',
'Taxes',
'Everyone',
'Aging@gmail.com',
'1991-01-2',
'2007-05-21',
'M');

insert into card values('visa');
insert into card values('debit');
insert into card values('mastercard');

insert into mobile values(4,554217087);
insert into mobile values(3,564217087);
insert into mobile values(2,564277087);
insert into mobile values(1,564277077);
insert into mobile values(1,564277066);

INSERT INTO SAVEDCARD VALUES(1,'VISA','ISHAQ BURGAH',45845455,'2020-3-24','BURGER VILLE');
INSERT INTO SAVEDCARD VALUES(1,'VISA','ISHAQ BURGAH',45845445,'2007-07-24','BURGER VILLE');
INSERT INTO SAVEDCARD VALUES(2,'DEBIT','depressed panda',458454515,'2017-3-24','nowhere');
INSERT INTO SAVEDCARD VALUES(3,'DEBIT','angry bear',4584515,'2027-3-24','forest');
INSERT INTO SAVEDCARD VALUES(4,'mastercard','death & taxes',14584515,'2017-3-24','everyone');

Insert into restaurant values('Burger King',5,10);
Insert into restaurant values('Shawarma King',4,8);
Insert into restaurant values('McKing',3,6);

Insert into RESTAURANTLOCATION values('McKing','Al Burger City 420'),('Shawarma King','Al Burger City 2'),('Burger King','Al Burger City 1');
 
Insert into product values(null,'burger king','not Shawarma',6.5);
Insert into product values(null,'burger king','king of burgah',1.5);
Insert into product values(null,'mcking','cucumber',7.8);
Insert into product values(null,'mcking','lettuce',6.99);
Insert into product values(null,'shawarma king','definetly a sharawma',10.01);
Insert into product values(null,'shawarma king','not a burger',20.20);

insert into customerorder values (null,1,'2017-3-24',30,0);
insert into customerorder values (null,1,'2017-3-3',15,1);
insert into customerorder values (null,2,'2017-3-3',10,1);
insert into customerorder values (null,3,'2017-3-5',20,1);

-- This part can produce errors mostly cause i created columns that overflowed and had to delete them correct the first fields as needed
insert into orderinfo values (1,1,3);
insert into orderinfo values (1,2,3);
insert into orderinfo values (1,4,3);
insert into orderinfo values (2,5,3);
insert into orderinfo values (2,6,3);
insert into orderinfo values (3,6,3);
insert into orderinfo values (4,6,3);

insert into loyalty values ('burger king',1,1);
insert into loyalty values ('burger king',3,2);
insert into loyalty values ('burger king',7,3);
insert into loyalty values ('burger king',11,4);
insert into loyalty values ('mcking',13,1);
insert into loyalty values ('mcking',17,2);
insert into loyalty values ('mcking',19,3);
insert into loyalty values ('mcking',23,4);
insert into loyalty values ('shawarma king',33,1);
insert into loyalty values ('shawarma king',43,2);
insert into loyalty values ('shawarma king',51,3);
insert into loyalty values ('shawarma king',57,4);
show tables;
show columns from card;
show columns from customerinfo;
show columns from customerorder;
show columns from loyalty;
show columns from mobile;
show columns from orderinfo;
show columns from product;
show columns from restaurant;
show columns from restaurantlocation;
show columns from savedcard;


