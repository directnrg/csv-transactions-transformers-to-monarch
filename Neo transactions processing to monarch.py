import pandas as pd
from pathlib import Path
from transaction_utils import CSVLoader, CategoryMapper, CategoryNormalizer

# Define the mapping of updated values and their keywords
keyword_mapping = {
    "Paychecks": ["paycheck", "salary", "wages", "income"],
    "Interest": ["interest", "savings", "bank"],
    "Business Income": ["business", "corporate", "profit"],
    "Other Income": ["other income", "miscellaneous"],
    "Returned Purchase": ["returned", "refund", "canceled", "reverse"],
    "Insurance": ["insurance", "employment", "jobless"],
    "Subscriptions": ["subscription", "recurring", "service", "membership"],
    "Charity": ["charity", "donation", "nonprofit", "aid"],
    "Gifts": ["gift", "present", "reward"],
    "Auto Payment": ["auto", "car", "vehicle"],
    "Gas": ["gas", "fuel", "petrol"],
    "Auto Maintenance": ["maintenance", "repair", "car service"],
    "Parking & Tolls": ["parking", "toll", "pass", "fee", "honk parking"],
    "Mortgage": ["mortgage", "house loan", "property loan"],
    "Household": ["household", "home supplies", "cleaning"],
    "Rent": ["rent", "lease"],
    "Home Improvement": ["home", "improvement", "renovation", "furniture"],
    "Water": ["water", "utility"],
    "Garbage": ["garbage", "waste", "trash", "disposal"],
    "Gas & Electric": ["electric", "electricity", "gas utility"],
    "Internet & Cable": ["internet", "cable", "broadband", "tv"],
    "Phone": ["phone", "mobile", "rogers", "bell", "telus"],
    "Groceries": [
        "grocery",
        "food",
        "supermarket",
        "wholesale",
        "market",
        "especialty foods",
        "freshco",
        "food basics",
        "costco",
        "metro",
        "loblaws",
        "longos",
        "sobeys",
        "rcss",
        "superstore",
        "valu-mart",
        "no frills",
        "nofrills",
        "ANDREW & SHELLEY'S",
        "bulk barn",
        "factor meals",
        "fresh one market",
        "damiano",
        "kuvera foods",
        "plank road market",
        "shoppers",
        "convenience",
        "Vm",
        "Value Market" "costco wholesale",
        "masellis",
        "galleria express",
    ],
    "Medical": [
        "medical",
        "health",
        "pharmacy",
        "hospital",
        "doctor",
        "therapy",
        "medication",
        "prescription",
        "pharma",
        "medicine",
        "shoppers",
    ],
    "Restaurants & Bars": [
        "restaurant",
        "bar",
        "dine",
        "eatery",
        "beer",
        "wine",
        "spirits",
        "sunset grill",
        "pub",
        "mad radish",
        "shake shack",
        "jimmy the greek",
        "cafe landwer",
        "kitchen market",
        "eggsmart",
        "vereda"
    ],
    "Delivery": ["delivery", "food delivery", "takeout", "food order"],
    "Coffee Shops": [
        "coffee",
        "cafe",
        "espresso",
        "cappuccino",
        "tim hortons",
        "starbucks",
        "second cup",
        "balzac",
        "aroma espresso",
        "pomarosa",
        "am coffee studio",
        "simple coffee",
    ],
    "Fast Food": [
        "fast food",
        "burger",
        "pizza",
        "fries",
        "McDonald's",
        "KFC",
        "Taco Bell",
        "Subway",
        "Wendy's",
        "A&W",
        "Harvey's",
        "HARVEYS" "Popeyes",
        "Domino's",
        "Pizza Hut",
        "Little Caesars",
        "Burger King",
        "Chipotle",
        "Five Guys",
        "Dairy Queen",
        "Pita Pit",
        "chick-fil-a",
        "barburrito",
        "osmow",
        "pita lite",
        "fat bastard",
        "burger bros",
        "mr sub",
        "krispy kreme",
        "happy sundae",
    ],
    "Travel & Vacation": ["travel", "vacation", "trip", "holiday", "flights"],
    "Beauty": [
        "beauty",
        "salon",
        "grooming",
        "cosmetics",
        "makeup",
        "skincare",
        "hair",
        "nails",
        "facial",
        "haircare",
    ],
    "Wellness": [
        "wellness",
        "health",
        "fitness",
        "massage",
        "spa",
        "gym",
        "exercise",
        "workout",
        "yoga",
        "nutrition",
        "meditation",
        "therapy",
        "counseling",
        "recovery",
        "rehabilitation",
        "treatment",
        "wellness services",
    ],
    "Personal": ["personal", "individual"],
    "Pets": ["pet", "animal", "dog", "cat"],
    "Fun Money": ["fun", "leisure", "hobby"],
    "Shopping": [
        "shopping",
        "retail",
        "purchase",
        "amazon",
        "ebay",
        "walmart",
        "wal-mart",
        "best buy",
        "target",
        "AMZ",
        "winners",
        "marshalls",
        "dollarama",
        "value village",
        "lucky mart",
        "bath & body works",
        "absolute dollar",
        "deserres",
        "playtime toys",
        "miniso",
        "pandora",
        "international news",
        "wellwise",
    ],
    "Clothing": [
        "clothing",
        "apparel",
        "fashion",
        "garments",
        "footwear",
        "accessories",
        "shoes",
        "clothes",
        "wardrobe",
        "Adidas",
        "Nike",
        "Zara",
        "H&M",
        "Gap",
        "Uniqlo",
        "old navy",
        "OLDNAVY.COM" "ardene",
    ],
    "Child Care": [
        "child",
        "baby",
        "daycare",
        "formula",
        "diapers",
        "nursery",
        "babysitting",
    ],
    "Child Activities": ["child activities", "toys", "play"],
    "Student Loans": ["student loans", "education loan"],
    "Education": [
        "education",
        "school",
        "tuition",
        "brillian.org",
        "courses",
        "classes",
        "training",
        "aruccmycreds",
    ],
    "Medical": [
        "medical",
        "pharmacy",
        "hospital",
        "doctor",
        "medication",
        "prescription",
        "pharma",
        "medicine",
    ],
    "Dentist": ["dentist", "teeth", "oral", "dentals"],
    "Loan Repayment": ["loan", "repayment"],
    "Financial & Legal Services": [
        "financial",
        "legal",
        "lawyer",
        "accountant",
        "services",
        "immigration canada",
    ],
    "Financial Fees": ["fees", "charges", "account fees"],
    "Cash & ATMS": ["cash", "atm"],
    "Taxes": ["taxes", "tax payment", "bridge commission"],
    "Uncategorized": ["uncategorized", "unknown"],
    "Miscellaneous": ["miscellaneous expense", "other"],
    "Friendly Loans": ["friendly loans", "family loans", "personal loans"],
    "FD Expenses": ["FD", "fixed deposit expenses"],
    "Advertising & Promotion": ["advertising", "promotion", "marketing"],
    "Employee Wages & Contract Labor": ["employee wages", "business salary", "contract labor"],
    "Business Travels & Meals": ["business travel", "meals", "trips"],
    "Business Auto Expenses": ["business auto", "business vehicle", "business car"],
    "Business Insurance": ["business insurance", "company policy"],
    "Business Supplies & Expenses": ["supplies", "business expenses"],
    "Office Rent": ["office", "business rent", "business lease"],
    "Postage & Shipping": ["postage", "shipping", "courier"],
    "Video Games": ["games", "video games", "playstation", "xbox"],
    "Entertainment & Recreation": [
        "entertainment",
        "movies",
        "attractions",
        "hobbies",
        "photography",
        "amusement parks",
        "eventbrite",
        "kids fun town",
        "cineplex",
        "famous player",
        "the rec room",
        "zed*80",
        "snakes & lattes",
        "performing arts",
        "gamestop",
        "village vacances",
        "wonderland",
    ],
    "Entertainment Subscriptions": [
        "video series",
        "games membership",
        "games services",
        "entertainment services",
        "PSN",
        "Xbox Live",
        "Netflix",
        "Netflix.com"
        "Hulu",
        "Disney+",
    ],
    "SaaS Subscriptions": [
        "software",
        "apps",
        "app",
        "blink",
        "microsoft 365",
        "skillsyncer",
        "chatgpt",
        "openai",
        "microsoft",
        "google cloud",
        "amazon web services",
        "brilliant.org",
        "aws",
    ],
    "Electronics & Gadgets": [
        "electronics",
        "gadgets",
        "devices",
        "apple store",
        "staples",
    ],
    "Transfer": ["transfer", "movement", "funds", "money request"],
    "Credit Card Payment": ["credit card", "card payment", "payment"],
    "Balance Adjustments": ["balance", "adjustments", "corrections"],
    "Transportation": [
        "transit",
        "bus",
        "train",
        "lyft",
        "ttc",
        "presto",
        "via rail",
        "taxi",
        "ride share",
        "Uber",
        "hopp",
        "beck taxi",
    ],
}


