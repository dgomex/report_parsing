import duckdb
import os
import pandas as pd
import re

from pathlib import Path

class ReportParser:
    def __init__(self, report_path):
        self.report_path = report_path
        path_obj = Path(report_path)
        self.file_name = path_obj.stem
        print(f"Constructed ReportParser with path: {self.report_path} and file name: {self.file_name}")

    def _generate_kv(self):
        """
        Generate key-value pairs from the report.
        """
        if self.report_path.lower().endswith((".xls", ".xlsx")):
            print("Reading as Excel file")
            with pd.ExcelFile(self.report_path) as excel_file:
                sheets = excel_file.sheet_names
                # Read an Excel and concat the content of all sheets in one dataframe
                df = pd.concat(
                    [
                        pd.read_excel(
                            excel_file, sheet_name=s, index_col=None, header=None
                        ).assign(sheet_name=s)
                        for s in sheets
                    ]
                )
        elif self.report_path.lower().endswith(".csv"):
            print("Reading as CSV file")
            max_columns = 100 
            df = pd.read_csv(
                self.report_path,
                header=None,
                index_col=None,
                names=list(range(0, max_columns)),
                engine="python"
            )
            df["sheet_name"] = "Sheet1"

        # Reshape the dataframe to have one row per cell
        # with columns for sheet name, row index, column index, and cell value
        print("Reshaping the dataframe to have one row/one column per cell")
        df = df.reset_index(names="idx_row")
        df = df.melt(id_vars=["idx_row", "sheet_name"], var_name="idx_column")
        df = df.rename(columns={"value": "cell_value"})
        df = df.dropna()
        return df.loc[
            df.cell_value.apply(
                lambda s: len(re.sub("\\s|_x000[A-F]_", "", str(s))) > 0
            )
        ]

    def process_file(self, output_dir):
        output_dir = output_dir if output_dir else "output"
        kv = self._generate_kv()
        
        # Example of using duckdb to query the generated key-value pairs
        con = duckdb.connect()
        print("Running DuckDB query to generate final table")
        result = con.execute("SELECT DISTINCT sheet_name FROM kv LIMIT 10").fetchdf()
        
        print("Ensuring output directory exists")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, f"{self.file_name}_result.csv")
        print(f"Writing output to: {output_path}")
        result.to_csv(output_path, index=False)