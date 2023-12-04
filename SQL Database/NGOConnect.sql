CREATE TABLE NGO (
    ngoID INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255),
    regDate DATE,
    address VARCHAR(255),
    ngoEmail VARCHAR(255),
    ngoPassword VARCHAR(255)
);

CREATE TABLE Project (
    projectID INT PRIMARY KEY IDENTITY(1,1),
    ngoID INT,
    projectName VARCHAR(255),
    scale INT,
    startDate DATE,
    endDate DATE NULL,
    FOREIGN KEY (ngoID) REFERENCES NGO (ngoID)
);

CREATE TABLE Users (
    userID INT PRIMARY KEY IDENTITY(1,1),
    userEmail VARCHAR(255),
    userName VARCHAR(255),
    userPassword VARCHAR(255)
);

CREATE TABLE Category (
    categoryName VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Donation (
    projectID INT,
    userID INT,
    donationDateTime DATETIME,
    amount INT,
    PRIMARY KEY (projectID, userID, donationDateTime),
    FOREIGN KEY (projectID) REFERENCES Project (projectID),
    FOREIGN KEY (userID) REFERENCES Users (userID)
);

CREATE TABLE OperatingCategories (
    ngoID INT,
    categoryName VARCHAR(255),
    PRIMARY KEY (ngoID, categoryName),
    FOREIGN KEY (ngoID) REFERENCES NGO (ngoID),
    FOREIGN KEY (categoryName) REFERENCES Category (categoryName)
);

CREATE TABLE Area (
    areaCode INT PRIMARY KEY IDENTITY(1,1),
    areaName VARCHAR(255),
    city VARCHAR(255),
    country VARCHAR(255)
);

CREATE TABLE OperatingAreas (
    areaCode INT,
    ngoID INT,
    PRIMARY KEY (areaCode, ngoID),
    FOREIGN KEY (areaCode) REFERENCES Area (areaCode),
    FOREIGN KEY (ngoID) REFERENCES NGO (ngoID)
);

CREATE TABLE Worker (
    workerID INT PRIMARY KEY IDENTITY(1,1),
    ngoID INT,
    workerEmail VARCHAR(255),
    workerName VARCHAR(255),
    workerPassword VARCHAR(255),
    gender VARCHAR(255),
    age INT,
    dateAdded DATE,
    FOREIGN KEY (ngoID) REFERENCES NGO (ngoID)
);

CREATE TABLE WorkerProject (
    workerID INT,
    projectID INT,
    workerStatus VARCHAR(255),
    PRIMARY KEY (workerID, projectID),
    FOREIGN KEY (workerID) REFERENCES Worker (workerID),
    FOREIGN KEY (projectID) REFERENCES Project (projectID)
);

ALTER TABLE Project
ADD categoryName VARCHAR(255);

ALTER TABLE Project
ADD areaName VARCHAR(255);

