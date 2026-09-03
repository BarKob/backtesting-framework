import matplotlib.pyplot as plt
from strategy_and_backtest import Final_data, Benchmark_Final_data, Final_metrics, Benchmark_Final_metrics

#Visualization
fig, axes = plt.subplots(3, 1)

axes[0].set_title("Portfolio against Benchmark")
axes[1].set_title("Portfolio components")

for asset, data in list(Final_data.items())[:-1]:
    axes[1].plot(data, label = asset)

for benchmark_asset, data in list(Benchmark_Final_data.items())[:-1]:
    axes[0].plot(data, label = "Benchmark", lw = 4)

axes[0].plot(Final_data["Total_Portfolio_Value"].tolist(), label = "Portfolio Value")

axes[0].legend()
axes[1].legend()


metrics_text = "STRATEGY: \n" + "\n".join(f"{metric_name}:  {round(value, 2)}" for metric_name, value in Final_metrics.items())
benchmark_metrics_text = "BENCHMARK: \n" + "\n".join(f"{metric_name}:  {round(value, 2)}" for metric_name, value in Benchmark_Final_metrics.items())

axes[2].axis("off")
axes[2].text(0.35, 0.5, metrics_text, transform = axes[2].transAxes, verticalalignment = "center")
axes[2].text(0.65, 0.5, benchmark_metrics_text, transform = axes[2].transAxes, verticalalignment = "center")

plt.tight_layout()
plt.show()
