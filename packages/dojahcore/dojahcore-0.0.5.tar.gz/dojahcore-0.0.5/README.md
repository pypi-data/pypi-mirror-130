#dojahcore-python


Python plugin for [Dojah](https://dojah.io/)


## Installation



## Instantiate Dojah


```python
from dojahcore.dojah import Dojah

dojah_api_key  = 'test_sk_someRandomSecretKey'
dojah_app_id = '99999999999'
dojah_api = Dojah(api_key=dojah_api_key,app_id=dojah_app_id)

# to use the general class
dojah_api.general.data_plans()
```