# Ask the user for the total bill
total_bill = float(input("Please enter the total bill: "))

# Ask the user for the tip percentage
tip_percentage = float(input("Please enter the tip percentage you want to leave: "))

# Calculate the tip amount
tip_amount = total_bill * (tip_percentage / 100)

# Round the tip amount to two decimal places
tip_amount_rounded = round(tip_amount, 2)

# Format the tip amount as currency
tip_amount_currency = "${:,.2f}".format(tip_amount_rounded)

# Print the tip amount
print("The tip amount to leave is: ", tip_amount_currency)