INSERT INTO NGO (name, regDate, address)
VALUES
('Edhi Foundation', '1957-02-28', '45-B, Korangi Road, Karachi'),
('Saylani Welfare Trust', '1982-05-28', '100, University Road, Karachi'),
('Akhtar Foundation', '1992-09-09', '32-B, Gulshan-e-Iqbal, Karachi'),
('The Citizens Foundation', '1995-10-25', 'A-10, Block-2, Clifton, Karachi');

INSERT INTO Project (ngoID, projectName, scale, startDate, endDate)
VALUES
(1, 'Free Education for Underprivileged Children', 3, '2023-01-01', '2023-12-31'),
(2, 'Providing Shelter and Rehabilitation to Homeless', 2, '2023-04-01', '2023-12-31'),
(3, 'Empowering Women through Vocational Training', 2, '2023-06-01', '2023-12-31'),
(4, 'Promoting Healthcare and Hygiene Awareness', 1, '2023-08-01', '2023-12-31');

INSERT INTO Users (userEmail, userName, userPassword)
VALUES
('ali.khan@gmail.com', 'Ali Khan', '123456'),
('fatima.raza@yahoo.com', 'Fatima Raza', 'password123'),
('hassan.ali@hotmail.com', 'Hassan Ali', 'abc123'),
('amna.khan@outlook.com', 'Amna Khan', 'xyz123');

INSERT INTO Category (categoryName)
VALUES
('Education'),
('Social Welfare'),
('Women Empowerment'),
('Healthcare');

INSERT INTO SavedProject (projectID, userID)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);

INSERT INTO DonatedProject (projectID, userID)
VALUES
(1, 4),
(2, 4),
(3, 3),
(4, 2);

INSERT INTO OperatingCategories (ngoID, categoryName)
VALUES
(1, 'Education'),
(2, 'Social Welfare'),
(3, 'Women Empowerment'),
(4, 'Healthcare');

INSERT INTO Area (areaName, city, country)
VALUES
('Gulshan-e-Iqbal', 'Karachi', 'Pakistan'),
('Defence Housing Authority', 'Karachi', 'Pakistan'),
('New Karachi', 'Karachi', 'Pakistan'),
('North Nazimabad', 'Karachi', 'Pakistan');

INSERT INTO OperatingAreas (areaCode, ngoID)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);

INSERT INTO Worker (ngoID, workerEmail, workerName, workerPassword, gender, age)
VALUES
(1, 'muhammad.ali@gmail.com', 'Muhammad Ali', '123456', 'Male', 32),
(2, 'fatima.ahmed@yahoo.com', 'Fatima Ahmed', 'password123', 'Female', 26),
(1, 'ali.khan1@gmail.com', 'Ali Ahmed', 'password123', 'Male', 30),
(1, 'sana.shah@hotmail.com', 'Sana Shah', 'abc123', 'Female', 28),
(1, 'saad.ali@gmail.com', 'Saad Ali', 'xyz123', 'Male', 35),
(1, 'farah.hussain@yahoo.com', 'Farah Hussain', 'pakistan123', 'Female', 32),
(1, 'asim.ahmed@gmail.com', 'Asim Ahmed', 'lahore123', 'Male', 29);

INSERT INTO WorkerProject (workerID, projectID, workerStatus)
VALUES
(1, 1, 'Active'),
(2, 2, 'Active'),
(3, 1, 'Inactive'),
(4, 1, 'Active'),
(5, 1, 'Active'),
(6, 1, 'Inactive'),
(7, 1, 'Active');