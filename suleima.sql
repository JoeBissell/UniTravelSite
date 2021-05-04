use suleima2abbara_prj;

CREATE TABLE coach (
	coachid INTEGER NOT NULL auto_increment,
    leaving VARCHAR(64) NOT NULL,
    leavingtime TIME NOT NULL,
    arrival VARCHAR(64) NOT NULL,
    arrivaltime TIME NOT NULL,
    primary key(coachid)
    );
    
INSERT INTO suleima2abbara_prj.coach VALUES 
	('NULL','Newcastle', '16:45:00', 'Bristol', '4:00:00'),
	('NULL','Bristol', '8:00:00', 'Newcastle', '19:15:00'),
    ('NULL','Cardiff', '6:00:00', 'Edinburgh', '19:30:00'),
    ('NULL','Bristol', '11:30:00', 'Manchester', '20:30:00'),
    ('NULL','Manchester', '12:20:00', 'Bristol', '21:30:00'),
    ('NULL','Bristol', '07:40:00', 'London', '13:40:00'),
    ('NULL','London', '11:00:00', 'Manchester', '23:00:00'),
    ('NULL','Manchester', '12:20:00', 'Glasgow', '22:40:00'),
    ('NULL','Bristol', '07:40:00', 'Glasgow', '17:25:00'),
    ('NULL','Glasgow', '14:30:00', 'Newcastle', '01:45:00'),
    ('NULL','Newcastle', '16:15:00', 'Manchester', '23:30:00'),
    ('NULL','Manchester', '18:25:00', 'Bristol', '04:10:00'),
    ('NULL','Bristol', '06:20:00', 'Manchester', '15:20:00'),
    ('NULL','Dundee', '10:00:00', 'Portsmouth', '03:00:00'),
    ('NULL','Edinburgh', '18:30:00', 'Cardiff', '08:00:00'),
    ('NULL','Southampton', '12:00:00', 'Manchester', '01:30:00'),
    ('NULL','Manchester', '19:00:00', 'Southampton', '08:30:00'),
    ('NULL','Birmingham', '16:00:00', 'Newcastle', '05:30:00'),
    ('NULL','Newcastle', '06:00:00', 'Birmingham', '19:30:00'),
    ('NULL','Aberdeen', '07:00:00', 'Portsmouth', '01:00:00')
;

CREATE TABLE coachusers (
	userid INTEGER NOT NULL auto_increment,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128),
    usertype VARCHAR(8) DEFAULT 'standard',
    primary key(userid)
    );