-- Create an index idx_name_first_score on the first letter of name and score columns
CREATE INDEX idx_name_first_score ON names (name(1), score);
