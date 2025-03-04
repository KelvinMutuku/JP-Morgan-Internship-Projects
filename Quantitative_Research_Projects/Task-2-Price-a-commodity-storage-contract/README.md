# Natural Gas Storage Contract Valuation

This project provides a prototype pricing model for valuing natural gas storage contracts. The model calculates the value of a contract based on injection and withdrawal dates, purchase and selling prices, storage costs, and other factors. It is designed to be used with manual oversight and can be further validated and tested before being incorporated into production code.

---

## Features
- **Generalized Function**: Handles multiple injection and withdrawal dates.
- **Cash Flow Calculation**: Accounts for purchase costs, selling revenue, storage costs, and injection/withdrawal costs.
- **Input Validation**: Ensures injection and withdrawal do not exceed storage capacity.
- **Flexible Inputs**: Allows customization of injection/withdrawal rates, storage capacity, and costs.

---

## Files
1. **`contract_valuation_v2.py`**:
   - The main Python script for calculating the contract value.
   - Takes inputs such as injection/withdrawal dates, prices, rates, and costs.
   - Outputs the total value of the contract.

2. **`Nat_Gas.csv`**:
   - Historical natural gas price data (optional for future enhancements).

3. **`README.md`**:
   - Documentation for the project.

---

## Input Parameters
The `calculate_contract_value` function takes the following inputs:
- **`injection_dates`**: List of dates when gas is injected (e.g., `[datetime(2023, 10, 1), datetime(2023, 10, 5)]`).
- **`withdrawal_dates`**: List of dates when gas is withdrawn (e.g., `[datetime(2023, 12, 1), datetime(2023, 12, 5)]`).
- **`purchase_prices`**: List of prices at which gas is purchased on injection dates (e.g., `[2.0, 2.1]`).
- **`selling_prices`**: List of prices at which gas is sold on withdrawal dates (e.g., `[3.0, 3.1]`).
- **`injection_rate`**: Rate at which gas is injected (MMBtu/day).
- **`withdrawal_rate`**: Rate at which gas is withdrawn (MMBtu/day).
- **`max_storage_volume`**: Maximum storage capacity (MMBtu).
- **`storage_cost_per_day`**: Daily storage cost.
- **`injection_cost`**: Cost per injection.
- **`withdrawal_cost`**: Cost per withdrawal.

---

## Example Usage
1. **Install Python**:
   - Ensure Python 3.x is installed. Download it from [python.org](https://www.python.org/downloads/).

2. **Run the Script**:
   - Navigate to the project folder and run:
     ```bash
     python contract_valuation.py
     ```

3. **Example Output**:
Contract Value: $146,666.68 

---

## Assumptions
- No transport delay.
- Interest rates are zero.
- Market holidays, weekends, and bank holidays are ignored.

---

## Future Enhancements
- Incorporate historical price data from `Nat_Gas.csv` for more accurate pricing.
- Add support for variable injection/withdrawal rates.
- Include interest rates and transport delays for more realistic modeling.

---

## Author
Kelvin Mutuku  
mutukuk553@gmail.com 
https://github.com/KelvinMutuku

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.