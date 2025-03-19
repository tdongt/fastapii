-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT current_timestamp(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6) COMMENT '更新时间',
  `name` varchar(20) DEFAULT NULL COMMENT '用户名',
  `typee` tinyint(1) NOT NULL DEFAULT 0 COMMENT '用户类型 True:管理员 False:普通用户',
  `passwd` varchar(255) DEFAULT NULL,
  `nickname` varchar(255) NOT NULL DEFAULT 'nait用户' COMMENT '昵称',
  `phone` varchar(11) DEFAULT NULL COMMENT '电话',
  `email` varchar(255) DEFAULT NULL COMMENT '邮箱',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='用户表';