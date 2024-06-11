import re 
import sys  
from openapi_client.model_utils import ( 
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)

def lazy_import():
    from openapi_client.model.address_response import AddressResponse
    from openapi_client.model.compensation_history_response import CompensationHistoryResponse
    from openapi_client.model.create_employee_request_bank_account import CreateEmployeeRequestBankAccount
    from openapi_client.model.create_employee_request_dependents import CreateEmployeeRequestDependents
    from openapi_client.model.create_employee_request_emergency_contacts import CreateEmployeeRequestEmergencyContacts
    from openapi_client.model.employee_response_manager import EmployeeResponseManager
    from openapi_client.model.employment_history_response import EmploymentHistoryResponse
    from openapi_client.model.employment_status_response import EmploymentStatusResponse
    from openapi_client.model.groups20230301_response import Groups20230301Response
    from openapi_client.model.location_response import LocationResponse
    globals()['AddressResponse'] = AddressResponse
    globals()['CompensationHistoryResponse'] = CompensationHistoryResponse
    globals()['CreateEmployeeRequestBankAccount'] = CreateEmployeeRequestBankAccount
    globals()['CreateEmployeeRequestDependents'] = CreateEmployeeRequestDependents
    globals()['CreateEmployeeRequestEmergencyContacts'] = CreateEmployeeRequestEmergencyContacts
    globals()['EmployeeResponseManager'] = EmployeeResponseManager
    globals()['EmploymentHistoryResponse'] = EmploymentHistoryResponse
    globals()['EmploymentStatusResponse'] = EmploymentStatusResponse
    globals()['Groups20230301Response'] = Groups20230301Response
    globals()['LocationResponse'] = LocationResponse


class EmployeeResponse(ModelNormal):

    allowed_values = {
        ('gender',): {
            'None': None,
            'MALE': "male",
            'FEMALE': "female",
            'NOT_SPECIFIED': "not_specified",
            'NULL': "null",
        },
        ('ethnicity',): {
            'None': None,
            'NULL': "null",
            'ASIAN': "asian",
            'BLACK': "black",
            'HISPANIC': "hispanic",
            'MIXED': "mixed",
            'NOT_SPECIFIED': "not_specified",
            'OTHER': "other",
            'WHITE': "white",
        },
        ('marital_status',): {
            'None': None,
            'SINGLE': "single",
            'MARRIED': "married",
            'DIVORCED': "divorced",
            'NOT_SPECIFIED': "not_specified",
            'OTHER': "other",
            'NULL': "null",
        },
        ('employment_type',): {
            'None': None,
            'NULL': "null",
            'FULL_TIME': "full_time",
            'PART_TIME': "part_time",
            'CONTRACTOR': "contractor",
            'OTHER': "other",
        },
    }

    validations = {
    }

    additional_properties_type = None

    _nullable = False