import pandas as pd
import re

class ReportParser:
    def __init__(self, report_path):
        self.report_path = report_path
        print(f"Constructed ReportParser with path: {self.report_path}")

    def generate_kv(self):
        """
        Generate key-value pairs from the report.
        """
        if self.report_path.lower().endswith((".xls", ".xlsx")):
            print("Reading as Excel file")
            excel_file = pd.ExcelFile(self.report_path)
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
            delimiter = ","
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
