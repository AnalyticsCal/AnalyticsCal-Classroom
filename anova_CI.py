import scipy.stats as stats
import stats_team3 as common
from linear_algebra import LinearAlgebra
import math


class AnovaConfidenceInterval:
    anova = {}

    def __init__(self, xList, yList, yCapList):
        self.anova['x'] = xList
        self.anova['y_cap'] = yCapList
        self.anova['y'] = yList
    

    def cal_CI_of_Y_for_linear_eq(self, user_input_x: float, confidence_precentage: int):
        xlist = self.anova.get("x")
        x_mean = common.mean()
        n = len(xlist)
        error_sd = standard_diviation_of_errors()
        varinace_sum_mean = get_sum_of_variance_sqt(xlist, x_mean)
        se_y = error_sd*common.sqrt(1+1/n + ((user_input_x-x_mean)**2)/varinace_sum_mean)
        t_table_value = ttablevalue(n-2, confidence_precentage)
        y_cap_value_range = t_table_value*se_y
        rtn_value = []
        rtn_value.append(
            {"Confidence_Percent": confidence_precentage, "Value": y_cap_value_range})
        return rtn_value

    def cal_CI_cal_CI_of_Y_for_linear_eq(self, x: float):
        confidence_precentage = [90, 95, 99]
        xlist = self.anova.get("x")
        x_mean = common.mean()
        n = len(xlist)
        confidence_precentage = [90, 95, 99]
        rtn_value = []
        error_sd = standard_diviation_of_errors()
        varinace_sum_mean = get_sum_of_variance_sqt(xlist, x_mean)
        se_y = error_sd*common.sqrt(1+1/n + ((x-x_mean)**2)/varinace_sum_mean)
        for cp in confidence_precentage:
            t_table_value = ttablevalue(n-2, confidence_precentage)
            y_cap_value_range = t_table_value*se_y
            rtn_value.append(
                {"Confidence_Percent": cp, "Value": y_cap_value_range})
        return rtn_value

    def cal_CI_cal_CI_of_for_multimomial_eq(self, x_values: [], confidence_precentage: int):
        x_list = self.anova.get("x")
        n = len(x_list)
        error_sd = standard_diviation_of_errors()
        se_y = error_sd * get_se_y_cap(x_list, x_values)
        t_table_value = ttablevalue(n-2, confidence_precentage)
        y_cap_value_range = t_table_value*se_y
        rtn_value = []
        rtn_value.append(
            {"Confidence_Percent": confidence_precentage, "Value": y_cap_value_range})
        return rtn_value

        def cal_CI_cal_CI_of_for_multimomial_eq(self, x_values: []):
            confidence_precentage = [90, 95, 99]
            x_list = self.anova.get("x")
            n = len(x_list)
            error_sd = standard_diviation_of_errors()
            se_y = error_sd * get_se_y_cap(x_list, x_values)
            rtn_value = []
            for cp in confidence_precentage:
                t_table_value = ttablevalue(n-2, confidence_precentage)
                y_cap_value_range = t_table_value*se_y
                rtn_value.append(
                    {"Confidence_Percent": cp, "Value": y_cap_value_range})
            return rtn_value

    def get_se_y_cap(self, x_list: [], x_values: []):
        la = LinearAlgebra(len(x_list))
        c_transpose = la.transposeMatrix(x_values)
        x_transpose = la.getTranspose(x_list)
        x_x_transpose_inverse = la.getMatrixInverse(
            la.getMatrixMultiplication(x_list, x_transpose))
        c_tanspose_x_compound_inverse = la.getMatrixMultiplication(
            c_transpose, x_x_transpose_inverse)
        final_matrix_multipication = la.getMatrixMultiplication(
            c_tanspose_x_compound_inverse, x_values)
        rtn = math.sqrt(1+final_matrix_multipication)
        return rtn

    def ttablevalue(self, degree_of_freedom, confidencePrecentage):
        confident_percent = self.anova["confident_percent"]
        return stats.t.ppf(confident_percent/100, degree_of_freedom)

    def get_sum_of_variance_sqt(self, values, mean):
        return sum([(val - mean) ** 2 for val in values])

    def standard_diviation_of_errors(self):
        y_list = self.anova.get('y')
        y_cap_list = self.anova.get('y_cap')
        n = len(y_cap_list)
        error_list()
        sum_error_sqt = self.anova.get('sum_error_sqrt')
        error_sd = common.sqrt(sum_error_sqt/(n-2))
        return error_sd

    def error_list(self):
        y_list = self.anova.get('y')
        y_cap_list = self.anova.get('y_cap')
        rtn = []
        rtnSqr = []
        for y, y_cap in zip(y_list, y_cap_list):
            val = (y-y_cap)
            rtn.append(val)
            rtnSqr.append(val**2)
        anova['error'] = rtn
        anova['error_sqrt_list'] = rtnSqr
        anova['sum_error_sqrt'] = sum(rtnSqr)


