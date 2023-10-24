from notion import utils as notion_utils

# Projects Notion Page
FINANCIAL_MONTH_PAGE_ID = "ecc237c39382476e8cefc7224ca5f87c"

def check_financial_month_totals(notion):
    data = notion_utils.notion_query(notion, FINANCIAL_MONTH_PAGE_ID, 
            notion_utils.notion_filter_checkbox("Mês atual", True)
        )
    full_message = ''
    if(len(data["results"]) > 0):
        full_message = "💰 Patrimonio"
        result = data["results"][0]

        invested = notion_utils.extract_formula_number(result, "Valor Investido")
        actual = notion_utils.extract_formula_number(result, "Valor Atual")
        percent = actual/invested - 1

        full_message += f"\n→ {notion_utils.format_real(invested)}"
        full_message += f"\n→ {notion_utils.format_real(actual)}"
        
        if(percent > 0):
            full_message += f"\t\t📈 {notion_utils.formatar_percentage(percent)}"
        else:
            full_message += f"\t\t📉 {notion_utils.formatar_percentage(percent)}"

    else:
        full_message = "💰 Sem dados! "

    return full_message