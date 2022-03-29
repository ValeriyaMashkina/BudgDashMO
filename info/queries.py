from .models import *
from .reference import *
from .database import Base,SessionLocal, engine
from sqlalchemy.sql import select, join
from sqlalchemy import text
from sqlalchemy import func
from datetime import date
from sqlalchemy import and_, or_, not_

def get_min_max_date_debt(session):
    res = session.query(func.max(DebtRow.date).label("max_date"),
                  func.min(DebtRow.date).label("min_date")).one()
    return res.min_date, res.max_date

def get_min_max_date_budg(session):
    res = session.query(func.max(BudgReportRow.report_date).label("max_date"),
                        func.min(BudgReportRow.report_date).label("min_date")).one()
    return res.min_date, res.max_date


def get_debt_data(session, indicator, start_date, finish_date, period):
    first_date = start_date
    last_date = finish_date
    if start_date > finish_date:
        first_date = finish_date
        last_date = start_date
    periods = get_periods(period)

    return session.query(DebtRow.date, debt_data_dict[indicator]). \
        filter(and_(DebtRow.date >= first_date, DebtRow.date <= last_date,
                    DebtRow.date.in_(tuple(periods)))).order_by(DebtRow.date)

def get_budget_indicators_names(session):
    return [{'label': x[1], 'value': x[0]} for x in session.query(BudgetIndicatorName.id,
            BudgetIndicatorName.indicator_name).filter(BudgetIndicatorName.id != 900).all()]

def get_dates_cities(session):
    return [{'label': x.date.strftime('%d-%m-%Y'), 'value': x.date}
            for x in session.query(CityDataRow.date).distinct().order_by(CityDataRow.date)]

def get_struct_dates(session):
    return [{'label': x.report_date.strftime('%d-%m-%Y'), 'value': x.report_date} for x in
            session.query(BudgReportRow.report_date).distinct().order_by(BudgReportRow.report_date)]

def get_struct_indicators_names(session):
    return [{'label': x[1], 'value': x[0]} for x in
            session.query(StructRow.header_id, BudgetIndicatorName.indicator_name).distinct().\
        filter(StructRow.header_id == BudgetIndicatorName.id).all()]

def get_struct_data(session, level, state, date, indicator):
    row_name = level + state
    return session.query(StructRow.struct_id, BudgetIndicatorName.indicator_name, budg_row_dict[row_name]). \
                filter(StructRow.header_id == indicator).\
                filter(BudgetIndicatorName.id == StructRow.struct_id).\
                filter(and_(BudgReportRow.report_date == date, BudgReportRow.indicator_id==StructRow.struct_id))


def get_names_cities(session):
    return [{'label': x[1], 'value': x[0]} for x in session.query(CityName.id, CityName.name).all()]

def get_cities_data(session, indicator, state, date, cities):
    indicator_name = indicator + state
    return session.query(CityDataRow.territory_id, func.sum(cities_indicators_dict[indicator_name])). \
            filter(and_(CityDataRow.date == date, CityDataRow.territory_id.in_(tuple(cities)))).\
        group_by(CityDataRow.territory_id)\
        .order_by(CityDataRow.territory_id)

def get_cities_names(session):
    return session.query(CityName.id, CityName.name)

def get_budget_data(session, indicators, level, state, start_date, finish_date, period):
    row_name = level + state
    first_date = start_date
    last_date = finish_date
    if start_date > finish_date:
        first_date = finish_date
        last_date = start_date
    periods = get_periods(period)

    return session.query(BudgReportRow.indicator_id, BudgReportRow.report_date,budg_row_dict[row_name]).\
            filter(and_
                   (
                    BudgReportRow.report_date >= first_date, BudgReportRow.report_date <= last_date,
                    BudgReportRow.report_date.in_(tuple(periods)), BudgReportRow.indicator_id.in_(tuple(indicators))
                    ))\
                    .order_by(BudgReportRow.report_date, BudgReportRow.indicator_id)





