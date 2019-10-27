/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     23.10.2019 22:14:03                          */
/*==============================================================*/


drop index "User Has Functions_FK";

drop index Fuction_PK;

drop table Fuction;

drop index "Function Has Test_Cases_FK";

drop index "Topic_Test Has Test_Cases_FK";

drop index Test_Case_PK;

drop table Test_Case;

drop index Topic_Test_PK;

drop table Topic_Test;

drop index User_PK;

drop table "User";

/*==============================================================*/
/* Table: Fuction                                               */
/*==============================================================*/
create table Fuction (
   fuction_id           INT4                 not null,
   user_email           TEXT                 null,
   function_name        TEXT                 null,
   function_language    TEXT                 null,
   constraint PK_FUCTION primary key (fuction_id)
);

/*==============================================================*/
/* Index: Fuction_PK                                            */
/*==============================================================*/
create unique index Fuction_PK on Fuction (
fuction_id
);

/*==============================================================*/
/* Index: "User Has Functions_FK"                               */
/*==============================================================*/
create  index "User Has Functions_FK" on Fuction (
user_email
);

/*==============================================================*/
/* Table: Test_Case                                             */
/*==============================================================*/
create table Test_Case (
   test_case_id         INT4                 not null,
   fuction_id           INT4                 null,
   topic_test_id        INT4                 null,
   test_case_description TEXT                 null,
   test_case_result     TEXT                 null,
   constraint PK_TEST_CASE primary key (test_case_id)
);

/*==============================================================*/
/* Index: Test_Case_PK                                          */
/*==============================================================*/
create unique index Test_Case_PK on Test_Case (
test_case_id
);

/*==============================================================*/
/* Index: "Topic_Test Has Test_Cases_FK"                        */
/*==============================================================*/
create  index "Topic_Test Has Test_Cases_FK" on Test_Case (
topic_test_id
);

/*==============================================================*/
/* Index: "Function Has Test_Cases_FK"                          */
/*==============================================================*/
create  index "Function Has Test_Cases_FK" on Test_Case (
fuction_id
);

/*==============================================================*/
/* Table: Topic_Test                                            */
/*==============================================================*/
create table Topic_Test (
   topic_test_id        INT4                 not null,
   topic_test_name      TEXT                 null,
   constraint PK_TOPIC_TEST primary key (topic_test_id)
);

/*==============================================================*/
/* Index: Topic_Test_PK                                         */
/*==============================================================*/
create unique index Topic_Test_PK on Topic_Test (
topic_test_id
);

/*==============================================================*/
/* Table: "User"                                                */
/*==============================================================*/
create table "User" (
   user_email           TEXT                 not null,
   user_name            TEXT                 null,
   user_password        TEXT                 null,
   constraint PK_USER primary key (user_email)
);

/*==============================================================*/
/* Index: User_PK                                               */
/*==============================================================*/
create unique index User_PK on "User" (
user_email
);

alter table Fuction
   add constraint "FK_FUCTION_USER HAS _USER" foreign key (user_email)
      references "User" (user_email)
      on delete restrict on update restrict;

alter table Test_Case
   add constraint "FK_TEST_CAS_FUNCTION _FUCTION" foreign key (fuction_id)
      references Fuction (fuction_id)
      on delete restrict on update restrict;

alter table Test_Case
   add constraint FK_TEST_CAS_TOPIC_TES_TOPIC_TE foreign key (topic_test_id)
      references Topic_Test (topic_test_id)
      on delete restrict on update restrict;

