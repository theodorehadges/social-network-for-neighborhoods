--drop table if exists block;
--drop table if exists neighborhood;

insert into neighborhood(name)
values('williamsbug'),
       ('midtown'),
       ('upper east side'),
       ('long island city'),
       ('mainville'),
       ('hotchiks'),
        ('harlem');

select * from neighborhood;
select * from block;
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
select * from block_apply;

select * from thread_friend;