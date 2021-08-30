import pint
from pint.errors import UndefinedUnitError

from django.core.exceptions import ValidationError

valid_units = ['pounds', 'lbs', 'oz', 'gram']

def validate_units(value):
    ureg = pint.UnitRegistry()
    try:
        single_unit = ureg[value]
    except UndefinedUnitError as e:
        raise ValidationError(f"'{value}' is not a valid unit")
    except:
        raise ValidationError(f"'{value}' is not a valid unit. Unknown error.")
