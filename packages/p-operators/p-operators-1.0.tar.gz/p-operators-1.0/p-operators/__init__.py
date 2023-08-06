# from Novigi_Operators.custom_csv_to_s3_opertor import CustomCSVToS3Operator
# from Novigi_Operators.novigi_csv_to_db import NovigiCSVToDatabaseExportOperator
# from Novigi_Operators.novigi_excel_to_csv import NovigiExcelToCSVExportOperator
# from Novigi_Operators.novigi_json_to_csv import NovigiJsonToCSVExportOperator
# from Novigi_Operators.novigi_xls_to_csv_operator import NovigiXlsToCSVOperator

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features. We recognize it's a bit unclean to define these in multiple places, but at this point it's the only workaround if you'd like your custom conn type to show up in the Airflow UI.
def get_provider_info():
    return {
        "package-name": "p-operators", # Required
        "name": "p-operators", # Required
        "description": "Novigi Custom Airflow Operators", # Required
        "extra-links": [
                         "novigi_operators.operators.sample_operator.CustomCSVToS3Operator",
                         "novigi_operators.operators.sample_operator.NovigiCSVToDatabaseExportOperator",
                         "novigi_operators.operators.sample_operator.NovigiExcelToCSVExportOperator",
                         "novigi_operators.operators.sample_operator.NovigiJsonToCSVExportOperator",
                         "novigi_operators.operators.sample_operator.NovigiXlsToCSVOperator"
                       ],
        "versions": ["1.0"] # Required
    }