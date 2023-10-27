-- Turn off foreign keys to remove constraint when dropping --
PRAGMA foreign_keys = off;
DROP TABLE IF EXISTS Applicants;
DROP TABLE IF EXISTS Applications;
DROP TABLE IF EXISTS VideoApplications;
DROP TABLE IF EXISTS Contact;
DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS Funding;
PRAGMA foreign_keys = on;

-- Applicant Table --

CREATE TABLE IF NOT EXISTS Applicants (
  'applicant_id' integer PRIMARY KEY AUTOINCREMENT,
  'name' text NOT NULL,
  'surname' text NOT NULL,
  'email' text unique NOT NULL
);

-- Applicant Table Data --
INSERT INTO Applicants (name , surname, email)
VALUES ('Joe', 'Taylor', 'example@test.co.uk');

INSERT INTO Applicants (name , surname, email)
VALUES ('Eric', 'Milligan', 'example2@test.com');

INSERT INTO Applicants (name , surname, email)
VALUES ('Oliver', 'Farmer', 'example3@test.com');

INSERT INTO Applicants (name , surname, email)
VALUES ('Meryl', 'Gwent', 'MadameGwent@test.com');

INSERT INTO Applicants (name , surname, email)
VALUES ('Gerry', 'Butcher', 'ButcherGer@test.com');

INSERT INTO Applicants (name , surname, email)
VALUES ('Mackenzie', 'River', 'McRiver@test.com');

INSERT INTO Applicants (name , surname, email)
VALUES ('Darius', 'Knight', 'DIKnight@test.com');

INSERT INTO Applicants (name , surname, email)
VALUES ('Beryl', 'King', 'BKing@test.com');

INSERT INTO Applicants (name , surname, email)
VALUES ('Martin', 'Bailey', 'MBailey@test.com');

INSERT INTO Applicants (name , surname, email)
VALUES ('Stephen', 'Goodwin', 'SGoodwin@test.com');

-- Applications Table --

CREATE TABLE IF NOT EXISTS Applications (
  'application_id' integer PRIMARY KEY AUTOINCREMENT,
  'applicant_id' integer NOT NULL,
  'answer1' text NOT NULL,
  'answer2' text NOT NULL,
  'answer3' text NOT NULL,
  'answer4' text NOT NULL,
  'answer5' text NOT NULL,
  'status' text DEFAULT 'open',
  FOREIGN KEY ('applicant_id') REFERENCES Applicants('applicant_id')
);

