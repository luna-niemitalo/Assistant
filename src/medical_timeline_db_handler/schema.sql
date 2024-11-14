CREATE TABLE Users (
                       user_id INT PRIMARY KEY AUTO_INCREMENT,
                       username VARCHAR(50) UNIQUE NOT NULL,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE Events (
                        event_id INT PRIMARY KEY AUTO_INCREMENT,
                        user_id INT NOT NULL,
                        title VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        event_type ENUM('at', 'around', 'between') NOT NULL,
                        timestamp TIMESTAMP NULL,              -- Central or specific timestamp for 'at' or 'around' events
                        falloff_range INT DEFAULT 120,                -- Range in minutes around timestamp for 'around' events
                        start_timestamp TIMESTAMP NULL,        -- Start timestamp for 'between' events
                        end_timestamp TIMESTAMP NULL,          -- End timestamp for 'between' events
                        notes TEXT,
                        severity FLOAT CHECK (severity >= 0.0 AND severity <= 10.0),  -- Severity score from 1 to 10
                        symptom BOOLEAN DEFAULT FALSE,              -- TRUE for symptom, FALSE for status
                        category VARCHAR(50),                  -- Flexible text-based category

                        FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

ALTER TABLE Events add (
    severity FLOAT CHECK (severity >= 0.0 AND severity <= 10.0),  -- Severity score from 1 to 10
    symptom BOOLEAN DEFAULT FALSE,              -- TRUE for symptom, FALSE for status
    category VARCHAR(50)                  -- Flexible text-based category
    );