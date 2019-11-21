import scipy.stats as stats
import stats_team3 as common
from linear_algebra import LinearAlgebra
import math


class AnovaConfidenceInterval:

    def __init__(self, x_list:[], y_list:[], y_cap_list:[],degree_of_feedom:int):

        #common values
        self.__confidence_precentage = [90, 95, 99]
        self.x_List = x_list
        self.y_cap_list = y_cap_list
        self.y_list= y_list
        self.x_mean = common.mean(x_list)
        self.number_data_point = len(y_cap_list)
        self.degree_of_freedom=degree_of_feedom
        self.error_standard_deviation = self.standard_deviation_of_errors(y_list,y_cap_list,self.number_data_point,2)
        self.varinace_sum_mean_of_x = self.get_sum_of_variance_sqt(self.x_List, self.x_mean)

    def cal_CI_tm_tc(self, confidence_percent: int):
        """Calculating Confidence Interval tm and tc"""      
        t_table_value = self.ttablevalue(self.number_data_point-2, confidence_percent)
        self.tm =  t_table_value * self.__get_se_m()
        self.tc =  t_table_value * self.__get_se_c()
        rtn_value = {'tm': self.tm,'tc' : self.tc}
        return rtn_value

    def cal_CI_of_Y_for_polynomial_eq(self, user_input_x: float, confidence_precent: int):
        se_y = self.error_standard_deviation  * common.sqrt( 1 + 1 /+ ((user_input_x-x_mean)**2)/self.varinace_sum_mean_of_x)
        return { confidence_precent: self.__get_y_confidence_value(se_y,confidence_precent)}

    def cal_CI_of_Y_for_polynomial_eq(self, user_input_x: float, confidence_precent: []):
        se_y = self.error_standard_deviation * common.sqrt(1 + 1/self.number_data_point + ((user_input_x-x_mean)**2)/self.varinace_sum_mean_of_x)
        self.confidence_interval_poly = {}
        for cp in confidence_precent:
            y_cap_value_range = __get_y_confidence_value(se_y, cp)
            self.confidence_interval_poly[cp]= y_cap_value_range
        return self.confidence_interval_poly

    def cal_CI_of_Y_for_polynomial_eq(self, user_input_x: float):
        return self.cal_CI_of_Y_for_polynomial_eq(user_input_x, __confidence_precentage)       

    def __get_se_m(self):
        return self.error_standard_deviation * common.sqrt(1 / self.varinace_sum_mean_of_x)

    def __get_se_c(self):
        return self.error_standard_deviation * common.sqrt(1 / self.number_data_point + (self.x_mean ** 2) / self.varinace_sum_mean_of_x)

    def __get_y_confidence_value(self,se_y:float,confidence_precent:int):
        t_table_value = self.ttablevalue(self.number_data_point-self.degree_of_freedom,confidence_precent)
        y_cap_value_range = t_table_value *  se_y    
        return y_cap_value_range
    
    def cal_CI_cal_CI_of_for_multimomial_eq(self, x_values: [], confidence_precent: int):
        se_y = self.standard_deviation_of_errors * self.get_se_y_cap(self.x_List, x_values)
        rtn_value = {confidence_precent:__get_y_confidence_value(se_y,confidence_precent)}
        return rtn_value

    def cal_CI_cal_CI_of_for_multimomial_eq(self, x_values: [],confidence_precent:[]):
        se_y = self.standard_diviation_of_errors * self.get_se_y_cap(self.x_List, x_values)
        rtn_value = {}
        for cp in confidence_precent:
             y_cap_value_range = __get_y_confidence_value(se_y, cp)
             rtn_value[cp]= y_cap_value_range
        return rtn_value

    def get_se_y_cap(self, x_list: [], x_values: []):
        la = LinearAlgebra(len(x_list))
        c_transpose = la.transposeMatrix(x_values)
        x_transpose = la.getTranspose(x_list)
        x_x_transpose_inverse = la.getMatrixInverse(la.getMatrixMultiplication(x_list, x_transpose))

        c_tanspose_x_compound_inverse = la.getMatrixMultiplication(c_transpose, x_x_transpose_inverse)

        final_matrix_multipication = la.getMatrixMultiplication(c_tanspose_x_compound_inverse, x_values)
        rtn = math.sqrt(1 + final_matrix_multipication)
        return rtn

    def ttablevalue(self, degree_of_freedom, confidence_precent):
        return stats.t.ppf(confidence_precent/100, degree_of_freedom)

    def get_sum_of_variance_sqt(self, values, mean):
        return sum([(val - mean) ** 2 for val in values])

    def standard_deviation_of_errors(self,y_list:[],y_cap_list:[],number_of_data_point:int,degree_of_freedom:int):
        sum_error_sqt =   self.error_list(y_list,y_cap_list)
        return common.sqrt(sum_error_sqt/(number_of_data_point - degree_of_freedom))

    def error_list(self,y_list:[],y_cap_list:[]):
        return sum([(y - y_cap) ** 2  for y, y_cap in zip(y_list, y_cap_list)])
