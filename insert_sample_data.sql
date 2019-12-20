
-----------------------------------------------------------------------------------------
--neighborhood
insert into neighborhood(name) values('upper west side');
insert into neighborhood(name) values('long island city');
-----------------------------------------------------------------------------------------
--block
insert into block(name, neighborhood_id) values('west 75th st between columbus ave and central park west', 1);
insert into block(name, neighborhood_id) values('queens blvd between 38th st and 39th st', 2);
insert into block(name, neighborhood_id) values('west 81st st between columbus ave and amsterdam ave', 1);

-----------------------------------------------------------------------------------------
-- register
insert into userm(username, firstname, lastname, email, description, photo, street, city, state, zipcode, lat, long, block_id, created_on)
    values('elaine','elaine', 'benes', 'eb@pendantpublishing.com',
           'I once broke up with someone for not offering me pie.', 'all/photos/elaine','16 west 75th street apt 2g',
           'new york', 'ny', 10023, 40.778854, -73.973874, 1, now());
insert into userm(username, firstname, lastname, email, description, photo, street, city, state, zipcode, lat, long, block_id, created_on)
    values('george','george', 'costanza', 'gcostanza@vandeleyindustries.com',
           'I am George and I love living in Queens since I am close to my parents, Frank and Estelle.',
           'all/photos/george', '1344 queens blvd',
           'queens', 'ny', 11101,40.744303, -73.926108, 2, now());
insert into userm(username, firstname, lastname, email, description, street, city, state, zipcode, lat, long, created_on) -- no photo/block_id
    values('art','art', 'vandeley', 'artvandaley@vandeleyindustries.com',
           'Here at Vandeley Industries we sell and manufacture latex and latex related products.',
           '129 w 81st street 5a', 'new york', 'ny', 10024,
           40.784045, -73.974923, now());
insert into userm(username, firstname, lastname, email, description, photo, street, city, state, zipcode, lat, long, block_id, created_on)
    values('jerry','jerry', 'seinfeld', 'jsein@nofaxmachine.com',
           'Why do they call it Ovaltine? The mug is round. The jar is round.' ||
           'They should call it Roundtine!', 'all/photos/jerry', '129 w 81st street 5a',
           'new york', 'ny', 10024, 40.784045, -73.974923, 3, now());
insert into userm(username, firstname, lastname, email, description, photo, street, city, state, zipcode, lat, long, block_id, created_on)
    values('cosmo','cosmo', 'kramer', 'kramer@kramericaindustries.com',
           'It''s like a sauna in here.', 'all/photos/kramer', '129 w 81st street 5b',
           'new york', 'ny', 10024, 40.784045, -73.974923, 3, now());
insert into userm(username, lastname, email, description, photo, street, city, state, zipcode, lat, long, block_id, created_on) -- no first name
    values('newman', 'newman', 'newman@postoffice.gov',
           'Hello Jerry.', 'all/photos/newman', '129 w 81st street 5e', 'new york',
           'ny', 10024, 40.784045, -73.974923, 3, now());
-----------------------------------------------------------------------------------------
-- Jerry logs in
insert into user_log(user_id, login_time) values(4, now()); -- Jerry (4) logs in
insert into user_log(user_id, login_time) values(1, now()); -- Elaine (1) logs inn

-----------------------------------------------------------------------------------------
-- insert profile data
--insert into userm(description, photo, user_id)
--    values('I once broke up with someone for not offering me pie.', 'all/photos/elaine', 1);
--insert into userm(description, photo, user_id)
 --   values('I am George and I love living in Queens since I am close to my parents, Frank and Estelle.',
  --         'all/photos/george', 2);
--insert into userm(description, user_id)
 --   values('Here at Vandeley Industries we sell and manufacture latex and latex related products.', 3);
--insert into userm(description, photo, user_id)
 --   values('Why do they call it Ovaltine? The mug is round. The jar is round.' ||
  --         'They should call it Roundtine!', 'all/photos/jerry', 4);

--insert into userm(description, photo, user_id)
 --   values('It''s like a sauna in here.', 'all/photos/kramer', 5);
