import pandas as pd
import numpy as np

# Define the mapping of updated values and their keywords
keyword_mapping = {
    "Paychecks": ["paycheck", "salary", "wages", "income"],
    "Interest": ["interest", "savings", "bank"],
    "Business Income": ["business", "corporate", "profit"],
    "Other Income": ["other income", "miscellaneous"],
    "Returned Purchase": ["returned", "refund", "canceled", "reverse"],
    "Employment Insurance": ["insurance", "employment", "jobless"],
    "Subscriptions": ["subscription", "recurring", "service", "membership"],
    "Charity": ["charity", "donation", "nonprofit", "aid"],
    "Gifts": ["gift", "present", "reward"],
    "Auto Payment": ["auto", "car", "vehicle"],
    "Public Transit": ["transit", "bus", "train", "metro"],
    "Gas": ["gas", "fuel", "petrol"],
    "Auto Maintenance": ["maintenance", "repair", "car service"],
    "Parking & Tolls": ["parking", "toll", "pass", "fee"],
    "Taxi & Ride Shares": ["taxi", "ride share", "Uber", "Lyft"],
    "Mortgage": ["mortgage", "house loan", "property loan"],
    "Rent": ["rent", "lease"],
    "Home Improvement": ["home", "improvement", "renovation", "furniture"],
    "Water": ["water", "utility"],
    "Garbage": ["garbage", "waste", "trash", "disposal"],
    "Gas & Electric": ["electric", "electricity", "gas utility"],
    "Internet & Cable": ["internet", "cable", "broadband", "tv"],
    "Phone": ["phone", "mobile"],
    "Groceries": ["grocery", "food", "supermarket", "wholesale", "market","especialty foods"],
    "Restaurants & Bars": ["restaurant", "bar", "dine", "cafe", "eatery", "beer", "wine", "spirits"],
    "Delivery":[ "delivery", "food delivery", "takeout", "food order"],
    "Coffee Shops": ["coffee", "cafe", "espresso", "cappuccino"],
    "Fast Food": ["fast food", "burger", "pizza", "fries"],
    "Travel & Vacation": ["travel", "vacation", "trip", "holiday", "flights"],
    "Entertainment & Recreation": ["entertainment", "fun", "movies", "games", "attractions","hobbies", "photography", "performing arts","amusement parks"],
    "Beauty": ["beauty", "salon", "grooming", "cosmetics", "makeup", "skincare", "hair", "nails", "facial", "haircare" ],
    "Wellness":["wellness", "health", "fitness", "massage", "spa", "gym", "exercise", "workout", "yoga", "nutrition", "meditation", "therapy", "counseling", "recovery", "rehabilitation", "treatment", "wellness services"],
    "Personal": ["personal", "individual", "miscellaneous"],
    "Pets": ["pet", "animal", "dog", "cat"],
    "Fun Money": ["fun", "leisure", "hobby"],
    "Shopping": ["shopping", "retail", "purchase"],
    "Clothing": ["clothing", "apparel", "fashion", "garments", "footwear", "accessories"],
    "Furniture & Housewares": ["furniture", "housewares", "decor","home goods","home garden"],
    "Electronics": ["electronics", "gadgets", "devices"],
    "Child Care": ["child", "baby", "daycare","formula","diapers","nursery","babysitting"],
    "Child Activities": ["child activities", "toys", "play", "games"],
    "Student Loans": ["student loans", "education loan"],
    "Education": ["education", "school", "tuition"],
    "Medical": ["medical", "health", "pharmacy", "hospital", "doctor","therapy","medication","prescription"],
    "Dentist": ["dentist", "teeth", "oral","dentals"],
    "Fitness": ["fitness", "gym", "sporting", "exercise"],
    "Loan Repayment": ["loan", "repayment"],
    "Financial & Legal Services": ["financial", "legal", "lawyer", "accountant", "services"],
    "Financial Fees": ["fees", "charges", "account fees"],
    "Cash & ATMS": ["cash", "atm"],
    "Insurance": ["insurance", "policy"],
    "Taxes": ["taxes", "tax payment"],
    "Uncategorized": ["uncategorized", "unknown"],
    "Check": ["check", "cheque"],
    "Miscellaneous": ["miscellaneous", "other"],
    "Friendly Loans": ["friendly loans", "family loans", "personal loans"],
    "FD Expenses": ["FD", "fixed deposit expenses"],
    "Advertising & Promotion": ["advertising", "promotion", "marketing"],
    "Business Utilities & Communication": ["business utilities", "internet", "phone", "cable"],
    "Employee Wages & Contract Labor": ["employee wages", "salary", "contract labor"],
    "Business Travels & Meals": ["business travel", "meals", "trips"],
    "Business Auto Expenses": ["business auto", "vehicle", "car"],
    "Business Insurance": ["business insurance", "company policy"],
    "Business Supplies & Expenses": ["supplies", "business expenses"],
    "Office Rent": ["office", "rent", "lease"],
    "Postage & Shipping": ["postage", "shipping", "courier"],
    "Video Games": ["games", "video games", "playstation", "xbox"],
    "Entertainment Subscriptions": ["video series", "games membership", "games services", "entertainment services"],
    "SaaS Subscriptions": ["software", "apps", "devices", "app"],
    "Electronics & Gadgets": ["electronics", "gadgets", "devices"],
    "Transfer": ["transfer", "movement", "funds"],
    "Credit Card Payment": ["credit card", "card payment", "payment"],
    "Balance Adjustments": ["balance", "adjustments", "corrections"]
}

