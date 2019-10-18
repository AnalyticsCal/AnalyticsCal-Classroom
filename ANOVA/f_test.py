"""
import pymysql
import os
import data_load
from data_load import load_and_filter_data_opeartion


dataset_file_name = "/home/archit/Documents/STUDY/CCE_IISC/BasicsofDataAnalytics/dataset/delhi_weather_sample.csv"
db = pymysql.connect("localhost", "root", "toortoor", "analytics")
cursor = db.cursor()
load_and_filter_data_opeartion(cursor, dataset_file_name)
"""
import scipy.stats as stats

anova_dict = {'x': [2, 4, 6, 8, 10], 'y': [6, 18, 38, 66, 102]}
model_eq = '11*X – 20'
co_efficients = [11,20]
degrees_of_freedom = len(co_efficients) #assuming Team 3 and 4 send list of co-efficients

def cal_average():
    """Calculates average (mean) of variable X"""
    anova_dict['y_bar'] = sum(anova_dict.get('y'))/len(anova_dict.get('y'))


def cal_y_cap():
    """Calculates y_cap for given value of x"""
    y_cap_list = []
    x_list = anova_dict.get('x')
    for x in x_list:
        y_cap_list.append(11*x-20)
    anova_dict['y_cap'] = y_cap_list
    anova_dict['y_cap_sum'] = sum(y_cap_list)


def cal_ssr():
    """Calculates SSR"""
    y_cap_list = anova_dict.get('y_cap')
    ssr_sum = 0
    y_bar = anova_dict['y_bar']
    for y in y_cap_list:
        ssr_sum = ssr_sum + ((y-y_bar)**2)
    anova_dict['ssr'] = ssr_sum


def cal_sse():
    """Calculates SSE"""
    y_list = anova_dict.get('y')
    y_cap_list = anova_dict.get('y_cap')
    sse_sum = 0
    for y, y_cap in zip(y_list, y_cap_list):
        sse_sum = sse_sum + (y-y_cap)**2
    anova_dict['sse'] = sse_sum


def cal_msr():
    """Calculates MSR with known SSR"""
    anova_dict['msr'] = anova_dict['ssr']/(degrees_of_freedom-1)


def cal_mse():
    """Calculates MSE with knowm SSE"""
    anova_dict['mse'] = anova_dict['sse']/(len(anova_dict.get('y'))-degrees_of_freedom)


def cal_f_and_p():
    """Calculates F and determines P"""
    f = anova_dict['msr']/anova_dict['mse']
    anova_dict['f'] = f
    F = (degrees_of_freedom-1)/(len(anova_dict.get('y'))-degrees_of_freedom)
    p = stats.f.sf(F, (degrees_of_freedom-1), (len(anova_dict.get('y'))-degrees_of_freedom))
    anova_dict['p'] = p


def main():
    cal_average()
    cal_y_cap()
    cal_ssr()
    cal_sse()
    cal_msr()
    cal_mse()
    cal_f_and_p()
    print(anova_dict)
    if anova_dict['p'] < anova_dict['f']:
        print("Best fit line is appropriate as per ANOVA.")
    else:
        print("Looks like the probablity of F being wrong is more; Please look for an alternate model!")


if __name__ == "__main__":
    main()
