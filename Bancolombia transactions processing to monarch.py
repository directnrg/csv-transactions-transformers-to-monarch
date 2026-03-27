import pandas as pd
from pathlib import Path
from transaction_utils import CSVLoader, CategoryMapper, CategoryNormalizer

# Keyword mapping for Bancolombia (Spanish keywords)
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

def transform_file(df, account_name, cop_to_cad_rate):
    """Transform Bancolombia CSV to standard format with currency conversion."""
    df = df.dropna(how='all')

    # Map columns
    df_renamed = pd.DataFrame()
    df_renamed['Date'] = df['FECHA']
    df_renamed['Merchant'] = df['DESCRIPCIÓN']
    df_renamed['Category'] = ""
    df_renamed['Account'] = account_name
    df_renamed['Original Statement'] = df['DESCRIPCIÓN'] + ' ' + df['REFERENCIA'].fillna('')

    # Clean and convert amounts from COP to CAD
    amount_cleaned = df['VALOR'].astype(str).str.replace(r'[\$\s,]', '', regex=True)
    amount_numeric = pd.to_numeric(amount_cleaned, errors='coerce') * cop_to_cad_rate
    df_renamed['Amount'] = amount_numeric

    # Store original COP amount in notes
    original_cop = pd.to_numeric(amount_cleaned, errors='coerce')
    df_renamed['Notes'] = ("Converted from COP to CAD (rate: " + str(cop_to_cad_rate) +
                          ") | Original: " + original_cop.astype(str) + " COP")
    df_renamed['Tags'] = ''

    return df_renamed


def process_csv(df, mapping):
    """Categorize transactions using keyword mapping."""
    print("Processing categories based on descriptions...")

    mapper = CategoryMapper(mapping)
    df['Category'] = df['Merchant'].apply(mapper.map_category)
    return df

def main():
    input_file = input("Enter the path to the input CSV file: ").strip('"').strip("'").strip()
    output_file = input("Enter the path to save the processed CSV file (leave blank for default): ").strip('"').strip("'").strip()
    account_name = input("Enter the account name to fill in the Account column: ")

    cop_to_cad_rate = float(0.00033333)

    if not output_file:
        output_file = input_file.rsplit(".", 1)[0] + "_processed.csv"

    # If user provided a directory path, append default filename
    output_path = Path(output_file)
    if output_path.is_dir() or (not output_path.suffix and output_file.endswith('\\')):
        output_file = str(output_path / (Path(input_file).stem + "_processed.csv"))

    print(f"Loading file: {input_file}")

    try:
        # Use CSVLoader for encoding detection
        df = CSVLoader.load(input_file)
        print(f"File loaded. Number of rows: {len(df)}")

        # Transform and categorize
        df = transform_file(df, account_name, cop_to_cad_rate)
        df = process_csv(df, keyword_mapping)

        # Normalize categories
        df['Category'] = df['Category'].apply(CategoryNormalizer.normalize)

        # Save
        print(f"Processing complete. Saving to file: {output_file}")
        df.to_csv(output_file, index=False)
        print(f"File saved: {output_file}")

    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()