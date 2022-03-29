from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

from info.models import CityDataRow, BudgReportRow, DebtRow

debt_drop_down = [
        {'label':'Государственный долг', 'value': 'total_state_debt'},
        {'label':'Государственные ценные бумаги', 'value': 'obligations'},
        {'label': 'Банковские кредиты', 'value': 'bank_credit'},
        {'label': 'Бюджетные кредиты', 'value': 'budget_credit'},
        {'label': 'Государственные гарантии', 'value': 'garanties'},
        {'label': 'Муниципальный долг', 'value': 'total_municipal_debt'}]


cities_indicators_drop_down = [
        {'label':'Доходы', 'value': 'income'},
        {'label':'Расходы', 'value': 'expense'},
        {'label': 'Муниципальный долг', 'value': 'municipal_debt'},
        {'label': 'Дефицит/профицит', 'value': 'result'},
        {'label': 'Налоговые и неналоговые доходы', 'value': 'tax_no_tax_income'},
        {'label': 'Безвозмездные поступления', 'value': 'gratuitious_income'},
        {'label': 'Дотации', 'value': 'dotations'},
        {'label': 'Субсидии', 'value': 'subsidies'},
        {'label': 'Субвенции', 'value': 'subventions'},
        {'label': 'Иные безвозмездные поступления', 'value': 'other_grat'},
        {'label': 'Налог на доходы физических лиц', 'value': 'ndfl'},
        {'label': 'Акцизы', 'value': 'excise'},
        {'label': 'Неналоговые доходы', 'value': 'no_taxes'}]

cities_indicators_names = {'income_plan': 'Доходы (утверждено), тыс.рублей',
     'income_fact': 'Доходы (исполнено), тыс.рублей',
     'expense_plan': 'Расходы (утверждено), тыс.рублей',
     'expense_fact': 'Расходы (исполнено), тыс.рублей',
     'municipal_debt_plan': 'Муниципальный долг, тыс.рублей',
     'municipal_debt_fact': 'Муниципальный долг, тыс.рублей',
     'result_plan': 'Дефицит/профицит (утверждено), тыс.рублей',
     'result_fact': 'Дефицит/профицит (исполнено), тыс.рублей',
     'tax_no_tax_income_plan': 'Налоговые, неналоговые доходы (утверждено), тыс.рублей',
     'tax_no_tax_income_fact': 'Налоговые, неналоговые доходы (исполнено), тыс.рублей',
     'gratuitious_income_plan': 'Безвозмездные поступления (утверждено), тыс.рублей',
     'gratuitious_income_fact': 'Безвозмездные поступления (исполнено), тыс.рублей',
     'dotations_plan': 'Дотации (утверждено), тыс.рублей',
     'dotations_fact': 'Дотации (исполнено), тыс.рублей',
     'subsidies_plan': 'Субсидии (утверждено), тыс.рублей',
     'subsidies_fact': 'Субсидии (исполнено), тыс.рублей',
     'subventions_plan': 'Субвенции (утверждено), тыс.рублей',
     'subventions_fact': 'Субвенции (исполнено), тыс.рублей',
     'other_grat_plan': 'Прочие безвозмездные поступления (утверждено), тыс.рублей',
     'other_grat_fact': 'Прочие безвозмездные поступления (исполнено), тыс.рублей',
     'ndfl_plan': 'Налог на доходы физических лиц (утверждено), тыс.рублей',
     'ndfl_fact': 'Налог на доходы физических лиц (исполнено), тыс.рублей',
     'excise_plan': 'Акцизы (утверждено), тыс.рублей',
     'excise_fact': 'Акцизы (исполнено), тыс.рублей',
     'no_taxes_plan': 'Неналоговые доходы (исполнено), тыс.рублей',
     'no_taxes_fact': 'Неналоговые доходы (исполнено), тыс.рублей'}

debt_indicators_names = {'total_state_debt': 'Государственный долг, тыс.руб.',
              'obligations': 'Государственные ценные бумаги, тыс.руб.',
              'bank_credit': 'Банковские кредиты, тыс.руб.',
              'budget_credit': 'Бюджетные кредиты, тыс.руб.',
              'garanties': 'Государственные гарантии, тыс.руб.',
              'total_municipal_debt': 'Муниципальный долг, тыс.руб.'}


cities_indicators_dict = {'income_plan': CityDataRow.income_plan,
     'income_fact': CityDataRow.income_fact,
     'expense_plan': CityDataRow.expense_plan,
     'expense_fact':CityDataRow.expense_fact,
     'municipal_debt_plan': CityDataRow.municipal_debt,
     'municipal_debt_fact': CityDataRow.municipal_debt,
     'result_plan':CityDataRow.result_plan,
     'result_fact': CityDataRow.result_fact,
     'tax_no_tax_income_plan': CityDataRow.tax_no_tax_income_plan,
     'tax_no_tax_income_fact':CityDataRow.tax_no_tax_income_fact,
     'gratuitious_income_plan':CityDataRow.gratuitious_income_plan,
     'gratuitious_income_fact':CityDataRow.gratuitious_income_fact,
     'dotations_plan':CityDataRow.dotations_plan,
     'dotations_fact':CityDataRow.dotations_fact,
     'subsidies_plan': CityDataRow.subsidies_plan,
     'subsidies_fact':CityDataRow.subsidies_fact,
     'subventions_plan':CityDataRow.subventions_plan,
     'subventions_fact':CityDataRow.subventions_fact,
     'other_grat_plan':CityDataRow.other_grat_plan,
     'other_grat_fact':CityDataRow.other_grat_fact,
     'ndfl_plan':CityDataRow.ndfl_plan,
     'ndfl_fact':CityDataRow.ndfl_fact,
     'excise_plan':CityDataRow.excise_plan,
     'excise_fact':CityDataRow.excise_fact,
     'no_taxes_plan':CityDataRow.no_taxes_plan,
     'no_taxes_fact':CityDataRow.no_taxes_fact}


budg_row_dict = {'consolidated_plan':BudgReportRow.consolidated_plan,
                      'consolidated_fact': BudgReportRow.consolidated_fact,
                      'region_plan': BudgReportRow.region_plan,
                      'region_fact': BudgReportRow.region_fact}

debt_data_dict ={'total_state_debt':DebtRow.total_state_debt,
                 'obligations': DebtRow.obligations,
                 'bank_credit':DebtRow.bank_credit,
                 'budget_credit': DebtRow.budget_credit,
                 'garanties': DebtRow.garanties,
                 'total_municipal_debt':DebtRow.total_municipal_debt}


def get_periods(key):
    start_date = date(2015,1, 1)
    finish_date = date(2021, 1, 1)
    kvart_list_debt = []
    month_list_debt = []
    current_date = start_date

    while current_date <= finish_date:
            if current_date.month in [1, 4, 7, 10]:
                    kvart_list_debt.append(current_date)
            month_list_debt.append(current_date)
            current_date = current_date + relativedelta(months=1)

    period_dict_debt= {1 : [date(2015,1, 1),date(2016,1, 1),
                   date(2017,1, 1),date(2018,1, 1),
                   date(2019,1, 1), date(2020,1, 1),
                   date(2021,1, 1)],
              4: kvart_list_debt,
              12: month_list_debt}
    return period_dict_debt[key]




