import aiohttp
from typing import List, Dict, Optional

class DexScreenerClient:
    def __init__(self, api_url: str = "https://api.dexscreener.com/latest/dex/tokens/", token_address: Optional[str] = None):
        self.api_url = f"{api_url}{token_address}" if token_address else api_url

    async def get_transactions(self, token_address: Optional[str] = None) -> List[Dict]:
        url = self.api_url if token_address is None else f"{self.api_url}{token_address}"
        print(f"Requesting URL: {url}")  # Отладочный вывод
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    print(f"Response status: {response.status}")  # Отладочный вывод
                    if response.status != 200:
                        print(f"⚠ API Error: {response.status}")
                        return []
                    data = await response.json()
                    print(f"Response data: {data}")  # Отладочный вывод
                    pairs = data.get('pairs', [])
                    if not pairs:
                        print("⚠ API returned no pairs or data malformed.")
                        return []
                    return pairs
        except Exception as e:
            print(f"⚠ Exception while getting data: {e}")
            return []

    def filter_transactions(self, data: List[Dict], min_usd: float = 0, tx_type: str = 'buy') -> List[Dict]:
        result = []
        for pair in data:
            txns_m5 = pair.get('txns', {}).get('m5', {})
            if not isinstance(txns_m5, dict):
                print(f"⚠ Invalid transaction structure: {txns_m5}")
                continue

            txs = txns_m5.get('buys' if tx_type == 'buy' else 'sells', [])
            print(f"Transactions for {tx_type}: {txs}")  # Отладочный вывод

            if isinstance(txs, list):
                for tx in txs:
                    if not isinstance(tx, dict):
                        print(f"⚠ Invalid transaction: {tx}")
                        continue
                    if tx.get('usd', 0) >= min_usd:
                        result.append(tx)
            elif isinstance(txs, int):
                print(f"ℹ {tx_type.upper()} transactions in last 5 minutes: {txs}")
                result.append({
                    'type': tx_type,
                    'usd': f"Number of transactions: {txs}"
                })
            else:
                print(f"⚠ Expected list or int for transactions, got: {txs}")
                continue
        return result