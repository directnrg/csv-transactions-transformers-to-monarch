import pandas as pd

# Define the mapping of English categories and their Spanish keywords
keyword_mapping = {
    "Paychecks": ["nomina", "sueldo", "salario", "pago", "honorarios"],
    "Interest": ["interes", "intereses", "ahorros", "abono intereses ahorros", "ajuste interes"],
    "Business Income": ["negocio", "corporativo", "ganancia", "utilidad"],
    "Other Income": ["otros ingresos", "ingreso", "consig", "transferencia recibida", "desde nequi", "transf internacional recibida", "transferencia desde nequi", "consig local caj multifunciona"],
    "Returned Purchase": ["devolucion", "reembolso", "cancelado", "reverso"],
    "Employment Insurance": ["seguro", "empleo", "desempleo"],
    "Subscriptions": ["suscripcion", "subscripcion", "servicio", "membresia"],
    "Charity": ["caridad", "donacion", "sin fines de lucro", "ayuda"],
    "Gifts": ["regalo", "presente", "recompensa"],
    "Auto Payment": ["auto", "carro", "vehiculo"],
    "Public Transit": ["transporte", "bus", "autobus", "tren", "metro"],
    "Gas": ["gasolina", "combustible", "gas", "eds", "servir", "eds servir"],
    "Auto Maintenance": ["mantenimiento", "reparacion", "servicio de carro"],
    "Parking & Tolls": ["estacionamiento", "peaje", "pase", "tarifa"],
    "Taxi & Ride Shares": ["taxi", "uber", "cabify", "beat", "didi"],
    "Mortgage": ["hipoteca", "prestamo de casa", "prestamo de propiedad"],
    "Rent": ["alquiler", "renta", "arriendo"],
    "Home Improvement": ["mejoras", "renovacion", "muebles", "hogar"],
    "Water": ["agua", "acueducto", "servicio de agua"],
    "Garbage": ["basura", "residuos", "desechos", "recoleccion"],
    "Gas & Electric": ["electricidad", "luz", "gas", "energia"],
    "Internet & Cable": ["internet", "cable", "banda ancha", "tv"],
    "Phone": ["telefono", "celular", "movil", "comunicacion celular", "pago pse comunicacion celular", "paquete todo incluido vo"],
    "Groceries": ["supermercado", "mercado", "alimentos", "comida", "nuestro bo", "nuestro bogota", "cc nuestro"],
    "Restaurants & Bars": ["restaurante", "bar", "comer", "cafe", "comedor", "cerveza", "vino", "licor", "ajiaco", "santos fri", "campo elia", "r59 crepes", "club 8", "ajiaco y f", "compa@ia d"],
    "Delivery": ["delivery", "domicilio", "pedido", "comida a domicilio"],
    "Coffee Shops": ["cafe", "cafeteria", "expreso", "capuchino", "avena", "bold*avena"],
    "Fast Food": ["comida rapida", "hamburguesa", "pizza", "papas fritas", "mcdonalds"],
    "Travel & Vacation": ["viaje", "vacacion", "viaje", "vacaciones", "vuelos"],
    "Entertainment & Recreation": ["entretenimiento", "diversion", "peliculas", "juegos", "atracciones", "pasatiempos", "fotografia", "artes escenicas", "parques de atracciones"],
    "Beauty": ["belleza", "salon", "aseo personal", "cosmeticos", "maquillaje", "cuidado de la piel", "cabello", "uñas", "facial", "cuidado del cabello"],
    "Wellness": ["bienestar", "salud", "fitness", "masaje", "spa", "gimnasio", "ejercicio", "entrenamiento", "yoga", "nutricion", "meditacion", "terapia", "asesoramiento", "recuperacion", "rehabilitacion", "tratamiento", "servicios de bienestar"],
    "Personal": ["personal", "individual", "miscelaneo"],
    "Pets": ["mascota", "animal", "perro", "gato"],
    "Fun Money": ["diversion", "ocio", "hobby", "pasatiempo"],
    "Shopping": ["compra", "compras", "retail", "tienda", "bold", "totto", "cco buleva", "compra en", "totto bogo", "bold*onas", "pasteleria", "plaza avent", "c.c plaza avent"],
    "Clothing": ["ropa", "vestimenta", "moda", "prendas", "calzado", "accesorios", "totto"],
    "Furniture & Housewares": ["muebles", "articulos para el hogar", "decoracion", "productos para el hogar", "hogar y jardin"],
    "Electronics": ["electronica", "gadgets", "dispositivos"],
    "Child Care": ["cuidado infantil", "bebe", "guarderia", "formula", "pañales", "cuarto de niños", "niñera"],
    "Child Activities": ["actividades infantiles", "juguetes", "juego", "juegos"],
    "Student Loans": ["prestamos estudiantiles", "prestamo educativo"],
    "Education": ["educacion", "escuela", "matricula", "colegiatura"],
    "Medical": ["medico", "salud", "farmacia", "hospital", "doctor", "terapia", "medicamento", "receta", "opticas la", "opticas", "cac suba b"],
    "Dentist": ["dentista", "dientes", "oral", "dental"],
    "Fitness": ["fitness", "gimnasio", "deportivo", "ejercicio"],
    "Loan Repayment": ["prestamo", "pago", "credito"],
    "Financial & Legal Services": ["financiero", "legal", "abogado", "contador", "servicios", "certificar"],
    "Financial Fees": ["tarifas", "cargos", "comisiones", "cuotas de cuenta", "4x1000", "impto gobierno", "impto gobierno 4x1000","cuota manejo", "cuota manejo tarjeta debito", "manejo tarjeta deb"],
    "Cash & ATM": ["efectivo", "cajero", "atm", "retiro", "multifunciona", "retiro cajero"],
    "Insurance": ["seguro", "poliza"],
    "Taxes": ["impuestos", "pago de impuestos", "secretaria de hacien", "pico y placa", "solicitud pico y placa", "pago pse secretaria de hacien"],
    "Uncategorized": ["sin categorizar", "desconocido"],
    "Check": ["cheque", "check"],
    "Miscellaneous": ["miscelaneo", "miscelaneos", "otro", "otros"],
    "Friendly Loans": ["prestamos personales", "prestamos familiares", "prestamos personales"],
    "Investments": ["inversion", "inversiones", "mercpago", "mercado pago", "gurus inve", "ak inversi", "mercpago*j", "gurus", "ak", "bold*"],
    "Advertising & Promotion": ["publicidad", "promocion", "marketing"],
    "Business Utilities & Communication": ["servicios de negocio", "internet", "telefono", "cable"],
    "Employee Wages & Contract Labor": ["salarios de empleados", "salario", "contratistas"],
    "Business Travels & Meals": ["viajes de negocios", "comidas", "viajes"],
    "Business Auto Expenses": ["gastos de auto para negocios", "vehiculo", "carro"],
    "Business Insurance": ["seguro de negocios", "poliza de empresa"],
    "Business Supplies & Expenses": ["suministros", "gastos de negocio"],
    "Office Rent": ["oficina", "renta", "arriendo"],
    "Postage & Shipping": ["correo", "envio", "mensajeria"],
    "Video Games": ["juegos", "videojuegos", "playstation", "xbox"],
    "Entertainment Subscriptions": ["series de video", "membresia de juegos", "servicios de juegos", "servicios de entretenimiento"],
    "SaaS Subscriptions": ["software", "apps", "dispositivos", "app"],
    "Electronics & Gadgets": ["electronica", "gadgets", "dispositivos"],
    "Transfer": ["transferencia", "movimiento", "fondos", "transferencia a nequi", "transferencia cta", "nequi", "transferencia cta suc virtual"],
    "Credit Card Payment": ["tarjeta de credito", "pago de tarjeta", "pago"],
    "Balance Adjustments": ["saldo", "ajustes", "correcciones", "ajuste", "ajuste interes", "ajuste interes ahorros db"]
}

