"""Generate synthetic IBM HR Employee Attrition dataset with realistic patterns."""
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)
N = 1470

age = np.random.randint(18, 61, N)
gender = np.random.choice(['Male', 'Female'], N, p=[0.6, 0.4])
marital = np.random.choice(['Single', 'Married', 'Divorced'], N, p=[0.32, 0.46, 0.22])
dept = np.random.choice(['Research & Development', 'Sales', 'Human Resources'], N, p=[0.65, 0.30, 0.05])
role_map = {
    'Research & Development': ['Research Scientist', 'Laboratory Technician', 'Manufacturing Director', 'Research Director', 'Manager'],
    'Sales': ['Sales Executive', 'Sales Representative', 'Manager'],
    'Human Resources': ['Human Resources', 'Manager'],
}
job_role = [np.random.choice(role_map[d]) for d in dept]
education = np.random.choice([1, 2, 3, 4, 5], N, p=[0.05, 0.12, 0.38, 0.30, 0.15])
education_field = np.random.choice(['Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Other', 'Human Resources'], N, p=[0.32, 0.25, 0.12, 0.12, 0.10, 0.09])

income_base = {
    'Research Scientist': 4500, 'Laboratory Technician': 3500, 'Manufacturing Director': 8000,
    'Research Director': 10000, 'Manager': 12000, 'Sales Executive': 7000,
    'Sales Representative': 3000, 'Human Resources': 5500,
}
monthly_income = np.array([int(np.clip(np.random.normal(income_base[r], income_base[r]*0.3), 1009, 19999)) for r in job_role])

years_company = np.random.randint(0, 41, N)
total_working = np.clip(years_company + np.random.randint(-5, 15, N), 0, 40)
years_role = np.clip(years_company - np.random.randint(0, 5, N), 0, 40)
years_manager = np.clip(years_role - np.random.randint(0, 3, N), 0, 40)
years_promo = np.random.choice(range(0, 16), N, p=[0.15, 0.15, 0.15, 0.12, 0.10, 0.08, 0.06, 0.05, 0.04, 0.03, 0.02, 0.02, 0.01, 0.01, 0.01, 0.00])

overtime = np.random.choice(['Yes', 'No'], N, p=[0.28, 0.72])
distance = np.random.randint(1, 30, N)
job_sat = np.random.choice([1, 2, 3, 4], N, p=[0.12, 0.22, 0.38, 0.28])
env_sat = np.random.choice([1, 2, 3, 4], N, p=[0.10, 0.20, 0.35, 0.35])
wlb = np.random.choice([1, 2, 3, 4], N, p=[0.05, 0.15, 0.45, 0.35])
job_inv = np.random.choice([1, 2, 3, 4], N, p=[0.05, 0.15, 0.40, 0.40])
num_companies = np.random.choice(range(0, 10), N, p=[0.20, 0.25, 0.20, 0.12, 0.08, 0.06, 0.04, 0.03, 0.01, 0.01])

# Attrition probability based on real patterns
log_odds = np.full(N, 0.3)
log_odds += 1.5 * (overtime == 'Yes').astype(float)
log_odds -= 0.4 * job_sat.astype(float)
log_odds -= 0.3 * wlb.astype(float)
log_odds -= 0.05 * monthly_income / 1000
log_odds += 1.0 * (years_company <= 2).astype(float)
log_odds -= 0.05 * years_company.astype(float)
log_odds += 0.7 * (years_promo >= 3).astype(float)
log_odds += np.random.normal(0, 0.3, N)

prob = 1 / (1 + np.exp(-log_odds))
attrition = (np.random.random(N) < prob).astype(int)
attrition_label = np.where(attrition, 'Yes', 'No')

daily_rate = np.random.randint(102, 1500, N)
hourly_rate = np.random.randint(30, 100, N)
monthly_rate = np.random.randint(2000, 30000, N)
percent_hike = np.random.choice(range(11, 26), N)
perf_rating = np.random.choice([1, 2, 3, 4], N, p=[0.05, 0.15, 0.60, 0.20])
rel_sat = np.random.choice([1, 2, 3, 4], N, p=[0.10, 0.20, 0.35, 0.35])
stock_opt = np.random.choice([0, 1, 2, 3], N, p=[0.35, 0.30, 0.20, 0.15])
training = np.random.choice([0, 1, 2, 3, 4, 5, 6], N, p=[0.05, 0.15, 0.30, 0.25, 0.15, 0.08, 0.02])
business_travel = np.random.choice(['Travel_Rarely', 'Travel_Frequently', 'Non-Travel'], N, p=[0.70, 0.18, 0.12])

df = pd.DataFrame({
    'Age': age,
    'Attrition': attrition_label,
    'BusinessTravel': business_travel,
    'DailyRate': daily_rate,
    'Department': dept,
    'DistanceFromHome': distance,
    'Education': education,
    'EducationField': education_field,
    'EmployeeCount': [1]*N,
    'EmployeeNumber': range(1, N+1),
    'EnvironmentSatisfaction': env_sat,
    'Gender': gender,
    'HourlyRate': hourly_rate,
    'JobInvolvement': job_inv,
    'JobLevel': np.clip(education, 1, 5),
    'JobRole': job_role,
    'JobSatisfaction': job_sat,
    'MaritalStatus': marital,
    'MonthlyIncome': monthly_income,
    'MonthlyRate': monthly_rate,
    'NumCompaniesWorked': num_companies,
    'Over18': ['Y']*N,
    'OverTime': overtime,
    'PercentSalaryHike': percent_hike,
    'PerformanceRating': perf_rating,
    'RelationshipSatisfaction': rel_sat,
    'StandardHours': [80]*N,
    'StockOptionLevel': stock_opt,
    'TotalWorkingYears': total_working,
    'TrainingTimesLastYear': training,
    'WorkLifeBalance': wlb,
    'YearsAtCompany': years_company,
    'YearsInCurrentRole': years_role,
    'YearsSinceLastPromotion': years_promo,
    'YearsWithCurrManager': years_manager,
})

out = Path(__file__).parent / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
df.to_csv(out, index=False)
print(f"Dataset saved: {len(df)} rows, {len(df.columns)} columns")
print(f"Attrition rate: {(df['Attrition']=='Yes').mean()*100:.1f}%")
print(df.head())
