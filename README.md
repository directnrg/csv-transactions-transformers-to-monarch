# CSV Transactions Transformers to Monarch

This repository contains Python scripts for transforming bank transaction CSV files into a format compatible with Monarch Money, a personal finance management tool. The scripts currently support Neo Bank and Bancolombia transaction formats.

## Scripts Overview

### 1. Neo Transactions Processing (`Neo transactions processing to monarch.py`)

This script processes CSV files from Neo Bank and transforms them into Monarch's expected format. 

**Features:**
- Transforms CSV files to match Monarch's column structure
- Automatically categorizes transactions based on an extensive keyword mapping
- Supports the following columns:
  - Date
  - Merchant
  - Category
  - Account
  - Original Statement
  - Notes
  - Amount
  - Tags

**Usage:**
```bash
python "Neo transactions processing to monarch.py"
```
The script will prompt you for:
- Input CSV file path
- Output CSV file path (optional)
- Account name

### 2. Bancolombia Transactions Processing (`Bancolombia transactions processing to monarch.py`)

This script processes CSV files from Bancolombia and transforms them into Monarch's format, with additional currency conversion functionality.

**Features:**
- Transforms Bancolombia's Spanish format to Monarch's English format
- Converts Colombian Pesos (COP) to Canadian Dollars (CAD)
- Includes extensive Spanish-English category mapping
- Preserves original transaction amounts in the Notes field
- Handles multiple CSV encoding formats (UTF-8, Latin1, CP1252)
- Supports the same column structure as the Neo transactions processor

**Usage:**
```bash
python "Bancolombia transactions processing to monarch.py"
```
The script will prompt you for:
- Input CSV file path
- Output CSV file path (optional)
- Account name

## Category Mapping

Both scripts include comprehensive category mappings that classify transactions into standard personal finance categories such as:
- Income categories (Paychecks, Business Income, etc.)
- Housing expenses (Rent, Mortgage, Utilities)
- Transportation (Auto Payment, Public Transit, Gas)
- Food and Dining (Groceries, Restaurants, Coffee Shops)
- Shopping (Clothing, Electronics, Home Improvement)
- And many more

## Requirements

- Python 3.x
- pandas
- numpy (for Neo transactions processing)

## License

This project is licensed under the terms included in the LICENSE file.

## Notes

- The Bancolombia script uses a fixed conversion rate (0.00033333) from COP to CAD. You may want to update this rate based on current exchange rates.
- Both scripts will create a processed file with "_processed" appended to the original filename if no output filename is specified.
- Make sure your input CSV files match the expected format for each bank.