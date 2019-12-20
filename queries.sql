
--find all friends and neighbors, assumes I'm id 4.
--I am looking for all users with id 4
--logic if user_1_id is 4 then make it null and select user_2_id
--if user_1_id is not 4 then it is the correct one and user_2_id is actually 4.
(select coalesce(nullif(user_1_id, 4), user_2_id) as friends_and_neighbors_id
from friend
where user_1_id = 4
or user_2_id = 4)
union
(select coalesce(nullif(user_1_id, 4), user_2_id) as friends_and_neighbors_id
from neighbor
where user_1_id = 4
or user_2_id = 4);

-------------------------------------------------------------------------------
--all threads in block feed that have new messages since last time logged on
select distinct tb.thread_id
from userm u inner join thread_block tb on u.block_id = tb.block_id
inner join thread_message tm on tm.thread_id =tb.thread_id
where u.id = 4
and tm.created_time > (select max(login_time) from user_log where user_id = 4);

-------------------------------------------------------------------------------
--all threads in friend feed that have not been read.
select distinct tf.thread_id
from userm u inner join friend f on u.id = f.user_1_id or u.id = f.user_2_id
inner join thread_friend tf on f.id = tf.friend_id
inner join thread_message tm on tf.thread_id = tm.thread_id
inner join message_read mr on u.id = mr.user_id and tm.id = mr.message_id
where u.id = 4
and mr.read = False;
-------------------------------------------------------------------------------
select * from friend;
select * from thread_message;
--all messages containing word bicycle accident accross all feeds
--friend
(select tm.id, tm.title, tm.body
from userm u inner join friend f on u.id = f.user_1_id or u.id = f.user_2_id
inner join thread_friend tf on f.id = tf.friend_id
inner join thread_message tm on tf.thread_id = tm.thread_id
where u.id = 1
and (tm.body ilike '%msg%'
or tm.title ilike '%msg%'))
union
--neighbor
(select tm.id, tm.title, tm.body
from userm u inner join neighbor n on u.id = n.user_1_id or u.id = n.user_2_id
inner join thread_friend tf on n.id = tf.friend_id
inner join thread_message tm on tf.thread_id = tm.thread_id
where u.id = 1
and (tm.body ilike '%msg%'
or tm.title ilike '%msg%'))
union
--neighborhood
(select tm.id, tm.title, tm.body
from userm u inner join block b on u.block_id = b.id
inner join neighborhood nh on b.neighborhood_id = nh.id
inner join thread_neighborhood tnh on nh.id = tnh.neighborhood_id
inner join thread_message tm on tm.thread_id =tnh.thread_id
where u.id = 1
and (tm.body ilike '%msg%'
or tm.title ilike '%msg%'))
union
--block
(select tm.id, tm.title, tm.body
from userm u inner join thread_block tb on u.block_id = tb.block_id
inner join thread_message tm on tm.thread_id =tb.thread_id
where u.id = 1
and (tm.body ilike '%msg%'
or tm.title ilike '%msg%'))

select * from thread_message;

CREATE OR REPLACE FUNCTION check_friend_request_approval()
RETURNS trigger AS
$BODY$
BEGIN
if new.approved = true THEN
raise notice 'inserting new record friend';
insert into friend(user_1_id, user_2_id, created_on)
values(new.user_1_id, new.user_2_id, now());
end if;
RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql VOLATILE;
CREATE TRIGGER check_update_friend_request
AFTER UPDATE ON friend_request
FOR EACH ROW
EXECUTE PROCEDURE check_friend_request_approval();




CREATE OR REPLACE FUNCTION check_block_approval()
RETURNS trigger AS
$BODY$
DECLARE
count_approvals int;
count_all int;
BEGIN
if new.given_approval = true THEN
select count(*) into count_approvals
from block_apply
where pending_user = new.pending_user
and block_id = new.block_id
and given_approval = true;
select count(*) into count_all
from block_apply
where pending_user = new.pending_user
and block_id = new.block_id;
if (count_approvals >= 3) or (count_approvals = count_all) then
update userm
set block_id = new.block_id
where id = new.pending_user;
end if;
end if;
RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql VOLATILE;
CREATE TRIGGER check_update_block_apply
AFTER UPDATE ON block_apply
FOR EACH ROW
EXECUTE PROCEDURE check_block_approval();
