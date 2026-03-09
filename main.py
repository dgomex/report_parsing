import duckdb

from src.report_parser.report_parser import ReportParser

if __name__ == "__main__":
    report_path = "Data Quality Ruleset 11.10.25.xlsx"
    parser = ReportParser(report_path)
    kv = parser.generate_kv()
    
    # Example of using duckdb to query the generated key-value pairs
    con = duckdb.connect()
    result = con.execute("SELECT DISTINCT sheet_name FROM kv LIMIT 10").fetchdf()
    result.to_csv("result.csv", index=False)