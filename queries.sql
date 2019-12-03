--neighborhood
insert into neighborhood(name)
values('midtown');

--block
insert into block(name, neighborhood_id)
values('37th and 10th', 1);

--register
insert into userm(firstname, lastname, email, street, city, state, zipcode, description, photo, lat, long, block_id, created_on)
values('Gregory', 'Livschitz', 'someemail@gmail.com', '123 main street', 'New York', 'NY', 10018, 'Life is tough',
'/all/photos/greg.png', 28.2929, 23.379732, 1, now());

--edit profile
update profile
set description = 'my new description'
where profile.user_id = 2;

--apply for block
insert into block_apply(pending_user, need_approval_by, given_approval, created_on, decided_on)
values(1,3,NULL, now(), NULL);
insert into block_apply(pending_user, need_approval_by, given_approval, created_on, decided_on)
values(1,4,NULL, now(), NULL);
insert into block_apply(pending_user, need_approval_by, given_approval, created_on, decided_on)
values(1,5,NULL, now(), NULL);

--create first message
with rows as (
insert into thread (created_on) VALUES (now()) RETURNING id
)
insert into thread_message(thread_id, author, created_time, title, body, lat, long)
SELECT id, 2,now(), 'Need parking spot', 'I would like a parking spot for 150',
28.439743, 34.48948
from rows;

--need to know the thread_id from the front end when a user replies I will have the thread_id
insert into thread_message(thread_id, author, created_time, title, body, lat, long, in_reply_to_message_id)
values(1, 3, now(), 'Have parking more expensive', 'I have parking for 200',
28.439743, 34.48948, 2);

--might want to keep friends that have been rejected so they can't spam invites over and over again, thats why it's insert null vs false
--friend request
insert into friend_request(user_1_id, user_2_id, approved, created_on)
values(1,6, NULL, now());

--one reason to do this is to keep --friend is accepted
update friend_request
set approved = True
where friend_request = 1
and user_1_id = 1
and user_2_id = 6;

--when friend is accepts a request simply add it to friend table
insert into friend(user_1_id, user_2_id, created_on)
values(1,6,now());

--find all friends and neighbors, assumes I'm id 1.
--I am looking for all users with id 1
--logic if user_1_id is 1 then make it null and select user_2_id
--if user_1_id is not 1 then it is the correct one and user_2_id is actually 1.
(select coalesce(nullif(user_1_id, 1), user_2_id) as friend_id
from friend
where user_1_id = 1
or user_2_id = 1)
union
(select coalesce(nullif(user_1_id, 1), user_2_id) as friend_id
from neighbor
where user_1_id = 1
or user_2_id = 1);


--all threads in block feed that have new messages since last time logged on
select distinct tb.thread_id
from userm u inner join thread_block tb on u.block_id = tb.block_id
inner join thread_message tm on tm.thread_id =tb.thread_id
where u.id = 2
and tm.created_time > (select max(login_time) from user_log where user_id = 2);

--all threads in friend feed that have not been read.
select distinct tf.thread_id
from userm u inner join friend f on u.id = f.user_1_id or u.id = f.user_2_id
inner join thread_friend tf on f.id = tf.friend_id
inner join thread_message tm on tf.thread_id = tm.thread_id
inner join message_read mr on u.id = mr.user_id and tm.id = mr.message_id
where u.id = 2
and mr.read = False;

--all messages containing word bicycle accident accross all feeds
--friend
(select tm.id, tm.title, tm.body
from userm u inner join friend f on u.id = f.user_1_id or u.id = f.user_2_id
inner join thread_friend tf on f.id = tf.friend_id
inner join thread_message tm on tf.thread_id = tm.thread_id
where u.id = 5
and (tm.body ilike '%bicycle accident%'
or tm.title ilike '%bicycle accident%'))
union
--neighbor
(select tm.id, tm.title, tm.body
from userm u inner join neighbor n on u.id = n.user_1_id or u.id = n.user_2_id
inner join thread_friend tf on n.id = tf.friend_id
inner join thread_message tm on tf.thread_id = tm.thread_id
where u.id = 5
and (tm.body ilike '%bicycle accident%'
or tm.title ilike '%bicycle accident%'))
union
--neighborhood
(select tm.id, tm.title, tm.body
from userm u inner join block b on u.block_id = b.id
inner join neighborhood nh on b.neighborhood_id = nh.id
inner join thread_neighborhood tnh on nh.id = tnh.neighborhood_id
inner join thread_message tm on tm.thread_id =tnh.thread_id
where u.id = 5
and (tm.body ilike '%bicycle accident%'
or tm.title ilike '%bicycle accident%'))
union
--block
(select tm.id, tm.title, tm.body
from userm u inner join thread_block tb on u.block_id = tb.block_id
inner join thread_message tm on tm.thread_id =tb.thread_id
where u.id = 5
and (tm.body ilike '%bicycle accident%'
or tm.title ilike '%bicycle accident%'))