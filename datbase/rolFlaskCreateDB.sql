CREATE SEQUENCE user_id_seq;
CREATE SEQUENCE game_id_seq;
CREATE SEQUENCE player_id_seq;
CREATE SEQUENCE item_id_seq;

--IMPORTANT: the password must be storaged using an encryptation algorithm
CREATE TABLE users (
	user_id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
	user_name varchar(50) NOT NULL,
	user_pswd varchar(50) NOT NULL,
	CONSTRAINT user_pkey PRIMARY KEY (user_id)
);

CREATE TABLE game (
	game_id integer NOT NULL DEFAULT nextval('game_id_seq'::regclass),
	game_name varchar(50) NOT NULL,
	game_desc text NOT NULL,
	CONSTRAINT game_pkey PRIMARY KEY (game_id)
);

--This table relates users and games. For each game we could have n different users
CREATE TABLE game_user (
	myuser integer NOT NULL,
	game integer NOT NULL,
	CONSTRAINT user_fkey FOREIGN KEY (myuser)
		REFERENCES public.users (user_id) MATCH SIMPLE
		ON UPDATE CASCADE ON DELETE NO ACTION,
	CONSTRAINT game_fkey FOREIGN KEY (game)
		REFERENCES public.game (game_id) MATCH SIMPLE
		ON UPDATE CASCADE ON DELETE NO ACTION,
	CONSTRAINT game_users_pkey PRIMARY KEY (game, myuser)
);

--This table relates games and game masters. We can have more than one GM for a game.
CREATE TABLE game_gm (
	master integer NOT NULL,
	game integer NOT NULL,
	CONSTRAINT master_fkey FOREIGN KEY (master)
		REFERENCES public.users (user_id) MATCH SIMPLE
		ON UPDATE CASCADE ON DELETE NO ACTION,
	CONSTRAINT game_master_fkey FOREIGN KEY (game)
		REFERENCES public.game (game_id) MATCH SIMPLE
		ON UPDATE CASCADE ON DELETE NO ACTION,
	CONSTRAINT game_gm_pkey PRIMARY KEY (game, master)
);
--TODO: some more gurps attributes need to be added 
CREATE TABLE player (
	player_id integer NOT NULL DEFAULT nextval('player_id_seq'::regclass),
	player_name varchar(50) NOT NULL,
	player_st integer NOT NULL,
	player_dx integer NOT NULL,
	player_iq integer NOT NULL,
	player_ht integer NOT NULL,
	player_hp_max integer NOT NULL,
	player_hp_current integer NOT NULL,
	player_will integer NOT NULL,
	player_per integer NOT NULL,
	player_fp_max integer NOT NULL,
	player_fp_current integer NOT NULL,
	CONSTRAINT player_pkey PRIMARY KEY (player_id)
);

CREATE TABLE item (
	item_id integer NOT NULL DEFAULT nextval('item_id_seq'::regclass),
	item_name varchar(50) NOT NULL,
	item_desc text NOT NULL,
	CONSTRAINT item_pkey PRIMARY KEY (item_id)
);

CREATE TABLE game_inventory (
	item integer NOT NULL,
	game integer NOT NULL,
	CONSTRAINT item_fkey FOREIGN KEY (item)
		REFERENCES public.item (item_id) MATCH SIMPLE
		ON UPDATE CASCADE ON DELETE NO ACTION,
	CONSTRAINT game_inventory_fkey FOREIGN KEY (game)
		REFERENCES public.game (game_id) MATCH SIMPLE
		ON UPDATE CASCADE ON DELETE NO ACTION,
	CONSTRAINT game_inventory_pkey PRIMARY KEY (game, item)
);

CREATE TABLE player_inventory(
	item integer NOT NULL,
	player integer NOT NULL,
	CONSTRAINT item_inventory_fkey FOREIGN KEY (item)
		REFERENCES public.item (item_id) MATCH SIMPLE
		ON UPDATE CASCADE ON DELETE NO ACTION,
	CONSTRAINT player_inventory_fkey FOREIGN KEY (player)
		REFERENCES public.game (game_id) MATCH SIMPLE
		ON UPDATE CASCADE ON DELETE NO ACTION,
	CONSTRAINT player_inventory_pkey PRIMARY KEY (item, player)
);





