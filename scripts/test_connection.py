from datetime import date
from pathlib import Path
from thetadata import ThetaClient

env_file = Path(__file__).resolve().parent.parent / ".env"
client = ThetaClient(dataframe_type="pandas", dotenv_path=str(env_file))
eod = client.stock_history_eod(
    symbol="AAPL",
    start_date=date(2026, 9, 1),
    end_date=date(2026, 9, 4),
)
print(eod.columns.tolist())
print(eod.head())