# Function to transform the file into the desired format
def transform_file(df, account_name):
    # Define the desired column order
    desired_order = [
        "Date", "Merchant", "Category", "Account", "Original Statement", "Notes", "Amount", "Tags"
    ]

    # Check if the DataFrame already matches the desired order
    if list(df.columns) == desired_order:
        print("The CSV already matches the desired column order.")
        return df

    # Rename columns
    df.rename(columns={
        "Payee": "Merchant",
        "Notes": "Original Statement"
    }, inplace=True)

    # Add missing columns
    if "Account" not in df.columns:
        df.insert(3, "Account", account_name)  # Add "Account" column with user-provided name
    if "Notes" not in df.columns:
        df.insert(df.columns.get_loc("Original Statement") + 1, "Notes", "")
    if "Tags" not in df.columns:
        df.insert(df.columns.get_loc("Amount") + 1, "Tags", "")

    # Rearrange columns to desired order
    desired_order = [
        "Date", "Merchant", "Category", "Account", "Original Statement", "Notes", "Amount", "Tags"
    ]
    df = df[desired_order]

    return df

# Function to process CSV for keyword mapping
def process_csv(df, column_position, mapping):
    print(f"Processing column at position: {column_position}")

    # Create a sorted list of (keyword, category) tuples
    sorted_keywords = sorted(
        ((kw, cat) for cat, keywords in mapping.items() for kw in keywords),
        key=lambda x: -len(x[0])  # Sort by keyword length (longer first)
    )

     # Copy values from column 4 (index 3) to column 2 (index 1)
    df.iloc[:, column_position] = df.iloc[:, 4]

    # Vectorized replacement
    def map_category(value):
        if pd.isna(value):
            return value
        value_lower = str(value).lower()
        for keyword, category in sorted_keywords:
            if keyword in value_lower:
                return category
        return value

    df.iloc[:, column_position] = df.iloc[:, column_position].apply(map_category)
    return df

# Main execution flow
def main():
    input_file = input("Enter the path to the input CSV file: ")
    output_file = input("Enter the path to save the processed CSV file (leave blank for default): ")
    account_name = input("Enter the account name to fill in the Account column: ")

    if not output_file:
        output_file = input_file.rsplit(".", 1)[0] + "_processed.csv"

    print(f"Loading file: {input_file}")
    df = pd.read_csv(input_file)
    print(f"File loaded. Number of rows: {len(df)}")

    # Transform the file to the desired format
    df = transform_file(df, account_name)

    # Process the keyword mapping
    column_position = 2  # Assuming category column is at position 2
    df = process_csv(df, column_position, keyword_mapping)

    # Save the transformed and processed file
    print(f"Processing complete. Saving to file: {output_file}")
    df.to_csv(output_file, index=False)
    print(f"File saved: {output_file}")

if __name__ == "__main__":
    main()
