CREATE DATABASE `db_zarplata_conference`

CREATE TABLE `conferences` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_unicode_ci',
	`description` VARCHAR(400) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	`is_current` TINYINT(1) UNSIGNED NULL DEFAULT '0',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE `users` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`tg_id` BIGINT UNSIGNED NOT NULL,
	`conference_id` INT(10) UNSIGNED NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `conference_id` (`conference_id`) USING BTREE,
	UNIQUE INDEX `tg_id` (`tg_id`),
	CONSTRAINT `FK__users_conferences` FOREIGN KEY (`conference_id`) REFERENCES `conferences` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE `moderators` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`tg_id` BIGINT UNSIGNED NOT NULL,
	`conference_id` INT(10) UNSIGNED NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `conference_id` (`conference_id`) USING BTREE,
	UNIQUE INDEX `tg_id` (`tg_id`),
	CONSTRAINT `FK__moderators_conferences` FOREIGN KEY (`conference_id`) REFERENCES `conferences` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE `speakers` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`tg_id` BIGINT UNSIGNED NOT NULL,
	`name` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`conference_id` INT(10) UNSIGNED NULL DEFAULT NULL,
	`is_current` TINYINT(1) UNSIGNED NULL DEFAULT '0',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `conference_id` (`conference_id`) USING BTREE,
	UNIQUE INDEX `tg_id` (`tg_id`),
	CONSTRAINT `FK__speakers_conferences` FOREIGN KEY (`conference_id`) REFERENCES `conferences` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;