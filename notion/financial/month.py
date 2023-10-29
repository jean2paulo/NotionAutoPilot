from notion.commons import utils as notion_utils
from .constants import * 
from .strings import *

def get_totals_message(notion):
     total_data = get_month_totals(notion)
     return format_month_totals_message(total_data)
    

def get_month_totals(notion):
    return notion_utils.notion_query(notion, FINANCIAL_MONTH_PAGE_ID, 
        notion_utils.notion_filter_checkbox(ACT_MONTH_NOTION_PROPERTY, True)
    )

def format_month_totals_message(data):
    if(len(data[RESULTS]) > 0):
        financial_message = TITLE_TEXT + "\n"
        result = data[RESULTS][0]

        total = notion_utils.extract_formula_number(result, TOTAL_NOTION_PROPERTY)
        actual = notion_utils.extract_formula_number(result, TOTAL_NOW_NOTION_PROPERTY)
        percent = actual/total - 1

        financial_message += ITEM_TEXT_FORMAT % notion_utils.format_real(total)
        financial_message += ITEM_TEXT_FORMAT % notion_utils.format_real(actual)
            
        if(percent > 0):
            financial_message += POSITIVE_TOTAL_NET_PERCENT_DATA_FORMAT % notion_utils.formatar_percentage(percent)
        else:
            financial_message += NEGATIVE_TOTAL_NET_PERCENT_DATA_FORMAT % notion_utils.formatar_percentage(percent)

        financial_message += "\n\n"
        financial_message += TITLE_2_TEXT

        incoming = notion_utils.extract_rollup_number(result, TOTAL_INCOMING_NOTION_PROPERTY)
        outcoming = notion_utils.extract_rollup_number(result, TOTAL_OUTCOMING_NOTION_PROPERTY)
        investement = notion_utils.extract_rollup_number(result, TOTAL_INVESTMENTS_NOTION_PROPERTY)

        financial_message += INCOMING_TEXT_FORMAT % notion_utils.format_real(incoming)
        financial_message += OUTCOMING_TEXT_FORMAT % notion_utils.format_real(outcoming)
        financial_message += INVESTIMENT_TEXT_FORMAT % notion_utils.format_real(investement)

    else:
        financial_message = NO_DATA_TEXT

    return financial_message

