CREATE TABLE brand (
	url varchar primary key,
	brand varchar,
	model_name varchar,
	model_no varchar,
	photo varchar,
	product_point varchar,
	price varchar,
	website varchar,
	os varchar,
	cpu varchar,
	cpu_gen varchar,
	ram varchar,
	disk_capacity varchar,
	screen_size varchar
);

ALTER TABLE brand 
    ALTER brand DROP NOT NULL,
    ALTER model_name DROP NOT NULL,
    ALTER model_no DROP NOT NULL,
    ALTER photo DROP NOT NULL,
    ALTER product_point DROP NOT NULL,
    ALTER price DROP NOT NULL,
    ALTER website DROP NOT NULL,
    ALTER os DROP NOT NULL,
    ALTER cpu DROP NOT NULL,
    ALTER cpu_gen DROP NOT NULL,
    ALTER ram DROP NOT NULL,
    ALTER disk_capacity DROP NOT NULL,
    ALTER screen_size DROP NOT NULL;