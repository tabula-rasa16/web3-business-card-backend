CREATE DATABASE `web3-business-card` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

-- `web3-business-card`.business_cards definition

CREATE TABLE `business_cards` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '所属⽤⼾ ID',
  `display_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '名⽚显⽰名称',
  `company` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '公司名称',
  `job_title` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '职位',
  `website_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '个⼈⽹站',
  `portfolio_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '作品集链接',
  `debox_account` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'debox账户',
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系邮箱',
  `phone` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '⼿机号',
  `data_status` smallint DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='名片表';


-- `web3-business-card`.card_collection definition

CREATE TABLE `card_collection` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `owner_id` bigint unsigned NOT NULL COMMENT '收藏名⽚的⽤⼾ ID',
  `card_id` bigint unsigned NOT NULL COMMENT '被收藏的名⽚ ID',
  `added_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
  `data_status` smallint DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_card` (`owner_id`,`card_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='名片收藏夹表';


-- `web3-business-card`.comments definition

CREATE TABLE `comments` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '评论⽤⼾ ID',
  `post_id` bigint unsigned NOT NULL COMMENT '评论的动态 ID',
  `parent_id` bigint unsigned DEFAULT '0' COMMENT '其父评论ID, 无父评论默认值为0',
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '评论内容',
  `data_status` smallint DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '评论时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评论表';


-- `web3-business-card`.digital_assets definition

CREATE TABLE `digital_assets` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '所属⽤⼾ ID',
  `asset_type` enum('NFT','TOKEN','OTHER') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '资产类型',
  `contract_address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '合约地址',
  `token_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Token ID（如果是 NFT）',
  `amount` decimal(30,10) DEFAULT NULL COMMENT '持有数量（如果是代币）',
  `asset_metadata` json DEFAULT NULL COMMENT '资产元数据（JSON 存储）',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
  `data_status` smallint DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数字资产信息表';


-- `web3-business-card`.follows definition

CREATE TABLE `follows` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `follower_id` bigint unsigned NOT NULL COMMENT '关注者⽤⼾ ID',
  `following_id` bigint unsigned NOT NULL COMMENT '被关注者⽤⼾ ID',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '关注时间',
  `data_status` smallint DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_follow` (`follower_id`,`following_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户关注关系表';


-- `web3-business-card`.likes definition

CREATE TABLE `likes` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '点赞⽤⼾ ID',
  `post_id` bigint unsigned NOT NULL COMMENT '被点赞的动态 ID',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '点赞时间',
  `data_status` smallint DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_like` (`user_id`,`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='点赞表';


-- `web3-business-card`.posts definition

CREATE TABLE `posts` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '发布动态的⽤⼾ ID',
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '动态内容',
  `media_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '附加图⽚或视频 URL',
  `data_status` smallint DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='动态发布表';


-- `web3-business-card`.social_accounts definition

CREATE TABLE `social_accounts` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '⽤⼾ ID',
  `platform` enum('twitter','linkedin','github','wechat','telegram','facebook','instagram','other') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '社交平台',
  `account_handle` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '社交账号标识',
  `profile_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '社交主⻚链接',
  `data_status` smallint DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='社交账户表';


-- `web3-business-card`.sys_user definition

