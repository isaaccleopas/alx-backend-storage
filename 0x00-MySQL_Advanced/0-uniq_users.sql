-- Create user table if it doesn't exist
-- With id, email and name
CREATE TABLE IF NOT EXISTS users (
	    id INT AUTO_INCREMENT PRIMARY KEY,
	    email VARCHAR(255) NOT NULL UNIQUE,
	    name VARCHAR(255)
	);
