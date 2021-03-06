## DB Tables
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(512) DEFAULT NULL,
  `email` varchar(512) DEFAULT NULL,
  `password` varchar(512) DEFAULT NULL,
  `first_name` varchar(512) DEFAULT NULL,
  `last_name` varchar(512) DEFAULT NULL,
  `sso_id` varchar(512) DEFAULT NULL,
  `action_token` varchar(512) DEFAULT NULL,
  `last_password_change` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  `past_passwords_hash` text DEFAULT NULL,
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `auth_user_tag_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(512) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `record_id_fk` (`record_id`),
  CONSTRAINT `record_id_fk` FOREIGN KEY (`record_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `py4web_session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rkey` varchar(512) DEFAULT NULL,
  `rvalue` text,
  `expiration` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `expires_on` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rkey__idx` (`rkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `watch_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_title` varchar(512),
  `watch_list_watched` int,
  `watch_list_date` DATE,
  `watch_list_user_email` varchar(512),
  `watch_list_user_name` varchar(512),
  `watch_list_rating` int,
  `watch_list_time_stamp` DATETIME,
  `watch_list_review` varchar(512),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `watch_list` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`movie_title` TEXT DEFAULT NULL,
	`watch_list_watched` TEXT DEFAULT NULL,
	`watch_list_date` DATE DEFAULT NULL,
	`watch_list_user_email` TEXT DEFAULT NULL,
	`watch_list_user_name` TEXT DEFAULT NULL,
	`watch_list_rating` INT DEFAULT '0',
	`watch_list_time_stamp` DATETIME DEFAULT NULL,
	`watch_list_review` TEXT DEFAULT NULL, 
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `review_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `watch_list_id` varchar(512),
  `user_email` varchar(512) DEFAULT NULL,
  `user_name` varchar(512) DEFAULT NULL,
  `comment` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `watch_list_id` FOREIGN KEY (`id`) REFERENCES `watch_list` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_email` varchar(512),
  `user_name` varchar(512),
  `thumbnail` BINARY(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `following` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `following_user_name` varchar(512),
  `following_user_email` varchar(512),
  `following_thumbnail` BINARY(255),
  `following_id` INT,
  `user_id` INT,
  PRIMARY KEY (`id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `follower` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `following_user_name` varchar(512),
  `following_user_email` varchar(512),
  `following_thumbnail` BINARY(255),
  `following_id` INT,
  `user_id` INT,
  PRIMARY KEY (`id`),
  CONSTRAINT `user_id_follower` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

