-- Create the procedure ComputeAverageWeightedScoreForUsers
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE avg_score FLOAT;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SELECT SUM(c.score * p.weight) / SUM(p.weight)
        INTO avg_score
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        UPDATE users SET average_score = avg_score WHERE id = user_id;
    END LOOP;

    CLOSE cur;
END;
//
DELIMITER ;
