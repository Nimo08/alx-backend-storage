-- Creates a stored procedure ComputeAverageScoreForUser that computes and
-- store the average score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser( IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;
    DECLARE average_score FLOAT;
    
    SELECT SUM(score) , COUNT(project_id)
    INTO total_score, total_projects
    FROM corrections
    WHERE user_id = user_id;

    IF total_projects > 0 THEN
        SET average_score = total_score / total_projects;
    ELSE
        SET average_score = 0;
    END IF;
END;
//

DELIMITER ;
