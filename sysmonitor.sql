grant select,update,insert,delete,alter,drop,create on sysmonitor.* to 'sysmonitor'@'192.168.1.%' ;

CREATE TABLE IF NOT EXISTS `sysmonitor`.`system_info` (
  `system_id` INT NULL COMMENT '主机ID',
  `system_name` VARCHAR(50) NOT NULL,
  `system_desc` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`system_id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `sysmonitor`.`host_info` (
  `host_id` INT NOT NULL,
  `system_id` INT NULL,
  `host_ip` VARCHAR(16) NULL,
  `host_name` VARCHAR(45) NULL,
  PRIMARY KEY (`host_id`),
  INDEX `fk_system_id_idx` (`system_id` ASC),
  CONSTRAINT `fk_system_id`
    FOREIGN KEY (`system_id`)
    REFERENCES `sysmonitor`.`system` (`system_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `sysmonitor`.`monitor_info` (
  `host_id` INT NOT NULL,
  `date` VARCHAR(45) NULL,
  `system_type` VARCHAR(45) NULL COMMENT '系统类型，该选项可以是主机、网络、数据库等',
  `monitor_type` VARCHAR(45) NULL COMMENT '监控项的类型，例如CPU、MEMORY、TABLESPACE、FILESYTEM等',
  `monitor_name` VARCHAR(45) NULL,
  `monitor_value` INT NULL,
  PRIMARY KEY (`host_id`),
  CONSTRAINT `fk_host_id`
    FOREIGN KEY (`host_id`)
    REFERENCES `sysmonitor`.`host` (`host_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;