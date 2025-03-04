from datetime import datetime

def calculate_contract_value(
    injection_dates,  # List of injection dates
    withdrawal_dates,  # List of withdrawal dates
    purchase_prices,  # List of purchase prices on injection dates
    selling_prices,  # List of selling prices on withdrawal dates
    injection_rate,  # Rate at which gas can be injected (MMBtu/day)
    withdrawal_rate,  # Rate at which gas can be withdrawn (MMBtu/day)
    max_storage_volume,  # Maximum storage volume (MMBtu)
    storage_cost_per_day,  # Daily storage cost
    injection_cost,  # Cost per injection
    withdrawal_cost,  # Cost per withdrawal
):
    # Validate input lengths
    if len(injection_dates) != len(purchase_prices) or len(withdrawal_dates) != len(selling_prices):
        raise ValueError("Injection/withdrawal dates and prices must have the same length.")

    # Initialize variables
    total_value = 0
    current_storage = 0

    # Combine and sort all dates
    all_dates = sorted(injection_dates + withdrawal_dates)

    # Iterate through all dates
    for date in all_dates:
        if date in injection_dates:
            # Injection event
            index = injection_dates.index(date)
            quantity = injection_rate  # Assume daily injection rate
            if current_storage + quantity > max_storage_volume:
                raise ValueError("Injection exceeds maximum storage volume.")
            current_storage += quantity
            total_value -= purchase_prices[index] * quantity  # Subtract purchase cost
            total_value -= injection_cost  # Subtract injection cost
        elif date in withdrawal_dates:
            # Withdrawal event
            index = withdrawal_dates.index(date)
            quantity = withdrawal_rate  # Assume daily withdrawal rate
            if current_storage - quantity < 0:
                raise ValueError("Withdrawal exceeds available storage volume.")
            current_storage -= quantity
            total_value += selling_prices[index] * quantity  # Add selling revenue
            total_value -= withdrawal_cost  # Subtract withdrawal cost

        # Subtract daily storage cost
        total_value -= storage_cost_per_day

    return total_value


# Example usage
if __name__ == "__main__":
    # Input parameters
    injection_dates = [datetime(2023, 10, 1), datetime(2023, 10, 5)]
    withdrawal_dates = [datetime(2023, 12, 1), datetime(2023, 12, 5)]
    purchase_prices = [2.0, 2.1]  # Prices on injection dates
    selling_prices = [3.0, 3.1]  # Prices on withdrawal dates
    injection_rate = 100_000  # 100,000 MMBtu/day
    withdrawal_rate = 100_000  # 100,000 MMBtu/day
    max_storage_volume = 1_000_000  # 1 million MMBtu
    storage_cost_per_day = 3_333.33  # $100K/month ≈ $3,333.33/day
    injection_cost = 10_000  # $10K per injection
    withdrawal_cost = 10_000  # $10K per withdrawal

    # Calculate the contract value
    contract_value = calculate_contract_value(
        injection_dates,
        withdrawal_dates,
        purchase_prices,
        selling_prices,
        injection_rate,
        withdrawal_rate,
        max_storage_volume,
        storage_cost_per_day,
        injection_cost,
        withdrawal_cost,
    )

    # Output the result
    print(f"Contract Value: ${contract_value:,.2f}")