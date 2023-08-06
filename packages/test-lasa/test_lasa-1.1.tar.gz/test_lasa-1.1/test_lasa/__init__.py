# from Novigi_Operators.custom_csv_to_s3_opertor import CustomCSVToS3Operator
# from Novigi_Operators.novigi_csv_to_db import NovigiCSVToDatabaseExportOperator
# from Novigi_Operators.novigi_excel_to_csv import NovigiExcelToCSVExportOperator
# from Novigi_Operators.novigi_json_to_csv import NovigiJsonToCSVExportOperator
# from Novigi_Operators.novigi_xls_to_csv_operator import NovigiXlsToCSVOperator

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features. We recognize it's a bit unclean to define these in multiple places, but at this point it's the only workaround if you'd like your custom conn type to show up in the Airflow UI.
def get_provider_info():
    return {
        "package-name": "test_lasa", # Required
        "name": "test_lasa", # Required
        "description": "Novigi Custom Airflow Operators", # Required
        "versions": ["1.0"] # Required
    }