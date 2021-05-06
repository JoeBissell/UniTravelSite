USE AirTravel;
CREATE TABLE airusers(
    airuserid INTEGER NOT NULL AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128),
    usertype VARCHAR(8) DEFAULT 'Standard',
    PRIMARY KEY (airuserid)
);
CREATE TABLE airroutes (
	airid INTEGER NOT NULL auto_increment,
    leaving VARCHAR(64) NOT NULL,
    leavingtime TIME NOT NULL,
    arrival VARCHAR(64) NOT NULL,
    arrivaltime TIME NOT NULL,
    totaltime TIME NOT NULL,
    primary key(airid)
    );
    
INSERT INTO AirTravel.airroutes(
    leaving,
    leavingtime,
    arrival,
    arrivaltime,
    totaltime
)
VALUES (
	('Newcastle', '16:45:00', 'Bristol', '18:00:00', '01:15:00'),
    ('Bristol', '8:00:00', 'Newcastle', '09:15:00', '01:15:00'),
    ('Cardiff', '6:00:00', 'Edinburgh', '07:30:00', '01:30:00'),
    ('Bristol', '11:30:00', 'Manchester', '12:30:00', '01:00:00'),
    ('Manchester', '12:20:00', 'Bristol', '13:20:00', '01:00:00'),
    ('Bristol', '07:40:00', 'London', '8:20:00', '00:40:00'),
    ('London', '11:00:00', 'Manchester', '12:20:00' , '01:20:00'),
    ('Manchester', '12:20:00', 'Glasgow', '13:30:00', '01:10:00'),
    ('Bristol', '07:40:00', 'Glasgow', '08:45:00', '01:05:00'),
    ('Glasgow', '14:30:00', 'Newcastle', '15:45:00', '01:15:00'),
    ('Newcastle', '16:15:00', 'Manchester', '17:05:00', '00:50:00'),
    ('Manchester', '18:25:00', 'Bristol', '19:30:00', '01:05:00'),
    ('Bristol', '06:20:00', 'Manchester', '07:20:00', '01:00:00'),
    ('Portsmouth', '12:00:00', 'Dundee', '14:00:00', '02:00:00'),
    ('Dundee', '10:00:00', 'Portsmouth', '12:00:00', '02:00:00'),
    ('Edinburgh', '18:30:00', 'Cardiff', '20:00:00', '01:30:00'),
    ('Southampton', '12:00:00', 'Manchester', '13:30:00', '01:30:00'),
    ('Manchester', '19:00:00', 'Southampton', '20:30:00', '01:30:00'),
    ('Birmingham', '16:00:00', 'Newcastle', '17:30:00', '01:30:00'),
    ('Newcastle', '06:00:00', 'Birmingham', '07:30:00', '01:30:00'),
    ('Aberdeen', '07:00:00', 'Portsmouth', '09:00:00', '02:00:00')
;
