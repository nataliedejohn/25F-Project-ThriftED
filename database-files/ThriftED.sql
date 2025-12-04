DROP DATABASE IF EXISTS ThriftED;
CREATE DATABASE ThriftED;
USE ThriftED;

CREATE TABLE IF NOT EXISTS Moderator (
    ModeratorID   INT UNSIGNED AUTO_INCREMENT,
    FirstName     VARCHAR(50) NOT NULL,
    LastName      VARCHAR(50) NOT NULL,
    EmailAddress  VARCHAR(255) NOT NULL UNIQUE,
    PhoneNumber   VARCHAR(20),
    Birthdate     DATE,
    Age           INT,
    PRIMARY KEY (ModeratorID)
);

CREATE TABLE IF NOT EXISTS Analyst (
    AnalystID   INT UNSIGNED AUTO_INCREMENT,
    FirstName   VARCHAR(50) NOT NULL,
    LastName    VARCHAR(50) NOT NULL,
    Email       VARCHAR(255) NOT NULL UNIQUE,
    Birthdate   DATE,
    Age         INT,
    PRIMARY KEY (AnalystID)
);

CREATE TABLE IF NOT EXISTS Buyer (
    BuyerID     INT UNSIGNED AUTO_INCREMENT,
    FirstName   VARCHAR(50) NOT NULL,
    LastName    VARCHAR(50) NOT NULL,
    Email       VARCHAR(255) NOT NULL UNIQUE,
    University  VARCHAR(150),
    PhoneNum    VARCHAR(20),
    Birthdate   DATE,
    Age         INT,
    Verification BOOLEAN DEFAULT TRUE,
    TermsAndConditions TEXT,
    ModeratorID INT UNSIGNED,
    AnalystID INT UNSIGNED,
    PRIMARY KEY (BuyerID),
    CONSTRAINT fk_buyer_moderator
        FOREIGN KEY (ModeratorID) REFERENCES Moderator(ModeratorID),
    CONSTRAINT fk_analyst1
        FOREIGN KEY (AnalystID) REFERENCES Analyst(AnalystID)
);

CREATE TABLE IF NOT EXISTS Seller (
    SellerID    INT UNSIGNED AUTO_INCREMENT,
    FirstName   VARCHAR(50) NOT NULL,
    LastName    VARCHAR(50) NOT NULL,
    Email       VARCHAR(255) NOT NULL UNIQUE,
    University  VARCHAR(150),
    PhoneNum    VARCHAR(20),
    Birthdate   DATE,
    Age         INT,
    Verification BOOLEAN DEFAULT TRUE,
    TermsAndConditions TEXT,
    Rating      DECIMAL(3,2),
    ModeratorID INT UNSIGNED,
    AnalystID INT UNSIGNED,
    PRIMARY KEY (SellerID),
    CONSTRAINT fk_seller_moderator
        FOREIGN KEY (ModeratorID) REFERENCES Moderator(ModeratorID),
    CONSTRAINT fk_analyst2
        FOREIGN KEY (AnalystID) REFERENCES Analyst(AnalystID)
);

CREATE TABLE IF NOT EXISTS PaymentMethod (
    PaymentMethodID  INT UNSIGNED AUTO_INCREMENT,
    BuyerID          INT UNSIGNED NOT NULL,
    FirstName        VARCHAR(50),
    LastName         VARCHAR(50),
    CardNum          VARCHAR(20) NOT NULL,
    ExpDate          DATE NOT NULL,
    CVV              VARCHAR(4) NOT NULL,
    Street           VARCHAR(100),
    City             VARCHAR(100),
    State            VARCHAR(50),
    Zip              VARCHAR(10),
    PRIMARY KEY (PaymentMethodID),
    CONSTRAINT fk_payment_buyer
        FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID)
);

CREATE TABLE IF NOT EXISTS Orders (
    OrderID       INT UNSIGNED AUTO_INCREMENT,
    BuyerID       INT UNSIGNED NOT NULL,
    OrderDate     DATE NOT NULL,
    PickupStreet  VARCHAR(100),
    PickupCity    VARCHAR(100),
    PickupState   VARCHAR(50),
    PickupZip     VARCHAR(10),
    PRIMARY KEY (OrderID),
    CONSTRAINT fk_orders_buyer
        FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID)
);


