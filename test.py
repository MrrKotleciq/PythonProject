from classes.data_manager import DataManager
from classes.optimizer import Optimizer
from classes.strategies import SMAStrategy, TrendFollowingStrategy

data_manager = DataManager(start_date="2009-01-01", end_date="2017-01-01")
df = data_manager.get_clean_data("AAPL")

optimizer_sma = Optimizer(df, "SMA_Opt", SMAStrategy)
best_results_sma = optimizer_sma.run()

optimizer_TFS = Optimizer(df, "TFS_Opt", TrendFollowingStrategy)
best_results_TFS = optimizer_TFS.run()

print("\nSMA")
print(best_results_sma.head(10))
print("\nTFS")
print(best_results_TFS.head(10))