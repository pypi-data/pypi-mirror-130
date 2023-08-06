CREATE TABLE `table_name` (
  `id_migration` INT NOT NULL AUTO_INCREMENT,
  `priority_script` INT NOT NULL,
  `version_script` VARCHAR(100) NOT NULL,
  `name_script` VARCHAR(300) NOT NULL,
  `date_migrate` TIMESTAMP NULL DEFAULT NOW(),
  `status_migrate` ENUM('Success', 'Error', 'Execution') NOT NULL,
  PRIMARY KEY (`id_migration`),
  UNIQUE INDEX `id_migration_UNIQUE` (`id_migration`),
  UNIQUE INDEX `priority_script_UNIQUE` (`priority_script`)
);