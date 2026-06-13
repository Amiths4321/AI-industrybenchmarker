# core/sector_repository.py

class SectorRepository:
    @staticmethod
    def get_market_benchmarks():
        """
        Standard sector thresholds. 
        Higher values are optimal for margins; lower is optimal for overhead/cycles.
        """
        return {
            "Gross_Margin_Pct": 42.0,       # Market Average Gross Margin: 42%
            "Net_Margin_Pct": 15.5,         # Market Average Net Margin: 15.5%
            "Overhead_Cost_Ratio": 35.0,    # Lower is better (Efficiency ceiling)
            "Cycle_Time_Days": 90.0         # Operations throughput time baseline
        }