-- Sample Applications Data --
INSERT INTO Applications (applicant_id, answer1, answer2, answer3, answer4, answer5, status)
VALUES (1, 'Barnardos', 'Barnardos is a British charity founded by
  Thomas John Barnardo in 1866, to care for vulnerable children.',
'Its vital that we speak up to help give young people the best
chance in life.','Abergavenny', 6, 'Accepted');

INSERT INTO Applications (applicant_id, answer1, answer2, answer3, answer4, answer5, status)
VALUES (2, 'British Heart Foundation', 'Funds medical research related to
heart and circulatory diseases and their risk factors.', 'The BHF relies
entirely on generous supporters to fund life-changing and life saving
research. ', 'Ebbw Vale', 4, 'Accepted');

INSERT INTO Applications (applicant_id, answer1, answer2, answer3, answer4, answer5, status)
VALUES (3, 'Mind Matters', 'Helping young people look after their mental
  health.', 'Help those in need with specialised support and tips.',
  'Newport', 3, 'Accepted');

INSERT INTO Applications (applicant_id, answer1, answer2, answer3, answer4, answer5, status)
VALUES (1, 'Dog Rescuers', 'Track down some of the UKs most abused and
mistreated animals in an attempt to rescue them.', 'When successful in
rescuing the dogs, the animals are rehabilitated and eventually
given new homes.', 'Pontypool', 7, 'Accepted');

INSERT INTO Applications (applicant_id, answer1, answer2, answer3, answer4, answer5, status)
VALUES (4, 'Macmillan Cancer Support', 'Specialist health care,
  information and financial support to  people affected by cancer.',
  'We also looks at the social, emotional and practical impact
  cancer can have,and campaigns for better cancer care.',
  'Monmouth', 7, 'Accepted');

INSERT INTO Applications (applicant_id, answer1, answer2, answer3, answer4, answer5, status)
VALUES (5, 'Age UK', 'UKs largest charity for older people.',
    'Too many older people feel they have no one to turn to for support.
    We exist to help older people when they need us the most.',
    'Brynmawr', 7, 'Accepted');

INSERT INTO Applications (applicant_id, answer1, answer2, answer3, answer4, answer5, status)
VALUES (6, 'Save the Children', 'Improve the lives of children through better
        education, health care, and economic opportunities',
        'Providing emergency aid in natural disasters, war, and other conflicts.',
        'Pontypool', 7, 'Accepted');

INSERT INTO Applications (applicant_id, answer1, answer2, answer3, answer4, answer5)
VALUES (8, 'Marie Curie', 'Marie Curie is a registered charitable
  organisation in the United Kingdom which provides care and support to
  people with terminal illnesses and their families.',
  'Providing support to people with terminal illnesses.',
  'Usk', 7);

INSERT INTO Applications (applicant_id, answer1, answer2, answer3, answer4, answer5)
VALUES (9, 'Guide Dogs', 'Guide Dogs helps blind and partially sighted people
  across the UK through the provision of guide dogs, mobility and other services
  for both adults and children.',
    'We also campaign for the rights of those with vision impairments and
    invest in research.',
    'Monmouth', 7);

-- Video Applications Table --

CREATE TABLE IF NOT EXISTS VideoApplications (
  'application_id' integer PRIMARY KEY AUTOINCREMENT,
  'applicant_id' integer NOT NULL,
  'video_name' text NOT NULL,
  'status' text DEFAULT 'open',
  FOREIGN KEY ('applicant_id') REFERENCES Applicants('applicant_id')
);

-- Contact Messages Table --

CREATE TABLE IF NOT EXISTS Contact (
  'contact_id' integer PRIMARY KEY AUTOINCREMENT,
  'name' text NOT NULL,
  'email' text unique NOT NULL,
  'message' text NOT NULL
);

-- Contact Messages Table Insert Sample --

INSERT INTO Contact (name, email, message)
VALUES('Eric Milligan', 'ric@kloopa.com', 'We love your site!');

-- Accounts table - For login system --

CREATE TABLE IF NOT EXISTS Admin (
  'userid'   integer PRIMARY KEY AUTOINCREMENT,
  'username' text unique NOT NULL,
  'password' text        NOT NULL,
  'userType' text        NOT NULL
);

-- Sample accounts data --
INSERT INTO Admin (userid, username, password, userType)
VALUES (0001, 'Admin', '1234', 'Admin');

INSERT INTO Admin (userid, username, password, userType)
VALUES (0002, 'Oliver', 'IsReallyCool', 'Customer');

--  - For location system --

-- Locations table - For dropdown list --

CREATE TABLE IF NOT EXISTS Locations (
  'locationid'   integer PRIMARY KEY AUTOINCREMENT,
  'locationName' text unique NOT NULL,
  'latitude'     text        NOT NULL,
  'longitude'    text        NOT NULL
);

-- Locations data --

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Abergavenny', '51.830644650558504', '-3.018399561895017');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Abertillery', '51.73419498192001', '-3.134954310274954');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Blaenavon', '51.77526526901892', '-3.0855317144923435');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Brynmawr', '51.79735813940495', '-3.1752148096679242');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Caerlon', '51.61429983812936', '-2.9579223525772376');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Caldicot', '51.59348987620318', '-2.7515170708982923');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Chepstow', '51.642468823675856', '-2.6743451362878217');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Cwmbran', '51.653045034070786', '-3.0333873873006634');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Ebbw Vale', '51.78049406377765', '-3.2061616029931317');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Llandogo', '51.736050094298115', '-2.686622017162991');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Monmouth', '51.81366280598221', '-2.716285693551137');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Newbridge', '51.667544015419935', '-3.143878754183492');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Newport', '51.591284903274996', '-2.997150253719862');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Pandy', '51.89767305577099', '-2.96666725137239');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Pontypool', '51.70403485528888', '-3.0460724351853954');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Raglan', '51.76636437561485', '-2.8521594896959956');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('St.Brides', '51.534877359900705', '-3.0190109390750868');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Tredegar', '51.77501290796547', '-3.246797137207292');

INSERT INTO Locations (locationName, latitude, longitude)
VALUES ('Usk', '51.70469539882075', '-2.9038956084109095');

-- Funding Table --

CREATE TABLE IF NOT EXISTS Funding (
  'locationid' integer PRIMARY KEY,
  'fundingAmount' float   NOT NULL,
  FOREIGN KEY ('locationid') REFERENCES Locations('locationid')
);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (1, 5000.00);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (2, 0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (3, 0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (4, 5000.0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (5, 0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (6, 0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (7, 0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (8, 0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (9, 5000.0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (10, 0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (11, 5000.0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (12, 0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (13, 5000.0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (14, 0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (15, 10000.0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (16, 0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (17, 0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (18, 5000.0);

INSERT INTO Funding (locationid, fundingAmount)
VALUES (19, 0);
