import os
import numpy as np
import pandas as pd

class ExploratoryDataAnalysis:
    def __init__(self, frame, save=False, path='ExploratoryDataAnalysis'):
        self.frame = frame
        self.path = path

        if save:
            self._excel()     

    def cleaning(self, priority_frame=None, save=False, path=None):
        if priority_frame is not None:
            table = priority_frame
        else:
            table = self.frame

        for column in table.columns:
            table[column] = table[column].astype(str) if table[column].dtype == 'object' else table[column].astype(float)

        if priority_frame is not None:
            return table
        else:
            self.frame = table
            return table

    def frequency(self, priority_frame=None, save=False, path=None):
        if priority_frame is not None:
            table = priority_frame
        else:
            table = self.frame

    def transformation(self, priority_frame=None, save=False, path=None):
        if priority_frame is not None:
            table = priority_frame
        else:
            table = self.frame

    def selection(self, priority_frame=None, save=False, path=None):
        if priority_frame is not None:
            table = priority_frame
        else:
            table = self.frame

    def visualization(self, priority_frame=None, save=False, path=None):
        if priority_frame is not None:
            table = priority_frame
        else:
            table = self.frame
    
    def _excel(self, priority_frame=None, save=False, path=None):
        pass

    def table_definition(self, priority_frame=None, save=False, path=None):
        if priority_frame is not None:
            table = priority_frame
        else:
            table = self.frame

        base_columns = ['NumRows', 'NumColumns', 'NumNumericColumnType', 'NumCategoricalColumnType', ]
        table_definition = pd.DataFrame(columns=base_columns)
        C = 0; N = 0
        for column in table.columns:
            ColumnType = 'Letter' if table[column].dtype == 'object' else 'Number'
            if ColumnType == 'Letter':
                C += 1
            else:
                N += 1
        a_row = pd.DataFrame(data=[[table.shape[0], table.shape[1], N, C]], columns=base_columns)
        table_definition = table_definition.append(a_row)
        _csv_saving(table_definition, save, self.path, path, 'EDA_TableDefinition.csv')
        return table_definition

    def attributes_specification(self, priority_frame=None, save=False, path=None):
        if priority_frame is not None:
            table = priority_frame
        else:
            table = self.frame

        base_columns = ['Column', 'ColumnType', 'NumUniqueInstance', 'NumMV', 'DataType', 'DataExample', 'MaxInstanceLength']
        attributes_matrix = pd.DataFrame(columns=base_columns)
        for column in table.columns:
            ColumnType = 'Letter' if table[column].dtype == 'object' else 'Number' 
            NumUniqueInstance = table[column].value_counts().shape[0]
            MaxInstanceLength = table[column].astype('str').apply(lambda x: len(x)).max()
            NumMV = table[column].isna().sum()
            DataType = table[column].dtype.type
            a_row = pd.DataFrame(data=[[column, ColumnType, NumUniqueInstance, NumMV, DataType, table[column].iloc[np.random.randint(NumUniqueInstance)], MaxInstanceLength]], columns=base_columns)
            attributes_matrix = attributes_matrix.append(a_row)

        attributes_matrix.insert(2, 'NumRows', table.shape[0])
        attributes_matrix.insert(4, 'IdealSymmericCount', table.shape[0]/attributes_matrix['NumUniqueInstance'])
        attributes_matrix.insert(5, 'IdealSymmericRatio', 1/attributes_matrix['NumUniqueInstance'])    
        attributes_matrix.insert(6, 'MVRate', attributes_matrix['NumMV']/table.shape[0])
        attributes_matrix = attributes_matrix.reset_index().drop('index', axis=1)
        _csv_saving(attributes_matrix, save, self.path, path, 'EDA_AttributesSpecification.csv')
        return attributes_matrix


    def univariate_frequency(self, priority_frame=None, save=False, path=None, mode='base'):
        if priority_frame is not None:
            table = priority_frame
        else:
            table = self.frame

        base_columns = ['Column', 'NumMV', 'Instance', 'NumUniqueInstance', 'Count', 'Rank']
        frequency_matrix = pd.DataFrame(columns=base_columns)
        for column in table.columns:
            instance_count = table.value_counts(column, ascending=False).to_frame()
            rank_mapper = instance_count.rank(ascending=False)
            instance_frequency = instance_count.sort_index(ascending=True).reset_index().rename(columns={column:'Instance', 0:'Count'})
            instance_frequency.insert(0, 'Column', column)
            instance_frequency.insert(2, 'NumMV', table[column].isna().sum())
            instance_frequency.insert(3, 'NumUniqueInstance', instance_count.shape[0] + int(bool(table[column].isna().sum())) if mode == 'missing' else instance_count.shape[0])
            instance_frequency.insert(5, 'Rank', instance_frequency.Instance.apply(lambda x: rank_mapper.loc[x]))
            frequency_matrix = frequency_matrix.append(instance_frequency)
        NumRows = table.shape[0]
        frequency_matrix.insert(1, 'NumRows', NumRows)
        frequency_matrix.insert(3, 'MVRate', frequency_matrix.NumMV/frequency_matrix.NumRows)
        frequency_matrix.insert(4, 'NumRows_EFMV', frequency_matrix.NumRows - frequency_matrix.NumMV)
        frequency_matrix.insert(7, 'IdealSymmericCount', frequency_matrix.NumRows/frequency_matrix.NumUniqueInstance)
        frequency_matrix.insert(9, 'IdealSymmericRatio', 1/frequency_matrix.NumUniqueInstance)
        frequency_matrix.insert(10, 'Ratio', frequency_matrix.Count/frequency_matrix.NumRows)
            
        _csv_saving(frequency_matrix, save, self.path, path, 'EDA_UnivariateFrequencyAnalysis.csv')
        return frequency_matrix


    def univariate_percentile(self, priority_frame=None, save=False, path=None, mode='base', view='all', percent=5):
        if priority_frame is not None:
            table = priority_frame
        else:
            table = self.frame
        
        # for Numeric Columns
        table = table[table.columns[table.dtypes != object]]
        assert table.shape[1] >= 1, "This table doesn't even have a single numerical column. Change data-type of columns on table"
        
        percentile_range = list()
        percent_ = (percent/100); i = 0
        while True:
            i += 1
            cumulative_percent = round(percent_*i, 4)
            if cumulative_percent >= 1 :
                break
            percentile_range.append(cumulative_percent)
            
        describing_matrix = table.describe(percentiles=percentile_range).T
        describing_matrix.insert(3, 'DiffMaxMin', describing_matrix['max'] - describing_matrix['min'])
        describing_matrix.insert(4, 'Density', describing_matrix['count']/(describing_matrix['max'] - describing_matrix['min']))
        describing_matrix.insert(5, 'DiffMaxMin_PRU', (describing_matrix['max'] - describing_matrix['min'])/(len(percentile_range)+1))    
        percentile_columns = describing_matrix.columns[3:]
        
        base_columns = ['Column', 'NumRows', 'NumRows_EFMV', 'MVRate' , 'NumUniqueInstance', 'IdealSymmetricCount', 'IdealSymmetricRatio']
        data = dict()
        data['Column'] = describing_matrix.index.to_list()
        data['NumRows'] = [table.shape[0]]*describing_matrix.shape[0]
        data['NumRows_EFMV'] = describing_matrix['count'].to_list()
        data['MVRate'] = ((table.shape[0] - describing_matrix['count'])/table.shape[0]).to_list()
        data['NumUniqueInstance'] = [table.value_counts(column, ascending=False).to_frame().shape[0] + int(bool(table[column].isna().sum())) if mode == 'missing' else table.value_counts(column, ascending=False).to_frame().shape[0] for column in describing_matrix.index ]
        data['IdealSymmetricCount'] = list(map(lambda x: table.shape[0]/x, data['NumUniqueInstance'])) 
        data['IdealSymmetricRatio'] = list(map(lambda x: 1/x, data['NumUniqueInstance']))

        percentile_base = pd.DataFrame(data=data, columns=base_columns)#percentile_matrix = pd.DataFrame(columns=describing_matrix.columns[4:-1])
        percentile_matrix = pd.concat([percentile_base, describing_matrix.reset_index().drop(['index', 'count'], axis=1)], axis=1)
        
        base_column_for_diff = 'min'
        percentile_matrix_for_diff = percentile_matrix.loc[:, 'min':'max']
        for column in percentile_matrix_for_diff.columns:
            percentile_matrix[base_column_for_diff+'-'+column] = percentile_matrix_for_diff[column] - percentile_matrix_for_diff[base_column_for_diff]
            base_column_for_diff = column 
        percentile_matrix.drop('min-min', axis=1, inplace=True)
        percentile_base_matrix = percentile_matrix.loc[:, f'{percent}%':'max']
        percentile_diff_matrix = percentile_matrix.loc[:, f'min-{percent}%':]
        percentile_matrix['HighDensityRange'] = percentile_diff_matrix.columns[percentile_diff_matrix.values.argmin(axis=1)]
        percentile_matrix['HighDensityInstance'] = list(map(lambda x: percentile_base_matrix.iloc[x[0], x[1]], zip(percentile_base_matrix.index, percentile_diff_matrix.values.argmin(axis=1))))
        percentile_matrix['HighDensityMinMaxRangeRatio'] = (percentile_matrix['HighDensityInstance'] - percentile_matrix['min'])/(percentile_matrix['max'] - percentile_matrix['min'])
        _csv_saving(percentile_matrix, save, self.path, path, 'EDA_UnivariatePercentileAnalysis.csv')
        
        if view == 'p': # percentils
            percentile_matrix = pd.concat([percentile_matrix['Column'], percentile_matrix.loc[:, 'min':'max'], percentile_matrix.loc[:, 'HighDensityRange' : 'HighDensityMinMaxRangeRatio']], axis=1)
        elif view == 'ap':
            percentile_matrix = pd.concat([percentile_matrix['Column'], percentile_matrix.loc[:, 'DiffMaxMin':'max'], percentile_matrix.loc[:, 'HighDensityRange': 'HighDensityMinMaxRangeRatio']], axis=1)
        elif view == 'dp':
            percentile_matrix = pd.concat([percentile_matrix['Column'], percentile_matrix.loc[:, f'min-{percent}%':]], axis=1)
        elif view == 'adp':
            percentile_matrix = pd.concat([percentile_matrix['Column'], percentile_matrix.loc[:,'DiffMaxMin':'min'], percentile_matrix.loc[:,'max'], percentile_matrix.loc[:, f'min-{percent}%':]], axis=1)
        elif view == 'result':
            percentile_matrix = pd.concat([percentile_matrix['Column'], percentile_matrix.loc[:, 'HighDensityRange': 'HighDensityMinMaxRangeRatio']], axis=1)


        return percentile_matrix


    def bivariate_frequency(self, priority_frame=None, save=False, path=None, base_column=None):
        if priority_frame is not None:
            table = priority_frame
        else:
            table = self.frame

        if base_column is not None:
            base = table.groupby([base_column])[base_column].count().to_frame()
            base.columns = pd.Index(map(lambda x : (x, 'Instance') ,base.columns))
            for idx, column in enumerate(table.columns):
                if column != base_column:
                    concatenation_frame = table.groupby([base_column, column])[base_column].count().to_frame().unstack(column)
                    multi_index_frame = concatenation_frame.columns.to_frame()
                    multi_index_frame[0] = concatenation_frame.columns.names[1]
                    concatenation_frame.columns = multi_index_frame.set_index([0, column]).index                
                    base = pd.concat([base, concatenation_frame], axis=1).fillna(0)
        else:
            for idx, column in enumerate(table.columns):
                if idx == 0:
                    base_column = column
                    base = table.groupby([base_column])[base_column].count().to_frame()
                    base.columns = pd.Index(map(lambda x : (x, 'Instance') ,base.columns))
                else:
                    concatenation_frame = table.groupby([base_column, column])[base_column].count().to_frame().unstack(column)
                    multi_index_frame = concatenation_frame.columns.to_frame()
                    multi_index_frame[0] = concatenation_frame.columns.names[1]
                    concatenation_frame.columns = multi_index_frame.set_index([0, column]).index                
                    base = pd.concat([base, concatenation_frame], axis=1).fillna(0)

        base = base.reset_index()            
        base.insert(0, 'Column', base_column)
        
        columnidx = base.columns.to_frame()
        columnidxframe = pd.DataFrame(columnidx.values)
        columnidxframe.iat[0,0] = 'BaseColumn'    
        columnidxframe.iat[1,0] = 'Column'
        columnidxframe.iat[1,1] = 'Instance'
        columnidxframe.iat[2,1] = 'InstanceCount'
        base.columns = columnidxframe.set_index([0,1]).index

        _csv_saving(base, save, self.path, path, 'EDA_BivariateFrequencyAnalysis.csv')
        return base


    def bivariate_percentile(self, priority_frame=None, save=False, path=None, mode='base', view='all', percent=5, depth=10):
	if priority_frame is not None:
	    table = priority_frame
	else:
	    table = self.frame

	# for Numeric&Categorical Columns
	numerical_table = table[table.columns[table.dtypes != object]]
	categorical_table = table[table.columns[table.dtypes == object]]
	assert numerical_table.shape[1] >= 1, "This table doesn't even have a single numerical column. Change data-type of columns on table"        
	assert categorical_table.shape[1] >= 1, "This table doesn't even have a single categorical column. Change data-type of columns on table"        
	
	base_percentile_matrix = self.univariate_percentile(numerical_table)
	base = pd.DataFrame(columns=base_percentile_matrix.columns.to_list() + ['ComparisonInstance', 'ComparisonColumn'])
	for numerical_column in base_percentile_matrix['Column']:
	    print(f'* Base Numeric Column : {numerical_column}')
	    base_percentile_row = base_percentile_matrix[base_percentile_matrix['Column'] == numerical_column]
	    base_percentile_row.insert(base_percentile_row.shape[1], 'ComparisonInstance', '-')
	    base_percentile_row.insert(base_percentile_row.shape[1], 'ComparisonColumn', '-')
	    for categorical_column in categorical_table.columns:
		base_row_frame = pd.DataFrame(columns=base_percentile_matrix.columns.to_list() + ['ComparisonInstance'])
		for categorical_instance  in categorical_table[categorical_column].value_counts().iloc[:depth].index:
		    appending_table = table[table[categorical_column] == categorical_instance]
		    appending_percentile_matrix = self.univariate_percentile(priority_frame=appending_table, save=save, path=path, mode=mode, view=view, percent=percent)
		    appending_percentile_matrix.loc[:,'ComparisonInstance'] = categorical_instance
		    base_row_frame = base_row_frame.append(appending_percentile_matrix[appending_percentile_matrix['Column']==numerical_column])
		base_row_frame.loc[:,'ComparisonColumn'] = categorical_column
		base_percentile_row = base_percentile_row.append(base_row_frame)
	    base = base.append(base_percentile_row)

        _csv_saving(base, save, self.path, path, 'EDA_BivariatePercentileAnalysis.csv')
	return base




