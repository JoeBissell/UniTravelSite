use suleima2abbara_prj;


CREATE TABLE coachroutes3 (
  idRoutes INT NOT NULL, 
  deptCity VARCHAR(45) NOT NULL, 
  deptTime VARCHAR(45) NOT NULL, 
  arrivCity VARCHAR(45) NOT NULL, 
  arrivTime VARCHAR(45) NOT NULL, 
  stFare double NOT NULL,
  PRIMARY KEY (idRoutes)); 
  
INSERT INTO suleima2abbara_prj.coachroutes3 VALUES 
  (1000, 'Newcastle', '16:45:00', 'Bristol', '4:00:00', 17.50), 
  (1001, 'Bristol', '8:00:00', 'Newcastle', '19:15:00', 17.50), 
  (1002, 'Cardiff', '6:00:00', 'Edinburgh', '19:30:00', 15.00), 
  (1003, 'Bristol', '11:30:00', 'Manchester', '20:30:00', 12.50), 
  (1004, 'Manchester', '12:20:00', 'Bristol', '21:30:00', 12.50), 
  (1005, 'Bristol', '07:40:00', 'London', '13:40:00', 12.50), 
  (1006, 'London', '11:00:00', 'Manchester', '23:00:00', 16.25), 
  (1007, 'Manchester', '12:20:00', 'Glasgow', '22:40:00', 16.25), 
  (1008, 'Bristol', '07:40:00', 'Glasgow', '17:25:00', 20.00), 
  (1009, 'Glasgow', '14:30:00', 'Newcastle', '01:45:00', 16.25), 
  (1010, 'Newcastle', '16:15:00', 'Manchester', '23:30:00', 16.25), 
  (1011, 'Manchester', '18:25:00', 'Bristol', '04:10:00', 16.25), 
  (1012, 'Bristol', '06:20:00', 'Manchester', '15:20:00', 12.25),
  (1013, 'Dundee', '10:00:00', 'Portsmouth', '03:00:00', 22.50), 
  (1014, 'Edinburgh', '18:30:00', 'Cardiff', '08:00:00', 15.00),
  (1015, 'Southampton', '12:00:00', 'Manchester', '01:30:00', 12.50),
  (1016, 'Manchester', '19:00:00', 'Southampton', '08:30:00', 12.50), 
  (1017, 'Birmingham', '16:00:00', 'Newcastle', '05:30:00', 16.25), 
  (1018, 'Newcastle', '06:00:00', 'Birmingham', '19:30:00', 16.25), 
  (1019, 'Aberdeen', '07:00:00', 'Portsmouth', '01:00:00', 16.25);
  
  select * from coachroutes3; 
  
CREATE TABLE c_bookings3 (
  idBooking INT NOT NULL auto_increment, 
  deptDate  datetime NOT NULL,   
  idRoutes INT NOT NULL,  
  noOfSeats INT NOT NULL default 1, 
  totFare Double NOT NULL,  
 FOREIGN KEY (idRoutes) REFERENCES coachroutes3 (idRoutes), 
 PRIMARY KEY (idBooking)
    ); 
SELECT * FROM coachroutes3 ;

select * from coachusers; 
CREATE TABLE coachusers (
	userid INTEGER NOT NULL auto_increment,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128),
    usertype VARCHAR(8) DEFAULT 'standard',
    primary key(userid)
    );

UPDATE coachusers
SET usertype = 'admin'
WHERE id = 13;

CREATE TABLE c_bookings3 (
  idBooking INT NOT NULL auto_increment, 
  deptDate  datetime NOT NULL,   
  idRoutes INT NOT NULL,  
  noOfSeats INT NOT NULL default 1, 
  totFare Double NOT NULL,  
 FOREIGN KEY (idRoutes) REFERENCES coachroutes3 (idRoutes), 
 FOREIGN KEY (userid) REFERENCES coachusers (userid)
 PRIMARY KEY (idBooking)
    ); 