import locale

# ---- UPDATE ---- #

def notion_update(notion, page_id, properties):
    notion.pages.update(page_id, properties = properties)

def notion_update_number(property_name, value):
    return { property_name:{ "number": value } }

def notion_update_string(property_name, value):
    return { property_name:{'rich_text': [{'text': { "content": value} }] } }

# ---- QUERY ---- #

def notion_query(notion, databaseId, filter=None, sort=None):
    query = { 'database_id': databaseId }
    if (filter != None):
        query['filter'] = filter
    if (sort != None):
        query['sort'] = sort
    return notion.databases.query(**query)

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

def notion_filter_number(property_name, number, condition='equals'):
    return {"property": property_name, "number": {condition: number}}

def notion_filter_number_greater_than_or_equal_to(property_name, number):
    return {"property": property_name, "number": {"greater_than_or_equal_to": number}}

# Sort

def notion_sort_asc(property_name):
    return{ "property": property_name, "direction": "ascending"}

def notion_sort_desc(property_name):
    return{ "property": property_name, "direction": "descending"}

# ---- RESPONSE ---- #

# extract title

def extract_id(result):
    return result["id"]

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
def extract_number(result, property_name):
    number = result["properties"][property_name]["number"]
    return number

def extract_formula_number(result, property_name):
    title = result["properties"][property_name]["formula"]

    if title:
        return title.get('number', {})
    else:
        return 0
    
def extract_rollup_number(result, property_name):
    title = result["properties"][property_name]["rollup"]

    if title:
        return title.get('number', {})
    else:
        return 0
# ---- FORMAT ---- #

def format_page_id(page_id): 
    return f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:]}"

def format_real(number):
    if number < 0:
        sinal = "-"
    else:
        sinal = ""
    return "{sinal}R$ {valor:,.2f}".format(sinal=sinal, valor=abs(number))

def formatar_percentage(number):
    return "%.2f%%" % (number * 100)

def format_float(number):
    return "{number:,.2f}".format(number=number)