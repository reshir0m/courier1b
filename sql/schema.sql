CREATE TABLE blocked_terms (
    term_id  INT IDENTITY(1,1) PRIMARY KEY,
    term     NVARCHAR(100) NOT NULL UNIQUE,
    category NVARCHAR(50) NULL
);
GO
INSERT INTO blocked_terms (term, category) VALUES ('badword1', 'test');
GO