# Function to transform the file into the desired format
def transform_file(df, account_name):
    # Define the desired column order
    desired_order = [
        "Date",
        "Merchant",
        "Category",
        "Account",
        "Original Statement",
        "Notes",
        "Amount",
        "Tags",
    ]

    # Check if the DataFrame already matches the desired order
    if list(df.columns) == desired_order:
        print("The CSV already matches the desired column order.")
        return df

    # Rename columns
    df.rename(
        columns={"Payee": "Merchant", "Notes": "Original Statement"}, inplace=True
    )

    # Add missing columns
    if "Account" not in df.columns:
        df.insert(
            3, "Account", account_name
        )  # Add "Account" column with user-provided name
    if "Notes" not in df.columns:
        df.insert(df.columns.get_loc("Original Statement") + 1, "Notes", "")
    if "Tags" not in df.columns:
        df.insert(df.columns.get_loc("Amount") + 1, "Tags", "")

    df = df[desired_order]

    return df


# Function to process CSV for keyword mapping
def process_csv(df, column_position, mapping):
    print(f"Processing column at position: {column_position}")

    mapper = CategoryMapper(mapping)
    original_statement = df.iloc[:, 4].copy()
    target_col_name = df.columns[column_position]

    # Map categories using the keyword mapper
    df[target_col_name] = original_statement.apply(mapper.map_category)

    return df


