-- Create and use database
CREATE DATABASE IF NOT EXISTS marketplace;
USE marketplace;

-- Create Moderator table (no foreign keys)
CREATE TABLE Moderator (
    moderatorID INT PRIMARY KEY,
    Birthdate DATE,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    EmailAddress VARCHAR(100),
    PhoneNumber VARCHAR(20),
    Age INT
);

-- Create Analyst table (no foreign keys)
CREATE TABLE Analyst (
    AnalystID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    BirthDate DATE,
    Age INT,
    Email VARCHAR(100)
);

-- Create ProductTags table (no foreign keys)
CREATE TABLE ProductTags (
    ProductTagID INT PRIMARY KEY,
    title VARCHAR(50)
);

-- Create Seller table
CREATE TABLE Seller (
    SellerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    University VARCHAR(100),
    Verification BOOLEAN,
    Email VARCHAR(100),
    Age INT,
    Rating DECIMAL(2,1),
    PhoneNumber VARCHAR(20),
    Birthdate DATE,
    TermsAndConditions BOOLEAN,
    moderatorID INT,
    FOREIGN KEY (moderatorID) REFERENCES Moderator(moderatorID)
);

-- Create Buyer table
CREATE TABLE Buyer (
    BuyerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    University VARCHAR(100),
    Age INT,
    Feedback TEXT,
    PhoneNumber VARCHAR(20),
    Birthdate DATE,
    TermsAndConditions BOOLEAN,
    Verification BOOLEAN,
    moderatorID INT,
    FOREIGN KEY (moderatorID) REFERENCES Moderator(moderatorID)
);

-- Create Products table
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    Status VARCHAR(20),
    Price DECIMAL(10,2),
    Name VARCHAR(100),
    Condition VARCHAR(20),
    PostedDate DATE,
    Description TEXT,
    Category VARCHAR(50),
    Saves INT,
    Views INT,
    Verified BOOLEAN,
    sellerID INT,
    DaysPosted INT,
    ProductSimilarID INT,
    FOREIGN KEY (sellerID) REFERENCES Seller(SellerID),
    FOREIGN KEY (ProductSimilarID) REFERENCES Products(ProductID)
);

-- Create BankAccount table
CREATE TABLE BankAccount (
    BankID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    AccountType VARCHAR(20),
    AccountNumber VARCHAR(50),
    RoutingNumber VARCHAR(20),
    BankName VARCHAR(50),
    SellerID INT,
    FOREIGN KEY (SellerID) REFERENCES Seller(SellerID)
);

-- Create PaymentMethod table
CREATE TABLE PaymentMethod (
    CardNum VARCHAR(20) PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    State VARCHAR(2),
    City VARCHAR(50),
    ZipStreet VARCHAR(10),
    CVV INT,
    ExpDate DATE,
    BuyerID INT,
    FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID)
);

-- Create Orders table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    OrderDate DATE,
    PickupAddress VARCHAR(200)
);

-- Create Product_Photo table
CREATE TABLE Product_Photo (
    ProductID INT,
    PhotoID INT,
    Photo VARCHAR(200),
    PRIMARY KEY (ProductID, PhotoID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- Create Messages table
CREATE TABLE Messages (
    convoID INT PRIMARY KEY,
    alerts BOOLEAN,
    Reported BOOLEAN,
    ConvoStartDate DATE,
    Body TEXT,
    moderatorID INT,
    BuyerID INT,
    SellerID INT,
    FOREIGN KEY (moderatorID) REFERENCES Moderator(moderatorID),
    FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID),
    FOREIGN KEY (SellerID) REFERENCES Seller(SellerID)
);

-- Create History table
CREATE TABLE History (
    HistoryID INT PRIMARY KEY,
    Searches VARCHAR(200),
    ProductsViewed INT,
    BuyerID INT,
    FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID),
    FOREIGN KEY (ProductsViewed) REFERENCES Products(ProductID)
);

-- Create TagsofProducts table (junction table)
CREATE TABLE TagsofProducts (
    ProductID INT,
    ProductTagID INT,
    PRIMARY KEY (ProductID, ProductTagID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (ProductTagID) REFERENCES ProductTags(ProductTagID)
);

-- Create Analyst_Product table (junction table)
CREATE TABLE Analyst_Product (
    AnalystID INT,
    ProductID INT,
    Revenue DECIMAL(10,2),
    PRIMARY KEY (AnalystID, ProductID),
    FOREIGN KEY (AnalystID) REFERENCES Analyst(AnalystID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);