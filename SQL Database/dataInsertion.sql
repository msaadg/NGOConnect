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

INSERT INTO Category (categoryName)
VALUES
('Education'),
('Healthcare'),
('Microfinance'),
('Social Welfare');

INSERT INTO Users (userEmail, userName, userPassword)
VALUES
('user1@gmail.com', 'user1', '123456'),
('user2@gmail.com', 'user2', '123456'),
('user3@gmail.com', 'user3', '123456');

INSERT INTO SavedProject (projectID, userID)
VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO DonatedProject (projectID, userID)
VALUES
(1, 2),
(2, 1),
(3, 3);

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

INSERT INTO Worker (ngoID, workerEmail, workerName, workerPassword, gender, age)
VALUES
(1, 'worker1@gmail.com', 'worker1', '123456', 'Male', 30),
(1, 'worker2@gmail.com', 'worker2', '123456', 'Female', 25),
(1, 'worker3@gmail.com', 'worker3', '123456', 'Male', 40),
(2, 'worker4@gmail.com', 'worker4', '123456', 'Female', 35),
(1, 'worker5@gmail.com', 'worker5', '123456', 'Male', 28),
(1, 'worker6@gmail.com', 'worker6', '123456', 'Female', 32),
(2, 'worker7@gmail.com', 'worker7', '123456', 'Male', 42),
(2, 'worker8@gmail.com', 'worker8', '123456', 'Female', 38);


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