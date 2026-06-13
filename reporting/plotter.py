# reporting/plotter.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class BenchmarkPlotter:
    @staticmethod
    def render_twin_panels(comparison_df, output_path="benchmark_metrics.png"):
        """Generates standalone visual comparison assets tracking performance vs market averages."""
        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(1, 2, figsize=(13, 5))
        fig.suptitle("Corporate Performance Matrix vs. Global Industry Averages", fontsize=14, fontweight='bold')
        
        # Left Panel: Profitability/Cost Margins Comparison
        ax1 = axes[0]
        ax1.set_title("Operational Proportions (%)")
        margin_df = comparison_df[comparison_df['Metric'].str.contains('Margin|Ratio')]
        
        plot_data = []
        for _, row in margin_df.iterrows():
            label = row["Metric"].replace("_Pct", "").replace("_", " ")
            plot_data.append({"Metric": label, "Source": "Your Data", "Value": row["Company_Value"]})
            plot_data.append({"Metric": label, "Source": "Industry Median", "Value": row["Industry_Average"]})
            
        sns.barplot(x="Metric", y="Value", hue="Source", data=pd.DataFrame(plot_data), ax=ax1, palette=["#2ca02c", "#7f7f7f"])
        ax1.set_ylabel("Percentage (%)")
        ax1.set_xlabel("")
        
        # Right Panel: Operational Cycle Efficiency Breakdown
        ax2 = axes[1]
        ax2.set_title("Throughput Latency Window (Days)")
        cycle_row = comparison_df[comparison_df['Metric'] == 'Cycle_Time_Days'].iloc[0]
        
        bars = ax2.barh([0, 1], [cycle_row["Company_Value"], cycle_row["Industry_Average"]], color=["#ff7f0e", "#7f7f7f"], height=0.4)
        ax2.set_yticks([0, 1])
        ax2.set_yticklabels(["Your Operations", "Industry Benchmark"])
        ax2.set_xlabel("Days Outstanding (Lower is Optimal)")
        
        for bar in bars:
            width = bar.get_width()
            ax2.text(width + 2, bar.get_y() + bar.get_height()/2, f'{width:.1f} Days', va='center', fontweight='bold')

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()