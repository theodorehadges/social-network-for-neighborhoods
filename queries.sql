
--find all friends and neighbors, assumes I'm id 4.
--I am looking for all users with id 4
--logic if user_1_id is 4 then make it null and select user_2_id
--if user_1_id is not 4 then it is the correct one and user_2_id is actually 4.
(select coalesce(nullif(user_1_id, 4), user_2_id) as friend_id
from friend
where user_1_id = 4
or user_2_id = 4)
union
(select coalesce(nullif(user_1_id, 4), user_2_id) as friend_id
from neighbor
where user_1_id = 4
or user_2_id = 4);

--all threads in block feed that have new messages since last time logged on
select distinct tb.thread_id
from userm u inner join thread_block tb on u.block_id = tb.block_id
inner join thread_message tm on tm.thread_id =tb.thread_id
where u.id = 4
and tm.created_time > (select max(login_time) from user_log where user_id = 4);

--------------------------------------------------------------------------------
-- CHECKED ALL EXCEPT THIS QUERY. need to add data to thread_friend,
--all threads in friend feed that have not been read.
select distinct tf.thread_id
from userm u inner join friend f on u.id = f.user_1_id or u.id = f.user_2_id
inner join thread_friend tf on f.id = tf.friend_id
inner join thread_message tm on tf.thread_id = tm.thread_id
inner join message_read mr on u.id = mr.user_id and tm.id = mr.message_id
where u.id = 4
and mr.read = False;
-------------------------------------------------------------------------------

--all messages containing word bicycle accident accross all feeds
--friend
(select tm.id, tm.title, tm.body
from userm u inner join friend f on u.id = f.user_1_id or u.id = f.user_2_id
inner join thread_friend tf on f.id = tf.friend_id
inner join thread_message tm on tf.thread_id = tm.thread_id
where u.id = 4
and (tm.body ilike '%bicycle accident%'
or tm.title ilike '%bicycle accident%'))
union
--neighbor
(select tm.id, tm.title, tm.body
from userm u inner join neighbor n on u.id = n.user_1_id or u.id = n.user_2_id
inner join thread_friend tf on n.id = tf.friend_id
inner join thread_message tm on tf.thread_id = tm.thread_id
where u.id = 4
and (tm.body ilike '%bicycle accident%'
or tm.title ilike '%bicycle accident%'))
union
--neighborhood
(select tm.id, tm.title, tm.body
from userm u inner join block b on u.block_id = b.id
inner join neighborhood nh on b.neighborhood_id = nh.id
inner join thread_neighborhood tnh on nh.id = tnh.neighborhood_id
inner join thread_message tm on tm.thread_id =tnh.thread_id
where u.id = 4
and (tm.body ilike '%bicycle accident%'
or tm.title ilike '%bicycle accident%'))
union
--block
(select tm.id, tm.title, tm.body
from userm u inner join thread_block tb on u.block_id = tb.block_id
inner join thread_message tm on tm.thread_id =tb.thread_id
where u.id = 4
and (tm.body ilike '%bicycle accident%'
or tm.title ilike '%bicycle accident%'))