--insert into userm(description, photo, user_id)
 --   values('Hello Jerry.', 'all/photos/newman', 6);

-----------------------------------------------------------------------------------------
-- populate neighbor table for upper west side neighbors (all users except id=2)
insert into neighbor(user_1_id, user_2_id) values (1, 3);
insert into neighbor(user_1_id, user_2_id) values (1, 4);
insert into neighbor(user_1_id, user_2_id) values (1, 5);
insert into neighbor(user_1_id, user_2_id) values (1, 6);
insert into neighbor(user_1_id, user_2_id) values (3, 4);
insert into neighbor(user_1_id, user_2_id) values (3, 5);
insert into neighbor(user_1_id, user_2_id) values (3, 6);
insert into neighbor(user_1_id, user_2_id) values (4, 5);
insert into neighbor(user_1_id, user_2_id) values (4, 6);



-----------------------------------------------------------------------------------------
--update profile
--set description = 'Well, I saw that it''s raining outside, so I called in sick. I don''t work in the rain.'
--where profile.id = 6;
-----------------------------------------------------------------------------------------
-- Jerry joins block. No other members, so he joins without approval
insert into block_apply(pending_user, block_id, given_approval, created_on, decided_on)
    values(4, 3, True, now(), NULL);

update userm
set block_id = 3
where id = 4;

-----------------------------------------------------------------------------------------
-- Kramer (5) joins block. One other member (4), so need approval by (4)
insert into block_apply(pending_user, block_id, need_approval_by, created_on, decided_on)
    values(5, 3, 4, now(), NULL);

-- Jerry approves Kramer's block request
update block_apply
set given_approval = True
where block_apply.id= 2
and pending_user = 5
and need_approval_by = 4;

update userm
set block_id = 3
where id = 5;
-----------------------------------------------------------------------------------------
-- Newman (6) wants to apply for block. 2 other members (4) and (5) must approve it
-- (same logic would work for three or more members)
insert into block_apply(pending_user, block_id, need_approval_by, given_approval, created_on, decided_on)
    values(6,3, 4,NULL, now(), NULL); -- Jerry needs to approve
insert into block_apply(pending_user, block_id, need_approval_by, given_approval, created_on, decided_on)
    values(6, 3,5,NULL, now(), NULL); -- Kramer needs to approve

-- Jerry approves Newman's block request
update block_apply
set given_approval = True
where block_apply.id= 3
and pending_user = 6
and need_approval_by = 4;

-- Kramer approves Newman's block request
update block_apply
set given_approval = True
where block_apply.id= 4
and pending_user = 6
and need_approval_by = 5;

--when block request is approved simply update the userm table
update userm
    set block_id = 3
where id = 6;
-----------------------------------------------------------------------------------------
-- FRIENDS
--might want to keep friends that have been rejected so they can't spam invites over and over again
-----------------------------------------------------------------------------------------
-- Elaine (1) sends friend request to Newman (6)
insert into friend_request(user_1_id, user_2_id, approved, created_on)
values(1,6, NULL, now());

-- Newman accepts friend request
update friend_request
set approved = True
where friend_request.id= 1
and user_1_id = 1
and user_2_id = 6;

--when friend is accepts a request simply add it to friend table
insert into friend(user_1_id, user_2_id, created_on)
values(1,6,now());

-----------------------------------------------------------------------------------------
-- Kramer (5) sends friend request to Jerry (4)
insert into friend_request(user_1_id, user_2_id, approved, created_on)
values(5,4, NULL, now());
-- question: should we allow new rows if a user makes a request that is pending?

--Jerry accepts friend request
update friend_request
set approved = True
where friend_request.id= 2
and user_1_id = 5
and user_2_id = 4;

--when friend is accepts a request simply add it to friend table
insert into friend(user_1_id, user_2_id, created_on)
values(5,4,now());
-----------------------------------------------------------------------------------------
-- George (2) sends friend request to Jerry (4)
insert into friend_request(user_1_id, user_2_id, approved, created_on)
values(2,4, NULL, now());

