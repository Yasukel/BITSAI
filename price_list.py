# Ask user to enter prices separated by commas
entry = input("Enter item prices separated by commas: ")

# Try to convert input into a list of floats
try:
    prices = [float(price.strip()) for price in entry.split(',') if price.strip() != '']
    
    # Calculations
    total_price = sum(prices)
    average_price = total_price / len(prices) if prices else 0
    count_over_10 = sum(1 for price in prices if price > 10)

    # Output results
    print("\nSummary:")
    print(f"Total price: {total_price:.2f}")
    print(f"Average price: {average_price:.2f}")
    print(f"Number of items costing more than 10: {count_over_10}")

except ValueError:
    print("Invalid input. Please enter only numbers separated by commas.")
