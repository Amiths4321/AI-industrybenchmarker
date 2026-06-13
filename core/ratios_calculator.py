# core/ratios_calculator.py
import pandas as pd
from core.sector_repository import SectorRepository

class RatiosCalculator:
    @staticmethod
    def process_company_metrics(raw_data_dict):
        """
        Transforms raw operational stats into financial ratios, performs 
        variance mapping against industry markers, and highlights performance bands.
        """
        benchmarks = SectorRepository.get_market_benchmarks()
        
        # Calculate Company Proportions
        rev = raw_data_dict["Revenue"]
        ops_cost = raw_data_dict["Operational_Cost"]
        net_prof = raw_data_dict["Net_Profit"]
        
        company_metrics = {
            "Gross_Margin_Pct": ((rev - ops_cost) / rev) * 100,
            "Net_Margin_Pct": (net_prof / rev) * 100,
            "Overhead_Cost_Ratio": (ops_cost / rev) * 100,
            "Cycle_Time_Days": raw_data_dict["Processing_Cycle_Days"]
        }
        
        records = []
        for metric, market_avg in benchmarks.items():
            comp_val = company_metrics[metric]
            variance = comp_val - market_avg
            
            # Context-sensitive variance routing
            if metric in ["Gross_Margin_Pct", "Net_Margin_Pct"]:
                status = "OUTPERFORM" if variance >= 0 else "UNDERPERFORM"
            else:
                # For expenses and time cycle constraints, lower is optimal
                status = "OUTPERFORM" if variance <= 0 else "UNDERPERFORM"
                
            records.append({
                "Metric": metric,
                "Company_Value": comp_val,
                "Industry_Average": market_avg,
                "Variance": variance,
                "Status": status
            })
            
        return pd.DataFrame(records)