-- Jerry accepts friend request
update friend_request
set approved = True
where friend_request.id= 1
and user_1_id = 2
and user_2_id = 4;

--when friend is accepts a request simply add it to friend table
insert into friend(user_1_id, user_2_id, created_on)
values(2,4,now());

-----------------------------------------------------------------------------------------
-- create a new thread with a message, then have a different person write a new message in that thread

-- George creates a thread called 'Need parking spot'
-- visible to friends
with rows as (
insert into thread (created_on) VALUES (now()) RETURNING id
)
insert into thread_message(thread_id, author, created_time, title, body, lat, long)
SELECT id, 2,now(), 'Need parking spot', 'I would like a parking spot for 150',
28.439743, 34.48948
from rows;

-- make thread (1) visible to George's (2) friends (only has one friend: row in friends with friend_id = 3)
insert into thread_friend(thread_id, friend_id) values (1, 3);

-- need to add to messages_read for each friend so that we can keep track of whether they read it
-- George (2) only has one friend, Jerry (4), so we only need to do one insert. (One insert per friend.)
insert into message_read(message_id, user_id, read) values (1, 4, FALSE);

-----------------------------------------------------------------------------------------
-- Jerry replies to George's message
insert into thread_message(thread_id, author, created_time, in_reply_to_message_id, title, body, lat, long)
values(1, 3, now(), 1,'Have parking more expensive',
       'I have parking for 200',28.439743, 34.48948);


-----------------------------------------------------------------------------------------
-- Newman (6) creates a thread called 'Caution: chinese food delivery person rides bike on sidewalk'
with rows as (
insert into thread (created_on) VALUES (now()) RETURNING id
)
insert into thread_message(thread_id, author, created_time, title, body, lat, long)
SELECT id, 6,now(), 'Caution: chinese food delivery person rides bike on sidewalk',
                'I almost got run over today as I was walking to my apartment. The delivery person zoomed' ||
                    ' by on his way to deliver food to my neighbor. This behavior is causing all sorts of ' ||
                    'bicycle accidents in the neighborhood. Later that day, I ordered Chinese food.', 28.439743, 34.48948
from rows;

-- Newman's new thread is viewable by the block on which he resides (3)
insert into thread_block(thread_id, block_id) values (2, 3);

-----------------------------------------------------------------------------------------
-- Jerry creates a thread called 'what's the deal with bicycle accidents?'
-- He chooses visibility: block and friends
with rows as (
insert into thread (created_on) VALUES (now()) RETURNING id
)
insert into thread_message(thread_id, author, created_time, title, body, lat, long)
SELECT id, 4,now(), 'What''s the deal with bicycle accidents?',
                'Seems like they''ve been happening a lot lately', 28.439743, 34.48948
from rows;

insert into thread_block(thread_id, block_id) values (3, 3);
-- Jerry's new thread is viewable by friends
-- for each row in Friends where Jerry (4) is present, insert the friend_id for that row
insert into thread_friend(thread_id, friend_id) values (3, 2);
insert into thread_friend(thread_id, friend_id) values (3, 3);

-----------------------------------------------------------------------------------------
-- Since Jerry posted this message after Kramer's most recent login time, Kramer has not yet seen it
insert into message_read(message_id, user_id, read) values (1, 4, FALSE);



insert into neighborhood(name)
values('williamsbug'),
       ('midtown'),
       ('upper east side'),
       ('long island city'),
       ('mainville'),
       ('hotchiks');

insert into block(name, neighborhood_id)
values('block11', 1),
       ('block21', 1),
       ('block31', 1),
       ('block12', 2),
       ('block22', 2),
       ('block32', 2),
       ('block13', 3),
       ('block23', 3),
       ('block33', 3),
       ('block14', 4),
       ('block24', 4),
       ('block34', 4),
       ('block15', 5),
       ('block25', 5),
       ('block35', 5),
       ('block16', 6),
       ('block26', 6),
       ('block36', 6),
       ('block17', 7),
       ('block27', 7),
       ('block37', 7);