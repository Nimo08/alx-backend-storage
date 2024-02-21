-- Creates an index idx_name_first_score on the table names and
-- the first letter of name and the score.

ALTER TABLE names
ADD first_char CHAR(1) AS (LEFT(name, 1)),
ADD first_num CHAR(1) AS (LEFT(CAST(score AS CHAR), 1));

CREATE INDEX idx_name_first_score ON names(first_char, first_num);