CREATE TABLE IF NOT EXISTS Product (
    ProductID    INT UNSIGNED AUTO_INCREMENT,
    SellerID     INT UNSIGNED NOT NULL,
    Name         VARCHAR(200) NOT NULL,
    Description  TEXT,
    Category     VARCHAR(100),
    `Condition`  VARCHAR(50),
    Status       VARCHAR(50),
    Price        DECIMAL(10,2),
    PostedDate   DATE,
    SoldDate     DATE,
    Views        INT DEFAULT 0,
    Saves        INT DEFAULT 0,
    Verified     BOOLEAN DEFAULT TRUE,
    OrderID      INT UNSIGNED,
    ModeratorID  INT UNSIGNED,
    AnalystID    INT UNSIGNED,
    PRIMARY KEY (ProductID),
    CONSTRAINT fk_product_seller
        FOREIGN KEY (SellerID) REFERENCES Seller(SellerID),
    CONSTRAINT fk_product_order
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    CONSTRAINT fk_product_moderator
        FOREIGN KEY (ModeratorID) REFERENCES Moderator(ModeratorID),
    CONSTRAINT fk_analyst3
        FOREIGN KEY (AnalystID) REFERENCES Analyst(AnalystID)
);

CREATE TABLE IF NOT EXISTS ProductPhoto (
    PhotoID    INT UNSIGNED AUTO_INCREMENT,
    ProductID  INT UNSIGNED NOT NULL,
    PhotoURL   VARCHAR(255) NOT NULL,
    PRIMARY KEY (PhotoID),
    CONSTRAINT fk_photo_product
        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ProductTag (
    ProductTagID  INT UNSIGNED AUTO_INCREMENT,
    Title         VARCHAR(100) NOT NULL,
    PRIMARY KEY (ProductTagID)
);

CREATE TABLE IF NOT EXISTS TagsOfProduct (
    ProductID     INT UNSIGNED NOT NULL,
    ProductTagID  INT UNSIGNED NOT NULL,
    PRIMARY KEY (ProductID, ProductTagID),
    CONSTRAINT fk_top_product
        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
        ON DELETE CASCADE,
    CONSTRAINT fk_top_tag
        FOREIGN KEY (ProductTagID) REFERENCES ProductTag(ProductTagID)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS BankAccount (
    BankID         INT UNSIGNED AUTO_INCREMENT,
    SellerID       INT UNSIGNED NOT NULL,
    FirstName      VARCHAR(50),
    LastName       VARCHAR(50),
    BankName       VARCHAR(100),
    AccountNumber  VARCHAR(30),
    RoutingNumber  VARCHAR(30),
    AccountType    VARCHAR(30),
    PRIMARY KEY (BankID),
    CONSTRAINT fk_bank_seller
        FOREIGN KEY (SellerID) REFERENCES Seller(SellerID)
);

CREATE TABLE IF NOT EXISTS Messages (
    ConvoID         INT UNSIGNED NOT NULL,
    BuyerID         INT UNSIGNED,
    ModeratorID     INT UNSIGNED,
    SellerID        INT UNSIGNED,
    ConvoStartDate  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Body            TEXT,
    Alerts          BOOLEAN DEFAULT FALSE,
    Reported        BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (ConvoID),
    CONSTRAINT fk_msg_buyer
        FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID),
    CONSTRAINT fk_msg_seller
        FOREIGN KEY (SellerID) REFERENCES Seller(SellerID),
    CONSTRAINT fk_msg_moderator
        FOREIGN KEY (ModeratorID) REFERENCES Moderator(ModeratorID)
);

CREATE TABLE IF NOT EXISTS History (
    HistoryID       INT UNSIGNED AUTO_INCREMENT,
    BuyerID         INT UNSIGNED NOT NULL,
    Searches        TEXT,
    ProductsViewed  TEXT,
    PRIMARY KEY (HistoryID),
    CONSTRAINT fk_history_buyer
        FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID)
);

CREATE TABLE IF NOT EXISTS AnalystProductAnalysis (
    AnalystID      INT UNSIGNED NOT NULL,
    ProductID      INT UNSIGNED NOT NULL,
    Revenue        DECIMAL(12,2),
    PRIMARY KEY (AnalystID, ProductID),
    CONSTRAINT fk_aprod_analyst
        FOREIGN KEY (AnalystID) REFERENCES Analyst(AnalystID),
    CONSTRAINT fk_aprod_product
        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);


