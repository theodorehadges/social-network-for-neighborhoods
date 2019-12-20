

--neighborhood
insert into neighborhood(name) values('upper west side');
insert into neighborhood(name) values('long island city');


--block
insert into block(name, neighborhood_id) values('west 75th st between columbus ave and central park west', 1);
insert into block(name, neighborhood_id) values('queens blvd between 38th st and 39th st', 2);
insert into block(name, neighborhood_id) values('west 81st st between columbus ave and amsterdam ave', 1);


-- register
insert into userm(firstname, lastname, email, street, city, state, zipcode, description, photo, lat, long, block_id, created_on)
    values('elaine', 'benes', 'eb@pendantpublishing.com', '16 west 75th street apt 2g', 'new york', 'ny', 10023,
           'I once broke up with someone for not offering me pie.',
           '/all/photos/elaine.png', 40.778854, -73.973874, 1, now());
insert into userm(firstname, lastname, email, street, city, state, zipcode, description, photo, lat, long, block_id, created_on)
    values('george', 'costanza', 'gcostanza@vandeleyindustries.com', '1344 queens blvd', 'queens', 'ny', 11101,
       'I am George and I love living in Queens since I am close to my parents, Frank and Estelle.',
       '/all/photos/george.png', 40.744303, -73.926108, 2, now());
insert into userm(firstname, lastname, email, street, city, state, zipcode, description, lat, long, created_on) -- no photo/block_id
    values('art', 'vandeley', 'artvandaley@vandeleyindustries.com', '129 w 81st street 5a', 'new york', 'ny', 10024,
           'Here at Vandeley Industries we sell and manufacture latex and latex related products.',
           40.784045, -73.974923, now());
insert into userm(firstname, lastname, email, street, city, state, zipcode, description, photo, lat, long, block_id, created_on)
    values('jerry', 'seinfeld', 'jsein@nofaxmachine.com', '129 w 81st street 5a', 'new york', 'ny', 10024,
           'Why do they call it Ovaltine? The mug is round. The jar is round. ' ||
           'They should call it Roundtine!',
           '/all/photos/jerry.png', 40.784045, -73.974923, 3, now());
insert into userm(firstname, lastname, email, street, city, state, zipcode, description, photo, lat, long, block_id, created_on)
    values('cosmo', 'kramer', 'kramer@kramericaindustries.com', '129 w 81st street 5b', 'new york', 'ny', 10024,
           'It''s like a sauna in here.',
           '/all/photos/kramer.png', 40.784045, -73.974923, 3, now());
insert into userm(lastname, email, street, city, state, zipcode, description, photo, lat, long, block_id, created_on)
    values('newman', 'newman@postoffice.gov', '129 w 81st street 5e', 'new york', 'ny', 10024,
           'Hello Jerry.',
           '/all/photos/newman.png', 40.784045, -73.974923, 3, now());


select * from userm;

-- apply for block: Newman wants to apply for block.
-- Since only 2 others live on block, all block members (Jerry and Kramer) have to approve
insert into block_apply(pending_user, need_approval_by, given_approval, created_on, decided_on)
    values(6,4,NULL, now(), NULL); -- Jerry needs to approve
insert into block_apply(pending_user, need_approval_by, given_approval, created_on, decided_on)
    values(6,5,NULL, now(), NULL); -- Kramer needs to approve

select * from block_apply;


create table thread(id serial primary key , name varchar, created_on timestamp);
create table thread_message(id serial primary key , thread_id int references thread(id), author int references userm(id),
created_time timestamp, title varchar, body varchar, lat float, long float);

with rows as (
insert into thread (created_on) VALUES (now()) RETURNING id
)
insert into thread_message(thread_id, author, created_time, title, body, lat, long)
SELECT id, 2,now(), 'Need parking spot', 'I would like a parking spot for 150',
28.439743, 34.48948
from rows;

--need to know the thread_id from the front end when a user replies I will have the thread_id
insert into thread_message(thread_id, author, created_time, title, body, lat, long)
values(1, 3, now(), 'Have parking more expensive', 'I have parking for 200',
28.439743, 34.48948);

select * from thread_message;

--might want to keep friends that have been rejected so they can't spam invites over and over again
insert into friend_request(user_1_id, user_2_id, approved, created_on)
    values(1,6, NULL, now());

select * from friend_request;

--friend is accepted
update friend_request
set approved = True
where friend_request = 1
and user_1_id = 1
and user_2_id = 6;

