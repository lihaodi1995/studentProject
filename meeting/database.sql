#CREATE DATABSE db_meeting;#
USE db_meeting;

SET NAMES utf8;

#DROP TABLE IF EXISTS `table_admin`;#
CREATE TABLE `table_admin` (
    `admin_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//管理员ID',
    `account` VARCHAR(100)
        BINARY
        NOT NULL
        COMMENT '//帐号',
    `hash` VARCHAR(100)
        BINARY
        NOT NULL
        COMMENT '//密码哈希',
    `salt` VARCHAR(100)
        BINARY
        NOT NULL
        COMMENT '//盐'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_user`;#
CREATE TABLE `table_user` (
    `user_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//注册会员ID',
    `email` VARCHAR(100)
        BINARY
        NOT NULL
        COMMENT '//邮箱',
    `hash` VARCHAR(100)
        BINARY
        NOT NULL
        COMMENT '//密码哈希',
    `salt` VARCHAR(100)
        BINARY
        NOT NULL
        COMMENT '//盐',
    `name` VARCHAR(100)
        NOT NULL
        COMMENT '//姓名',
    `confirm` BOOL
        DEFAULT 0
        NOT NULL
        COMMENT '//是否验证'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_company`;#
CREATE TABLE `table_company` (
    `company_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//单位ID',
    `account` VARCHAR(100)
        BINARY
        NOT NULL
        COMMENT '//帐号',
    `hash` VARCHAR(100)
        BINARY
        NOT NULL
        COMMENT '//密码哈希',
    `salt` VARCHAR(100)
        BINARY
        NOT NULL
        COMMENT '//盐',
    `name` VARCHAR(1000)
        NOT NULL
        COMMENT '//单位名称',
    `confirm` INT(11)
        DEFAULT 2
        NOT NULL
        COMMENT '//是否审核, 0-审核中, 1-通过审核, 2-未通过审核'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_company_addition`;#
CREATE TABLE `table_company_addition` (
    `company_addition_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//单位额外信息ID',
    `company_id` INT(11)
        NOT NULL
        COMMENT '//单位ID',
    `url` VARCHAR(1000)
        NOT NULL
        COMMENT '//额外信息URL'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_company_unit`;#
CREATE TABLE `table_company_unit` (
    `company_unit_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//单位个人账号ID',
    `company_id` INT(11)
        NOT NULL
        COMMENT '//单位ID',
    `account` VARCHAR(100)
        BINARY
        NOT NULL
        COMMENT '//帐号',
    `password` VARCHAR(100)
        BINARY
        NOT NULL
        COMMENT '//密码',
    `name` VARCHAR(100)
        NOT NULL
        COMMENT '//昵称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_meeting`;#
CREATE TABLE `table_meeting` (
    `meeting_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//会议ID',
    `company_id` INT(11)
        NOT NULL
        COMMENT '//单位ID',
    `template_id` INT(11)
        NOT NULL
        COMMENT '//会议模板ID',
    `title` VARCHAR(100)
        NOT NULL
        COMMENT '//会议标题',
    `description` VARCHAR(1000)
        NOT NULL
        COMMENT '//会议简介',
    `solicit_info` VARCHAR(1000)
        NOT NULL
        COMMENT '//征文信息',
    `agenda` VARCHAR(2000)
        NOT NULL
        COMMENT '//日程安排',
    `organization` VARCHAR(1000)
        NOT NULL
        COMMENT '//组织机构',
    `manuscript_template_url` VARCHAR(1000)
        NOT NULL
        COMMENT '//论文模版',
    `fee` VARCHAR(1000)
        NOT NULL
        COMMENT '//注册费用',
    `accom_traffic` VARCHAR(1000)
        NOT NULL
        COMMENT '//住宿交通',
    `contact_us` VARCHAR(1000)
        NOT NULL
        COMMENT '//联系我们',
    `place` VARCHAR(1000)
        NOT NULL
        COMMENT '//地点'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_meeting_date`;#
CREATE TABLE `table_meeting_date` (
    `meeting_date_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//会议日期ID',
    `meeting_id` INT(11)
        NOT NULL
        COMMENT '//会议ID',
    `manuscript_date` DATETIME
        NOT NULL
        COMMENT '//截稿日期',
    `manuscript_modify_date` DATETIME
        NOT NULL
        COMMENT '//修改稿截止日期',
    `inform_date` DATETIME
        NOT NULL
        COMMENT '//录用通知日期',
    `register_begin_date` DATETIME
        NOT NULL
        COMMENT '//注册开始日期',
    `register_end_date` DATETIME
        NOT NULL
        COMMENT '//注册结束日期',
    `meeting_begin_date` DATETIME
        NOT NULL
        COMMENT '//会议开始日期',
    `meeting_end_date` DATETIME
        NOT NULL
        COMMENT '//会议结束日期'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_subscribe`;#
CREATE TABLE `table_subscribe` (
    `subscribe_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//收藏ID',
    `user_id` INT(11)
        NOT NULL
        COMMENT '//会员ID',
    `meeting_id` INT(11)
        NOT NULL
        COMMENT '//会议ID',
    `type` INT(11)
        NOT NULL
        COMMENT '//收藏方式(1-主动收藏, 2-投稿收藏, 3-注册收藏)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_manuscript`;#
CREATE TABLE `table_manuscript` (
    `manuscript_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//稿件ID',
    `user_id` INT(11)
        NOT NULL
        COMMENT '//会员ID',
    `meeting_id` INT(11)
        NOT NULL
        COMMENT '//会议ID',
    `type` INT
        NOT NULL
        COMMENT '//稿件类型(1-投稿, 2-修改稿)',
    `valid` BOOL
        NOT NULL
        COMMENT '//有效性',
    `url` VARCHAR(1000)
        NOT NULL
        COMMENT '//稿件url',
    `create_time` DATETIME,
    `update_time` DATETIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_manuscript_info`;#
CREATE TABLE `table_manuscript_info` (
    `manuscript_info_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//稿件信息ID',
    `manuscript_id` INT(11)
        NOT NULL
        COMMENT '//稿件ID',
    `author` VARCHAR(10000)
        NOT NULL
        COMMENT '//作者',
    `title` VARCHAR(100)
        NOT NULL
        COMMENT '//题目',
    `organization` VARCHAR(1000)
        NOT NULL
        COMMENT '//单位',
    `abstract` VARCHAR(2000)
        NOT NULL
        COMMENT '//摘要',
    `modify_info` VARCHAR(2000)
        COMMENT '//修改信息'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_review`;#
CREATE TABLE `table_review` (
    `review_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//评审信息ID',
    `manuscript_id` INT(11)
        NOT NULL
        COMMENT '//稿件ID',
    `result` INT(11)
        NOT NULL
        COMMENT '//评审结果(0-未录用, 1-录用, 2-修改后录用)',
    `suggestion` VARCHAR(1000)
        NOT NULL
        COMMENT '//评审意见',
    `create_time` DATETIME,
    `update_time` DATETIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_register`;#
CREATE TABLE `table_register` (
    `register_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//注册ID',
    `user_id` INT(11)
        NOT NULL
        COMMENT '//会员ID',
    `meeting_id` INT(11)
        NOT NULL
        COMMENT '//会议ID',
    `manuscript_id` INT(11)
        DEFAULT 0
        NOT NULL
        COMMENT '//稿件ID',
    `type` INT(11)
        NOT NULL
        COMMENT '//参会类型(1-投稿参会, 2-聆听参会)',
    `check` INT(11)
        NOT NULL
        COMMENT '//审核信息(1-未审核, 2-审核通过, 3-审核未通过)',
    `create_time` DATETIME,
    `update_time` DATETIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_register_person`;#
CREATE TABLE `table_register_person` (
    `register_person_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//注册人ID',
    `register_id` INT(11)
        NOT NULL
        COMMENT '//注册信息ID',
    `name` VARCHAR(100)
        NOT NULL
        COMMENT '//姓名',
    `gender` VARCHAR(100)
        NOT NULL
        COMMENT '//性别',
    `accomodation` BOOL
        NOT NULL
        COMMENT '//是否预定住宿'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_register_addition`;#
CREATE TABLE `table_register_addition` (
    `register_addition_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//注册额外信息ID',
    `register_id` INT(11)
        NOT NULL
        COMMENT '//注册信息ID',
    `url` VARCHAR(1000)
        NOT NULL
        COMMENT '//额外信息URL'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#DROP TABLE IF EXISTS `table_template`;#
CREATE TABLE `table_template` (
    `template_id` INT(11)
        PRIMARY KEY
        AUTO_INCREMENT
        NOT NULL
        COMMENT '//模板ID',
    `name` VARCHAR(1000)
        NOT NULL
        COMMENT '//模板名字',
    `imgUrl` VARCHAR(1000)
        COMMENT '//模板图片URL'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;