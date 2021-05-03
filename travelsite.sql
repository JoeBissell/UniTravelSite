CREATE database travelsite;
USE travelsite;

CREATE TABLE taxiusers (
	userid INTEGER NOT NULL auto_increment,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128),
    usertype VARCHAR(8) DEFAULT 'standard',
    primary key(id)
    );

CREATE TABLE taxiroutes (
	routeid INTEGER NOT NULL auto_increment,
    leaving VARCHAR(64) NOT NULL,
    leavingtime TIME(0) NOT NULL,
    arrival VARCHAR(64) NOT NULL,
    arrivaltime TIME NOT NULL,
    miles INTEGER NOT NULL,
    primary key(id)
    );
INSERT INTO travelsite.taxiroutes (
	leaving,
    leavingtime,
    arrival,
    arrivaltime,
    miles
    ) 
VALUES 
	('Newcastle', '16:45:00', 'Bristol', '18:00:00', 295),
    ('Bristol', '8:00:00', 'Newcastle', '09:15:00', 295),
    ('Cardiff', '6:00:00', 'Edinburgh', '07:30:00', 394),
    ('Bristol', '11:30:00', 'Manchester', '12:30:00', 168),
    ('Manchester', '12:20:00', 'Bristol', '13:20:00', 168),
    ('Bristol', '07:40:00', 'London', '8:20:00', 118),
    ('London', '11:00:00', 'Manchester', '12:20:00' , 212),
    ('Manchester', '12:20:00', 'Glasgow', '13:30:00', 215),
    ('Bristol', '07:40:00', 'Glasgow', '08:45:00', 371),
    ('Glasgow', '14:30:00', 'Newcastle', '15:45:00', 152),
    ('Newcastle', '16:15:00', 'Manchester', '17:05:00', 146),
    ('Manchester', '18:25:00', 'Bristol', '19:30:00', 168),
    ('Bristol', '06:20:00', 'Manchester', '07:20:00', 168),
    ('Portsmouth', '12:00:00', 'Dundee', '14:00:00', 514),
    ('Dundee', '10:00:00', 'Portsmouth', '12:00:00', 514),
    ('Edinburgh', '18:30:00', 'Cardiff', '20:00:00', 400),
    ('Southampton', '12:00:00', 'Manchester', '13:30:00', 224),
    ('Manchester', '19:00:00', 'Southampton', '20:30:00', 224),
    ('Birmingham', '16:00:00', 'Newcastle', '17:30:00', 207),
    ('Newcastle', '06:00:00', 'Birmingham', '07:30:00', 207),
    ('Aberdeen', '07:00:00', 'Portsmouth', '09:00:00', 579
);

CREATE TABLE taxibookings (
    bookingid INT NOT NULL auto_increment,
    leavingdate  date NOT NULL,   
    routeid INT NOT NULL,  
    userid VARCHAR(64) NOT NULL,
    numseats INT NOT NULL default 1, 
    totalfare Double NOT NULL,  
    FOREIGN KEY (routeid) REFERENCES taxiroutes (routeid), 
    FOREIGN KEY (userid) REFERENCES userid (userid), 
    PRIMARY KEY (bookingid)
); 

UPDATE taxiusers
SET usertype = 'admin'
WHERE id = 1;

CREATE TABLE coachroutes (
	coachid INTEGER NOT NULL auto_increment,
    leaving VARCHAR(64) NOT NULL,
    leavingtime TIME(0) NOT NULL,
    arrival VARCHAR(64) NOT NULL,
    arrivaltime TIME NOT NULL,
    primary key(coachid)
    );

INSERT INTO travelsite.coachroutes (
	leaving,
    leavingtime,
    arrival,
    arrivaltime,
    ) 

VALUES 
	('Newcastle', '16:45:00', 'Bristol', '4:00:00'),
    ('Bristol', '8:00:00', 'Newcastle', '19:15:00'),
    ('Cardiff', '6:00:00', 'Edinburgh', '19:30:00'),
    ('Bristol', '11:30:00', 'Manchester', '20:30:00'),
    ('Manchester', '12:20:00', 'Bristol', '21:30:00'),
    ('Bristol', '07:40:00', 'London', '13:40:00'),
    ('London', '11:00:00', 'Manchester', '23:00:00'),
    ('Manchester', '12:20:00', 'Glasgow', '22:40:00'),
    ('Bristol', '07:40:00', 'Glasgow', '17:25:00'),
    ('Glasgow', '14:30:00', 'Newcastle', '01:45:00'),
    ('Newcastle', '16:15:00', 'Manchester', '23:30:00'),
    ('Manchester', '18:25:00', 'Bristol', '04:10:00'),
    ('Bristol', '06:20:00', 'Manchester', '15:20:00'),
    ('Dundee', '10:00:00', 'Portsmouth', '03:00:00'),
    ('Edinburgh', '18:30:00', 'Cardiff', '08:00:00'),
    ('Southampton', '12:00:00', 'Manchester', '01:30:00'),
    ('Manchester', '19:00:00', 'Southampton', '08:30:00'),
    ('Birmingham', '16:00:00', 'Newcastle', '05:30:00'),
    ('Newcastle', '06:00:00', 'Birmingham', '19:30:00'),
    ('Aberdeen', '07:00:00', 'Portsmouth', '01:00:00'
);