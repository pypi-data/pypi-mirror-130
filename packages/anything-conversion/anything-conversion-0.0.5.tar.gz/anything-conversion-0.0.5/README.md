# anything-conversion


Hello Pythoniers!...... this package is used to convert from one to another...

Currently WeightConversion,VolumeConversion,CurrencyConversion,TemperatureConversion,AreaConversion

A lot more yet to come in future.....

Need your blessings...If you like my content..please give a star **************

Developed by sairamdgr8 (c) 2021

## Examples of How To Use (anything-conversion)

Installing anything-convertor package

```
pip install anything-conversion

```

```python

from anything_conversion.converter import WeightConverter,AreaConverter
x=WeightConverter.kilogram_gram(120)
print(x)

```
```
output: 120000

```

```python

from anything_conversion.CurrencyConversion import CurrencyConverter
y1=CurrencyConverter.currency_conversion("USD","INR",54)
print("currency_conversion: ",y1)

```
```
output: currency_conversion:  ('current_currency=USD', 'convert_currency=INR', 'convert_amount=54.0 USD', 'final_converted_amount=4063.04 INR')

```


```python

from anything_conversion.TemperatureConversion import TemperatureConveter
y2=TemperatureConveter.Fahrenheit_Celsius(100)
print("TemperatureConveter.Fahrenheit_Celsius: ",y2)


```
```
output: TemperatureConveter.Fahrenheit_Celsius:  37.77777777777778

```

