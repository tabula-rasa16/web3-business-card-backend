ALTER TABLE business_cards ADD COLUMN share_token VARCHAR(36) UNIQUE;
ALTER TABLE business_cards ADD COLUMN shared_status smallint DEFAULT 0;

ALTER TABLE `web3-business-card`.digital_assets ADD name varchar(100) NULL COMMENT '名称';
ALTER TABLE `web3-business-card`.digital_assets CHANGE name name varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '名称' AFTER asset_type;
ALTER TABLE `web3-business-card`.digital_assets ADD is_display smallint DEFAULT 0 NOT NULL COMMENT '是否在名片中展示（0否，1是）';
ALTER TABLE `web3-business-card`.digital_assets CHANGE is_display is_display smallint DEFAULT 0 NOT NULL COMMENT '是否在名片中展示（0否，1是）' AFTER asset_metadata;
ALTER TABLE `web3-business-card`.digital_assets ADD `display_order` smallint DEFAULT 0 NOT NULL COMMENT '展示顺序，0最低，越大越高';
ALTER TABLE `web3-business-card`.digital_assets CHANGE `display_order` `display_order` smallint DEFAULT 0 NOT NULL COMMENT '展示顺序，0最低，越大越高' AFTER is_display;
ALTER TABLE `web3-business-card`.t_user_feedback CHANGE rel_user_wallet_address rel_user_id BIGINT UNSIGNED NOT NULL COMMENT '对应用户的钱包地址';
ALTER TABLE `web3-business-card`.t_user_feedback MODIFY COLUMN rel_user_id BIGINT UNSIGNED NOT NULL COMMENT '对应用户的钱包地址';
ALTER TABLE `web3-business-card`.t_user_feedback MODIFY COLUMN handle_status smallint DEFAULT 0 NULL COMMENT '处理状态：0待处理，1处理完成';
ALTER TABLE `web3-business-card`.t_user_feedback MODIFY COLUMN data_status smallint DEFAULT 0 NULL;
ALTER TABLE `web3-business-card`.t_user_feedback CHANGE edit_time update_time timestamp NULL;
ALTER TABLE `web3-business-card`.t_user_feedback MODIFY COLUMN create_time timestamp DEFAULT CURRENT_TIMESTAMP  NULL;
ALTER TABLE `web3-business-card`.t_user_feedback MODIFY COLUMN update_time timestamp DEFAULT CURRENT_TIMESTAMP  NULL;
ALTER TABLE `web3-business-card`.t_user_feedback MODIFY COLUMN id bigint auto_increment NOT NULL COMMENT 'id';