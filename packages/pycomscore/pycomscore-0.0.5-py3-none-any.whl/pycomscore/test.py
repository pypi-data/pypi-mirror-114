# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:16:32 2021

@author: Carlos.Trujillo
"""


from pycomscore import comscore_omnicom_database

coms_obj = comscore_omnicom_database(user = 'user', password = 'pass')

#Modulo 1.
dataframe_time = coms_obj.domain_by_time(domain = 'sodimac.cl', 
                                         country = 'cl')

#Modulo 2.
dataframe_geo = coms_obj.demographics_by_web(country = 'mx', start_date = '2020-01-01', end_date = '2020-12-31', 
                                            event_like = 'atv', 
                                            domain = 'brp.com', 
                                            saved = False, 
                                            age_group = True,
                                            ages_between = None, gender_between = None)

#Modulo 3.
dataframe, dataframe_corr, dataframe_uniq_matrix, final_corr = coms_obj.correlation_between_domains(country = 'cl', 
                                                                            url_site = 'sodimac.cl')

#Modulo 4.
dataframes, matrix_overlap = coms_obj.overlaps_between_pages(country = 'mx', start_date = '2020-01-01', end_date = '2020-12-31',
                                                             domain = 'brp.com', competitors = ('polarismexico.com', 'harley-davidson.com'),
                                                             like_domain = 'offroad', like_competitors = 'atv',
                                                             saved = False)

#Modulo 5.
all_probabilities, short_frame_probabilities = coms_obj.bayesian_inference_over_sites(country = 'cl', 
                                                                                      domain = 'sodimac.cl', 
                                                                                      time_spent = 300, 
                                                                                      start_date = '2021-01-01',
                                                                                      end_date ='2021-05-01')

#Modulo 6.
short_frame_probabilities, all_complete_frame = coms_obj.bayesian_site_predictor(country = 'cl', 
                                                                                 domain = 'sodimac.cl', 
                                                                                 #time_spent = time_spent_site, 
                                                                                 start_date = '2021-01-01',
                                                                                 end_date ='2021-05-01')