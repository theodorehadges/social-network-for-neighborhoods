drop table if exists user_log;
drop table if exists message_read;
drop table if exists thread_neighborhood;
drop table if exists thread_block;
drop table if exists thread_neighbor;
drop table if exists thread_friend;
drop table if exists thread_message;
drop table if exists thread;
drop table if exists neighbor;
drop table if exists block_user;
drop table if exists block_apply;
drop table if exists friend;
drop table if exists friend_request;
drop table if exists profile;
drop table if exists userm;
drop table if exists block;
drop table if exists neighborhood;

create table neighborhood(id serial primary key, name varchar);
create table block(id serial primary key , name varchar, neighborhood_id int references neighborhood(id) not null);
create table userm(id serial primary key , username varchar, password bytea, firstname varchar, lastname varchar, email varchar, street varchar,
    city varchar, state char(2), zipcode int, lat float, long float, block_id int references block(id), created_on timestamp);
create table profile(id serial primary key, description varchar, photo varchar,
    user_id int references userm(id) unique not null, updated_on timestamp);
create table friend(id serial primary key , user_1_id int references userm(id) not null,
    user_2_id int references userm(id) not null, unique (user_1_id, user_2_id), created_on timestamp);
create table friend_request(id serial primary key , user_1_id int references userm(id) not null,
    user_2_id int references userm(id) not null, approved bool, created_on timestamp);
--create table block_apply(id serial primary key , pending_user int references userm(id) not null,
--   need_approval_by int references userm(id) not null, given_approval bool, block_id int references block(id) not null,
--  created_on timestamp, decided_on timestamp);
create table block_apply(id serial primary key , pending_user int references userm(id) not null,
    need_approval_by int references userm(id), given_approval bool, block_id int references block(id) not null,
    created_on timestamp, decided_on timestamp);
create table neighbor(id serial primary key, user_1_id int references userm(id) not null,
    user_2_id int references userm(id) not null);
create table thread(id serial primary key, name varchar, created_on timestamp);
create table thread_message(id serial primary key , thread_id int references thread(id) not null,
    author int references userm(id), created_time timestamp, title varchar, body varchar, lat float, long float,
    in_reply_to_message_id int references thread_message(id));
create table thread_friend(id serial primary key, thread_id int references thread(id) not null,
    friend_id int references friend(id) not null);
create table thread_neighbor(id serial primary key, thread_id int references thread(id) not null,
    neighbor_id int references neighbor(id) not null);
create table thread_block(id serial primary key, thread_id int references thread(id) not null,
    block_id int references block(id) not null);
create table thread_neighborhood(id serial primary key, thread_id int references thread(id) not null,
    neighborhood_id int references neighborhood(id) not null);
create table message_read(id serial primary key, message_id int references thread_message(id) not null,
    user_id int references userm(id) not null, read bool);
create table user_log(id serial primary key, user_id int references userm(id) not null, login_time timestamp);

