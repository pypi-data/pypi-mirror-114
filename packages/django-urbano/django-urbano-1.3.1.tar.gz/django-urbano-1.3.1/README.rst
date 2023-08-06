
# django-urbano

## Starting
_These instructions will allow you to install the library in your python project._

### Current features

-   Get tracking info.

### Pre-requisitos

-   Python >= 3.7
-   Django >= 3
-   requests >= 2
***
## Installation

1. To get the latest stable release from PyPi:
```
pip install django-urbano
```
or

2. From a build
```
git clone https://gitlab.com/linets/ecommerce/oms/integrations/django-urbano
```

```
cd {{project}}
```

```
python setup.py sdist
```
and, install in your project django
```
pip install {{path}}/django-urbano/dist/{{tar.gz file}}
```

3. Settings in django project

```
DJANGO_URBANO = {
    'URBANO': {
        'BASE_URL': '<URBANO_BASE_URL>',
        'USER': '<URBANO_USER>',
        'PASSWORD': '<URBANO_PASSWORD>',
        'ID_CONTRATO': '<URBANO_ID_CONTRATO>',
    }
}
```

## Usage
1. Create instance to be sent
    ```
    import json
    from types import SimpleNamespace

    dict_ = {
        'reference': '99999',
        'created_at': '12/12/21',
        'shipping_date': '12/12/21',
        'expiration_date': '26/12/21'
        'tracking_code': '6075620-1',
        'transport_guide_number': '1121632479536-01-1',
        'purchase_number': 'CLV0048146676851-1',
        'customer': {
            'first_name': 'Marcos',
            'last_name': 'Sac',
            'full_name': 'Marcos Sac',
            'phone': '932932932',
            'email': 'test@gmail.com',
            'rut': '16936195-9'
        },
        'address': {
            'street': 'ALEJANDRO VENEGAS CADIZ',
            'number': '513',
            'unit': 'DEPTO 6A',
            'full_address': 'ALEJANDRO VENEGAS CADIZ 513 DEPTO 6A'
        },
        'commune': {
            'name': 'Aisen',
            'code': '',
            'zone_code': '11201',
            'zone_post': 'WPA',
        },
        'location': {
            'code': 'MONTANDON',
            'name': 'MNN',
        },
        'region': {
            'name': 'Aysén del General Carlos Ibáñez del Campo',
            'code': '11',
            'iso_code': 'CL-XI',
        }
    }

    instance = json.loads(json.dumps(dict_), object_hook=lambda attr: SimpleNamespace(**attr))
    ```


2. Get tracking info:
```
from urbano.handler import UrbanoHandler

handler = UrbanoHandler()

tracking_info = handler.get_tracking(<identifier>)
```

3. Get default payload:
```
from urbano.handler import UrbanoHandler

handler = UrbanoHandler()
default_data = handler.get_default_payload(<instance>)
```

4. Create shipping:
```
from urbano.handler import UrbanoHandler

handler = UrbanoHandler()
default_data = handler.create_shipping(<default_data>)
```

5. Get events:
```
from urbano.handler import UrbanoHandler

handler = UrbanoHandler()

raw_data = {
    'tracking_number': 999999,
    'status': 'ENTREGADO',
    'events': [{
        'city': 'Santiago'
        'state': 'RM',
        'description': 'Llego al almacén',
        'date': '12/12/2021'
    }]
}
response = handler.get_events(raw_data)

Output:
[{
    'city': 'Santiago'
    'state': 'RM',
    'description': 'Llego al almacén',
    'date': '12/12/2021'
}]
```

6. Get status and if "is_delivered":
```
from urbano.handler import UrbanoHandler

handler = UrbanoHandler()

raw_data = {
    'tracking_number': 999999,
    'status': 'ENTREGADO',
    'events': [{
        'city': 'Santiago'
        'state': 'RM',
        'description': 'Llego al almacén',
        'date': '12/12/2021'
    }]
}
response = handler.get_status(raw_data)

Output:
('ENTREGADO', True)
```
