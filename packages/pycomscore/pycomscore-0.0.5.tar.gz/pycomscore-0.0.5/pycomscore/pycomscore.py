"""
This is a module that allows you to connect to the Comscore library 
developed by Annalect and obtain synthesized information.
"""

__author__ = "Carlos Trujillo, Data analytics Manager"
__email__ = "carlos.trujillo@omnicommediagroup.com"
__status__ = "planning"


from sqlalchemy import create_engine
from pandas import read_sql, DataFrame

import numpy as np
import pandas as pd

from collections import Counter

class comscore_omnicom_database:
    """Class to generate a connection to the OMG comscore database.

    Example:
    >>> comscore = comscore_omnicom_database(user = 'user_name', password = 'password_value')
    >>> dataframe_time = comscore.domain_by_time(country = 'cl')
    >>> dataframe_time.head(5)

    """
    
    def __init__(self, user, password, endpoint = None):
        """Login into our database.

        Note:
            All users and passwords must have been provided by the annalect team. 
            Additionally, they must be connected to the Annalect VPN to be able to access, otherwise, you will get a connection error.

        Args:
            user (str): User name that will connect to the database. Delivered by the annalect team.
            password (str): User password that will connect to the database. Delivered by the annalect team.
            endpoint (:obj:`str`, optional): Database endpoint, by default the redshift database comes but you can choose another one. 
                                            This step is optional

        """

        self.user = user
        self.password = password
        
        if isinstance(endpoint, type(None)):
     
            self.engine_str = 'postgresql://' + str(self.user) + ':' + str(self.password) + '@dsdk-v0p1-annalect.clf6bikxcquu.us-east-1.redshift.amazonaws.com:5439/dsdk'
        
        else:
            self.engine_str = 'postgresql://' + str(self.user) + ':' + str(self.password) + str(endpoint)
        
        self.engine = create_engine(self.engine_str)
        self.connection = self.engine.connect()
    
    def domain_by_time(self, country = None, start_date = None, end_date = None, event_like = False, domain = None, saved = False):
        """Function to generate a query to the database and obtain the total number of visits and reach in a period of time.

        Note:
            To use this method, you must have previously logged in.

        Args:
            country (str, required): Select the country code on which you want to create a query. 
                Possible options are: ['us','ar', 'au','br', 'ca', 'cl', 'co', 'hk', 'id', 'in', 'mx', 'my', 'nz', 'sg', 'tw']

            start_date (str, optional): Select from which date you want to see your data.
                The default is 2019-01-01

            end_date (str, optional): Select the maximum date to consult.
                The default value is 2019-06-01

            event_like (str, optional): An additional WHERE statement that adds the "LIKE" in SQL. All the words you consider will be taken.
                if you use the event_like operator your query will look like the following.
                Example: SELECT * FROM table WHERE domain = somedomain.com AND event_detail LIKE '% event_like_value %' 

            domain (str, required): The specified domain you want to know about. This value is required.

            saved (bool, optional): If saved is true then you must indicate the path where you want to save 
                the file and it will be saved on your local machine.
                This is optional.

        Returns:
            DataFrame: If the process occurs correctly, you will get a dataframe with all the required data.
        
        Raises:
            TypeError: If any of the arguments is sent with the wrong data type, a TypeError will be obtained, 
                also if some mandatory value is not delivered to the function.

        """
        
        query = """
        SELECT calendar_date as date, domain, event,
            count(distinct guid) as total_reach,
            count(guid) as total_visits, sum(time_spent) as total_time, total_time / total_visits as avg_time_per_visit
        
        FROM spectrum_comscore.clickstream_{country_in}
        where calendar_date between '{start_date_in}' and '{end_date_in}'
        and domain = '{domain_in}'
        {statement_like}
        group by calendar_date, domain, event
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)
        
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')

        if isinstance(end_date, type(None)):
            end_date = '2019-06-01'
            print('The preset date was defined, which starts from June 1, 2019')

        if isinstance(domain, type(None)):
            error = 'Define your specific domain'
            raise TypeError(error)

        if not isinstance(event_like, type(False)):
            if not isinstance(event_like, str):
                error = 'Verify your ilike, you use other type value different to string'
                raise TypeError(error)
            else:
                ilike = "and event_detail like '%%{}%%'".format(event_like)
        else:
            ilike = ''
            print('you dont define ilike statement')
        
        setence = query.format(start_date_in = start_date, country_in = country, end_date_in = end_date, domain_in = domain, statement_like = ilike)
        print(setence + '\n')
        dataframe = read_sql(setence, con = self.connection)

        if saved:
            path_file = input('define your personal path to save the file: ')
            dataframe.to_csv(path_file + '{}_{}_{}.csv'.format(domain.replace('.', '-'), start_date, end_date))
        
        return dataframe

    def custom_query_statement(self, query):
        """A function that allows you to create a custom query on the comscore database.

        Note:
            To use this method, you must have previously logged in.

        Args:
            query (str, required): Full statement of the query.

        Returns:
            DataFrame: If the process works correctly, you will get a dataframe with all the required data.

        """
        return read_sql(query, con = self.connection)

    def demographics_by_web(self, country = None, start_date = None, end_date = None, 
                                event_like = False, domain = None, saved = False, age_group = False,
                                ages_between = None, gender_between = None):
        """A function that displays all demographic values for a specific domain.

        Note:
            To use this method, you must have previously logged in.

        Args:
            country (str, required): Select the country code on which you want to create a query. 
                Possible options are: ['us','ar', 'au','br', 'ca', 'cl', 'co', 'hk', 'id', 'in', 'mx', 'my', 'nz', 'sg', 'tw']

            start_date (str, optional): Select from which date you want to see your data.
                The default is 2019-01-01

            end_date (str, optional): Select the maximum date to consult.
                The default value is 2019-06-01

            event_like (str, optional): An additional WHERE statement that adds the "LIKE" in SQL. All the words you consider will be taken.
                if you use the event_like operator your query will look like the following.
                Example: SELECT * FROM table WHERE domain = somedomain.com AND event_detail SIMILAR TO '% event_like_value %' 

            domain (str, required): The specified domain you want to know about. This value is required.

            saved (bool, optional): If saved is true then you must indicate the path where you want to save 
                the file and it will be saved on your local machine.
                This is optional.
            
            age_group (bool, optional): A selection of true or false, if it is false it will not be grouped by age range, 
                if it is true it will be grouped by age range.

            ages_between (tuple, optional): A tuple value, which must have two integer values (min age, max age).

            gender_between (tuple, optional): A tuple that contains the strings of all the genres that you want to examine.
                example: ('Male', 'Female', 'other')

        Returns:
            DataFrame: If the process occurs correctly, you will get a dataframe with all the required data.
        
        Raises:
            TypeError: If any of the arguments is sent with the wrong data type, a TypeError will be obtained, 
                also if some mandatory value is not delivered to the function.

        """

        query = """
        SELECT main_base.domain, main_base.device, user_base.gender, 
               
                {age_group_statement},
        
        
               user_base.children_present,
               count(distinct main_base.guid) as reach, count(main_base.guid) as visits, count(main_base.machine_id) as number_of_devices,
               sum(main_base.time_spent) as total_time, total_time / visits as avg_time_per_visit
               
               FROM spectrum_comscore.clickstream_{country_in} main_base
        
        LEFT JOIN
            (select person_id, gender, age, children_present
            from spectrum_comscore.person_demographics_{country_in}
            where date >= '{start_date_in}'
            group by person_id, gender, age, children_present) user_base
        
        ON main_base.guid = user_base.person_id
        
        where calendar_date between '{start_date_in}' and '{end_date_in}'
        and domain = '{domain_in}'
        {statement_like}
        {statement_ages}
        
        group by 1,2,3,4,5
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)

        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        if isinstance(end_date, type(None)):
            end_date = '2019-06-01'
            print('The preset date was defined, which starts from June 1, 2019')
        
        if isinstance(domain, type(None)):
            error = 'Define your specific domain'
            raise TypeError(error)

        if isinstance(ages_between, type(None)):
            ages_state = ''
        else:
            if not isinstance(ages_between, tuple):
                error = 'Verify your ages, you use other type value different to tuple'
                raise TypeError(error)
            else:
                ages_state = 'and user_base.age between ' + str(ages_between[0]) + ' and ' + str(ages_between[1])

        if not isinstance(event_like, type(False)):
            if not isinstance(event_like, str):
                error = 'Verify your ilike, you use other type value different to string'
                raise TypeError(error)
            else:
                ilike = "and event_detail SIMILAR TO '%%{}%%'".format(event_like)
        else:
            ilike = ''
            print('you dont define ilike statement')

        if age_group:
            age_group_value = """
            CASE
                    WHEN user_base.age > 13 AND user_base.age <= 17 THEN '13-17'
                    WHEN user_base.age > 17 AND user_base.age <= 34 THEN '18-34'
                    WHEN user_base.age > 34 AND user_base.age <= 54 THEN '35-54'
                    WHEN user_base.age > 54 THEN '55+'
                ELSE
                    'Undetermined'
                END
                AS age_group
            """
        else:
            age_group_value = """ user_base.age """

        setence = query.format(start_date_in = start_date, end_date_in = end_date, domain_in = domain, statement_like = ilike, 
                                country_in = country, age_group_statement = age_group_value,
                                statement_ages = ages_state)
        print(setence + '\n')
        dataframe = read_sql(setence, con = self.connection)
        dataframe.gender = dataframe.gender.astype(str).replace('nan', 'Undetermined')
        dataframe.children_present = dataframe.children_present.astype(str).replace('nan', 'Undetermined')

        if isinstance(gender_between, type(None)):
            pass
        else:
            if not isinstance(gender_between, tuple):
                error = 'Gender is not a tuple'
                raise TypeError(error)
            
            else:
                dataframe = dataframe.query('gender in {}'.format(gender_between))

        if saved:
            path_file = input('define your personal path to save the file: ')
            dataframe.to_csv(path_file + 'demographics_{}_{}_{}.csv'.format(domain.replace('.', '-'), start_date, end_date))
        
        return dataframe
    
    def correlation_between_domains(self, country = None, start_date = None, end_date = None, url_site = None,
                                    domain_name_like = False, reach_greater_than = 8, corr_greater = 0.75, saved = False):

        """Correlation between a specific domain and others.

        Note:
            To use this method, you must have previously logged in.

        Args:
            country (str, required): Select the country code on which you want to create a query. 
                Possible options are: ['us','ar', 'au','br', 'ca', 'cl', 'co', 'hk', 'id', 'in', 'mx', 'my', 'nz', 'sg', 'tw']

            start_date (str, optional): Select from which date you want to see your data.
                The default is 2019-01-01

            end_date (str, optional): Select the maximum date to consult.
                The default value is 2019-06-01

            url_site (str, optional): 

            domain_name_like (str, required): An additional WHERE statement that adds the "LIKE" in SQL. All the words you consider will be taken.
                if you use the event_like operator your query will look like the following.
                Example: SELECT * FROM table WHERE domain = somedomain.com AND event_detail SIMILAR TO '% event_like_value %' 

            reach_greater_than (int, optional): This indicator by default has a value of eight and represents 
                that all the pages that are studied for the correlation must have a scope greater than 8 people.
                You can adjust this number, using this argument.
            
            corr_greater (float, optional): It is a filter to show only those pages that have a 
                correlation with the main domain greater than 0.75, which is the default value. 
                You can adjust this number, using this argument.

            saved (bool, optional): If saved is true then you must indicate the path where you want to save 
                the file and it will be saved on your local machine.
                This is optional.

        Returns:
            DataFrame: If the process occurs correctly, you will get a dataframe with all the required data.
        
        Raises:
            TypeError: If any of the arguments is sent with the wrong data type, a TypeError will be obtained, 
                also if some mandatory value is not delivered to the function.

        """

        query = """
        select calendar_date as date, domain, count(distinct guid) as reach, count(guid) as visits 
        from spectrum_comscore.clickstream_{country_in}
        where domain = '{url_site_in}' 
        {domain_like_statement}
        and calendar_date between '{start_date_in}' and '{end_date_in}'
        group by date, domain
        having reach >= {reach_greater_than_in}
        
        UNION ALL
        
        select calendar_date as date, domain, count(distinct guid) as reach, count(guid) as visits 
        from spectrum_comscore.clickstream_{country_in}
        where guid in (select guid from spectrum_comscore.clickstream_{country_in}
                       where domain = '{url_site_in}' 
                       {domain_like_statement}
                       group by guid)
        and calendar_date  between '{start_date_in}' and '{end_date_in}'
        and domain not in ('facebook.com', 'netflix.com', 'google.com', 'gmail.com', 'twitter.com', 'google.cl', 'instagram.com', 'youtube.com')
        group by date, domain
        having count(distinct guid) >= {reach_greater_than_in}
        
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)

        if not isinstance(domain_name_like, type(False)):
            if not isinstance(domain_name_like, str):
                error = 'Verify your domain like, you use other type value different to string'
                raise TypeError(error)
            else:
                domainlike = "or event_detail SIMILAR TO '%%{}%%' ".format(domain_name_like)
        else:
            domainlike = ''
            print('you dont define domain like statement')

        if isinstance(url_site, type(None)):
            error = 'Define the url of the site'
            raise TypeError(error)
            
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        if isinstance(end_date, type(None)):
            end_date = '2019-05-01'
            print('The preset date was defined, which end from May 1, 2019')

        sentence = query.format(country_in = country, start_date_in = start_date, end_date_in = end_date,
                                        url_site_in = url_site, domain_like_statement = domainlike,
                                        reach_greater_than_in = reach_greater_than)

        print(sentence + '\n')

        dataframe = read_sql(sentence,
                         con = self.connection)
        
        dataframe = dataframe.drop_duplicates().pivot(index='date', columns='domain', values='reach')
        dataframe_corr = dataframe.corr(method='pearson')

        if domain_name_like == False:
            dataframe_uniq_matrix = dataframe_corr[[url_site]]
            final_corr = dataframe_uniq_matrix[dataframe_uniq_matrix[url_site] >= corr_greater]
        else:
            dataframe_uniq_matrix = dataframe_corr[dataframe_corr.index.str.contains(domain_name_like)]

            mask = ~(dataframe_uniq_matrix.mask(np.eye(len(dataframe_uniq_matrix), dtype=bool)).abs() > corr_greater).any()

            final_corr = dataframe_uniq_matrix.loc[mask, mask]

        if saved:
            path_file = input('define your personal path to save the file: ')
            final_corr.to_csv(path_file + 'corr_{}_{}_{}.csv'.format(url_site.replace('.', '-'), start_date, end_date))
        
        return dataframe, dataframe_corr, dataframe_uniq_matrix, final_corr
    
    def overlaps_between_pages(self, country = None, start_date = None, end_date = None, 
                                domain = None, competitors = None, like_domain = None,
                                like_competitors = None, saved = False):
        """A function to obtain the interdomain overexposure.

        Note:
            To use this method, you must have previously logged in.

        Args:
            country (str, required): Select the country code on which you want to create a query. 
                Possible options are: ['us','ar', 'au','br', 'ca', 'cl', 'co', 'hk', 'id', 'in', 'mx', 'my', 'nz', 'sg', 'tw']

            start_date (str, optional): Select from which date you want to see your data.
                The default is 2019-01-01

            end_date (str, optional): Select the maximum date to consult.
                The default value is 2019-06-01

            domain (str, optional): The main domain on which we want to overlap

            competitors (tuple, required): All competitors stored in a tuple, where the inner values are strings

            like_domain (str, optional): An additional WHERE statement that adds the "LIKE" in SQL. All the words you consider will be taken.
                if you use the event_like operator your query will look like the following.
                Example: SELECT * FROM table WHERE domain = somedomain.com AND event_detail SIMILAR TO '% event_like_value %' 
            
            like_competitors (str, optional): An additional WHERE statement that adds the "LIKE" in SQL. All the words you consider will be taken.
                if you use the event_like operator your query will look like the following.
                Example: SELECT * FROM table WHERE domain = somedomain.com AND event_detail SIMILAR TO '% event_like_value %' 

            saved (bool, optional): If saved is true then you must indicate the path where you want to save 
                the file and it will be saved on your local machine.
                This is optional.

        Returns:
            DataFrame: If the process occurs correctly, you will get a dataframe with all the required data.
        
        Raises:
            TypeError: If any of the arguments is sent with the wrong data type, a TypeError will be obtained, 
                also if some mandatory value is not delivered to the function.

        """

        testing = """
        select guid, domain
        from spectrum_comscore.clickstream_{country_in}
        where domain = '{domain_in}'
        {main_domain_statement_like}
        and calendar_date between '{start_date_in}' and '{end_date_in}'
        group by guid, domain
        
        UNION ALL
        
        select guid, domain
        from spectrum_comscore.clickstream_{country_in}
        where domain in {competidors_in}
        {competidors_statement_like}
        and calendar_date between '{start_date_in}' and '{end_date_in}'
        group by guid, domain
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)
        
        if isinstance(domain, type(None)):
            error = 'Define your domain'
            raise TypeError(error)
            
        if isinstance(competitors, type(None)):
            error = 'Define your competitors'
            raise TypeError(error)
        else:
            if not isinstance(competitors, tuple):
                error = 'Competitors must be entered in parentheses'
                raise TypeError(error)
            else:
                pass
            
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        if isinstance(end_date, type(None)):
            end_date = '2019-06-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        if isinstance(like_domain, type(None)):
            domainlike = ''
        else:
            if not isinstance(like_domain, str):
                error = 'domain like is not a string'
                raise TypeError(error)
            else:
                domainlike = "and event_detail SIMILAR TO '%%{}%%'".format(like_domain)
        
        if isinstance(like_competitors, type(None)):
            competitorslike = ''
        else:
            if not isinstance(like_competitors, str):
                error = 'domain like is not a string'
                raise TypeError(error)
            else:
                competitorslike = "and event_detail SIMILAR TO '%%{}%%'".format(like_competitors)
        
        sentence = testing.format(country_in = country, start_date_in = start_date, end_date_in = end_date, 
                                    domain_in = domain, competidors_in = competitors,
                                    main_domain_statement_like = domainlike, 
                                    competidors_statement_like = competitorslike)
        print(sentence, '\n')

        tests = read_sql(sentence,
                         con = self.connection)
        
        #create unique list of names
        uniqueNames = tests.domain.unique()
        print(uniqueNames)
        
        #create a data frame dictionary to store your data frames
        DataFrameDict = {elem : pd.DataFrame for elem in uniqueNames}
        
        my_list = []
        
        for key in DataFrameDict.keys():
            DataFrameDict[key] = tests[:][tests.domain == key].reset_index(drop = True)
            my_list.append(list(tests[:][tests.domain == key].reset_index(drop = True).guid))
        
        frame = pd.DataFrame()
        
        for index in range(len(my_list)):
          lista_final = [list(filter(lambda x: x in my_list[index], sublist)) for sublist in my_list]
          
          mt = [len(x) / len(my_list[index]) for x in lista_final]
          frame = pd.concat([frame, DataFrame(mt)], axis = 1)
        
        frame.columns = list(uniqueNames)
        frame.index = list(uniqueNames)

        if saved:
            path_file = input('define your personal path to save the file: ')
            frame.to_csv(path_file + 'overlap_{}_{}_{}.csv'.format(domain.replace('.', '-'), start_date, end_date))

        return DataFrameDict, frame
    
    def bayesian_inference_over_sites(self, country = None, domain = None, 
                                      time_spent = None, start_date = None, end_date = None, saved = False):
        """A function that uses the Bayes theorem to calculate which sites are most likely to be visited by a user who visits our site.

        Note:
            To use this method, you must have previously logged in.

        Args:
            country (str, required): Select the country code on which you want to create a query. 
                Possible options are: ['us','ar', 'au','br', 'ca', 'cl', 'co', 'hk', 'id', 'in', 'mx', 'my', 'nz', 'sg', 'tw']

            start_date (str, optional): Select from which date you want to see your data.
                The default is 2019-01-01

            end_date (str, optional): Select the maximum date to consult.
                The default value is 2019-06-01

            domain (str, optional): The main domain on which we want to overlap

            time_spent (int, required): The minimum amount of time a user has to spend on the site and the competitor's site to be examined.
                The default value is 300.

        Returns:
            DataFrame: If the process occurs correctly, you will get a dataframe with all the required data.
        
        Raises:
            TypeError: If any of the arguments is sent with the wrong data type, a TypeError will be obtained, 
                also if some mandatory value is not delivered to the function.

        """
        query = """

        WITH my_table_3 as (
          select domain
            from spectrum_comscore.clickstream_{country_in}
              where guid in (select guid from spectrum_comscore.clickstream_{country_in} 
                              where domain = '{domain_in}' 
                              and calendar_date between '{start_date_in}' and '{end_date_in}'
                              and time_spent >= {time_spent_in}
                                group by guid)
              and time_spent >= {time_spent_in}
                group by domain
        ),
        
        my_table_4 as (
          select guid
            from spectrum_comscore.clickstream_{country_in}
              where guid in (select guid from spectrum_comscore.clickstream_{country_in} 
                              where domain = '{domain_in}' 
                              and calendar_date between '{start_date_in}' and '{end_date_in}'
                              and time_spent >= {time_spent_in}
                                group by guid)
                group by guid
        
        )
        
        SELECT domain, 'visitors' as type, count(distinct guid) as reach 
        from spectrum_comscore.clickstream_{country_in}
          where domain in (select domain from my_table_3) and guid in (select guid from my_table_4)
          and domain not in ('facebook.com', 'netflix.com', 'google.com', 'gmail.com', 'twitter.com', 'google.cl', 'instagram.com', 'youtube.com', 'bing.com', 'whatsapp.com', 'msn.com', 'live.com', '{domain_in}')
        group by 1,2
        
        UNION ALL
        
        SELECT domain, 'outsiders' as type, count(distinct guid) as reach 
        from spectrum_comscore.clickstream_{country_in}
          where domain in (select domain from my_table_3) and guid not in (select guid from my_table_4)
          and domain not in ('facebook.com', 'netflix.com', 'google.com', 'gmail.com', 'twitter.com', 'google.cl', 'instagram.com', 'youtube.com', 'bing.com', 'whatsapp.com', 'msn.com', 'live.com')
        group by 1,2

        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)
        
        if isinstance(domain, type(None)):
            error = 'Define your domain'
            raise TypeError(error)
            
        if isinstance(time_spent, type(None)):
            time_spent = 300
            print('The preset time_spent was defined, which 300 seconds')
    
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        if isinstance(end_date, type(None)):
            end_date = '2019-06-01'
            print('The preset date was defined, which ends from June 1, 2019')
        
        sentence = query.format(country_in = country, start_date_in = start_date, end_date_in = end_date,
                                domain_in = domain, time_spent_in = time_spent)
        print(sentence, '\n')

        table3 = read_sql(sentence, con = self.connection)
        
        pivot_table_3 = pd.pivot_table(table3, values = 'reach', index = 'type', columns = 'domain')
        
        dataframe_probs_a = pd.DataFrame(columns=['domain', 'p(a)', 'p(x | a)'])
        
        totals = pivot_table_3.iloc[0].sum() + pivot_table_3.iloc[1].sum()
        
        for indexs in range(pivot_table_3.shape[1]):
          dataframe_probs_a.loc[indexs] = [str(pivot_table_3.iloc[:,indexs].name), 
                                           pivot_table_3.iloc[:,indexs].sum() / totals, 
                                           pivot_table_3.iloc[:,indexs].visitors / pivot_table_3.iloc[:,indexs].sum()]
        
        dataframe_probs_a['p(a)*p(x | a)'] = dataframe_probs_a['p(a)'] * dataframe_probs_a['p(x | a)']
        dataframe_probs_a['bayes'] = dataframe_probs_a['p(a)*p(x | a)'] / dataframe_probs_a['p(a)*p(x | a)'].sum()
        dataframe_probs_a['bayes %'] = dataframe_probs_a['bayes'] * 100
        dataframe_probs_a.sort_values('bayes %', ascending = False,inplace=True)
        dataframe_probs_a.reset_index(drop = True, inplace = True)
        
        short_frame = dataframe_probs_a[dataframe_probs_a['bayes %'] > 0.4].reset_index(drop = True)

        if saved:
            path_file = input('define your personal path to save the file: ')
            short_frame.to_csv(path_file + 'bayesianinference_sites_prob_{}_{}_{}.csv'.format(domain.replace('.', '-'), start_date, end_date))
        
        return dataframe_probs_a, short_frame

    def bayesian_site_predictor(self, country = None, 
                                domain = None, time_spent = None, 
                                start_date = None, end_date = None, saved = False):
            """A function to know which is the next most likely site to visit after a user visits our site.

        Note:
            To use this method, you must have previously logged in.

        Args:
            country (str, required): Select the country code on which you want to create a query. 
                Possible options are: ['us','ar', 'au','br', 'ca', 'cl', 'co', 'hk', 'id', 'in', 'mx', 'my', 'nz', 'sg', 'tw']

            start_date (str, optional): Select from which date you want to see your data.
                The default is 2019-01-01

            end_date (str, optional): Select the maximum date to consult.
                The default value is 2019-06-01

            domain (str, optional): The main domain on which we want to overlap

            time_spent (int, required): The minimum amount of time a user has to spend on the site and the competitor's site to be examined.
                The default value is 300.

        Returns:
            DataFrame: If the process occurs correctly, you will get a dataframe with all the required data.
        
        Raises:
            TypeError: If any of the arguments is sent with the wrong data type, a TypeError will be obtained, 
                also if some mandatory value is not delivered to the function.

            """

            query_1 = """
            
            SELECT a.guid, concat(concat(b.domain,'_'),a.domain) AS trans_domain, b.positive_interval_time, b.timestamp_date_min, 
                min(a.visit_date_event) as min_visit
            
            
            FROM
            
                (select guid, domain, CONVERT(datetime,dateadd(s, event_time,'2000-01-01')) at time zone 'utc' at time zone 'clst' visit_date_event
                from spectrum_comscore.clickstream_{country_in}
                where guid in (select guid from spectrum_comscore.clickstream_{country_in} 
                    where domain = '{domain_in}' and calendar_date between '{start_date_in}' and '{end_date_in}' and time_spent >= {time_spent_in}
                    group by guid) and time_spent >= 30
                group by guid, domain, event_time) a
            
            LEFT JOIN
            
            (select guid, domain, min(timestamp_date) as timestamp_date_min,
                        timestamp_date_min + INTERVAL '1 hour' as positive_interval_time
                    from (
                        select guid, domain,
                        CONVERT(datetime, dateadd(s, event_time,'2000-01-01')) at time zone 'utc' at time zone 'clst' timestamp_date
                        from spectrum_comscore.clickstream_{country_in}
                        where domain = '{domain_in}' and calendar_date between '{start_date_in}' and '{end_date_in}' and time_spent >= {time_spent_in}
                        ) group by guid, domain) b
            
            ON a.guid = b.guid
            
            where a.visit_date_event <= b.positive_interval_time and a.visit_date_event > b.timestamp_date_min
            
            group by 1,2,3,4
            
            having trans_domain not in ('{domain_in}_{domain_in}')
            
            """
            
            if isinstance(country, type(None)):
                error = 'Define your country'
                raise TypeError(error)
            
            if isinstance(domain, type(None)):
                error = 'Define your domain'
                raise TypeError(error)
                
            if isinstance(time_spent, type(None)):
                time_spent = 300
                print('The preset time_spent was defined, which 300 seconds')
        
            if isinstance(start_date, type(None)):
                start_date = '2019-01-01'
                print('The preset date was defined, which starts from January 1, 2019')
            
            if isinstance(end_date, type(None)):
                end_date = '2019-06-01'
                print('The preset date was defined, which ends from June 1, 2019')
            
            sentence1 = query_1.format(country_in = country, start_date_in = start_date, 
                                        end_date_in = end_date,
                                        domain_in = domain, time_spent_in = time_spent)


            print(sentence1, '\n')

            tests = read_sql(sentence1, con = self.connection)
            
            new = tests.sort_values(by = ['guid', 'min_visit'])
            new.drop_duplicates(subset = 'guid', keep = 'first', inplace = True)
            
            new['list_domains'] = new.trans_domain.str.split('_')
            
            list_of_domains = list(new['list_domains'])
            
            list_a = map(tuple, list_of_domains) #must convert to tuple because list is an unhashable type
            
            final_count = Counter(list_a)
            
            dataframe_of_visits = pd.DataFrame.from_dict(final_count, orient = 'index')
            
            dataframe_of_visits['other_index'] = dataframe_of_visits.index
            dataframe_of_visits.reset_index(inplace = True, drop = True)
            
            dataframe_of_visits['list'] = dataframe_of_visits.other_index.apply(list)
            dataframe_of_visits['list_str'] = dataframe_of_visits['list'].apply(','.join)
            dataframe_of_visits[['orig', 'desti']] = [sub.split(",") for sub in dataframe_of_visits.list_str]
            
            dataframe_of_visits['type'] = 'from_me_to_destiny' 
            
            dataframe_of_visits.columns = ['reach', 'indexs', 'list_index', 'list_index_str', 'orig', 'domain', 'type']
            final_a_frame = dataframe_of_visits[['domain', 'type', 'reach']]
            
            second_query = """
            
            SELECT a.guid, b.domain as orig, a.domain as desti, b.positive_interval_time, b.timestamp_date_min, min(a.visit_date_event) as min_visit
            
            
            FROM
            
                (select guid, domain, CONVERT(datetime,dateadd(s, event_time,'2000-01-01')) at time zone 'utc' at time zone 'clst' visit_date_event
                from spectrum_comscore.clickstream_{country_in}
                where guid in (select guid from spectrum_comscore.clickstream_{country_in} 
                    where domain in {domain_in} and calendar_date between '{start_date_in}' and '{end_date_in}' and time_spent >= {time_spent_in}
                    group by guid) and time_spent >= 30
                group by guid, domain, event_time) a
            
            LEFT JOIN
            
            (select guid, domain, min(timestamp_date) as timestamp_date_min,
                        timestamp_date_min + INTERVAL '1 hour' as positive_interval_time
                    from (
                        select guid, domain,
                        CONVERT(datetime, dateadd(s, event_time,'2000-01-01')) at time zone 'utc' at time zone 'clst' timestamp_date
                        from spectrum_comscore.clickstream_{country_in}
                        where domain in {domain_in} and calendar_date between '{start_date_in}' and '{end_date_in}' and time_spent >= {time_spent_in}
                        ) group by guid, domain) b
            
            ON a.guid = b.guid
            
            where a.visit_date_event <= b.positive_interval_time and a.visit_date_event > b.timestamp_date_min
            and a.domain != b.domain
            
            group by 1,2,3,4,5
            
            """
            
            optilist = list(dataframe_of_visits.domain)
            strings = ','.join(optilist)
            my_tuple = tuple(strings.split(','))

            sentence2 = second_query.format(country_in = country, start_date_in = start_date, 
                                            domain_in = my_tuple, time_spent_in = time_spent,
                                            end_date_in = end_date)

            print(sentence2, '\n')

            second_frame_test = read_sql(sentence2, con = self.connection)

            to_my_domain = second_frame_test[second_frame_test.desti == domain]
            
            new = to_my_domain.sort_values(by = ['guid', 'min_visit']).reset_index(drop = True)
            new.drop_duplicates(subset = 'guid', keep = 'first', inplace = True)
            new['trans_domain'] = new.orig + '_' + new.desti
            
            new['list_domains'] = new.trans_domain.str.split('_')
            
            list_of_domains = list(new['list_domains'])
            
            list_a = map(tuple, list_of_domains) #must convert to tuple because list is an unhashable type
            
            final_count = Counter(list_a)
            
            dataframe_of_visits_to_me = pd.DataFrame.from_dict(final_count, orient = 'index')
            
            dataframe_of_visits_to_me['other_index'] = dataframe_of_visits_to_me.index
            dataframe_of_visits_to_me.reset_index(inplace = True, drop = True)
            
            dataframe_of_visits_to_me['list'] = dataframe_of_visits_to_me.other_index.apply(list)
            dataframe_of_visits_to_me['list_str'] = dataframe_of_visits_to_me['list'].apply(','.join)
            dataframe_of_visits_to_me[['orig', 'desti']] = [sub.split(",") for sub in dataframe_of_visits_to_me.list_str]
            
            dataframe_of_visits_to_me['type'] = 'from_domains_to_me'
            
            dataframe_of_visits_to_me.columns = ['reach', 'indexs', 'list_index', 'list_index_str', 'domain', 'desti', 'type']
            final_b_frame = dataframe_of_visits_to_me[['domain', 'type', 'reach']]

            to_others_domain = second_frame_test[second_frame_test.desti != domain]
            
            new = to_others_domain.sort_values(by = ['guid', 'min_visit']).reset_index(drop = True)
            new.drop_duplicates(subset = 'guid', keep = 'first', inplace = True)
            new['trans_domain'] = new.orig + '_' + new.desti
            
            new['list_domains'] = new.trans_domain.str.split('_')
            
            list_of_domains = list(new['list_domains'])
            
            list_a = map(tuple, list_of_domains) #must convert to tuple because list is an unhashable type
            
            final_count = Counter(list_a)
            
            dataframe_of_visits_to_others = pd.DataFrame.from_dict(final_count, orient = 'index')
            
            dataframe_of_visits_to_others['other_index'] = dataframe_of_visits_to_others.index
            dataframe_of_visits_to_others.reset_index(inplace = True, drop = True)
            
            dataframe_of_visits_to_others['list'] = dataframe_of_visits_to_others.other_index.apply(list)
            dataframe_of_visits_to_others['list_str'] = dataframe_of_visits_to_others['list'].apply(','.join)
            dataframe_of_visits_to_others[['orig', 'desti']] = [sub.split(",") for sub in dataframe_of_visits_to_others.list_str]
            
            dataframe_of_visits_to_others['type'] = 'from_domains_to_others'
            
            dataframe_of_visits_to_others.columns = ['reach', 'indexs', 'list_index', 'list_index_str', 'orig', 'domain', 'type']
            final_c_frame = dataframe_of_visits_to_others[['domain', 'type', 'reach']]

            final_frame = pd.concat([final_a_frame, final_b_frame, final_c_frame])
            
            pivot_table_3 = pd.pivot_table(final_frame, values = 'reach', index = 'type', columns = 'domain').fillna(0)
            
            dataframe_probs_a = pd.DataFrame(columns=['domain', 'p(a)', 'split'])

            totals = pivot_table_3.iloc[0].sum() + pivot_table_3.iloc[1].sum() + pivot_table_3.iloc[2].sum()
            
            for indexs in range(pivot_table_3.shape[1]):
                dataframe_probs_a.loc[indexs] = [str(pivot_table_3.iloc[:,indexs].name), 
                                                pivot_table_3.iloc[:,indexs].sum() / totals, 
                                                pivot_table_3.iloc[:,indexs].from_me_to_destiny / pivot_table_3.iloc[:,indexs].sum()]
            
            dataframe_probs_a['p(X)'] = dataframe_probs_a['p(a)'] * dataframe_probs_a['split']
            dataframe_probs_a['bayes'] = (dataframe_probs_a['p(a)'] * dataframe_probs_a['split']) / dataframe_probs_a['p(X)'].sum()
            dataframe_probs_a['bayes %'] = dataframe_probs_a['bayes'] * 100
            
            dataframe_probs_a.sort_values('bayes %', inplace=True, ascending = False,)
            dataframe_probs_a.reset_index(drop = True, inplace = True)
            
            short_frame_a = dataframe_probs_a[dataframe_probs_a['bayes %'] > 0.4].reset_index(drop = True)
            
            if saved:
                path_file = input('define your personal path to save the file: ')
                short_frame_a.to_csv(path_file + 'bayesianinference_sites_prob_{}_{}_{}.csv'.format(domain.replace('.', '-'), start_date, end_date))

            return short_frame_a, dataframe_probs_a
    
    def costumer_journey_site(self, country = None, age_group = False,
                                domain = None, time_spent = 350, like_domain = None, interval_time = None,
                                start_date = None, end_date = None, saved = False):

        """A function that generates the path traveled by a user who entered your site, based on a time interval.

        Note:
            To use this method, you must have previously logged in.

        Args:
            country (str, required): Select the country code on which you want to create a query. 
                Possible options are: ['us','ar', 'au','br', 'ca', 'cl', 'co', 'hk', 'id', 'in', 'mx', 'my', 'nz', 'sg', 'tw']

            start_date (str, optional): Select from which date you want to see your data.
                The default is 2019-01-01

            end_date (str, optional): Select the maximum date to consult.
                The default value is 2019-06-01

            domain (str, optional): The main domain on which we want to overlap

            time_spent (int, required): The minimum amount of time a user has to spend on the site and the competitor's site to be examined.
                The default value is 350.

        Returns:
            DataFrame: If the process occurs correctly, you will get a dataframe with all the required data.
        
        Raises:
            TypeError: If any of the arguments is sent with the wrong data type, a TypeError will be obtained, 
                also if some mandatory value is not delivered to the function.

            """
        
        query = """

            WITH guid_tables AS ( ---- QUERY TO CREATE AUDIENCE 
            select guid, domain,
            min(CONVERT(datetime,dateadd(s, event_time,'2000-01-01')) at time zone 'utc' at time zone 'clst') as target_time,
            target_time + INTERVAL '{interval_time}' as positive_interval_time,
            target_time - INTERVAL '{interval_time}' as negative_interval_time
            from spectrum_comscore.clickstream_{country}
            
            where domain = '{domain_in}'
            {event_detail_like}
            and calendar_date between '{start_date_in}' and '{end_date_in}'
            group by 1,2
            
            ),

            demographics AS ( ---- QUERY TO EXTRACT DEMOGRAPHICS
            select 
            {age_value} as age_column,
            *
            from guid_tables a 
            join spectrum_comscore.person_demographics_{country} b
            on a.guid = b.person_id
            ),

            final_table as ( --- COMPLETE QUERY
            select
            a.guid,
            b.gender,
            b.age_column,
            b.hh_income,
            b.children_present,
                case a.event
                when 'SEARCH' then a.event_detail
                when 'WEB' then a.domain
                when 'PRODUCT VIEW' then a.event_detail
                when 'SOCIAL' then a.event_detail
                when 'VIDEO' then a.event_detail
                    else a.event_detail 
                    end as domain,
            b.target_time,
                CONVERT(datetime,dateadd(s, a.event_time,'2000-01-01')) at time zone 'utc' at time zone 'clst' as timestamp,
                count(a.guid) as visit_count,
                sum(a.time_spent) as seconds_spent
            from spectrum_comscore.clickstream_{country} a
            join demographics b 
                using (guid)
            where time_spent >= {time_spent_greater_than}
            and timestamp >= b.negative_interval_time and timestamp <= b.positive_interval_time
            group by 1,2,3,4,5,6,7,8)

            select * from final_table
            """

        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)
        
        if isinstance(domain, type(None)):
            error = 'Define your domain'
            raise TypeError(error)
            
        if isinstance(like_domain, type(None)):
            domainlike = ''
        else:
            if not isinstance(like_domain, str):
                error = 'domain like is not a string'
                raise TypeError(error)
            else:
                domainlike = "and event_detail SIMILAR TO '%%{}%%'".format(like_domain)
            
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        if isinstance(end_date, type(None)):
            end_date = '2019-06-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        if not isinstance(interval_time, str):
            error = 'interval_time like is not a string'
            raise TypeError(error)
        else:
            pass

        if age_group:
            age_group_value = """
            CASE
                    WHEN age > 13 AND age <= 17 THEN '13-17'
                    WHEN age > 17 AND age <= 34 THEN '18-34'
                    WHEN age > 34 AND age <= 54 THEN '35-54'
                    WHEN age > 54 THEN '55+'
                ELSE
                    'Undetermined'
                END
            """
        else:
            age_group_value = """ age """
        

        sentence = query.format(interval_time = interval_time,
                                start_date_in = start_date, 
                                end_date_in = end_date,
                                domain_in = domain,
                                country = country, 
                                event_detail_like = domainlike, 
                                time_spent_greater_than = time_spent, 
                                age_value = age_group_value
                                )
        
        print(sentence + '\n')
        dataframe = read_sql(sentence, con = self.connection)

        dataframe['diff_timestamp'] = dataframe.timestamp - dataframe.target_time
        dataframe.sort_values(['guid', 'diff_timestamp']).reset_index(drop = True, inplace = True)

        if saved:
            path_file = input('define your personal path to save the file: ')
            dataframe.to_csv(path_file + 'journey_{}_{}_{}.csv'.format(domain.replace('.', '-'), start_date, end_date))
        
        return dataframe