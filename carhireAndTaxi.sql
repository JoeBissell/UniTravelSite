DROP database travelsite;
CREATE database travelsite;
USE travelsite;

-- Car Hire (Joe)

CREATE TABLE carhire (
	carid INTEGER NOT NULL auto_increment,
    manufacturer VARCHAR(30) NOT NULL,
    brand VARCHAR(64) NOT NULL,
    numberOfSeats VARCHAR(64) NOT NULL,
    costPerDay INTEGER NOT NULL,
    type VARCHAR(10) NOT NULL,
    bookedBy INTEGER,
    bookedFrom DATE,
    bookedTo DATE,

    primary key(carid)
    );

INSERT INTO travelsite.carhire (
	manufacturer,
    brand,
    numberOfSeats,
    costPerDay,
    type
    ) 

VALUES 
	('Vauxhall', 'Corsa', '5', '32', 'Standard'),
	('Fiat', '500', '4', '23', 'Standard'),
	('Peugeot', '208', '5', '27', 'Standard'),
	('Opel', 'Corsa', '5', '28', 'Standad'),
	('Fiat', 'Tipo', '5', '32', 'Standard'),
	('Volkswagen', 'Golf', '4', '36', 'Standard'),
	('Ford', 'Fiesta', '4', '26', 'Standard'),
    ('Mercedes', 'Premium', '5', '167', 'Executive'),
    ('Tesla', 'Model S', '5', '178', 'Executive'
);

CREATE TABLE carhireusers (
	userid INTEGER NOT NULL auto_increment,
    username VARCHAR(24) NOT NULL UNIQUE,
    email VARCHAR(70) NOT NULL UNIQUE,
    password_hash VARCHAR(128),
    usertype VARCHAR(8) DEFAULT 'standard',
    primary key(userid)
);

INSERT INTO travelsite.carhireusers (
	username,
    email,
    password_hash,
    usertype
    ) 

VALUES 
	('joebissell', 'joe.bissell@email.co.uk', 'pass', 'admin'),
	('johndoe', 'john.doe@email.co.uk', 'pass', 'standard'),
	('sarahdoe', 'sarah.doe@email.co.uk', 'pass', 'standard'),
	('scottwalker', 'scott.walker@email.co.uk', 'pass', 'standard'),
	('janedoe', 'jane.doe@email.co.uk', 'pass', 'standard'
);

CREATE TABLE taxiusers (
	userid INTEGER NOT NULL auto_increment,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128),
    usertype VARCHAR(8) DEFAULT 'standard',
    primary key(userid)
    );

CREATE TABLE taxiroutes (
	routeid INTEGER NOT NULL auto_increment,
    leaving VARCHAR(64) NOT NULL,
    leavingtime TIME(0) NOT NULL,
    arrival VARCHAR(64) NOT NULL,
    arrivaltime TIME NOT NULL,
    miles INTEGER NOT NULL,
    primary key(routeid)
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

-- Taxi (Oscar) 

CREATE TABLE taxibookings (
    bookingid INT NOT NULL auto_increment,
    leavingdate  date NOT NULL,   
    routeid INT NOT NULL,  
    numseats INT NOT NULL default 1, 
    totalfare Double NOT NULL, 
    userid INT NOT NULL,
    leaving VARCHAR(64) NOT NULL,
    arrival VARCHAR(64) NOT NULL,
    FOREIGN KEY (routeid) REFERENCES taxiroutes (routeid), 
    FOREIGN KEY (userid) REFERENCES taxiusers (userid), 
    PRIMARY KEY (bookingid)
); 	

SELECT * FROM carhire