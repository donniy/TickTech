/* Add test courses */
insert or replace into course values ('71d929a86b1311e8adc0fa7ae01bbebc',"project software engineering","this is a test description","mail@mail.com","",1,"");
insert or replace into course values ('51d929a86b1311e8adc0fa7ae01bbebc',"operating systems","this is a test description 2","test@test.com","",1,"");

/* Add test users */
insert or replace into user values (1234,"Erik","ERIK@mail.com");
insert or replace into user values (4321,"Kire","KIRE@mail.com");
insert or replace into user values (5678, "student","student@mail.com");

/* link users to course as ta */
insert or replace into ta_link_course values (1234,'71d929a86b1311e8adc0fa7ae01bbebc');
insert or replace into ta_link_course values (1234,'51d929a86b1311e8adc0fa7ae01bbebc');
insert or replace into ta_link_course values (4321,'71d929a86b1311e8adc0fa7ae01bbebc');

/* Create ticket statuses */
insert or replace into ticket_status values (1,'Unassigned');
insert or replace into ticket_status values (3,'Assigned');
insert or replace into ticket_status values (4,'Receiving help');
insert or replace into ticket_status values (2,'Closed');

/* Create tickets */
insert or replace into ticket values ('126b261c6d7011e8adc0fa7ae01bbebc',5678,'71d929a86b1311e8adc0fa7ae01bbebc',1,'pieter@test.nl','ticketnaam','2018-06-11 13:25:05');
insert or replace into ticket values ('326b261c6d7011e8adc0fa7ae01bbebc',5678,'71d929a86b1311e8adc0fa7ae01bbebc',2,'pieter2@test.nl','ticketnaam2','2018-06-11 13:25:06');
insert or replace into ticket values ('526b261c6d7011e8adc0fa7ae01bbebc',4321,'71d929a86b1311e8adc0fa7ae01bbebc',3,'pieter3@test.nl','ticketnaam3','2018-06-11 13:25:02');

/* link ta's to a ticket */
insert or replace into ta_tracker values ('126b261c6d7011e8adc0fa7ae01bbebc',1234);
insert or replace into ta_tracker values ('326b261c6d7011e8adc0fa7ae01bbebc',1234);

insert or replace into label values ('fa1b7b20307e4250b59c6d0811315203','testlabel');

insert or replace into label_link_course values ('71d929a86b1311e8adc0fa7ae01bbebc','fa1b7b20307e4250b59c6d0811315203');
insert or replace into label_link_course values ('51d929a86b1311e8adc0fa7ae01bbebc','fa1b7b20307e4250b59c6d0811315203');

