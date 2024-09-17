import spacy

nlp = spacy.load('en_core_web_sm')

def extract_query_details(query):
    doc = nlp(query.lower())
    if 'sales' in query:
        if "top" in query and "products" in query:
            return 'top_sales_products'
        elif "total" in query and "last week" in query:
            return 'total_sales_last_week'
        elif "product" in query:
            return 'product_sales'
    elif 'inventory' in query:
        if "low stock" in query:
            return 'low_stock_products'
        elif "stock" in query:
            return 'current_stock'
    elif 'product' in query:
        if "details" in query:
            return 'product_details'
        elif "list" in query:
            return 'list_products'
    return 'unknown'

def extract_product_name(query):
    # Extract product name from query (this is a simplified example)
    # You might need a more advanced method to extract product names
    doc = nlp(query.lower())
    for ent in doc.ents:
        if ent.label_ == 'PRODUCT':
            return ent.text
    return 'Unknown Product'
