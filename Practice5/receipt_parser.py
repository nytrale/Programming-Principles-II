import re
import json


with open("raw.txt", "r", encoding="utf-8") as f:
    txt = f.read()

# 1

price_pattern = r'\d{1,3}(?:\s\d{3})*,\d{2}'

prices1 = re.findall(price_pattern, txt)

print("All prices:", prices1)


print("\n")


# 2

product_pattern = r'\d+\.\n(.+?)\n\d+,\d{3}\s+x'
products = re.findall(product_pattern, txt, re.DOTALL)


print("Products: ", products)

print("\n")

# 3 

total_pattern = r'ИТОГО:\n(\d{1,3}(?:\s\d{3})*,\d{2})'
match = re.search(total_pattern, txt)

if match:
    total_amount = match.group(1)
else:
    total_amount = None

print("Total amount:", total_amount)

print("\n")

# 4

datetime_pattern = r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})'
match = re.search(datetime_pattern, txt)

datetime_value = match.group(1) if match else None

print("Date & Time:", datetime_value)

print("\n")


# 5

if "Банковская карта" in txt:
    payment_method = "Банковская карта"
elif "Наличные" in txt:
    payment_method = "Наличные"
else:
    payment_method = "Unknown"

print("Payment method:", payment_method)

# 6

structured_data = {
    "products": products,
    "prices": prices1,
    "total_amount": total_amount,
    "datetime": datetime_value,
    "payment_method": payment_method
}

print("\nJSON Output:")
print(json.dumps(structured_data, ensure_ascii=False, indent=4))