from src.data_loader import BinanceDataLoader

loader = BinanceDataLoader(symbol="BTCUSDT", depth_levels=10)

book = loader.get_order_book()
trades = loader.get_recent_trades()

print(book.head())
print(trades.head())
