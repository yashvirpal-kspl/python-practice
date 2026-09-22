chai_type="Ginger Chai"
customer_name="Priya"

print(f"Order for {customer_name} : {chai_type}\n")

chai_description="Aromatic Bold"
print(f"First Word: {chai_description[0:8]}\n")
print(f"First Word: {chai_description[0:8:1]}\n")  # Every 1st Charecter
print(f"Second Word: {chai_description[0:8:2]}\n")  # Every 2nd Charecter 
print("####################")

print(f"First Word: {chai_description[:8]}\n")
print(f"Last Word: {chai_description[12:]}\n")
print(f"First Word: {chai_description[::-1]}\n")  # Reverse the whole string

print("##############")
label_text="Chai Sp`e"
encoded_label=label_text.encode('utf-8')
print(f"Non Encoded label: {label_text}")
print(f"Encoded label: {encoded_label}")
decoded_label=encoded_label.decode('utf-8')
print(f"Decoded label: {decoded_label}")