#!/home/daniil/uni/diploma/diploma-report/tex-generator/.venv/bin/python
import os
import re
from jinja2 import Environment, FileSystemLoader

def latex_escape(text):
    if not isinstance(text, str):
        return text
    conv = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
        '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}', '\\': r'\textbackslash{}',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: -len(item))))
    return regex.sub(lambda mo: conv[mo.group()], text)

month_working_hours = 168
price_bonus = 1.5
extra_norm = 20
social_needs = 34
social_protection = 0.6
social_total = social_needs + social_protection
additional_outcome = 20
rental = 35
income_fine = 20

stuff = [
    {
        "role": "Системный архитектор",
        "price_month": 8600.00,
        "working_hours": 168
    },
    {
        "role": "Бизнес-аналитик",
        "price_month": 5600.00,
        "working_hours": 160
    },
    {
        "role": "Инженер-программист",
        "price_month": 7100.00,
        "working_hours": 480
    },
    {
        "role": "Дизайнер",
        "price_month": 4900.00,
        "working_hours": 140
    },
    {
        "role": "Тестировщик",
        "price_month": 4600.00,
        "working_hours": 200
    }
]

total_salary = 0
for p in stuff:
    p["hourly_salary"] = p["price_month"] / month_working_hours
    p["total"] = price_bonus * p["hourly_salary"] * p["working_hours"]
    total_salary += p["total"]

extra_salary = total_salary * extra_norm / 100
social_needs_payment = (total_salary + extra_salary) * social_total / 100
additional_outcome_payment = total_salary * additional_outcome / 100
development_cost_total = total_salary + extra_salary + social_needs_payment + additional_outcome_payment
planned_income = development_cost_total * rental / 100
product_price = development_cost_total + planned_income

producer_economical_effect = planned_income * (1 - income_fine / 100)
producer_rental = producer_economical_effect / development_cost_total * 100

work_amount_after_implementation = 0.2
hour_customer_employee_payment = 22
planned_customer_employee_working_volume = 2016
maintanence_cost = 0

salary_benefit = price_bonus * (1 - work_amount_after_implementation) * hour_customer_employee_payment * planned_customer_employee_working_volume * (1 + extra_norm / 100) * (1 + social_total / 100)
customer_economical_effect = (salary_benefit - maintanence_cost) * (1 - income_fine / 100)

bank_refinancial = 9.75
years = [1, 2, 3, 4]
years_rates = []

results = []
discounted_results = []
investments = [development_cost_total, 0, 0, 0]
discounted_investments = []
npv_yearly = []
npv_cumulative = []
implementation_period_months = 3
first_year_factor = (12 - implementation_period_months) / 12

cumulative = 0
for i, y in enumerate(years):
    alpha = 1 / ((1 + bank_refinancial / 100) ** (y - 1))
    years_rates.append(alpha)

    if (i == 0):
        res = first_year_factor * customer_economical_effect
    else:
        res = customer_economical_effect

    results.append(res)
    disc_res = res * alpha
    discounted_results.append(disc_res)
    
    inv = investments[i]
    disc_inv = inv * alpha
    discounted_investments.append(disc_inv)
    
    npv = disc_res - disc_inv
    npv_yearly.append(npv)
    
    cumulative += npv
    npv_cumulative.append(cumulative)

payback_period = sum(discounted_investments) / (sum(discounted_results) / len(years))
profitability_index = sum(discounted_results) / sum(discounted_investments)

data = {
    "stuff": stuff,
    "month_working_hours": month_working_hours,
    "price_bonus": price_bonus,
    "extra_norm": extra_norm,
    "social_needs": social_needs,
    "social_protection": social_protection,
    "social_total": social_total,
    "additional_outcome": additional_outcome,
    "rental": rental,
    "income_fine": income_fine,
    "total_salary": total_salary,
    "extra_salary": extra_salary,
    "social_needs_payment": social_needs_payment,
    "additional_outcome_payment": additional_outcome_payment,
    "development_cost_total": development_cost_total,
    "planned_income": planned_income,
    "product_price": product_price,
    "producer_economical_effect": producer_economical_effect,
    "producer_rental": producer_rental,
    "work_amount_after_implementation": work_amount_after_implementation,
    "hour_customer_employee_payment": hour_customer_employee_payment,
    "planned_customer_employee_working_volume": planned_customer_employee_working_volume,
    "salary_benefit": salary_benefit,
    "customer_economical_effect": customer_economical_effect,
    "bank_refinancial": bank_refinancial,
    "years": years,
    "years_rates": years_rates,
    "results": results,
    "discounted_results": discounted_results,
    "investments": investments,
    "discounted_investments": discounted_investments,
    "npv_yearly": npv_yearly,
    "npv_cumulative": npv_cumulative,
    "payback_period": payback_period,
    "profitability_index": profitability_index,
    "implementation_period_months": implementation_period_months
}

env = Environment(
    block_start_string='((%',
    block_end_string='%))',
    variable_start_string='((*',
    variable_end_string='*))',
    loader=FileSystemLoader('.')
)
env.filters['tex'] = latex_escape

template = env.get_template('economics.tpl')
rendered_tex = template.render(**data)

print(rendered_tex)
