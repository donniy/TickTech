/* Add test courses */
insert or replace into course values ('71d929a86b1311e8adc0fa7ae01bbebc',"Project Software Engineering","this is a test description","uvapsetest@gmail.com","","","");
insert or replace into course values ('51d929a86b1311e8adc0fa7ae01bbebc',"Operating Systems","this is a test description 2","tiktech.noreply@gmail.com","","","");
insert or replace into course values ('31d929a86b1311e8adc0fa7ae01bbebc',"Compiler Construction","this is a test description 3","tiktech.noreply@gmail.com","","","");

-- SET @ta1 = 12345678;
-- SET @ta2 = 87654321;
-- SET @student1 = 10203040;
-- SET @student2 = 50607080;
/* Add test users psw=1*/
insert or replace into user values (12345678,"Erik","erik@a.a", b'$2b$12$1Y21IaNbwu357bI4ipaZO.GVvzouAEvnrAy80TGCBRtX5q8OUlIr2');
insert or replace into user values (87654321,"Kire","kire@a.a", b'$2b$12$1Y21IaNbwu357bI4ipaZO.GVvzouAEvnrAy80TGCBRtX5q8OUlIr2');
insert or replace into user values (10203040, "student1","studend1@a.a", b'$2b$12$1Y21IaNbwu357bI4ipaZO.GVvzouAEvnrAy80TGCBRtX5q8OUlIr2');
insert or replace into user values (50607080, "student2","student2@a.a", b'$2b$12$1Y21IaNbwu357bI4ipaZO.GVvzouAEvnrAy80TGCBRtX5q8OUlIr2');

/* link users to course as ta */
insert or replace into ta_link_course values (12345678,'71d929a86b1311e8adc0fa7ae01bbebc');
insert or replace into ta_link_course values (12345678,'51d929a86b1311e8adc0fa7ae01bbebc');
insert or replace into ta_link_course values (12345678,'31d929a86b1311e8adc0fa7ae01bbebc');
insert or replace into ta_link_course values (87654321,'71d929a86b1311e8adc0fa7ae01bbebc');

/* link users to course as student */
insert or replace into student_link_course values (87654321,'71d929a86b1311e8adc0fa7ae01bbebc');
insert or replace into student_link_course values (87654321,'51d929a86b1311e8adc0fa7ae01bbebc');

/* Create ticket statuses */
insert or replace into ticket_status values (1,'Unassigned');
insert or replace into ticket_status values (3,'Assigned');
insert or replace into ticket_status values (4,'Receiving help');
insert or replace into ticket_status values (2,'Closed');

/* Create a test label */
insert or replace into label values ('fa1b7b20307e4250b59c6d0811315203','test');

/* Create tickets */
insert or replace into ticket values ('126b261c6d7011e8adc0fa7ae01bbebc',10203040,'71d929a86b1311e8adc0fa7ae01bbebc',12345678,1,'pieter@test.nl','ticketnaam','2018-06-11 13:25:05','fa1b7b20307e4250b59c6d0811315203');
insert or replace into ticket values ('326b261c6d7011e8adc0fa7ae01bbebc',10203040,'71d929a86b1311e8adc0fa7ae01bbebc',87654321,2,'pieter2@test.nl','ticketnaam2','2018-06-11 13:25:06','fa1b7b20307e4250b59c6d0811315203');
insert or replace into ticket values ('526b261c6d7011e8adc0fa7ae01bbebc',87654321,'71d929a86b1311e8adc0fa7ae01bbebc',12345678,3,'pieter3@test.nl','ticketnaam3','2018-06-11 13:25:02','fa1b7b20307e4250b59c6d0811315203');
insert or replace into ticket values ('726b261c6d7011e8adc0fa7ae01bbebc',87654321,'51d929a86b1311e8adc0fa7ae01bbebc',12345678,1,'pieter4@test.nl','ticketnaam4','2018-06-11 13:25:02','fa1b7b20307e4250b59c6d0811315203');

/* link ta's to a ticket */
insert or replace into ta_tracker values ('126b261c6d7011e8adc0fa7ae01bbebc',12345678);
insert or replace into ta_tracker values ('326b261c6d7011e8adc0fa7ae01bbebc',12345678);

insert or replace into label values ('fa1b7b20307e4250b59c6d0811315203','testlabel');

insert or replace into label_link_course values ('71d929a86b1311e8adc0fa7ae01bbebc','fa1b7b20307e4250b59c6d0811315203');
insert or replace into label_link_course values ('51d929a86b1311e8adc0fa7ae01bbebc','fa1b7b20307e4250b59c6d0811315203');