# Function to transform the file into the desired format
def transform_file(df, account_name, cop_to_cad_rate):
    # Clean the data
    df = df.dropna(how='all')
    
    # Rename columns to match the desired output format
    df_renamed = pd.DataFrame()
    
    # Map original columns to new column names
    df_renamed['Date'] = df['FECHA']
    df_renamed['Merchant'] = df['DESCRIPCIÓN']
    # Initialize Category with empty strings
    df_renamed['Category'] = ""
    df_renamed['Account'] = account_name
    df_renamed['Original Statement'] = df['DESCRIPCIÓN'] + ' ' + df['REFERENCIA'].fillna('')
    df_renamed['Notes'] = ''
    
    # Process the amount column
    df_renamed['Amount'] = df['VALOR'].apply(lambda x: str(x).replace('$', '').replace(' ', '').replace(',', ''))
    df_renamed['Amount'] = pd.to_numeric(df_renamed['Amount'], errors='coerce')
    
    # Convert the amount from COP to CAD
    df_renamed['Amount'] = df_renamed['Amount'] * cop_to_cad_rate
    
    # Add currency information to Notes
    df_renamed['Notes'] = "Converted from COP to CAD (rate: " + str(cop_to_cad_rate) + ")"
    
    # Add original COP amount to Notes
    df_renamed['Original_COP'] = df['VALOR'].apply(lambda x: str(x).replace('$', '').replace(' ', '').replace(',', ''))
    df_renamed['Original_COP'] = pd.to_numeric(df_renamed['Original_COP'], errors='coerce')
    df_renamed['Notes'] = df_renamed['Notes'] + " | Original: " + df_renamed['Original_COP'].astype(str) + " COP"
    df_renamed.drop('Original_COP', axis=1, inplace=True)
    
    df_renamed['Tags'] = ''

    return df_renamed

