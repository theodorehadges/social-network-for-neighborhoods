-- create tables
create table neighborhood(id serial primary key, name varchar);
create table block(id serial primary key , name varchar, neighborhood_id int references neighborhood(id));
create table userm(id serial primary key , name varchar, email varchar, street varchar, city varchar, state char(2), zipcode int,
description varchar, photo varchar, lat float, lon float, block_id int references block(id), created_on timestamp);
create table friend(id serial primary key , user_1_id int references userm(id), user_2_id int references userm(id),
created_on timestamp);
--this one is weird
create table block_apply(id serial primary key , pending_user int references userm(id), need_approval_by int references userm(id),
given_approval bool, created_on timestamp, decided_on timestamp);
create table block_user(id serial primary key, block_id int references block(id), user_id int references userm(id));
create table neighbor(id serial primary key , user_1_id int references userm(id), user_2_id int references userm(id));
create table thread(id serial primary key , name varchar, created_on timestamp);
create table thread_message(id serial primary key , thread_id int references thread(id), author int references userm(id),
created_time timestamp, title varchar, body varchar, lat float, lon float);
create table thread_friend(id serial primary key, thread_id int references thread(id),friend_id int references friend(id));
create table thread_neighbor(id serial primary key, thread_id int references thread(id), neighbor_id int references neighbor(id));
create table thread_block(id serial primary key, thread_id int references thread(id), block_id int references block(id));
create table thread_neighborhood(id serial primary key, thread_id int references thread(id), neighborhood_id int references neighborhood(id));


