from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    def __init__(self, login, password, name, surname):
        self.login = login
        self.password = password
        self.name = name
        self.surname = surname

class DebtRow(Base):
    __tablename__ = 'debt'
    date = Column(Date, primary_key=True)
    total_state_debt = Column(Float, nullable=False)
    obligations = Column(Float, nullable=False)
    bank_credit = Column(Float, nullable=False)
    budget_credit = Column(Float, nullable=False)
    garanties = Column(Float, nullable=False)
    total_municipal_debt = Column(Float, nullable=False)

    def __init__(self, date, total_state_debt, obligations, bank_credit,
                 budget_credit, garanties, total_municipal_debt):
        self.date = date
        self.total_state_debt = total_state_debt
        self.obligations = obligations
        self.bank_credit = bank_credit
        self.budget_credit = budget_credit
        self.garanties = garanties
        self.total_municipal_debt = total_municipal_debt


class BudgReportRow(Base):
    __tablename__ = 'report'
    indicator_code = Column(String, primary_key=True)
    report_date = Column(Date, primary_key=True)
    code_name = Column(String)
    consolidated_plan = Column(Float)
    region_plan = Column(Float)
    consolidated_fact = Column(Float)
    region_fact = Column(Float)
    year = Column(Integer)
    indicator_id = Column(Integer)
    report_type_id = Column(Integer, primary_key=True)

    def __init__(self, indicator_code, report_date, code_name,
                 consolidated_plan, region_plan, consolidated_fact, region_fact,
                 year,indicator_id, report_type_id):
        self.indicator_code = indicator_code
        self.report_date = report_date
        self.code_name = code_name
        self.consolidated_plan = consolidated_plan
        self.region_plan = region_plan
        self.consolidated_fact = consolidated_fact
        self.region_fact = region_fact
        self.year = year
        self.indicator_id = indicator_id
        self.report_type_id = report_type_id

class CityDataRow(Base):
    __tablename__ = 'cities_data'
    date = Column(Date, primary_key=True)
    territory_name_on_date = Column(String, primary_key=True)
    territory_id = Column(Integer,primary_key=True)
    income_plan = Column(Integer)
    income_fact = Column(Integer)
    expense_plan = Column(Integer)
    expense_fact = Column(Integer)
    municipal_debt = Column(Integer)
    result_plan = Column(Integer)
    result_fact = Column(Integer)
    tax_no_tax_income_plan = Column(Integer)
    tax_no_tax_income_fact = Column(Integer)
    gratuitious_income_plan = Column(Integer)
    gratuitious_income_fact = Column(Integer)
    dotations_plan = Column(Integer)
    dotations_fact = Column(Integer)
    subsidies_plan = Column(Integer)
    subsidies_fact = Column(Integer)
    subventions_plan = Column(Integer)
    subventions_fact = Column(Integer)
    other_grat_plan = Column(Integer)
    other_grat_fact = Column(Integer)
    ndfl_plan = Column(Integer)
    ndfl_fact = Column(Integer)
    excise_plan = Column(Integer)
    excise_fact = Column(Integer)
    no_taxes_plan = Column(Integer)
    no_taxes_fact = Column(Integer)

    def __init__(self, date, territory_name_on_date, territory_id, income_plan, income_fact, expense_plan, expense_fact,
                 municipal_debt, result_plan, result_fact, tax_no_tax_income_plan, tax_no_tax_income_fact,
                 gratuitious_income_plan,gratuitious_income_fact, dotations_plan, dotations_fact,
                 subsidies_plan, subsidies_fact, subventions_plan, subventions_fact,
                 other_grat_plan, other_grat_fact, ndfl_plan, ndfl_fact, excise_plan, excise_fact,
                 no_taxes_plan, no_taxes_fact):
        self.date = date
        self.territory_name_on_date = territory_name_on_date
        self.territory_id = territory_id
        self.income_plan = income_plan
        self.income_fact = income_fact
        self.expense_plan = expense_plan
        self.expense_fact = expense_fact
        self.municipal_debt = municipal_debt
        self.result_plan = result_plan
        self.result_fact = result_fact
        self.tax_no_tax_income_plan = tax_no_tax_income_plan
        self.tax_no_tax_income_fact = tax_no_tax_income_fact
        self.gratuitious_income_plan = gratuitious_income_plan
        self.gratuitious_income_fact = gratuitious_income_fact
        self.dotations_plan = dotations_plan
        self.dotations_fact = dotations_fact
        self.subsidies_plan = subsidies_plan
        self.subsidies_fact = subsidies_fact
        self.subventions_plan = subventions_plan
        self.subventions_fact = subventions_fact
        self.other_grat_plan = other_grat_plan
        self.other_grat_fact = other_grat_fact
        self.ndfl_plan = ndfl_plan
        self.ndfl_fact = ndfl_fact
        self.excise_plan = excise_plan
        self.excise_fact = excise_fact
        self.no_taxes_plan = no_taxes_plan
        self.no_taxes_fact = no_taxes_fact


class CityName(Base):
    __tablename__ = 'cities_names'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

class BudgetIndicatorName(Base):
    __tablename__ = 'indicators'
    id = Column(Integer, primary_key=True)
    indicator_name = Column(String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

class StructRow(Base):
    __tablename__ = 'struct'
    header_id = Column(Integer, primary_key=True)
    struct_id = Column(Integer, primary_key=True)

    def __init__(self, header_id, struct_id):
        self.header_id = header_id
        self.struct_id = struct_id
