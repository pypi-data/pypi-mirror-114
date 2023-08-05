import teradatasql as t
import pandas as pd
import string
import math
import numpy as np

class upload_to_tera:
    """
    Uploading large dataframes to tera
    
    """
    def __init__(self, df, q, main_table_name, tmp_table_name, memory=10000000):
        """
        ARGS:
        df - dataframe
        q - string - query
        main_table_name - string
        tmp_table_name - string

        example format:
        q = Insert into d_digital_data.blabla_tmp values (?, ?, ?, ?)
        main_table_name = d_digital_data.blabla
        tmp_table_name = main_table_name
        """
        self.memory = memory
        self.df = df
        self.rows = 0
        self.q = q
        self.num = 0
        self.main_table_name = main_table_name
        self.tmp_table_name = tmp_table_name
        self.alphabet_string = string.ascii_lowercase
        self.alphabet_list = list(self.alphabet_string) 
        self.uploade_how_many_rows_we_want(self.df)
        
    def is_ascii(self, s):
        if all(ord(c) < 128 for c in s):
            return False
        return True
    
    
    def insert(self, df):
        """
        1. Insert into tmp table.
        2. *In tera* insert into main table
        3. Delete tmp table.
        """
        with t.connect('{"host":"tdprd","logmech":"krb5"}') as con:
            with con.cursor () as cur:
#                 try:
#                     cur.execute(q, df.values.tolist())
#                 except Exception as ex:
#                     if "Duplicate row error" in str(ex):
#                         cur.execute("delete {0}".format(self.tmp_table_name))
#                         cur.execute(q, df.values.tolist())
                cur.execute(self.q, df.values.tolist())       
                cur.execute("insert into {0} sel * from {1}".format(self.main_table_name, self.tmp_table_name))
                cur.execute("delete {0}".format(self.tmp_table_name))
                self.num += len(df)
                print("{0} lines were added out of {1}".format(str(self.num), str(len(self.df))))
        
    
    def uploade_how_many_rows_we_want(self, df):
        """
        A recursion that will divide our data into several parts and upload them to tera.

        ARGS:
        df - dataframe
        q - string - query
        table_name - string

        example format:
        q = Insert into d_digital_data.blabla_tmp values (?, ?, ?, ?)
        main_table_name = d_digital_data.blabla
        tmp_table_name = main_table_name

        Return:
        nan
        """
        try:
            if len(df) > 300000 or df.memory_usage(deep=True).sum() > self.memory:
                raise Exception("batch request")
            try:
                self.insert(df)
                
            except Exception as ex:
                if 'string contains an untranslatable character' in str(ex):
                    for i in np.where(df.dtypes != np.float)[0]:
                        df['drop'] = df[df.columns[i]].apply(lambda x: self.is_ascii(x))
                        l_tmp = (df['drop'][df['drop']].index)
                        if len(l_tmp) > 0:
                            print("rows remove: " + str(list(l_tmp)))
                        df.drop(l_tmp, inplace=True)
                        df.drop('drop', axis=1, inplace=True)
                elif 'batch request' in str(ex) or 'LAN message' in str(ex):
                    raise Exception("batch request")
                else:
                    print('error')
                    print(ex)
                    raise error
            self.rows += len(df)


        except Exception as ex:
            if "batch request" in str(ex):
                
                # split the data to 2 dataframes
                len_data = math.ceil(len(df)/2)
                df1 = df.iloc[:len_data]
                df2 = df.iloc[len_data:]

                self.uploade_how_many_rows_we_want(df1)
                self.uploade_how_many_rows_we_want(df2)


            else:
                print (ex)
                raise error
