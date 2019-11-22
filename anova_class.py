# How to use..?
# 1. import anova
# 2. Pass y_list=y vaues, y_cap_list=y predected values, degree_of_freedom= number of parameters to class

import scipy.stats as stats
import stats_team3 as common

# Structure of the dictionary we deal with
# This same dictionary will be returned with updated values once the computations are done successfully


class Anova:

    def __init__(self, y_list, y_cap_list, degree_of_freedom):
        # calucation point required
        degree_of_freedom = degree_of_freedom
        number_of_data_points = len(y_cap_list)

        # ssr calcualtion
        self.ssr_drg_of_freedom = degree_of_freedom-1
        self.ssr = self.sum_of_squred_regression(y_cap_list)
        self.msr = self.ssr/self.ssr_drg_of_freedom

        # sse calculation
        self.sse = self.sum_of_squred_error(y_list, y_cap_list)
        self.sse_dgr_pf_freedom = number_of_data_points-degree_of_freedom

        self.mse = self.sse/self.sse_dgr_pf_freedom

        # calculate F P and Model Confidence
        self.f = self.msr/self.mse
        self.p = stats.f.ppf(0.05,self.ssr_drg_of_freedom, self.sse_dgr_pf_freedom)
        self.model_confidence = self.get_model_confidence(self.p)

    def get_model_confidence(self,p:float):
        return (1-p)*100
    # caluate sum of error
    def sum_of_squred_error(self, y_list: [], y_cap_list: []):
        return sum([(y-y_cap) ** 2 for y, y_cap in zip(y_list, y_cap_list)])

    # cal sum of regression
    def sum_of_squred_regression(self, values):
        ymean = common.mean(values)
        return sum([(val - ymean) ** 2 for val in values])


if __name__ == "__main__":
    y_list=[]
    y_cap_list=[]
    degree_of_freedom=2
    anova = Anova(y_list,y_cap_list,degree_of_freedom)
    print("ssr=" + anova.ssr)
    print("sse=" + anova.sse)
    print("msr=" + anova.msr)
    print("mse=" + anova.mse)
    print("f=" + anova.f)
    print("p=" + anova.p)

