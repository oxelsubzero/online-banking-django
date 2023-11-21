from main.models import Rib

# Retrieve all records from the Rib table
rib_records = Rib.objects.all()

# Iterate through the records and print the data
for record in rib_records:
    print(f"User: {record.user}")
    print(f"Bank Name: {record.bank_name}")
    print(f"Code Bank: {record.code_bank}")
    print(f"Code Guichet: {record.code_guichet}")
    print(f"Account Number: {record.account_number}")
    print(f"IBAN: {record.iban}")
    print(f"BIC/SWIFT: {record.bic_swift}")
    print("\n")
