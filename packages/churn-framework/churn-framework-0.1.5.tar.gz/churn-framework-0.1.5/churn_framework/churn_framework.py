import pandas as pd
import numpy as np
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm



def evaluate_metrics(df_client, df_churn, dict_df, clients, churns, mask_cliente, mask_churn):
	""" 
 	Method that calculates the evaluation metrics that best separates clients and churn 
 	cases and return thhose metrics on a data frame

	Returns
	-------
	dict_df: pd.DataFrame
	"""
	tp = df_client.loc[mask_cliente,:].shape[0]/clients
	fn = 1-tp
	fp = df_churn.loc[mask_churn,:].shape[0]/churns
	tn = 1-fp
	delta = tp - fp
	precision = tp/(tp+fp)
	recall = tp/(tp+fn)
	dict_df['precision'].append(precision)
	dict_df['recall'].append(recall)
	dict_df['f05'].append((1.25 * precision * recall) / (0.25 * precision + recall))
	dict_df['f1'].append((2*(precision*recall)/(precision+recall)))
	dict_df['perc_churn'].append(fp)
	dict_df['perc_client'].append(tp)
	dict_df['delta'].append(delta)
	return dict_df


def apply_filters(params, mask, df_mes, accumulated, min_values):
	""" 
 	Method that filters dataframe of results according to constraints
        
	Returns
	-------
	df_mes: pd.DataFrame
	"""
	for key in params['constrains'].keys():
		mask = mask & (df_mes[key]>params['constrains'][key])
	if accumulated and sum(min_values.values()) > 0:
		for key in min_values.keys():
			mask = mask & (df_mes[key]>min_values[key])
	df_mes = df_mes.loc[mask,:].reset_index(drop=True)
	return df_mes


def get_best_value(df_mes, params, min_values, df_optms):
	""" 
 	Method that returns maximum point of the parameter to be optimized
        
	Returns
	-------
	df_optms: pd.DataFrame
	"""

	df_mes = df_mes[df_mes[params['optimize']] == df_mes[params['optimize']].max()].head(1)
	if df_mes.shape[0]>0:
		for key in min_values.keys():
			min_values[key] = df_mes[key].values[0]
	df_optms = pd.concat([df_optms,df_mes])
	return df_optms


def get_great_value(metrics, params, accumulated, df_months):
    """ 
 	Method that finds the optimal value for one or more features based on constraints
        
    Parameters
    ----------            
    metrics: dict
             Dictionary containing name of feature to be tested and list containing range of numerical values
    params: dict
            Dictionary containing: optimize: optimization metric('f05', 'f1', 'precision', 'recall'),
                                   counterins: constraints used 
    accumulated: Bool
    			 True if metrics/feature is accumulated
    df_months: pd.Dataframe
    		   list of data frames, based on month   
    Returns
    -------
    df_results: pd.Dataframe
    df_months: pd.Dataframe
	"""

    # cria data frames de retorno
    df_results = []
    df_optms = pd.DataFrame()
    min_values = {}
    for key in metrics.keys():
        min_values[key] = 0
        
    # intera cada data frame por mês
    for mes in tqdm(range(1,7)):
        df_alvo = df_months[mes]
        #cria df do mês e parametros
        df_mes = pd.DataFrame()
        dict_df = {'precision':[],'recall':[],'f05':[],'f1':[], 'perc_churn':[], 'perc_client':[], 'delta':[]}
        for key in metrics.keys():
            dict_df[key] = []
            
        # total de clientes e churn e separa os dataframes em cliente e churn
        clients = sum(df_alvo['Churn']=='Client')
        churns = sum(df_alvo['Churn']=='Churn')
        df_client = df_alvo[df_alvo['Churn']=='Client'].reset_index(drop=True)
        df_churn = df_alvo[df_alvo['Churn']=='Churn'].reset_index(drop=True)
        #faz o produto cartesiano de todas as possibilidades dos ranges
        for item in list(itertools.product(*list(metrics.values()))):
            
            #cria filtros para as métricas
            mask_cliente = True
            mask_churn = True
            for key in metrics.keys():
                dict_df[key].append(item[list(metrics.keys()).index(key)])
                mask_cliente = mask_cliente & (df_client[key]>=item[list(metrics.keys()).index(key)])
                mask_churn = mask_churn & (df_churn[key]>=item[list(metrics.keys()).index(key)])
                
            #calcula parametros
            dict_df = evaluate_metrics(df_client, df_churn, dict_df, clients, churns, mask_cliente, mask_churn)
        
        #salva o resultado do mês
        df_mes = pd.DataFrame(dict_df)
        df_results.append(pd.DataFrame(df_mes))
        
        #calculando ponto ótimo
        df_mes['mes'] = mes
        mask = df_mes['precision']>df_mes['recall']
        
        
        #filtra dataframe de resultados conforme restrições
        df_mes = apply_filters(params, mask, df_mes, accumulated, min_values)
        
        #ponto máximo do parametro a otimizar
        df_optms = get_best_value(df_mes, params, min_values, df_optms)
        
        
        
    return df_results,df_optms



def plot_metrics(df_result, df_optms, month, metric):
	""" 
 	Method that plots evaluation metrics for each value on df_result

	"""
	sns.lineplot(data=df_result[month], x=metric, y="precision", color='green', label="precision")
	sns.lineplot(data=df_result[month], x=metric, y="recall" , color='red', label="recall")
	sns.lineplot(data=df_result[month], x=metric, y="f1", color='blue', label="f1")
	sns.lineplot(data=df_result[month], x=metric, y="f05", color='orange', label="f05")
	plt.axvline(df_optms[df_optms.mes==month][metric].item())

def get_confusion_matrix(df_optms, month):
	""" 
 	Method that returns Client/Churn confusion matrix values for a specific month

    Returns
    -------
    np.array
	"""
	perc_churn = df_optms[df_optms.mes==month].perc_churn.item()
	perc_client = df_optms[df_optms.mes==month].perc_client.item()
	return np.asarray([[perc_client, 1-perc_client], [perc_churn, 1-perc_churn]])

def plot_matrix(matrix):
	""" 
 	Method that plots Client/Churn confusion matrix

	"""
	group_names = ['Client Atingiu','Client Não Atingiu', 'Churn Atingiu', 'Churn Não Atingiu']
	group_percentages = ['{0:.2%}'.format(value) for value in
                     matrix.flatten()]
	labels = [f'{v1}\n{v2}' for v1, v2 in
          zip(group_names,group_percentages)]
	labels = np.asarray(labels).reshape(2,2)
	print('Teste')
	sns.heatmap(matrix, annot=labels, fmt='', cmap='Reds_r', cbar=False)