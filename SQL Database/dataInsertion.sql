INSERT INTO NGO (name, regDate, address, ngoEmail, ngoPassword)
VALUES
('Edhi Foundation', '1951-02-28', 'House No. 601-A, 2nd Floor, Commercial Area, Gulshan-e-Iqbal, Karachi.', 'edhi@gmail.com', '123456'),
('The Citizens Foundation', '1995-09-11', '55-A Kashmir Road, Off M.M. Alam Road, Gulberg III, Lahore.', 'tcf@gmail.com', '123456'),
('Akhuwat', '2001-09-11', '2nd Floor, 17-A Commercial Area, Main Boulevard, Lahore.', 'akhuwat@gmail.com', '123456'),
('Saylani Welfare Trust', '1960-01-01', '162-A, S.M. Society, North Nazimabad, Karachi.', 'saylani@gmail.com', '123456');

INSERT INTO Project (ngoID, projectName, scale, startDate, endDate)
VALUES
(1, 'Edhi Home', 3, '2021-01-01', NULL),
(1, 'Edhi Ambulance Service', 5, '1951-02-28', NULL),
(2, 'The Citizens Foundation School', 4, '1995-09-11', NULL),
(2, 'The Citizens Foundation Hospital', 4, '2000-01-01', NULL),
(3, 'Akhuwat Microfinance Program', 5, '2001-09-11', NULL),
(3, 'Akhuwat Education Program', 4, '2004-01-01', NULL),
(4, 'Saylani Mobile Clinic', 3, '1960-01-01', NULL),
(4, 'Saylani Eye Camp', 3, '1970-01-01', NULL);

INSERT INTO Users (userEmail, userName, userPassword)
VALUES
('user1@gmail.com', 'user1', '123456'),
('user2@gmail.com', 'user2', '123456'),
('user3@gmail.com', 'user3', '123456');

INSERT INTO Category (categoryName)
VALUES
('Education'),
('Healthcare'),
('Microfinance'),
('Social Welfare');

INSERT INTO Donation (projectID, userID, donationDateTime, amount)
VALUES
(1, 1, '2023-01-01 10:00:00', 1000),
(1, 1, '2023-01-15 14:00:00', 500),
(2, 2, '2023-01-02 11:00:00', 1500),
(2, 2, '2023-01-20 09:30:00', 800),
(3, 3, '2023-01-03 12:00:00', 2000),
(3, 3, '2023-11-10 16:45:00', 1200),
(1, 2, '2023-02-05 13:30:00', 700),
(2, 1, '2023-01-18 11:15:00', 1000),
(3, 1, '2023-01-25 10:50:00', 1500),
(1, 3, '2023-10-08 15:25:00', 850),
(2, 3, '2023-05-22 18:00:00', 600),
(3, 2, '2023-01-30 20:30:00', 1300);

INSERT INTO OperatingCategories (ngoID, categoryName)
VALUES
(1, 'Education'),
(1, 'Healthcare'),
(1, 'Social Welfare'),
(2, 'Education'),
(2, 'Healthcare'),
(3, 'Microfinance'),
(4, 'Healthcare'),
(4, 'Social Welfare');

INSERT INTO Area (areaName, city, country)
VALUES
('Gulshan-e-Iqbal', 'Karachi', 'Pakistan'),
('Gulberg III', 'Lahore', 'Pakistan'),
('Commercial Area', 'Lahore', 'Pakistan'),
('North Nazimabad', 'Karachi', 'Pakistan');

INSERT INTO OperatingAreas (areaCode, ngoID)
VALUES
(1, 1),
(1, 4),
(2, 2),
(3, 3);

INSERT INTO Worker (ngoID, workerEmail, workerName, workerPassword, gender, age, dateAdded)
VALUES
(1, 'worker1@gmail.com', 'worker1', '123456', 'Male', 30, '2022-01-01'),
(1, 'worker2@gmail.com', 'worker2', '123456', 'Female', 25, '2022-02-20'),
(1, 'worker3@gmail.com', 'worker3', '123456', 'Male', 40, '2022-10-03'),
(2, 'worker4@gmail.com', 'worker4', '123456', 'Female', 35, '2022-12-04'),
(1, 'worker5@gmail.com', 'worker5', '123456', 'Male', 28, '2023-03-05'),
(1, 'worker6@gmail.com', 'worker6', '123456', 'Female', 32, '2023-05-26'),
(2, 'worker7@gmail.com', 'worker7', '123456', 'Male', 42, '2023-08-07'),
(2, 'worker8@gmail.com', 'worker8', '123456', 'Female', 38, '2023-11-08');

INSERT INTO WorkerProject (workerID, projectID, workerStatus)
VALUES
(1, 1, 'Assigned'),
(2, 1, 'Assigned'),
(3, 2, 'Assigned'),
(4, 3, 'Assigned'),
(5, 2, 'Assigned'),
(6, 1, 'Assigned'),
(7, 4, 'Assigned'),
(8, 3, 'Assigned');

UPDATE Project
SET categoryName = 'Education'
WHERE projectName IN ('The Citizens Foundation School', 'Akhuwat Education Program');

UPDATE Project
SET categoryName = 'Healthcare'
WHERE projectName IN ('Edhi Ambulance Service', 'Saylani Mobile Clinic', 'Saylani Eye Camp',  'The Citizens Foundation Hospital');

UPDATE Project
SET categoryName = 'Microfinance'
WHERE projectName = 'Akhuwat Microfinance Program';

UPDATE Project
SET categoryName = 'Social Welfare'
WHERE projectName = 'Edhi Home';


UPDATE Project
SET areaName = 'Gulshan-e-Iqbal'
WHERE projectName IN ('Edhi Home', 'The Citizens Foundation School');

UPDATE Project
SET areaName = 'Gulistan-e-Johar'
WHERE projectName IN ('Edhi Ambulance Service', 'The Citizens Foundation Hospital');

UPDATE Project
SET areaName = 'Gulberg'
WHERE projectName IN ('Akhuwat Microfinance Program', 'Saylani Mobile Clinic');

UPDATE Project
SET areaName = 'Defence'
WHERE projectName IN ('Akhuwat Education Program', 'Saylani Eye Camp');
