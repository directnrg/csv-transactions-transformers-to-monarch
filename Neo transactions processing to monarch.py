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
    "Parking & Tolls": ["parking", "toll", "pass", "fee", "honk parking"],
    "Mortgage": ["mortgage", "house loan", "property loan"],
    "Household": ["dollarama", "household", "home supplies", "cleaning"],
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
        "cafe",
        "eatery",
        "beer",
        "wine",
        "spirits",
        "sunset grill",
        "pub",
        "mad radish",
        "chick-fil-a",
        "shake shack",
        "jimmy the greek",
        "cafe landwer",
        "kitchen market",
        "eggsmart",
        "vereda",
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
        "MCDONALD'S" "KFC",
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
    "Entertainment & Recreation": [
        "entertainment",
        "fun",
        "movies",
        "games",
        "attractions",
        "hobbies",
        "photography",
        "performing arts",
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
    "Personal": ["personal", "individual", "miscellaneous"],
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
        "costco",
        "target",
        "AMZ",
        "winners",
        "marshalls",
        "dollarama",
        "value village",
        "miniso",
        "lucky mart",
        "international news",
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
    "Furniture & Housewares": [
        "furniture",
        "housewares",
        "decor",
        "home goods",
        "home garden",
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
    "Child Activities": ["child activities", "toys", "play", "games"],
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
        "health",
        "pharmacy",
        "hospital",
        "doctor",
        "therapy",
        "medication",
        "prescription",
        "pharma",
        "medicine",
    ],
    "Dentist": ["dentist", "teeth", "oral", "dentals"],
    "Fitness": ["fitness", "gym", "sporting", "exercise"],
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
    "Insurance": ["insurance", "policy"],
    "Taxes": ["taxes", "tax payment", "bridge commission"],
    "Uncategorized": ["uncategorized", "unknown"],
    "Miscellaneous": ["miscellaneous", "other"],
    "Friendly Loans": ["friendly loans", "family loans", "personal loans"],
    "FD Expenses": ["FD", "fixed deposit expenses"],
    "Advertising & Promotion": ["advertising", "promotion", "marketing"],
    "Business Utilities & Communication": [
        "business utilities",
        "internet",
        "phone",
        "cable",
    ],
    "Employee Wages & Contract Labor": ["employee wages", "salary", "contract labor"],
    "Business Travels & Meals": ["business travel", "meals", "trips"],
    "Business Auto Expenses": ["business auto", "vehicle", "car"],
    "Business Insurance": ["business insurance", "company policy"],
    "Business Supplies & Expenses": ["supplies", "business expenses"],
    "Office Rent": ["office", "rent", "lease"],
    "Postage & Shipping": ["postage", "shipping", "courier"],
    "Video Games": ["games", "video games", "playstation", "xbox"],
    "Entertainment Subscriptions": [
        "video series",
        "games membership",
        "games services",
        "entertainment services",
        "PSN",
        "Xbox Live",
        "Netflix",
        "Hulu",
        "Disney+",
    ],
    "SaaS Subscriptions": [
        "software",
        "apps",
        "devices",
        "app",
        "blink",
        "openAI",
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
        "best buy",
        "staples",
    ],
    "Transfer": ["transfer", "movement", "funds", "money request"],
    "Credit Card Payment": ["credit card", "card payment", "payment"],
    "Balance Adjustments": ["balance", "adjustments", "corrections"],
    "Transportation": [
        "transit",
        "bus",
        "train",
        "metro",
        "lyft",
        "ttc",
        "presto",
        "via rail",
        "taxi",
        "ride share",
        "Uber",
        "lyft",
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

    # Create a sorted list of (keyword, category) tuples
    sorted_keywords = sorted(
        ((kw, cat) for cat, keywords in mapping.items() for kw in keywords),
        key=lambda x: -len(x[0]),  # Sort by keyword length (longer first)
    )

    # Copy values from column 4 (index 3) to column 2 (index 1)
    df.iloc[:, column_position] = df.iloc[
        :, 4
    ]  # Assuming the category column is at position 2 (index 1)

    # Vectorized replacement
    import re

    def map_category(value):
        if pd.isna(value):
            return value
        value_lower = str(value).lower()
        for keyword, category in sorted_keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, value_lower):
                return category
        return value

    df.iloc[:, column_position] = df.iloc[:, column_position].apply(map_category)
    return df


# Main execution flow
def main():
    input_file = input("Enter the path to the input CSV file: ")
    output_file = input(
        "Enter the path to save the processed CSV file (leave blank for default): "
    )
    account_name = input("Enter the account name to fill in the Account column: ")

    if not output_file:
        output_file = input_file.rsplit(".", 1)[0] + "_processed.csv"

    print(f"Loading file: {input_file}")
    df = pd.read_csv(input_file)
    print(f"File loaded. Number of rows: {len(df)}")

    # Transform the file to the desired format
    df = transform_file(df, account_name)

    # Process the keyword mapping
    column_position = (
        2  # Assuming category column of the destination file is at position 2
    )
    df = process_csv(df, column_position, keyword_mapping)

    # Save the transformed and processed file
    print(f"Processing complete. Saving to file: {output_file}")
    df.to_csv(output_file, index=False)
    print(f"File saved: {output_file}")


if __name__ == "__main__":
    main()
