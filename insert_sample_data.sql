

--neighborhood
insert into neighborhood(name) values('upper west side');
insert into neighborhood(name) values('long island city');


--block
insert into block(name, neighborhood_id) values('west 75th st between columbus ave and central park west', 1);
insert into block(name, neighborhood_id) values('queens blvd between 38th st and 39th st', 2);
insert into block(name, neighborhood_id) values('west 81st st between columbus ave and amsterdam ave', 1);


-- register
insert into userm(name, email, street, city, state, zipcode, description, photo, lat, lon, block_id, created_on)
    values('elaine benes', 'eb@pendantpublishing.com', '16 west 75th street apt 2g', 'new york', 'ny', 10023,
           'I once broke up with someone for not offering me pie.',
           '/all/photos/elaine.png', 40.778854, -73.973874, 1, now());
insert into userm(name, email, street, city, state, zipcode, description, photo, lat, lon, block_id, created_on)
    values('george costanza', 'gcostanza@vandeleyindustries.com', '1344 queens blvd', 'queens', 'ny', 11101,
       'I am George and I love living in Queens since I am close to my parents, Frank and Estelle.',
       '/all/photos/george.png', 40.744303, -73.926108, 2, now());
insert into userm(name, email, street, city, state, zipcode, description, lat, lon, created_on) -- no photo/block_id
    values('art vandeley', 'artvandaley@vandeleyindustries.com', '129 w 81st street 5a', 'new york', 'ny', 10024,
           'Here at Vandeley Industries we sell and manufacture latex and latex related products.',
           40.784045, -73.974923, now());
insert into userm(name, email, street, city, state, zipcode, description, photo, lat, lon, block_id, created_on)
    values('jerry seinfeld', 'jsein@nofaxmachine.com', '129 w 81st street 5a', 'new york', 'ny', 10024,
           'Why do they call it Ovaltine? The mug is round. The jar is round. ' ||
           'They should call it Roundtine!',
           '/all/photos/jerry.png', 40.784045, -73.974923, 3, now());
insert into userm(name, email, street, city, state, zipcode, description, photo, lat, lon, block_id, created_on)
    values('cosmo kramer', 'kramer@kramericaindustries.com', '129 w 81st street 5b', 'new york', 'ny', 10024,
           'It''s like a sauna in here.',
           '/all/photos/kramer.png', 40.784045, -73.974923, 3, now());

