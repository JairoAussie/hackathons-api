-- first of all drop the tables, the order matters
drop table tech_stack;
drop table members;
drop table technologies;
drop table projects;

-- Table creation, the order matters
-- start with the tables that don't have foreign keys
create table projects (
    id serial primary key,
    title varchar(50) not null,
    repository varchar(75) not null,
    description text
);

create table technologies (
    id serial primary key,
    name varchar(50) not null,
    category varchar(40) not null,
    description text
);

create table members (
    id serial primary key,
    username varchar(30) not null unique,
    email varchar(50) not null unique,
    role varchar(30) default 'Developer',
    age integer check (age >= 18),
    project_id integer not null,
    foreign key (project_id) references projects (id) on delete cascade
);

create table tech_stack (
    id serial primary key,
    project_id integer not null,
    -- tech_id integer not null REFERENCES technologies(id)
    tech_id integer not null,
    foreign key (project_id) references projects (id) on delete cascade,
    foreign key (tech_id) references technologies (id) on delete cascade
);

-- seed the tables with data

insert into projects (title, repository, description) 
values ('Brisbane Traffic Solver', 'https://github.com/traffic_team/traffic_solver', 'description goes here...');

insert into projects (title, repository) 
values ('Sustainability coding board game', 'https://github.com/ca_team/coding_board_game');

insert into members (username, email, role, age, project_id) 
values ('James', 'james@email.com', 'student', 28, 1);

insert into members (username, email, role, age, project_id) 
values ('Dillon', 'dillon@email.com', 'student', 28, 1);

insert into members (username, email, age, project_id) 
values ('Mark', 'mark@email.com', 24, 2);

insert into members (username, email, age, project_id) 
values ('Theo', 'theo@email.com', 24, 2);

insert into members (username, email, age, project_id) 
values ('Kiran', 'kiran@email.com', 24, 1);