CREATE TABLE `sys_user` (
  `user_id` bigint NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `user_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户账号',
  `nick_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户昵称',
  `user_type` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '00' COMMENT '用户类型（00系统用户）',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '用户邮箱',
  `phonenumber` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '手机号码',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '密码',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '0' COMMENT '帐号状态（0正常 1停用）',
  `del_flag` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  `login_ip` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '最后登录IP',
  `login_date` datetime DEFAULT NULL COMMENT '最后登录时间',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理员用户信息表';


-- `web3-business-card`.t_pending_review_content definition

CREATE TABLE `t_pending_review_content` (
  `id` bigint NOT NULL COMMENT 'id',
  `rel_user_wallet_address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '对应用户的钱包地址',
  `profile_pic` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像图片',
  `personal_description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '个人简介',
  `s1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s4` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s5` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s6` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s7` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s8` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s10` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s11` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s12` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s13` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s14` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s15` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s16` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s17` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s18` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s19` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `s20` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sf1` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `sf2` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `i81` bigint DEFAULT NULL,
  `i82` bigint DEFAULT NULL,
  `i83` bigint DEFAULT NULL,
  `i84` bigint DEFAULT NULL,
  `i85` bigint DEFAULT NULL,
  `i41` int DEFAULT NULL,
  `i42` int DEFAULT NULL,
  `i43` int DEFAULT NULL,
  `i44` int DEFAULT NULL,
  `i45` int DEFAULT NULL,
  `i21` smallint DEFAULT NULL,
  `i22` smallint DEFAULT NULL,
  `i23` smallint DEFAULT NULL,
  `i24` smallint DEFAULT NULL,
  `i25` smallint DEFAULT NULL,
  `t1` date DEFAULT NULL,
  `t2` date DEFAULT NULL,
  `t3` timestamp NULL DEFAULT NULL,
  `t4` timestamp NULL DEFAULT NULL,
  `t5` timestamp(6) NULL DEFAULT NULL,
  `t6` timestamp NULL DEFAULT NULL,
  `review_status` smallint DEFAULT NULL COMMENT '审核状态：0待审核，1审核通过，2未过审',
  `last_review_time` datetime DEFAULT NULL COMMENT '最近审核时间',
  `fail_cause` smallint DEFAULT NULL COMMENT '未过审原因',
  `review_remarks` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '未过审说明',
  `data_status` smallint DEFAULT NULL,
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT NULL,
  `edit_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='待审核内容表';


-- `web3-business-card`.t_social_media definition

CREATE TABLE `t_social_media` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'app名称',
  `app_type` smallint DEFAULT NULL COMMENT '预留，后续可对应字典表【dict_key】',
  `app_key` int DEFAULT NULL COMMENT '标签key',
  `style` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '对应前端展示样式',
  `data_status` smallint DEFAULT '0' COMMENT '数据状态',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `creator` bigint DEFAULT NULL COMMENT 'user_id',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='社交软件类别表';


-- `web3-business-card`.t_user_feedback definition

CREATE TABLE `t_user_feedback` (
  `id` bigint NOT NULL COMMENT 'id',
  `rel_user_wallet_address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '对应用户的钱包地址',
  `feedback_content` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户反馈内容',
  `rel_record_id` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '关联记录号',
  `satisfaction` smallint DEFAULT NULL COMMENT '用户满意度等级',
  `handle_status` smallint DEFAULT NULL COMMENT '处理状态：0待处理，1处理完成',
  `data_status` smallint DEFAULT NULL,
  `job_number` bigint DEFAULT NULL COMMENT '处理人工号',
  `remark` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '处理人回复内容',
  `create_time` timestamp NULL DEFAULT NULL,
  `edit_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户反馈表';


-- `web3-business-card`.users definition

CREATE TABLE `users` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `wallet_address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '区块链钱包地址（唯⼀标识）',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '⽤⼾名',
  `avatar_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像 URL',
  `gender` enum('male','female','other') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '性别',
  `bio` text COLLATE utf8mb4_unicode_ci COMMENT '个⼈介绍',
  `data_status` smallint DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `wallet_address` (`wallet_address`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';




INSERT INTO `web3-business-card`.users
(wallet_address, username, avatar_url, gender, bio)
VALUES('0x2F2aCcF905b2Af0dFd448B9c816754f411A6DEB3', '张三', 'https://th.bing.com/th/id/OIP.7GLMYPqMlt2LgkbPsOnDIAAAAA?rs=1&pid=ImgDetMain', 'male', '这里是我的个人简介');
INSERT INTO `web3-business-card`.users
(wallet_address, username, avatar_url, gender, bio)
VALUES('0xCDD52806557259B590FB07273933dDdD76d0C43A', '王五', NULL, NULL, '这是修改后的简介');

INSERT INTO `web3-business-card`.business_cards
(user_id, display_name, company, job_title, website_url, portfolio_url, debox_account, email, phone, data_status)
VALUES(1, '张三的名片-改', 'Debox', '项目经理', 'https://www.baidu.com', 'https://a.520gexing.com/uploads/allimg/2021042109/uqaqhuvavt0.jpg', '1q2we', '123456@qq.com', '+86 13823456780', 0);

INSERT INTO `web3-business-card`.social_accounts
(user_id, platform, account_handle, profile_url, data_status)
VALUES(1, 'wechat', 'user1', 'https://wechat.com/user1', 0);
INSERT INTO `web3-business-card`.social_accounts
(user_id, platform, account_handle, profile_url, data_status)
VALUES(1, 'github', 'user1', 'https://github.com/user1', 0);
INSERT INTO `web3-business-card`.social_accounts
(user_id, platform, account_handle, profile_url, data_status)
VALUES(1, 'telegram', 'user1-t', 'https://telegram.com/user1', 0);


INSERT INTO `web3-business-card`.t_social_media
(app_name, app_type, app_key, `style`, data_status, remark, creator)
VALUES('twitter', NULL, 1, NULL, 0, NULL, NULL);
INSERT INTO `web3-business-card`.t_social_media
(app_name, app_type, app_key, `style`, data_status, remark, creator)
VALUES('linkedin', NULL, 2, NULL, 0, NULL, NULL);
INSERT INTO `web3-business-card`.t_social_media
(app_name, app_type, app_key, `style`, data_status, remark, creator)
VALUES('github', NULL, 3, NULL, 0, NULL, NULL);
INSERT INTO `web3-business-card`.t_social_media
(app_name, app_type, app_key, `style`, data_status, remark, creator)
VALUES('wechat', NULL, 4, NULL, 0, NULL, NULL);
INSERT INTO `web3-business-card`.t_social_media
(app_name, app_type, app_key, `style`, data_status, remark, creator)
VALUES('telegram', NULL, 5, NULL, 0, NULL, NULL);
INSERT INTO `web3-business-card`.t_social_media
(app_name, app_type, app_key, `style`, data_status, remark, creator)
VALUES('facebook', NULL, 6, NULL, 0, NULL, NULL);
INSERT INTO `web3-business-card`.t_social_media
(app_name, app_type, app_key, `style`, data_status, remark, creator)
VALUES('instagram', NULL, 7, NULL, 0, NULL, NULL);
INSERT INTO `web3-business-card`.t_social_media
(app_name, app_type, app_key, `style`, data_status, remark, creator)
VALUES('other', NULL, 8, NULL, 0, NULL, NULL);