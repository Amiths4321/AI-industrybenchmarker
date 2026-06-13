# reporting/narrative.py
import os
import requests

class IndustryAnalysisNarrativeEngine:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://10.22.39.192:11434")
        self.model_name = os.getenv("OLLAMA_MODEL_NAME", "qwen2.5-coder:14b")

    def run_strategic_appraisal(self, comparison_df):
        """Dispatches payload to remote processing model, fallback automatically handles timeouts/failures."""
        payload_data = comparison_df.to_string(index=False)
        system_prompt = (
            "You are an expert market positioning analyst.\n"
            "Review this raw benchmark data dataframe and structure an executive performance checklist.\n"
            "Explicitly emphasize where the subject is OUTPERFORMING or UNDERPERFORMING the industry averages."
        )

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Analyze these comparative industry metrics:\n\n{payload_data}"}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.1}
                },
                timeout=4  # ⚡ Hard-cap protection covering both socket links and generation waits
            )
            if response.status_code == 200:
                return response.json().get("message", {}).get("content", "Brief construction aborted.")
                
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            print("⚠️ Remote AI cluster unreachable/lagging. Activating Local Programmatic Verification Core...")
            return self._execute_deterministic_fallback(comparison_df)
        except Exception as e:
            return f"Fatal reporting runtime fault: {e}"

    def _execute_deterministic_fallback(self, df):
        """Constructs text outputs natively when remote nodes fail or timing windows close."""
        gross = df[df['Metric'] == 'Gross_Margin_Pct'].iloc[0]
        net = df[df['Metric'] == 'Net_Margin_Pct'].iloc[0]
        cycle = df[df['Metric'] == 'Cycle_Time_Days'].iloc[0]

        report = f"### 📊 STANDALONE INDUSTRY COMPETITOR APPRASIAL REPORT\n\n"
        report += "#### 🔍 VARIANCE & PERFORMANCE MATRIX TRACKING\n"
        
        # Gross profit evaluation layout string
        report += f"* **Gross Profit Margin Efficiency:**\n"
        report += f"  * *Status:* **{gross['Status']}**\n"
        report += f"  * *Variance:* Your gross margin is {gross['Company_Value']:.1f}% vs industry average of {gross['Industry_Average']:.1f}% — **{abs(gross['Variance']):.1f} points below benchmark**.\n\n"
        
        # Net profit evaluation layout string
        report += f"* **Net Return Margin Footprint:**\n"
        report += f"  * *Status:* **{net['Status']}**\n"
        report += f"  * *Variance:* Currently holding at {net['Company_Value']:.1f}% vs market baseline of {net['Industry_Average']:.1f}% ({abs(net['Variance']):.1f} points delta).\n\n"

        # Throughput time cycle evaluation layout string
        report += f"* **Production Throughput Latency:**\n"
        report += f"  * *Status:* **{cycle['Status']}**\n"
        report += f"  * *Variance:* Operation requires {cycle['Company_Value']:.1f} days vs industry average target of {cycle['Industry_Average']:.1f} days (**+{abs(cycle['Variance']):.1f} days overhead delay**).\n\n"

        report += "#### 🛠️ COMPETITIVE REMEDIATION DIRECTIVES\n"
        report += f"1. **Supply Chain Restructuring:** Address the severe {abs(gross['Variance']):.1f} point deficit below market gross profit norms immediately.\n"
        report += f"2. **Cycle Optimization:** Compress internal handoffs to remove the extra {abs(cycle['Variance']):.1f} days from your operational throughput loop."
        
        return report