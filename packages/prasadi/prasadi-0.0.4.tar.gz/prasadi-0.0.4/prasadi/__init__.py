## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features. We recognize it's a bit unclean to define these in multiple places, but at this point it's the only workaround if you'd like your custom conn type to show up in the Airflow UI.
# def get_provider_info():
#     return {
#         "package-name": "prasadi", # Required
#         "name": "Sample Airflow Provider", # Required
#         "description": "A sample template for airflow providers.", # Required
#         "hook-class-names": ["prasadi.hooks.sample_hook.SampleHook"],
#         "extra-links": ["prasadi.operators.sample_operator.ExtraLink"],
#         "versions": ["0.0.2"] # Required
#     }
# from Novigi_Operators.novigi_excel_to_csv import NovigiExcelToCSVExportOperator
# from Novigi_Operators.novigi_json_to_csv import NovigiJsonToCSVExportOperator
# from Novigi_Operators.novigi_xls_to_csv_operator import NovigiXlsToCSVOperator

#from prasadi.operators.sample_operator import SampleOperator

from airflow.plugins_manager import AirflowPlugin

#from mailgun_plugin.hooks import MailgunHook
#from mailgun_plugin.operators import EmailValidationOperator

from prasadi.operators import SampleOperator



class Prasadi(AirflowPlugin):
    name = 'prasadi'
    
    operators = [
        SampleOperator
    ]
