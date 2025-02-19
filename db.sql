CREATE DATABASE `db_zarplata_event`

CREATE TABLE `events` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_unicode_ci',
	`content` VARCHAR(400) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`img` VARCHAR(400) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`date` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE `questions` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`content` VARCHAR(500) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`cell` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`speaker_id` INT(10) UNSIGNED NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK__questions_speakers` (`speaker_id`) USING BTREE,
	CONSTRAINT `FK__questions_speakers` FOREIGN KEY (`speaker_id`) REFERENCES `speakers` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE `quizes` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`content` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`cell` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`img` VARCHAR(400) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`event_id` INT(10) UNSIGNED NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `event_id` (`event_id`) USING BTREE,
	CONSTRAINT `FK__events_quizes` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE `speakers` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`content` VARCHAR(400) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`cell` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`img` VARCHAR(400) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`event_id` INT(10) UNSIGNED NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `conference_id` (`event_id`) USING BTREE,
	CONSTRAINT `FK__speakers_conferences` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE `users` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`tg_id` BIGINT(20) UNSIGNED NOT NULL,
	`event_id` INT(10) UNSIGNED NULL DEFAULT NULL,
	`is_passed` TINYINT(1) UNSIGNED NULL DEFAULT '0',
	`msg_id` BIGINT(20) UNSIGNED NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `tg_id` (`tg_id`) USING BTREE,
	INDEX `conference_id` (`event_id`) USING BTREE,
	CONSTRAINT `FK__users_conferences` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE `variants` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`quiz_id` INT(10) UNSIGNED NULL DEFAULT NULL,
	`cell` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`result` INT(10) UNSIGNED NULL DEFAULT '0',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK__variants_quizes` (`quiz_id`) USING BTREE,
	CONSTRAINT `FK__variants_quizes` FOREIGN KEY (`quiz_id`) REFERENCES `quizes` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;