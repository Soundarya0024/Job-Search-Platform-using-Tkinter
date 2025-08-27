DROP DATABASE job_db; 
CREATE DATABASE job_db;
USE job_db;
CREATE TABLE Admin_table( job_id INT,job_name VARCHAR(100), location VARCHAR(100), roles VARCHAR(50),job_description VARCHAR(100),company VARCHAR(100)); 
INSERT INTO Admin_table (job_id, job_name, location, roles, job_description, company)
VALUES (1, 'Python Developer', 'Chennai', 'Developer', '2+ yrs exp needed', 'Infosys');
INSERT INTO Admin_table (job_id, job_name, location, roles, job_description, company)
VALUES (2, 'Data Analyst', 'Bangalore', 'Analyst', 'Must have knowledge in SQL & Excel', 'TCS');
INSERT INTO Admin_table (job_id, job_name, location, roles, job_description, company)
VALUES (3, 'AI Engineer', 'Coimbatore', 'AI Engineer', 'Experience with ML models & Python', 'Wipro');
SELECT * FROM Admin_table;
CREATE TABLE User_table(email_id VARCHAR(50),Upload_resume VARCHAR(255),user_name VARCHAR(100),experience INT,phone_no BIGINT);
INSERT INTO User_table (user_name, email_id, experience, phone_no, upload_resume)
VALUES ('Soundarya', 'abc@gmail.com', '2', '9876543210', 'resumes/abc.pdf');
SELECT * FROM User_table;