INSERT INTO Buyer (FirstName, LastName, Email, University, PhoneNum, Birthdate, Age, Verification, TermsAndConditions) 
VALUES ('Serena', 'Williams', 'serenawilliams@gmail.com', 'UCLA', '323-582-1944', '1981-09-26', 44, TRUE, 'Don’t send any personal information.'),
('Simone', 'Biles', 'simonebiles@gmail.com', 'USC', '409-772-6618', '1997-03-14', 28, TRUE, 'Don’t send any personal information.');

INSERT INTO Seller (FirstName, LastName, Email, University, PhoneNum, Birthdate, Age, Verification, TermsAndConditions, Rating) 
VALUES ('Naomi', 'Osaka', 'naomiosaka@gmail.com', 'Stanford University', '206-991-4823', '1997-10-16', 28, TRUE, 'Accepted terms', 4.95),
('Megan', 'Rapinoe', 'meganrapinoe@gmail.com', 'University of Portland', '541-330-7741', '1985-07-05', 40, TRUE, 'Accepted terms', 4.88);

INSERT INTO Moderator (FirstName, LastName, EmailAddress, PhoneNumber, Birthdate, Age) 
VALUES ('Chloe', 'Kim', 'chloekim@gmail.com', '714-993-5508', '2000-04-23', 25),
('Alex', 'Morgan', 'alexmorgan@gmail.com', '619-441-1287', '1989-07-02', 36);

INSERT INTO Analyst (FirstName, LastName, Email, Birthdate, Age) 
VALUES ('Katie', 'Ledecky', 'katieledecky@gmail.com', '1997-03-17', 28),
('Allyson', 'Felix', 'allysonfelix@gmail.com', '1985-11-18', 39);

INSERT INTO PaymentMethod (BuyerID, FirstName, LastName, CardNum, ExpDate, CVV, Street, City, State, Zip) 
VALUES (1, 'Serena', 'Williams', '4929138473621947', '2028-05-01', '392', '613 Ace Court', 'Los Angeles', 'CA', '90032'),
(2, 'Simone', 'Biles', '5249910047338201', '2029-08-01', '847', '147 Victory Way', 'Houston', 'TX', '77021');

INSERT INTO Orders (BuyerID, OrderDate, PickupStreet, PickupCity, PickupState, PickupZip) 
VALUES (1, '2025-11-01', '482 Market St', 'Los Angeles', 'CA', '90007'),
(2, '2025-11-03', '298 Campus Dr', 'Houston', 'TX', '77004');

INSERT INTO Product (SellerID, Name, Description, Category, `Condition`, Status, Price, PostedDate, Views, Saves, Verified) 
VALUES (1, 'Nike Court Tennis Racket', 'Lightweight racket used in training.', 'Sports Equipment', 'Good', 'Available', 120.00, '2025-10-20', 87, 15, TRUE),
(2, 'USA Soccer Warmup Jacket', 'Official team jacket worn during practice.', 'Clothing', 'Like New', 'Available', 85.00, '2025-10-25', 112, 24, TRUE);

INSERT INTO ProductPhoto (ProductID, PhotoURL) 
VALUES (1, 'https://example.com/photos/racket1.jpg'),
(2, 'https://example.com/photos/jacket1.jpg');

INSERT INTO ProductTag (Title) 
VALUES ('Sports'),
('Apparel');

INSERT INTO TagsOfProduct (ProductID, ProductTagID) 
VALUES (1, 1),
(2, 2);

INSERT INTO BankAccount (SellerID, FirstName, LastName, BankName, AccountNumber, RoutingNumber, AccountType) 
VALUES (1, 'Naomi', 'Osaka', 'Chase Bank', '73649281944', '021004298', 'Checking'),
(2, 'Megan', 'Rapinoe', 'Bank of America', '19384755201', '026001742', 'Savings');

INSERT INTO Messages (ConvoID, BuyerID, ModeratorID, SellerID, Body) 
VALUES (1, 1, 1, 1, 'Is the racket still available?'),
(2, 2, 2, 2, 'Can I pick up the jacket tomorrow?');

INSERT INTO History (BuyerID, Searches, ProductsViewed) 
VALUES (1, 'tennis racket; court shoes', '1,3,5'),
(2, 'jackets; athletic wear', '2,4');

INSERT INTO AnalystProductAnalysis (AnalystID, ProductID, Revenue) 
VALUES (1, 1, 120.00),
(2, 2, 85.00);
