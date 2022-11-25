DROP TABLE IF EXISTS saberworks_file ;
DROP TABLE IF EXISTS saberworks_screenshot ;
DROP TABLE IF EXISTS saberworks_post ;
DROP TABLE IF EXISTS saberworks_project_tags ;
DROP TABLE IF EXISTS saberworks_project_games ;
DROP TABLE IF EXISTS saberworks_project ;
DROP TABLE IF EXISTS saberworks_tag ;
DROP TABLE IF EXISTS saberworks_tagtype ;
DROP TABLE IF EXISTS saberworks_game ;

DELETE from django_migrations WHERE app = 'saberworks';

