CREATE VIEW gm_openings AS 
SELECT move_1, move_2, move_3, move_4, move_5,COUNT(datetime)
FROM gm_games2
GROUP BY move_1, move_2, move_3, move_4, move_5,ending;

SELECT * from encyclopedia_chess_openings;

CREATE VIEW opponent_openings AS 
SELECT move_1, move_2, move_3, move_4, move_5,COUNT(datetime)
FROM opponents_games
GROUP BY move_1, move_2, move_3, move_4, move_5
ORDER BY COUNT(datetime) DESC;
SELECT * FROM my_gamesgm_games2;

CREATE VIEW gm_theory AS
SELECT gm.civil_name, AVG(e.theoretical_moves)
FROM grand_masters gm
JOIN gm_games2 gmg ON gm.id = gmg.player_id
JOIN encyclopedia_chess_openings e ON gmg.ECO = e.eco
GROUP BY gm.civil_name;