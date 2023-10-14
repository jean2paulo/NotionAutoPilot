import locale

def notion_query(notion, databaseId, filter, sort=None):
    if(sort==None):
        query = {"database_id": databaseId,"filter": filter}
    else:
        query = {"database_id": databaseId,"filter": filter, "sorts": sort}
    return notion.databases.query(**query)

# ---- REQUEST ---- #

# Filter

def notion_filter_and(condition_1, condition_2):
    return {"and": [condition_1, condition_2]}

def notion_filter_or(condition_1, condition_2):
    return { "or": [ condition_1, condition_2 ]}

# Filter properties

def notion_filter_relation(property_name, page_id):
    return { "property": property_name, "relation": { "contains": page_id } }

def notion_filter_not_status(property_name, status_id):
    return { "property": property_name, "status": { "does_not_equal": status_id }}

def notion_filter_status(property_name, status_id):
    return { "property": property_name, "status": { "equals": status_id }}

def notion_filter_checkbox(property_name, checked):
    return { "property": property_name, "checkbox": { "equals": checked }}

# Sort

def notion_sort_asc(property_name):
    return{ "property": property_name, "direction": "ascending"}

def notion_sort_desc(property_name):
    return{ "property": property_name, "direction": "descending"}

# ---- RESPONSE ---- #

# extract title

def extract_title(result, property_name):
    title = result["properties"][property_name]["title"]

    if title:
        return title[0].get('text', {}).get('content', '')
    else:
        return ''
    
def extract_status_name(result, property_name):
    title = result["properties"][property_name]["status"]

    if title:
        return title.get('name', {})
    else:
        return ''
    
def extract_relation_id(result, property_name):
    try:
        relation = result["properties"][property_name]["relation"]
        return relation[0]['id']
    except:
        return -1
    
def extract_formula_number(result, property_name):
    title = result["properties"][property_name]["formula"]

    if title:
        return title.get('number', {})
    else:
        return 0
    
# ---- FORMAT ---- #

def format_real(number):
    if number < 0:
        sinal = "-"
    else:
        sinal = ""
    return "{sinal}R$ {valor:,.2f}".format(sinal=sinal, valor=abs(number))

def formatar_percentage(number):
    return "%.2f%%" % (number * 100)