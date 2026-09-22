import sys
from fractions import Fraction
from decimal import Decimal

ideal_temp=95.5
current_temp=95.499999999999999999999
print(f"Ideal Temp: {ideal_temp}\n")
print(f"Current Temp: {current_temp}\n")
print(f"Difference Temp: {ideal_temp - current_temp}\n")

print(sys.float_info)