class Counting:
    def __init__(self, frame, path='ExploratoryDataAnalysis'):
        self.frame = frame
        self.path = path

    def CountUniqueValues(self, view='table', save=False, path=None):
        if view == 'table':
            data = list()
            for column in self.frame.columns:
                data.append([column, self.frame.value_counts(column).shape[0]])
            EDAframe = pd.DataFrame(data, columns=['Column', 'NumUniqueInstance'])
            _csv_saving(EDAframe, save, self.path, path, 'CountColumns.csv')

        elif view == 'column':
            EDAframe = pd.DataFrame(columns=['Column', 'Instance', 'Count'])
            for column in self.frame.columns:
                base = self.frame[column].value_counts().reset_index().rename(columns={'index':'Instance', column:'Count'})
                base.insert(0, 'Column', column)
                EDAframe = EDAframe.append(base)
            _csv_saving(EDAframe, save, self.path, path, 'CountInstances.csv')

        return EDAframe



def _csv_saving(frame, save, default_path, priority_path, name):
    if save:
        if not priority_path:
            if not os.path.isdir(default_path):
                os.mkdir(default_path)
            frame.to_csv(os.path.join(default_path, name))
            print(f'[AILEVER] The file {name} is saved at {default_path}.')

        else:
            if not os.path.isdir(priority_path):
                os.mkdir(priority_path)
            frame.to_csv(os.path.join(priority_path, name))
            print(f'[AILEVER] The file {name} is saved at {priority_path}.')