# Function to process CSV for keyword mapping
def process_csv(df, mapping):
    print("Processing categories based on descriptions...")

    # Create a sorted list of (keyword, category) tuples
    sorted_keywords = sorted(
        ((kw, cat) for cat, keywords in mapping.items() for kw in keywords),
        key=lambda x: -len(x[0])  # Sort by keyword length (longer first)
    )

    # Vectorized replacement
    def map_category(value):
        if pd.isna(value):
            return "Uncategorized"
        value_lower = str(value).lower()
        for keyword, category in sorted_keywords:
            if keyword.lower() in value_lower:
                return category
        return "Uncategorized"

    # Use the Merchant column to determine the category
    df['Category'] = df['Merchant'].apply(map_category)
    return df

# Main execution flow
def main():
    input_file = input("Enter the path to the input CSV file: ")
    output_file = input("Enter the path to save the processed CSV file (leave blank for default): ")
    account_name = input("Enter the account name to fill in the Account column: ")
    
    # Currency conversion rate - average
    cop_to_cad_rate = float(0.00033333)
    
    if not output_file:
        output_file = input_file.rsplit(".", 1)[0] + "_processed.csv"

    print(f"Loading file: {input_file}")
    
    try:
        # Try to load with different encodings
        try:
            df = pd.read_csv(input_file, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(input_file, encoding='latin1')
            except:
                df = pd.read_csv(input_file, encoding='cp1252')
                
        print(f"File loaded. Number of rows: {len(df)}")

        # Transform the file to the desired format
        df = transform_file(df, account_name, cop_to_cad_rate)

        # Process the keyword mapping
        df = process_csv(df, keyword_mapping)

        # Save the transformed and processed file
        print(f"Processing complete. Saving to file: {output_file}")
        df.to_csv(output_file, index=False)
        print(f"File saved: {output_file}")
        
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()