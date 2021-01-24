-- CREATE DATABASE seiseki_information;
CREATE TABLE seiseki (
    subject_name VARCHAR(255) NOT NULL,
    teacher_name VARCHAR(255) NOT NULL,
    subject_classification VARCHAR(255) NOT NULL,
    required_selection_category VARCHAR(255) NOT NULL,
    unit INTEGER NOT NULL,
    evaluation VARCHAR(5) NOT NULL,
    score FLOAT NOT NULL,
    gp FLOAT NOT NULL,
    acquisition_year INTEGER NOT NULL,
    reporting_date DATE NOT NULL
);
