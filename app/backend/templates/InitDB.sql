insert into course values ('71d929a8-6b13-11e8-adc0-fa7ae01bbebc',"mail@mail.com","course 1","this is a test description");
insert into course values ('51d929a8-6b13-11e8-adc0-fa7ae01bbebc',"test@test.com","course 2","this is a test description 2");

insert into user values (1234,"Erik","ERIK@mail.com");
insert into user values (4321,"Kire","KIRE@mail.com");

insert into ta_link_course values (1234,'71d929a8-6b13-11e8-adc0-fa7ae01bbebc');
insert into ta_link_course values (1234,'51d929a8-6b13-11e8-adc0-fa7ae01bbebc');
insert into ta_link_course values (4321,'71d929a8-6b13-11e8-adc0-fa7ae01bbebc');

insert into ticket_status values (11,'Unassigned');
insert into ticket_status values (12,'Assigned');
insert into ticket_status values (13,'Receiving help');
insert into ticket_status values (14,'Closed');

insert into ticket values ('126b261c-6d70-11e8-adc0-fa7ae01bbebc',5678,'71d929a8-6b13-11e8-adc0-fa7ae01bbebc',11,'pieter@test.nl','ticketnaam','2018-06-11 13:25:05');
insert into ticket values ('326b261c-6d70-11e8-adc0-fa7ae01bbebc',5678,'71d929a8-6b13-11e8-adc0-fa7ae01bbebc',12,'pieter2@test.nl','ticketnaam2','2018-06-11 13:25:06');
insert into ticket values ('526b261c-6d70-11e8-adc0-fa7ae01bbebc',0000,'71d929a8-6b13-11e8-adc0-fa7ae01bbebc',13,'pieter3@test.nl','ticketnaam3','2018-06-11 13:25:02');
