from datetime import date
from pathlib import Path
from thetadata import ThetaClient

env_file = Path(__file__).resolve().parent.parent / ".env"
client = ThetaClient(dataframe_type="pandas", dotenv_path=str(env_file))
chain = client.option_history_eod(
    symbol="AAPL",
    expiration=date(2026, 9,18),
    start_date=date(2026, 9, 2),
    end_date=date(2026, 9, 2),
)

print(len(chain))
print(chain.columns.tolist())
print(chain.head())

data_dir = Path(__file__).resolve().parent.parent / "data"
data_dir.mkdir(exist_ok=True)
chain.to_csv(data_dir / "AAPL_20260902_exp20260918.csv", index=False)