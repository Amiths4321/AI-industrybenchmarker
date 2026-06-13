# run_benchmarker.py
from dotenv import load_dotenv
load_dotenv()

from core.ratios_calculator import RatiosCalculator
from reporting.plotter import BenchmarkPlotter
from reporting.narrative import IndustryAnalysisNarrativeEngine

def main():
    print("=============================================================")
    # Mock input entry data profile mapping standard company financials
    # (e.g., Gross Margin comes out to 34.0% vs Industry baseline 42.0%)
    input_company_data = {
        "Revenue": 500000,
        "Operational_Cost": 330000,
        "Net_Profit": 60000,
        "Processing_Cycle_Days": 112.5
    }
    
    print("🚀 Initializing Standalone Sector Benchmarking Diagnostics...")
    
    # Run analytics comparisons
    metrics_dataframe = RatiosCalculator.process_company_metrics(input_company_data)
    
    # Output visual graphics
    BenchmarkPlotter.render_twin_panels(metrics_dataframe, "benchmark_metrics.png")
    print("💾 Analysis visual matrix successfully rendered to disk as 'benchmark_metrics.png'.")
    
    # Generate executive brief summary report
    engine = IndustryAnalysisNarrativeEngine()
    narrative_report = engine.run_strategic_appraisal(metrics_dataframe)
    
    print("\n=============================================================")
    print("                SECTOR BENCHMARK REPORT OUTPUT               ")
    print("=============================================================\n")
    print(narrative_report)
    print("\n=============================================================")

if __name__ == "__main__":
    main()