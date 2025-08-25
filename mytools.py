import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from IPython.display import display, Markdown


def display_md(text):
    display(Markdown(text))

def fws(x):
    # French formatter
    s = f"{x:,.0f}"
    # replace comma by space
    s = s.replace(',', ' ')
    # replace point by comma
    s = s.replace('.', ',')
    # Delete unusefull zeros and comma
    #s = s.rstrip('0').rstrip(',')
    return s

COLNAME = 'Column Name'
PERCMISS = 'Percent Missing'
MISSVAL = 'Missing Values'
CANDKEY = 'Candidate Key'
UNICVAL = 'Unique Values'

class CustomDF():
    """
    A subclass of pandas DataFrame for exploratory data analysis.
    
    This class can be used to create a DataFrame with additional methods for EDA.
    
    Parameters:
        csv_file : str
            Csv file path to read data from.
        tablename : str, optional    
    Returns:
        None
    """
    
    def __init__(self, df, csv_file= '', name = '', tablename ='', *args, **kwargs):
        # Read the CSV file into a DataFrame
        self.df = df
        msg = f'by reading CSV file : {csv_file} ###' if csv_file else ''
        display_md(f"### **Create the DataFrame : {name}**  {msg} ###")
        self.csv_file = csv_file
        # If a tablename is provided, set it as an attribute
        self.name = name
        if tablename:
            self.tablename = tablename
        else:
            self.tablename = name
        display(self.df.head())


    def describe(self, figsize=(), report_groups=[]):
        """        Generate descriptive statistics for the DataFrame.
        This method computes the data types, missing values, unique values, and checks for primary key potential.
        It displays the results in a formatted table.
        Returns:
            None
        """
        display_md(f"#### **Descriptive Statistics for DataFrame :** {self.name} ({self.tablename})")
        
        #self.df = self.df.reset_index()
        # first get the data types
        dtype = self.df.dtypes
        # overwrite dtype index when df is created from pivot table (and named from pivot table column)
        dtype.index.name = 'Column Name'
        dtype = dtype.to_frame().reset_index().rename(columns={0: 'Data Type', 'index': COLNAME})
        
        # get the number of missing values 
        self.description = (self.df.isna().sum()).reset_index().rename(columns={0: MISSVAL, 'index': COLNAME})
        
        # merge the data types and missing values        
        self.description = dtype.merge(self.description, on=COLNAME, how='left').reset_index(drop=True)
        
        #add column  and compute the percentage of missing values
        self.description[PERCMISS] =  self.description[MISSVAL] / self.df.shape[0] * 100
        self.description[PERCMISS] = self.description[PERCMISS].astype('float').round(1)
        
        # get the number of  unique values
        nun = self.df.nunique().reset_index().rename(columns={0: UNICVAL, 'index': COLNAME})
        
        #merge the data types, missing values, and unique values
        self.description = self.description.merge(nun, on=COLNAME, how='left').reset_index(drop=True)
        
        # add a column to check if the column is a candidate key
        self.description[CANDKEY] =  (self.df.shape[0]- self.description[UNICVAL])  == 0     
        
    
        ylabels = self.description['Column Name'].str[:50] + " / " + self.description['Data Type'].astype('string') 
        if not isinstance(figsize, tuple) or len(figsize) != 2:  figsize = (8,8)
        fig, ax = plt.subplots(figsize=figsize)
        sns.set_theme(context='notebook', style='whitegrid')
        sns.barplot(self.description,y='Column Name',x = 100- self.description['Percent Missing'],hue='Candidate Key', palette = {True: "#4BE14D", False: "#E9190AAD"})
        
        # Unique values comment on bar
        for x, (y, unic_values) in enumerate(zip(self.description['Column Name'], self.description[UNICVAL])):
            # ax.text(x, y, texte, ...)
            if unic_values >0 :
                pos = int(unic_values/self.df.shape[0]*100)
                if pos >=75:
                    align = 'right'
                elif pos <= 25:
                    align = 'left'
                else:
                    align='center'
                ax.text(pos + 0.5, x, f"U:{fws(unic_values)}" , va='center', ha=align, fontsize=10, color='black')
        
        plt.suptitle(f'Descriptive informations about {self.name} ({self.csv_file})  \n {self.tablename} ')
        plt.title(f'Number of row : {fws(self.df.shape[0])}    -    Number of columns : {fws(self.df.shape[1])} ')
        plt.xlabel('Present data in %\n U: Number of unique values')
        ax.set_xticks(np.arange(0, 101, 10))
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))
        ax.set_yticks(range(len(ylabels)))
        ax.set_yticklabels(labels=ylabels)
        plt.grid(which='major', axis='x')
        plt.tight_layout()
        plt.show()
        self.group_report(report_groups)

        

        

    def group_report(self, groups,figsize =()):
        """
        Generate a group report based on a specified column and aggregation function.
        
        Parameters:
            groupby_col : str
                The column to group by.
            agg_col : str
                The column to aggregate.
            agg_func : str, optional
                The aggregation function to apply (default is 'mean').
                
        Returns:
            pd.DataFrame
                A DataFrame containing the grouped and aggregated data.
        """
        # check if groups is a single string
        if not isinstance(figsize, tuple) or len(figsize) != 2:  figsize = (8,8)
        if isinstance(groups, str): groups = [groups] # change it to list
        if groups:
            nb_groups = len(groups)
            display_md(f"#### **Groups Report for DataFrame :** {self.name} ###")
            sns.set_theme(context='notebook', style='whitegrid')
            fig, ax = plt.subplots(1,nb_groups,figsize=(8*nb_groups, 8))
            # force ax to [] when a single graph
            if nb_groups == 1: ax = np.array([ax])
            for col, group in enumerate(groups):

                report = (
                    self.df.groupby(group,dropna=False)
                    .size( )
                    .to_frame()
                    .rename(columns={0:'Qty'})
                    .reset_index()
                    .sort_values(by='Qty', ascending=False))
                ylabels = report[group].astype(str).str[:40].fillna('(empty)')

                sns.barplot(report, y=report[group].fillna('(empty)'), x='Qty',orient='h',ax=ax[col])
                ax[col].set_title(f'Distribution of {group} categories among {fws(self.df.shape[0])} individuals')
                ax[col].set_xlabel(f'Quantity of individuals by {group}')
                ax[col].set_yticks(range(len(ylabels)))
                ax[col].set_yticklabels(labels=ylabels)
                ax[col].set_ylabel(group)
            plt.suptitle(f'Categories in possible categorical variables in {self.name}')
            plt.tight_layout()
            plt.show()
    
    def variable_report(self, serie_code, df_series):
        '''
        function to display descriptive informations about an indicator
        '''
        var_name = df_series.loc[df_series['Series Code'] == serie_code]['Indicator Name'].iloc[0]
                
        fig, ax = plt.subplots(1,2,figsize=(12,6),gridspec_kw={'width_ratios': [1, 2]})
        sns.boxplot(self.df, 
                    y= serie_code, 
                    ax= ax[0], 
                    color="#77C37E",
                    flierprops=dict(markerfacecolor='orange', marker='o', markersize=6)
                    )
        ax[0].set_xlabel('Quantiles View')
        ax[0].set_ylabel('')
        ax[0].set_title('')
        sns.histplot(self.df, x = serie_code, ax= ax[1], color="#5EAAD0")
        ax[1].set_xlabel('Bins Distribution')
        ax[1].set_title('')
        plt.suptitle(f"Dataframe {self.name} : Descriptive information on \n {serie_code} : {var_name}", fontsize=18)
        plt.tight_layout()
        plt.show()
    
    
    def shape(self, rows_cols =(), show_header = True, state = 'Actual'):
        """
        Get the shape of the DataFrame.

        Parameters:
            rows_cols : tuple (optional)
                specify a tuple to display
            show_header : boolean default : True
                whether or not display header 
        
        Returns:
            string
                A text describing the number of rows and columns in the DataFrame.
        """
        result = "| **State** | **Number of Rows** | **Number of Cols** |\n|--------------------|-------------------:|-------------------:|\n" if show_header else ""
        if not isinstance(rows_cols, tuple) or len(rows_cols) != 2:  rows_cols = self.df.shape
        result += f"| {state} | {fws(rows_cols[0])} | {fws(rows_cols[1])} |\n" 
        return  result

    def drop(self, *args, **kwargs):
        '''
        function to trace dropping process
        forward all parameters to dataframe drop function
        '''
        savedshape = self.df.shape
        msg = f"#### Dataframe {self.name} : ####  \n**Dropping operation on {self.name}**\n\n  "
        msg += self.shape(state = 'Before') 
        self.df.drop(*args, **kwargs)
        savedshape= tuple([a - b for a, b in zip(savedshape, self.df.shape)])
        msg += self.shape(rows_cols = savedshape, state = "Removed", show_header= False)
        msg += self.shape(state = "After", show_header= False) + "\n\n---\n\n"
        if 'columns' in kwargs:
            columns = kwargs['columns']
            if len(columns):
                msg += "\n| **Removed variables** |\n|--------|\n"
                for name in   columns:
                    msg += f"| {name} |\n"
        return msg
            
    def rename(self, *args, ** kwargs):
        
        if 'columns' in kwargs:
            msg = f"#### Dataframe {self.name} :  ####  \n**Renaming operation on {self.name}**   \n\n  "
            columns = kwargs['columns']
            if len(columns):
                msg += "|  **Variable old name**  |  **Variable new Name**  |  \n|--------------------|--------------------|  \n"
                for oldname, newname in   columns.items():
                    msg += f"|  {oldname}  |  {newname}  |   \n"
        self.df.rename(*args, **kwargs) 
        return msg

    
    def remove_na_cols(self, percent=50):
        """
        Remove columns with more than a specified percentage of missing values.
        
        Parameters:
            percent : float
                The percentage threshold for removing columns.
                
        Returns:
            None
        """
        msg = f"**Remove Columns with more than {percent}% Missing Values  \nfrom DataFrame : {self.name}**  \n "
        cols_to_remove = self.description[self.description['Percent Missing'] >= percent]['Column Name'].tolist()
        msg += self.drop(columns=cols_to_remove, inplace=True)
        return msg
        
        