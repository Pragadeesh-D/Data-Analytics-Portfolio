from fpdf import FPDF
import os

def generate_report():
    output_path = '../reports/accident_analysis_report.pdf'
    insights_path = '../outputs/insights_summary.txt'
    
    print("Generating PDF report...")
    
    # Read insights
    try:
        with open(insights_path, 'r') as f:
            content = f.read()
    except:
        content = "Insights summary not found. Please run analysis first."

    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 18)
    pdf.cell(200, 20, "Road Accident Data Analysis Report", ln=True, align="C")
    
    # Content
    pdf.set_font("Arial", "", 11)
    pdf.ln(10)
    pdf.multi_cell(0, 8, content)
    
    # Recommendations
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Safety Recommendations", ln=True)
    pdf.set_font("Arial", "", 11)
    recommendations = [
        "1. Increase police patrol in identified high-risk districts.",
        "2. Implement seasonal safety awareness campaigns during peak accident months.",
        "3. Review road infrastructure in areas with high 'Serious' and 'Fatal' accident clusters.",
        "4. Improve street lighting to mitigate night-time accident severity."
    ]
    for rec in recommendations:
        pdf.cell(0, 8, rec, ln=True)

    pdf.output(output_path)
    print(f"Report saved to {output_path}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    generate_report()
