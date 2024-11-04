DROP TABLE IF EXISTS workouts;
DROP SEQUENCE IF EXISTS user_username;
DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS username;


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username text UNIQUE,
    password text,
    workout_list text[]
);

CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    date text,
    exercise_list jsonb,
    complete boolean,
    user_username text,
    constraint fk_username foreign key(user_username)
    references users(username)
    on delete set null
    on update set default
);

DROP TABLE IF EXISTS Exercise;

CREATE TABLE Exercise (
    id SERIAL PRIMARY KEY,
    name text,
    type text,
    muscle text,
    equipment text,
    difficulty text,
    instructions text
);