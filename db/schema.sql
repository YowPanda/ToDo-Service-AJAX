create table users
(
	id integer not null
		constraint users_pk
			primary key autoincrement,
	email text not null,
	password text not null
);

create unique index users_email_uindex
	on users (email);

create table tasks
(
	id integer not null
		constraint task_pk
			primary key autoincrement,
	title text not null,
	description text,
	status integer(1) default 0,
	user_id integer not null,
		foreing key user_id references users(id)
);