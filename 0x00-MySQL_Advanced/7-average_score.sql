-- Creates a stored procedure ComputeAverageScoreForUser that computes and
-- store the average score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser( IN user_id INT)
BEGIN
    DECLARE average_score FLOAT;
    
    SELECT AVG(score) INTO average_score
    FROM corrections
    WHERE user_id = user_id;

END;
//

DELIMITER ;
