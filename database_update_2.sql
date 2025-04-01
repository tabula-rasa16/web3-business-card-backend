CREATE TABLE `web3-business-card`.supported_chain (
	id INT UNSIGNED auto_increment NOT NULL COMMENT 'id',
	`key` varchar(100) NOT NULL COMMENT '链名称的key',
	descrpition varchar(100) NULL COMMENT '该链的描述',
	data_status smallint NOT NULL COMMENT '数据状态',
	created_at timestamp DEFAULT CURRENT_TIMESTAMP  NULL COMMENT '创建时间',
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP  NULL COMMENT '最后更新时间',
	CONSTRAINT supported_chain_pk PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;



INSERT INTO `web3-business-card`.supported_chain (`key`, descrpition, data_status) VALUES
('eth', 'ETH', 0),
('0x0', 'X0', 0),
('sepolia', 'SEPOLIA', 0),
('0xaa36a7', 'XAA36A7', 0),
('polygon', 'POLYGON', 0),
('0x89', 'X89', 0),
('bsc', 'BSC', 0),
('0x38', 'X38', 0),
('bsc testnet', 'BSC_TESTNET', 0),
('0x60', 'X60', 0),
('avalanche', 'AVALANCHE', 0),
('0xa86a', 'XA86A', 0),
('fantom', 'FANTOM', 0),
('0xfa', 'XFA', 0),
('palm', 'PALM', 0),
('0x2a05c308d', 'X2A05C308D', 0),
('cronos', 'CRONOS', 0),
('0x09', 'X09', 0),
('arbitrum', 'ARBITRUM', 0),
('0xa4b0', 'XA4B0', 0),
('chiliz', 'CHILIZ', 0),
('0x05b38', 'X05B38', 0),
('chiliz testnet', 'CHILIZ_TESTNET', 0),
('0x05b32', 'X05B32', 0),
('gnosis', 'GNOSIS', 0),
('0x64', 'X64', 0),
('gnosis testnet', 'GNOSIS_TESTNET', 0),
('0x27d8', 'X27D8', 0),
('base', 'BASE', 0),
('0x2005', 'X2005', 0),
('base sepolia', 'BASE_SEPOLIA', 0),
('0x04a34', 'X04A34', 0),
('optimism', 'OPTIMISM', 0),
('0xa', 'XA', 0),
('holesky', 'HOLESKY', 0),
('0x4268', 'X4268', 0),
('polygon amoy', 'POLYGON_AMOY', 0),
('0x03882', 'X03882', 0),
('linea', 'LINEA', 0),
('0xe708', 'XE708', 0),
('moonbeam', 'MOONBEAM', 0),
('0x504', 'X504', 0),
('moonriver', 'MOONRIVER', 0),
('0x505', 'X505', 0),
('moonbase', 'MOONBASE', 0),
('0x507', 'X507', 0),
('linea sepolia', 'LINEA_SEPOLIA', 0),
('0xe705', 'XE705', 0);

ALTER TABLE `web3-business-card`.digital_assets MODIFY COLUMN is_display smallint DEFAULT 0 NULL COMMENT '是否在名片中展示（0否，1是）';
ALTER TABLE `web3-business-card`.digital_assets MODIFY COLUMN display_order smallint DEFAULT 0 NULL COMMENT '展示顺序，0最低，越大越高';
