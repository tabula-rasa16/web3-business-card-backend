ALTER TABLE `web3-business-card`.digital_assets ADD chain_key varchar(100) NOT NULL;
ALTER TABLE `web3-business-card`.digital_assets CHANGE chain_key chain_key varchar(100) NOT NULL AFTER asset_metadata;
