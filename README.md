Project Report: Secure Cloud-Based Personal Health Record (PHR) System

1. Introduction
   
The Secure Cloud-Based Personal Health Record (PHR) System is designed to provide users with a centralized platform for securely managing their health information. The system involve agile methodologies, microservices architecture, and emphasizes security and privacy.

To summarize, here are the key steps I've taken:
Docker Setup:
Created a docker-compose.yml file to define  MySQL service.
Used docker-compose up to start the MySQL container.
MySQL Database Setup:
Connected to the MySQL container .
Created a new database (project1) using the CREATE DATABASE command.
Switched to the newly created database using the USE command.
Created tables (users, patients, medical_records, healthcare_providers, appointments) with appropriate columns.
Data Insertion:
Inserted sample data into the patients table.
Addressed issues with missing columns in other tables (healthcare_providers, medical_records, appointments), adding the missing columns and inserting data.
Verification:
Checked the structure of each table using the DESCRIBE command.