def main():
    input_file = input("Enter the path to the input CSV file: ").strip('"').strip("'").strip()
    output_file = input(
        "Enter the path to save the processed CSV file (leave blank for default): "
    )
    output_file = output_file.strip('"').strip("'").strip()  # Remove quotes and whitespace

    account_name = input("Enter the account name to fill in the Account column: ")

    if not output_file:
        output_file = input_file.rsplit(".", 1)[0] + "_processed.csv"

    # If user provided a directory path, append default filename
    output_path = Path(output_file)
    if output_path.is_dir() or (not output_path.suffix and output_file.endswith('\\')):
        output_file = str(output_path / (Path(input_file).stem + "_processed.csv"))

    print(f"Loading file: {input_file}")
    df = CSVLoader.load(input_file)
    print(f"File loaded. Number of rows: {len(df)}")

    # Transform the file to the desired format
    df = transform_file(df, account_name)

    # Process the keyword mapping
    column_position = 2  # Category column position
    df = process_csv(df, column_position, keyword_mapping)

    # Normalize category names
    df.iloc[:, column_position] = df.iloc[:, column_position].apply(CategoryNormalizer.normalize)

    # Save the transformed and processed file
    print(f"Processing complete. Saving to file: {output_file}")
    df.to_csv(output_file, index=False)
    print(f"File saved: {output_file}")


if __name__ == "__main__":
    main()
