USE bradley2verrinder_prj;

CREATE TABLE journeys (
    idJourneys INT NOT NULL,
    departureCity VARCHAR(40) NOT NULL,
    departureTime VARCHAR(5) NOT NULL,
    destination VARCHAR (40) NOT NULL,
    destinationTime VARCHAR(5) NOT NULL,
    price double NOT NULL,
    PRIMARY KEY (idJourneys));

INSERT INTO journeys VALUES
     (0001, 'Newcastle', '16:45', 'Bristol', '23:00', 140.00),
     (0002, 'Bristol', '08:00', 'Newcastle', '14:15', 140.00),
     (0003, 'Cardiff', '06:00', 'Edinburgh', '13:30', 120.00),
     (0004, 'Bristol', '11:30', 'Manchester', '16:30', 100.00),
     (0005, 'Manchester', '12:20', 'Bristol', '17:20', 100.00),
     (0006, 'Bristol', '07:40', 'London', '11:00', 100.00),
     (0007, 'London', '11:00', 'Manchester', '17:00', 130.00),
     (0008, 'Manchester', '12:20', 'Glasgow', '18:10', 130.00),
     (0009, 'Bristol', '07:40', 'Glasgow', '13:05', 160.00),
     (0010, 'Glasgow', '14:30', 'Newcastle', '20:45', 130.00),
     (0011, 'Newcastle', '16:15', 'Manchester', '22:25', 130.00),
     (0012, 'Manchester', '18:25', 'Bristol', '23:50', 100.00),
     (0013, 'Bristol', '06:20', 'Manchester', '12:20', 100.00),
     (0014, 'Dundee', '10:00', 'Portsmouth', '20:00', 180.00),
     (0015, 'Southampton', '12:00', 'Manchester', '19:30', 100.00),
     (0016, 'Manchester', '19:00', 'Southampton', '02:30', 100.00),
     (0017, 'Birmingham', '16:00', 'Newcastle', '23:30', 130.00),
     (0018, 'Newcastle', '06:00', 'Birmingham', '13:30', 130.00),
     (0019, 'Aberdeen', '07:00', 'Portsmouth', '17:00', 130.00);

CREATE TABLE reservation (
     idReserve INT NOT NULL auto_increment,
     departureDate DATE NOT NULL,
     destinationDate DATE NOT NULL,
     idJourneys INT NOT NULL,
     ticketFare Double NOT NULL,
     seatNum INT NOT NULL default 1,
     userId INT NOT NULL,
     FOREIGN KEY(userId) REFERENCES trainusers (userId),
     FOREIGN KEY(idJourneys) REFERENCES journeys (idJourneys),
     PRIMARY KEY (idReserve));

CREATE TABLE trainusers (
     userId INTEGER NOT NULL auto_increment,
     username VARCHAR(50) NOT NULL UNIQUE,
     email VARCHAR(80) NOT NULL UNIQUE,
     password_hash VARCHAR(50),
     accountType VARCHAR(10) DEFAULT 'standard',
     primary key(userId));