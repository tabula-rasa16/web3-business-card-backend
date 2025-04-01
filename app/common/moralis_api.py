from moralis import evm_api
from app import app

api_key = app.config["MORALIS_API_KEY"]

# 获取钱包的token信息
def get_token_balance(wallet_address, chain, token_addresses=[], limit= 100):

    params = {
        "chain": chain,
        "address": wallet_address,
        "token_addresses": token_addresses if token_addresses else [],
        "limit": limit if limit else 100
    }

    result = evm_api.wallets.get_wallet_token_balances_price(
        api_key=api_key,
        params=params,
    )
    print(result)
    return result


# 获取钱包的nft信息
def get_wallet_nfts(wallet_address, chain="eth", format="decimal", limit= 100, exclude_spam=True, token_addresses= [], normalizeMetadata=True, media_items=False, include_prices=False):


    params = {
    "chain": chain,
    "format": format if format else "decimal",
    "media_items": media_items if media_items else False,
    "address": wallet_address,
    "exclude_spam": exclude_spam if exclude_spam else True,
    "include_prices": include_prices if include_prices else False,
    "limit": limit if limit else 100,
    "token_addresses": token_addresses if token_addresses else [],
    "normalizeMetadata": normalizeMetadata if normalizeMetadata else True
    }

    result = evm_api.nft.get_wallet_nfts(
    api_key=api_key,
    params=params,
    )

    print(result)
    return result
