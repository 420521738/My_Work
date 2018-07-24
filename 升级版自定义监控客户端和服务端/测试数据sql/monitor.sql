/*
Navicat MySQL Data Transfer

Source Server         : LocalMySQL
Source Server Version : 50640
Source Host           : localhost:3306
Source Database       : monitor

Target Server Type    : MYSQL
Target Server Version : 50640
File Encoding         : 65001

Date: 2018-07-24 11:28:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_58c48ba9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_bin NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`),
  CONSTRAINT `auth_permissi_content_type_id_51277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry');
INSERT INTO `auth_permission` VALUES ('2', 'Can change log entry', '1', 'change_logentry');
INSERT INTO `auth_permission` VALUES ('3', 'Can delete log entry', '1', 'delete_logentry');
INSERT INTO `auth_permission` VALUES ('4', 'Can add permission', '2', 'add_permission');
INSERT INTO `auth_permission` VALUES ('5', 'Can change permission', '2', 'change_permission');
INSERT INTO `auth_permission` VALUES ('6', 'Can delete permission', '2', 'delete_permission');
INSERT INTO `auth_permission` VALUES ('7', 'Can add group', '3', 'add_group');
INSERT INTO `auth_permission` VALUES ('8', 'Can change group', '3', 'change_group');
INSERT INTO `auth_permission` VALUES ('9', 'Can delete group', '3', 'delete_group');
INSERT INTO `auth_permission` VALUES ('10', 'Can add user', '4', 'add_user');
INSERT INTO `auth_permission` VALUES ('11', 'Can change user', '4', 'change_user');
INSERT INTO `auth_permission` VALUES ('12', 'Can delete user', '4', 'delete_user');
INSERT INTO `auth_permission` VALUES ('13', 'Can add content type', '5', 'add_contenttype');
INSERT INTO `auth_permission` VALUES ('14', 'Can change content type', '5', 'change_contenttype');
INSERT INTO `auth_permission` VALUES ('15', 'Can delete content type', '5', 'delete_contenttype');
INSERT INTO `auth_permission` VALUES ('16', 'Can add session', '6', 'add_session');
INSERT INTO `auth_permission` VALUES ('17', 'Can change session', '6', 'change_session');
INSERT INTO `auth_permission` VALUES ('18', 'Can delete session', '6', 'delete_session');
INSERT INTO `auth_permission` VALUES ('19', 'Can add user profile', '7', 'add_userprofile');
INSERT INTO `auth_permission` VALUES ('20', 'Can change user profile', '7', 'change_userprofile');
INSERT INTO `auth_permission` VALUES ('21', 'Can delete user profile', '7', 'delete_userprofile');
INSERT INTO `auth_permission` VALUES ('22', 'Can add idc', '8', 'add_idc');
INSERT INTO `auth_permission` VALUES ('23', 'Can change idc', '8', 'change_idc');
INSERT INTO `auth_permission` VALUES ('24', 'Can delete idc', '8', 'delete_idc');
INSERT INTO `auth_permission` VALUES ('25', 'Can add group', '9', 'add_group');
INSERT INTO `auth_permission` VALUES ('26', 'Can change group', '9', 'change_group');
INSERT INTO `auth_permission` VALUES ('27', 'Can delete group', '9', 'delete_group');
INSERT INTO `auth_permission` VALUES ('28', 'Can add host', '10', 'add_host');
INSERT INTO `auth_permission` VALUES ('29', 'Can change host', '10', 'change_host');
INSERT INTO `auth_permission` VALUES ('30', 'Can delete host', '10', 'delete_host');
INSERT INTO `auth_permission` VALUES ('31', 'Can add server status', '11', 'add_serverstatus');
INSERT INTO `auth_permission` VALUES ('32', 'Can change server status', '11', 'change_serverstatus');
INSERT INTO `auth_permission` VALUES ('33', 'Can delete server status', '11', 'delete_serverstatus');
INSERT INTO `auth_permission` VALUES ('34', 'Can add trunk servers', '12', 'add_trunkservers');
INSERT INTO `auth_permission` VALUES ('35', 'Can change trunk servers', '12', 'change_trunkservers');
INSERT INTO `auth_permission` VALUES ('36', 'Can delete trunk servers', '12', 'delete_trunkservers');
INSERT INTO `auth_permission` VALUES ('37', 'Can add templates', '13', 'add_templates');
INSERT INTO `auth_permission` VALUES ('38', 'Can change templates', '13', 'change_templates');
INSERT INTO `auth_permission` VALUES ('39', 'Can delete templates', '13', 'delete_templates');
INSERT INTO `auth_permission` VALUES ('40', 'Can add services', '14', 'add_services');
INSERT INTO `auth_permission` VALUES ('41', 'Can change services', '14', 'change_services');
INSERT INTO `auth_permission` VALUES ('42', 'Can delete services', '14', 'delete_services');
INSERT INTO `auth_permission` VALUES ('43', 'Can add items', '15', 'add_items');
INSERT INTO `auth_permission` VALUES ('44', 'Can change items', '15', 'change_items');
INSERT INTO `auth_permission` VALUES ('45', 'Can delete items', '15', 'delete_items');
INSERT INTO `auth_permission` VALUES ('46', 'Can add service list', '16', 'add_servicelist');
INSERT INTO `auth_permission` VALUES ('47', 'Can change service list', '16', 'change_servicelist');
INSERT INTO `auth_permission` VALUES ('48', 'Can delete service list', '16', 'delete_servicelist');
INSERT INTO `auth_permission` VALUES ('49', 'Can add graphs', '17', 'add_graphs');
INSERT INTO `auth_permission` VALUES ('50', 'Can change graphs', '17', 'change_graphs');
INSERT INTO `auth_permission` VALUES ('51', 'Can delete graphs', '17', 'delete_graphs');
INSERT INTO `auth_permission` VALUES ('52', 'Can add actions', '18', 'add_actions');
INSERT INTO `auth_permission` VALUES ('53', 'Can change actions', '18', 'change_actions');
INSERT INTO `auth_permission` VALUES ('54', 'Can delete actions', '18', 'delete_actions');
INSERT INTO `auth_permission` VALUES ('55', 'Can add formulas', '19', 'add_formulas');
INSERT INTO `auth_permission` VALUES ('56', 'Can change formulas', '19', 'change_formulas');
INSERT INTO `auth_permission` VALUES ('57', 'Can delete formulas', '19', 'delete_formulas');
INSERT INTO `auth_permission` VALUES ('58', 'Can add operators', '20', 'add_operators');
INSERT INTO `auth_permission` VALUES ('59', 'Can change operators', '20', 'change_operators');
INSERT INTO `auth_permission` VALUES ('60', 'Can delete operators', '20', 'delete_operators');
INSERT INTO `auth_permission` VALUES ('61', 'Can add conditions', '21', 'add_conditions');
INSERT INTO `auth_permission` VALUES ('62', 'Can change conditions', '21', 'change_conditions');
INSERT INTO `auth_permission` VALUES ('63', 'Can delete conditions', '21', 'delete_conditions');
INSERT INTO `auth_permission` VALUES ('64', 'Can add operations', '22', 'add_operations');
INSERT INTO `auth_permission` VALUES ('65', 'Can change operations', '22', 'change_operations');
INSERT INTO `auth_permission` VALUES ('66', 'Can delete operations', '22', 'delete_operations');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8_bin NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) COLLATE utf8_bin NOT NULL,
  `first_name` varchar(30) COLLATE utf8_bin NOT NULL,
  `last_name` varchar(30) COLLATE utf8_bin NOT NULL,
  `email` varchar(75) COLLATE utf8_bin NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES ('1', 'pbkdf2_sha256$12000$hsRPqN1fy80z$HBJK/sabmb54WKbajsoTFAB9ctbMPeOxVnqXjvYIWVY=', '2018-07-23 06:50:47', '1', 'chenqiufei', '', '', '', '1', '1', '2018-07-23 06:44:46');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_30a071c9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_24702650_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_7cd7acb6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext COLLATE utf8_bin,
  `object_repr` varchar(200) COLLATE utf8_bin NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8_bin NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_5151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_1c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
INSERT INTO `django_admin_log` VALUES ('1', '2018-07-23 06:52:08', 0x31, '中山联通机房', '1', '', '8', '1');
INSERT INTO `django_admin_log` VALUES ('2', '2018-07-23 06:53:07', 0x31, 'TestServer ubuntu主机', '1', '', '10', '1');
INSERT INTO `django_admin_log` VALUES ('3', '2018-07-23 07:09:49', 0x31, 'linux.cpu.iowait', '1', '', '15', '1');
INSERT INTO `django_admin_log` VALUES ('4', '2018-07-23 07:10:15', 0x32, 'linux.cpu.idle', '1', '', '15', '1');
INSERT INTO `django_admin_log` VALUES ('5', '2018-07-23 07:10:41', 0x33, 'linux.cpu.usage', '1', '', '15', '1');
INSERT INTO `django_admin_log` VALUES ('6', '2018-07-23 07:10:53', 0x31, 'linux.cpu', '1', '', '14', '1');
INSERT INTO `django_admin_log` VALUES ('7', '2018-07-23 07:20:43', 0x31, '最近5分钟平均值', '1', '', '19', '1');
INSERT INTO `django_admin_log` VALUES ('8', '2018-07-23 07:21:22', 0x31, '小于', '1', '', '20', '1');
INSERT INTO `django_admin_log` VALUES ('9', '2018-07-23 07:21:30', 0x31, 'LinuxTemplate.linux.cpu.idle', '1', '', '21', '1');
INSERT INTO `django_admin_log` VALUES ('10', '2018-07-23 07:21:58', 0x31, 'LinuxTemplate.linux.cpu', '1', '', '16', '1');
INSERT INTO `django_admin_log` VALUES ('11', '2018-07-23 07:23:47', 0x34, 'linux.memory.free', '1', '', '15', '1');
INSERT INTO `django_admin_log` VALUES ('12', '2018-07-23 07:24:16', 0x35, 'linux.memory.cached', '1', '', '15', '1');
INSERT INTO `django_admin_log` VALUES ('13', '2018-07-23 07:24:57', 0x36, 'linux.memory.total', '1', '', '15', '1');
INSERT INTO `django_admin_log` VALUES ('14', '2018-07-23 07:25:16', 0x37, 'linux.memory.usage', '1', '', '15', '1');
INSERT INTO `django_admin_log` VALUES ('15', '2018-07-23 07:25:28', 0x32, 'linux.memory', '1', '', '14', '1');
INSERT INTO `django_admin_log` VALUES ('16', '2018-07-23 07:26:45', 0x32, '大于', '1', '', '20', '1');
INSERT INTO `django_admin_log` VALUES ('17', '2018-07-23 07:27:48', 0x33, '大于运算符', '1', '', '20', '1');
INSERT INTO `django_admin_log` VALUES ('18', '2018-07-23 07:27:54', 0x32, 'LinuxTemplate.linux.memory', '1', '', '21', '1');
INSERT INTO `django_admin_log` VALUES ('19', '2018-07-23 07:28:13', 0x32, 'LinuxTemplate.linux.memory', '1', '', '16', '1');
INSERT INTO `django_admin_log` VALUES ('20', '2018-07-23 07:29:09', 0x31, 'LinuxTemplate', '1', '', '13', '1');
INSERT INTO `django_admin_log` VALUES ('21', '2018-07-23 07:29:40', 0x32, 'LinuxTemplate.linux.memory', '2', 0x4368616E67656420636865636B5F696E74657276616C2E, '16', '1');
INSERT INTO `django_admin_log` VALUES ('22', '2018-07-23 07:34:01', 0x31, 'TestServer ubuntu主机', '2', 0x4368616E6765642074656D706C6174655F6C6973742E, '10', '1');
INSERT INTO `django_admin_log` VALUES ('23', '2018-07-23 07:56:45', 0x32, 'LinuxTemplate.linux.memory', '2', 0x4368616E67656420636865636B5F696E74657276616C2E, '16', '1');
INSERT INTO `django_admin_log` VALUES ('24', '2018-07-23 08:04:14', 0x32, 'LinuxTemplate.linux.memory', '2', 0x4368616E67656420636865636B5F696E74657276616C2E, '16', '1');
INSERT INTO `django_admin_log` VALUES ('25', '2018-07-23 08:34:13', 0x32, '最近30分钟超过次数', '1', '', '19', '1');

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_bin NOT NULL,
  `app_label` varchar(100) COLLATE utf8_bin NOT NULL,
  `model` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_3ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('1', 'log entry', 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES ('2', 'permission', 'auth', 'permission');
INSERT INTO `django_content_type` VALUES ('3', 'group', 'auth', 'group');
INSERT INTO `django_content_type` VALUES ('4', 'user', 'auth', 'user');
INSERT INTO `django_content_type` VALUES ('5', 'content type', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('6', 'session', 'sessions', 'session');
INSERT INTO `django_content_type` VALUES ('7', 'user profile', 'web', 'userprofile');
INSERT INTO `django_content_type` VALUES ('8', 'idc', 'web', 'idc');
INSERT INTO `django_content_type` VALUES ('9', 'group', 'web', 'group');
INSERT INTO `django_content_type` VALUES ('10', 'host', 'web', 'host');
INSERT INTO `django_content_type` VALUES ('11', 'server status', 'web', 'serverstatus');
INSERT INTO `django_content_type` VALUES ('12', 'trunk servers', 'web', 'trunkservers');
INSERT INTO `django_content_type` VALUES ('13', 'templates', 'web', 'templates');
INSERT INTO `django_content_type` VALUES ('14', 'services', 'web', 'services');
INSERT INTO `django_content_type` VALUES ('15', 'items', 'web', 'items');
INSERT INTO `django_content_type` VALUES ('16', 'service list', 'web', 'servicelist');
INSERT INTO `django_content_type` VALUES ('17', 'graphs', 'web', 'graphs');
INSERT INTO `django_content_type` VALUES ('18', 'actions', 'web', 'actions');
INSERT INTO `django_content_type` VALUES ('19', 'formulas', 'web', 'formulas');
INSERT INTO `django_content_type` VALUES ('20', 'operators', 'web', 'operators');
INSERT INTO `django_content_type` VALUES ('21', 'conditions', 'web', 'conditions');
INSERT INTO `django_content_type` VALUES ('22', 'operations', 'web', 'operations');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8_bin NOT NULL,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2018-07-23 06:38:59');
INSERT INTO `django_migrations` VALUES ('2', 'auth', '0001_initial', '2018-07-23 06:39:10');
INSERT INTO `django_migrations` VALUES ('3', 'admin', '0001_initial', '2018-07-23 06:39:14');
INSERT INTO `django_migrations` VALUES ('4', 'sessions', '0001_initial', '2018-07-23 06:39:14');
INSERT INTO `django_migrations` VALUES ('5', 'web', '0001_initial', '2018-07-23 06:40:26');
INSERT INTO `django_migrations` VALUES ('6', 'web', '0002_auto_20150118_1229', '2018-07-23 06:40:31');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8_bin NOT NULL,
  `session_data` longtext COLLATE utf8_bin NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('4ziszgu7u2ls3fh9ah1snzqtu8ctgpfm', 0x4E4749305957457A59544D7959545135596D4977593251794E54686D4D4755314D6A457A4F4464684E3256695A6D566D5A474D344E7A703766513D3D, '2018-08-06 06:47:24');
INSERT INTO `django_session` VALUES ('puprr0mfcwot4s9sa9gb1uelhm5l5fgh', 0x5A5446684F4463335A6D466A4E54526C5A5445784F574930595759325A5441354E5459334D6D466D4E6D49795A475A6A4E7A4A6A5A547037496C39686458526F5833567A5A584A666147467A61434936496A6B334D5751314D47457A5A6A6C6D596D4A6B4D5449354D7A59325A57526D4E4449355A6A5930595755794E7A4A694D32557A4D7A41694C434A6659585630614639316332567958324A685932746C626D51694F694A6B616D46755A3238755932397564484A70596935686458526F4C6D4A685932746C626D527A4C6B31765A475673516D466A613256755A434973496C39686458526F5833567A5A584A66615751694F6A4639, '2018-08-06 06:50:47');

-- ----------------------------
-- Table structure for web_actions
-- ----------------------------
DROP TABLE IF EXISTS `web_actions`;
CREATE TABLE `web_actions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_bin NOT NULL,
  `subject` varchar(100) COLLATE utf8_bin NOT NULL,
  `message` varchar(250) COLLATE utf8_bin NOT NULL,
  `recovery_notice` tinyint(1) NOT NULL,
  `recovery_subject` varchar(100) COLLATE utf8_bin NOT NULL,
  `recovery_message` varchar(250) COLLATE utf8_bin NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_actions
-- ----------------------------

-- ----------------------------
-- Table structure for web_actions_condition_list
-- ----------------------------
DROP TABLE IF EXISTS `web_actions_condition_list`;
CREATE TABLE `web_actions_condition_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `actions_id` int(11) NOT NULL,
  `conditions_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `actions_id` (`actions_id`,`conditions_id`),
  KEY `web_actions_condition_list_29a087ae` (`actions_id`),
  KEY `web_actions_condition_list_0bd39122` (`conditions_id`),
  CONSTRAINT `web_actions_condition_conditions_id_5a6a40f_fk_web_conditions_id` FOREIGN KEY (`conditions_id`) REFERENCES `web_conditions` (`id`),
  CONSTRAINT `web_actions_condition_list_actions_id_ed174c7_fk_web_actions_id` FOREIGN KEY (`actions_id`) REFERENCES `web_actions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_actions_condition_list
-- ----------------------------

-- ----------------------------
-- Table structure for web_actions_operation_list
-- ----------------------------
DROP TABLE IF EXISTS `web_actions_operation_list`;
CREATE TABLE `web_actions_operation_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `actions_id` int(11) NOT NULL,
  `operations_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `actions_id` (`actions_id`,`operations_id`),
  KEY `web_actions_operation_list_29a087ae` (`actions_id`),
  KEY `web_actions_operation_list_75ca764d` (`operations_id`),
  CONSTRAINT `web_actions_operatio_operations_id_11d44de1_fk_web_operations_id` FOREIGN KEY (`operations_id`) REFERENCES `web_operations` (`id`),
  CONSTRAINT `web_actions_operation_list_actions_id_5e48dc2b_fk_web_actions_id` FOREIGN KEY (`actions_id`) REFERENCES `web_actions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_actions_operation_list
-- ----------------------------

-- ----------------------------
-- Table structure for web_conditions
-- ----------------------------
DROP TABLE IF EXISTS `web_conditions`;
CREATE TABLE `web_conditions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_bin NOT NULL,
  `data_type` varchar(32) COLLATE utf8_bin NOT NULL,
  `threshold` varchar(64) COLLATE utf8_bin NOT NULL,
  `formula_id` int(11),
  `item_id` int(11) NOT NULL,
  `operator_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `web_conditions_31082a44` (`formula_id`),
  KEY `web_conditions_82bfda79` (`item_id`),
  KEY `web_conditions_4d14a16b` (`operator_id`),
  CONSTRAINT `web_conditions_formula_id_3aa376_fk_web_formulas_id` FOREIGN KEY (`formula_id`) REFERENCES `web_formulas` (`id`),
  CONSTRAINT `web_conditions_item_id_743bc7e2_fk_web_items_id` FOREIGN KEY (`item_id`) REFERENCES `web_items` (`id`),
  CONSTRAINT `web_conditions_operator_id_69a50e5d_fk_web_operators_id` FOREIGN KEY (`operator_id`) REFERENCES `web_operators` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_conditions
-- ----------------------------
INSERT INTO `web_conditions` VALUES ('1', 'LinuxTemplate.linux.cpu.idle', 'int', '20', '1', '2', '1');
INSERT INTO `web_conditions` VALUES ('2', 'LinuxTemplate.linux.memory', 'int', '95', '1', '7', '3');

-- ----------------------------
-- Table structure for web_formulas
-- ----------------------------
DROP TABLE IF EXISTS `web_formulas`;
CREATE TABLE `web_formulas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_bin NOT NULL,
  `key` varchar(64) COLLATE utf8_bin NOT NULL,
  `memo` longtext COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_formulas
-- ----------------------------
INSERT INTO `web_formulas` VALUES ('1', '最近5分钟平均值', 'avg_5', 0xE6B58BE8AF95E6B58BE8AF95);
INSERT INTO `web_formulas` VALUES ('2', '最近30分钟超过次数', 'tigger_time_30', 0x7465737420E6B58BE8AF95);

-- ----------------------------
-- Table structure for web_graphs
-- ----------------------------
DROP TABLE IF EXISTS `web_graphs`;
CREATE TABLE `web_graphs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_bin NOT NULL,
  `graph_type` varchar(50) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_graphs
-- ----------------------------

-- ----------------------------
-- Table structure for web_graphs_datasets
-- ----------------------------
DROP TABLE IF EXISTS `web_graphs_datasets`;
CREATE TABLE `web_graphs_datasets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `graphs_id` int(11) NOT NULL,
  `items_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `graphs_id` (`graphs_id`,`items_id`),
  KEY `web_graphs_datasets_45e6d2f5` (`graphs_id`),
  KEY `web_graphs_datasets_475535d3` (`items_id`),
  CONSTRAINT `web_graphs_datasets_graphs_id_547474fa_fk_web_graphs_id` FOREIGN KEY (`graphs_id`) REFERENCES `web_graphs` (`id`),
  CONSTRAINT `web_graphs_datasets_items_id_66723a0a_fk_web_items_id` FOREIGN KEY (`items_id`) REFERENCES `web_items` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_graphs_datasets
-- ----------------------------

-- ----------------------------
-- Table structure for web_group
-- ----------------------------
DROP TABLE IF EXISTS `web_group`;
CREATE TABLE `web_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_bin NOT NULL,
  `display_name` varchar(50) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_group
-- ----------------------------

-- ----------------------------
-- Table structure for web_group_template_list
-- ----------------------------
DROP TABLE IF EXISTS `web_group_template_list`;
CREATE TABLE `web_group_template_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `templates_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`templates_id`),
  KEY `web_group_template_list_0e939a4f` (`group_id`),
  KEY `web_group_template_list_d8dfa94a` (`templates_id`),
  CONSTRAINT `web_group_template_lis_templates_id_45ef74e1_fk_web_templates_id` FOREIGN KEY (`templates_id`) REFERENCES `web_templates` (`id`),
  CONSTRAINT `web_group_template_list_group_id_6ca9dba3_fk_web_group_id` FOREIGN KEY (`group_id`) REFERENCES `web_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_group_template_list
-- ----------------------------

-- ----------------------------
-- Table structure for web_host
-- ----------------------------
DROP TABLE IF EXISTS `web_host`;
CREATE TABLE `web_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(50) COLLATE utf8_bin NOT NULL,
  `display_name` varchar(50) COLLATE utf8_bin NOT NULL,
  `ip` char(15) COLLATE utf8_bin NOT NULL,
  `port` int(11) NOT NULL,
  `os` varchar(20) COLLATE utf8_bin NOT NULL,
  `status_monitor_on` tinyint(1) NOT NULL,
  `snmp_on` tinyint(1) NOT NULL,
  `snmp_version` varchar(10) COLLATE utf8_bin NOT NULL,
  `snmp_community_name` varchar(50) COLLATE utf8_bin NOT NULL,
  `snmp_security_level` varchar(50) COLLATE utf8_bin NOT NULL,
  `snmp_auth_protocol` varchar(50) COLLATE utf8_bin NOT NULL,
  `snmp_user` varchar(50) COLLATE utf8_bin NOT NULL,
  `snmp_pass` varchar(50) COLLATE utf8_bin NOT NULL,
  `child_of_id` int(11),
  `idc_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  UNIQUE KEY `display_name` (`display_name`),
  UNIQUE KEY `ip` (`ip`),
  KEY `web_host_bf4ce882` (`child_of_id`),
  KEY `web_host_0869e37a` (`idc_id`),
  CONSTRAINT `web_host_child_of_id_74d6fa1_fk_web_trunkservers_id` FOREIGN KEY (`child_of_id`) REFERENCES `web_trunkservers` (`id`),
  CONSTRAINT `web_host_idc_id_60b31754_fk_web_idc_id` FOREIGN KEY (`idc_id`) REFERENCES `web_idc` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_host
-- ----------------------------
INSERT INTO `web_host` VALUES ('1', 'TestServer', 'TestServer ubuntu主机', '192.168.1.234', '22612', 'linux', '1', '1', '2c', 'public', 'auth', 'MD5', 'triaquae_snmp', 'my_pass', null, '1');

-- ----------------------------
-- Table structure for web_host_custom_services
-- ----------------------------
DROP TABLE IF EXISTS `web_host_custom_services`;
CREATE TABLE `web_host_custom_services` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_id` int(11) NOT NULL,
  `services_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `host_id` (`host_id`,`services_id`),
  KEY `web_host_custom_services_8396f175` (`host_id`),
  KEY `web_host_custom_services_658bf95e` (`services_id`),
  CONSTRAINT `web_host_custom_services_host_id_46809e26_fk_web_host_id` FOREIGN KEY (`host_id`) REFERENCES `web_host` (`id`),
  CONSTRAINT `web_host_custom_services_services_id_44964d38_fk_web_services_id` FOREIGN KEY (`services_id`) REFERENCES `web_services` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_host_custom_services
-- ----------------------------

-- ----------------------------
-- Table structure for web_host_group
-- ----------------------------
DROP TABLE IF EXISTS `web_host_group`;
CREATE TABLE `web_host_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `host_id` (`host_id`,`group_id`),
  KEY `web_host_group_8396f175` (`host_id`),
  KEY `web_host_group_0e939a4f` (`group_id`),
  CONSTRAINT `web_host_group_group_id_58271eb7_fk_web_group_id` FOREIGN KEY (`group_id`) REFERENCES `web_group` (`id`),
  CONSTRAINT `web_host_group_host_id_3a19da51_fk_web_host_id` FOREIGN KEY (`host_id`) REFERENCES `web_host` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_host_group
-- ----------------------------

-- ----------------------------
-- Table structure for web_host_template_list
-- ----------------------------
DROP TABLE IF EXISTS `web_host_template_list`;
CREATE TABLE `web_host_template_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_id` int(11) NOT NULL,
  `templates_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `host_id` (`host_id`,`templates_id`),
  KEY `web_host_template_list_8396f175` (`host_id`),
  KEY `web_host_template_list_d8dfa94a` (`templates_id`),
  CONSTRAINT `web_host_template_list_host_id_338c8e91_fk_web_host_id` FOREIGN KEY (`host_id`) REFERENCES `web_host` (`id`),
  CONSTRAINT `web_host_template_list_templates_id_d6cc6b5_fk_web_templates_id` FOREIGN KEY (`templates_id`) REFERENCES `web_templates` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_host_template_list
-- ----------------------------
INSERT INTO `web_host_template_list` VALUES ('1', '1', '1');

-- ----------------------------
-- Table structure for web_idc
-- ----------------------------
DROP TABLE IF EXISTS `web_idc`;
CREATE TABLE `web_idc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_idc
-- ----------------------------
INSERT INTO `web_idc` VALUES ('1', '中山联通机房');

-- ----------------------------
-- Table structure for web_items
-- ----------------------------
DROP TABLE IF EXISTS `web_items`;
CREATE TABLE `web_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_bin NOT NULL,
  `key` varchar(100) COLLATE utf8_bin NOT NULL,
  `data_type` varchar(50) COLLATE utf8_bin NOT NULL,
  `unit` varchar(30) COLLATE utf8_bin NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_items
-- ----------------------------
INSERT INTO `web_items` VALUES ('1', 'linux.cpu.iowait', 'linux.cpu.iowait', 'integer', '%', '1');
INSERT INTO `web_items` VALUES ('2', 'linux.cpu.idle', 'linux.cpu.idle', 'integer', '%', '1');
INSERT INTO `web_items` VALUES ('3', 'linux.cpu.usage', 'linux.cpu.usage', 'integer', '%', '1');
INSERT INTO `web_items` VALUES ('4', 'linux.memory.free', 'linux.memory.free', 'integer', '%', '1');
INSERT INTO `web_items` VALUES ('5', 'linux.memory.cached', 'linux.memory.cached', 'integer', '%', '1');
INSERT INTO `web_items` VALUES ('6', 'linux.memory.total', 'linux.memory.total', 'integer', '%', '1');
INSERT INTO `web_items` VALUES ('7', 'linux.memory.usage', 'linux.memory.usage', 'integer', '%', '1');

-- ----------------------------
-- Table structure for web_operations
-- ----------------------------
DROP TABLE IF EXISTS `web_operations`;
CREATE TABLE `web_operations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `send_via` varchar(30) COLLATE utf8_bin NOT NULL,
  `notice_times` int(11) NOT NULL,
  `notice_interval` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_operations
-- ----------------------------

-- ----------------------------
-- Table structure for web_operations_send_to_groups
-- ----------------------------
DROP TABLE IF EXISTS `web_operations_send_to_groups`;
CREATE TABLE `web_operations_send_to_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operations_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `operations_id` (`operations_id`,`group_id`),
  KEY `web_operations_send_to_groups_75ca764d` (`operations_id`),
  KEY `web_operations_send_to_groups_0e939a4f` (`group_id`),
  CONSTRAINT `web_operations_send__operations_id_50290d84_fk_web_operations_id` FOREIGN KEY (`operations_id`) REFERENCES `web_operations` (`id`),
  CONSTRAINT `web_operations_send_to_groups_group_id_44463d38_fk_web_group_id` FOREIGN KEY (`group_id`) REFERENCES `web_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_operations_send_to_groups
-- ----------------------------

-- ----------------------------
-- Table structure for web_operations_send_to_users
-- ----------------------------
DROP TABLE IF EXISTS `web_operations_send_to_users`;
CREATE TABLE `web_operations_send_to_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operations_id` int(11) NOT NULL,
  `userprofile_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `operations_id` (`operations_id`,`userprofile_id`),
  KEY `web_operations_send_to_users_75ca764d` (`operations_id`),
  KEY `web_operations_send_to_users_9c2a73e9` (`userprofile_id`),
  CONSTRAINT `web_operations_sen_userprofile_id_3029dfd8_fk_web_userprofile_id` FOREIGN KEY (`userprofile_id`) REFERENCES `web_userprofile` (`id`),
  CONSTRAINT `web_operations_send__operations_id_1c8b0ec7_fk_web_operations_id` FOREIGN KEY (`operations_id`) REFERENCES `web_operations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_operations_send_to_users
-- ----------------------------

-- ----------------------------
-- Table structure for web_operators
-- ----------------------------
DROP TABLE IF EXISTS `web_operators`;
CREATE TABLE `web_operators` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_bin NOT NULL,
  `key` varchar(32) COLLATE utf8_bin NOT NULL,
  `memo` longtext COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_operators
-- ----------------------------
INSERT INTO `web_operators` VALUES ('1', '小于', 'lt', 0xE6B58BE8AF95E6B58BE8AF95);
INSERT INTO `web_operators` VALUES ('2', '大于', '95', 0xE6B58BE8AF95E6B58BE8AF95);
INSERT INTO `web_operators` VALUES ('3', '大于运算符', 'gt', 0xE6B58BE8AF95E6B58BE8AF95);

-- ----------------------------
-- Table structure for web_serverstatus
-- ----------------------------
DROP TABLE IF EXISTS `web_serverstatus`;
CREATE TABLE `web_serverstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(100) COLLATE utf8_bin NOT NULL,
  `host_status` varchar(10) COLLATE utf8_bin NOT NULL,
  `ping_status` varchar(100) COLLATE utf8_bin NOT NULL,
  `last_check` varchar(100) COLLATE utf8_bin NOT NULL,
  `host_uptime` varchar(50) COLLATE utf8_bin NOT NULL,
  `attempt_count` int(11) NOT NULL,
  `breakdown_count` int(11) NOT NULL,
  `up_count` int(11) NOT NULL,
  `snmp_alert_count` int(11) NOT NULL,
  `availability` varchar(20) COLLATE utf8_bin NOT NULL,
  `host_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `host_id` (`host_id`),
  CONSTRAINT `web_serverstatus_host_id_11e5ed66_fk_web_host_id` FOREIGN KEY (`host_id`) REFERENCES `web_host` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_serverstatus
-- ----------------------------

-- ----------------------------
-- Table structure for web_servicelist
-- ----------------------------
DROP TABLE IF EXISTS `web_servicelist`;
CREATE TABLE `web_servicelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_bin NOT NULL,
  `check_interval` int(11) NOT NULL,
  `description` longtext COLLATE utf8_bin NOT NULL,
  `service_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `web_servicelist_b0dc1e29` (`service_id`),
  CONSTRAINT `web_servicelist_service_id_5ae408db_fk_web_services_id` FOREIGN KEY (`service_id`) REFERENCES `web_services` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_servicelist
-- ----------------------------
INSERT INTO `web_servicelist` VALUES ('1', 'LinuxTemplate.linux.cpu', '30', 0xE6B58BE8AF95E6B58BE8AF95, '1');
INSERT INTO `web_servicelist` VALUES ('2', 'LinuxTemplate.linux.memory', '50', 0xE6B58BE8AF95E6B58BE8AF95, '2');

-- ----------------------------
-- Table structure for web_servicelist_conditons
-- ----------------------------
DROP TABLE IF EXISTS `web_servicelist_conditons`;
CREATE TABLE `web_servicelist_conditons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `servicelist_id` int(11) NOT NULL,
  `conditions_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `servicelist_id` (`servicelist_id`,`conditions_id`),
  KEY `web_servicelist_conditons_3c412b2e` (`servicelist_id`),
  KEY `web_servicelist_conditons_0bd39122` (`conditions_id`),
  CONSTRAINT `web_servicelist_co_servicelist_id_4f7438c5_fk_web_servicelist_id` FOREIGN KEY (`servicelist_id`) REFERENCES `web_servicelist` (`id`),
  CONSTRAINT `web_servicelist_cond_conditions_id_5359ca8f_fk_web_conditions_id` FOREIGN KEY (`conditions_id`) REFERENCES `web_conditions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_servicelist_conditons
-- ----------------------------
INSERT INTO `web_servicelist_conditons` VALUES ('1', '1', '1');
INSERT INTO `web_servicelist_conditons` VALUES ('5', '2', '2');

-- ----------------------------
-- Table structure for web_services
-- ----------------------------
DROP TABLE IF EXISTS `web_services`;
CREATE TABLE `web_services` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_bin NOT NULL,
  `monitor_type` varchar(50) COLLATE utf8_bin NOT NULL,
  `plugin` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_services
-- ----------------------------
INSERT INTO `web_services` VALUES ('1', 'linux.cpu', 'agent', 'LinuxCpu');
INSERT INTO `web_services` VALUES ('2', 'linux.memory', 'agent', 'LinuxMemory');

-- ----------------------------
-- Table structure for web_services_item_list
-- ----------------------------
DROP TABLE IF EXISTS `web_services_item_list`;
CREATE TABLE `web_services_item_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `services_id` int(11) NOT NULL,
  `items_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `services_id` (`services_id`,`items_id`),
  KEY `web_services_item_list_658bf95e` (`services_id`),
  KEY `web_services_item_list_475535d3` (`items_id`),
  CONSTRAINT `web_services_item_list_items_id_368826ff_fk_web_items_id` FOREIGN KEY (`items_id`) REFERENCES `web_items` (`id`),
  CONSTRAINT `web_services_item_list_services_id_79bbbd70_fk_web_services_id` FOREIGN KEY (`services_id`) REFERENCES `web_services` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_services_item_list
-- ----------------------------
INSERT INTO `web_services_item_list` VALUES ('1', '1', '1');
INSERT INTO `web_services_item_list` VALUES ('2', '1', '2');
INSERT INTO `web_services_item_list` VALUES ('3', '1', '3');
INSERT INTO `web_services_item_list` VALUES ('4', '2', '4');
INSERT INTO `web_services_item_list` VALUES ('5', '2', '5');
INSERT INTO `web_services_item_list` VALUES ('6', '2', '6');
INSERT INTO `web_services_item_list` VALUES ('7', '2', '7');

-- ----------------------------
-- Table structure for web_templates
-- ----------------------------
DROP TABLE IF EXISTS `web_templates`;
CREATE TABLE `web_templates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_templates
-- ----------------------------
INSERT INTO `web_templates` VALUES ('1', 'LinuxTemplate');

-- ----------------------------
-- Table structure for web_templates_graph_list
-- ----------------------------
DROP TABLE IF EXISTS `web_templates_graph_list`;
CREATE TABLE `web_templates_graph_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `templates_id` int(11) NOT NULL,
  `graphs_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `templates_id` (`templates_id`,`graphs_id`),
  KEY `web_templates_graph_list_d8dfa94a` (`templates_id`),
  KEY `web_templates_graph_list_45e6d2f5` (`graphs_id`),
  CONSTRAINT `web_templates_graph_li_templates_id_6c5c54b8_fk_web_templates_id` FOREIGN KEY (`templates_id`) REFERENCES `web_templates` (`id`),
  CONSTRAINT `web_templates_graph_list_graphs_id_6bd0096f_fk_web_graphs_id` FOREIGN KEY (`graphs_id`) REFERENCES `web_graphs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_templates_graph_list
-- ----------------------------

-- ----------------------------
-- Table structure for web_templates_service_list
-- ----------------------------
DROP TABLE IF EXISTS `web_templates_service_list`;
CREATE TABLE `web_templates_service_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `templates_id` int(11) NOT NULL,
  `servicelist_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `templates_id` (`templates_id`,`servicelist_id`),
  KEY `web_templates_service_list_d8dfa94a` (`templates_id`),
  KEY `web_templates_service_list_3c412b2e` (`servicelist_id`),
  CONSTRAINT `web_templates_serv_servicelist_id_59c2e2d9_fk_web_servicelist_id` FOREIGN KEY (`servicelist_id`) REFERENCES `web_servicelist` (`id`),
  CONSTRAINT `web_templates_service__templates_id_7ea691a1_fk_web_templates_id` FOREIGN KEY (`templates_id`) REFERENCES `web_templates` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_templates_service_list
-- ----------------------------
INSERT INTO `web_templates_service_list` VALUES ('1', '1', '1');
INSERT INTO `web_templates_service_list` VALUES ('2', '1', '2');

-- ----------------------------
-- Table structure for web_trunkservers
-- ----------------------------
DROP TABLE IF EXISTS `web_trunkservers`;
CREATE TABLE `web_trunkservers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_bin NOT NULL,
  `description` varchar(150) COLLATE utf8_bin NOT NULL,
  `ip_address` char(15) COLLATE utf8_bin NOT NULL,
  `port` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_trunkservers
-- ----------------------------

-- ----------------------------
-- Table structure for web_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `web_userprofile`;
CREATE TABLE `web_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(75) COLLATE utf8_bin NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `web_userprofile_user_id_77b33737_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of web_userprofile
-- ----------------------------
