-- Check if project_name exists, create if not
-- Insert the new correction
-- Update average_score for the user
DELIMITER //
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    DECLARE project_id INT;
    SELECT id INTO project_id FROM projects WHERE name = project_name;
    
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
    UPDATE users SET average_score = (
        SELECT AVG(score)
        FROM corrections
        WHERE user_id = user_id
    ) WHERE id = user_id;
END;
//
DELIMITER ;
