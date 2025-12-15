import pandas as pd
import numpy as np

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

    """Map descriptions to categories using `mapping`.

    Behavior and improvements:
    - Build a single keyword -> category map preserving the first-seen category
      to avoid ambiguous duplicate keywords across categories.
    - Use lookaround anchors so keywords with non-word characters are matched
      correctly (e.g. "C#", "3.14").
    - Ensure idempotency: once a row's target column is changed from the
      original description it will not be overwritten by later keywords.
    """
    import re

    # Preserve the original source column (column 4) so we can test if
    # a target cell has been changed by this process.
    original_statement = df.iloc[:, 4].copy()
    # Preserve the pre-mapping value of the target column (usually the
    # original Category coming from the CSV). We'll only update rows that
    # still equal this pre-mapping value to ensure idempotency.
    pre_target = df.iloc[:, column_position].copy()

    # Build a keyword->category map, preserving first occurrence as precedence
    keyword_to_category = {}
    duplicates = {}
    for category, keywords in mapping.items():
        for kw in keywords:
            kw_norm = str(kw).lower()
            if kw_norm in keyword_to_category:
                duplicates.setdefault(kw_norm, set()).add(category)
            else:
                keyword_to_category[kw_norm] = category

    if duplicates:
        print("Warning: duplicate keywords found across categories; using first occurrence for each:")
        # Show up to 10 duplicate examples to avoid spamming output
        for kw, cats in list(duplicates.items()):
            print(f"  '{kw}' also appeared in: {', '.join(sorted(cats))}")

    # Sort keywords by length (longer first) to prefer longer matches
    sorted_keywords = sorted(keyword_to_category.items(), key=lambda x: -len(x[0]))

    # Prepare lowercase series for matching from both the original
    # statement and the original category value from the input CSV.
    desc_lower = original_statement.fillna("").astype(str).str.lower()
    cat_lower = pre_target.fillna("").astype(str).str.lower()

    # Apply keywords in order; only assign to rows that haven't been changed
    # since the initial copy (this makes the operation idempotent in a single
    # run and prevents later keywords from overwriting earlier matches).
    target_col_name = df.columns[column_position]
    for kw, category in sorted_keywords:
        # Use lookarounds rather than \b to correctly handle non-word chars
        pattern = r"(?<!\w)" + re.escape(kw) + r"(?!\w)"
        # Match against either the original statement or the original
        # category value from the input file.
        match_mask = (
            desc_lower.str.contains(pattern, regex=True, na=False)
            | cat_lower.str.contains(pattern, regex=True, na=False)
        )
        # Only update rows that haven't been changed since we started
        # (i.e., they still equal the pre-mapping target value).
        still_original_mask = df.iloc[:, column_position].isna() | (df.iloc[:, column_position] == pre_target)
        apply_mask = match_mask & still_original_mask
        if apply_mask.any():
            df.loc[apply_mask, target_col_name] = category

    return df


def normalize_category(category):
    """Normalize category names by removing underscores and applying title case.
    
    Rules:
    - Remove underscores and split by them
    - Capitalize the first letter of each word
    
    Examples:
    - "PHARMACY" -> "Pharmacy"
    - "HEALTH_WELLNESS" -> "Health Wellness"
    - "grocery" -> "Grocery"
    - "specialty_foods" -> "Specialty Foods"
    """
    if pd.isna(category):
        return category
    
    category_str = str(category).strip()
    parts = category_str.split('_')
    
    # Title case each word
    return ' '.join(word.capitalize() for word in parts)


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
    column_position = 2  # Assuming category column of the destination file is at position 2
    df = process_csv(df, column_position, keyword_mapping)

    # Normalize category names (remove underscores, apply proper capitalization)
    df.iloc[:, column_position] = df.iloc[:, column_position].apply(normalize_category)

    # Save the transformed and processed file
    print(f"Processing complete. Saving to file: {output_file}")
    df.to_csv(output_file, index=False)
    print(f"File saved: {output_file}")


if __name__ == "__main__":
    main()
