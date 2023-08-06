import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.express as px
import statsmodels.api as sm

safegraph_cm = mpl.colors.LinearSegmentedColormap.from_list(
    'WhToBl', ['#ffffff', #0-1 
                '#f7fbff','#f7fbff','#f7fbff','#f7fbff',
                '#deebf7','#deebf7','#deebf7','#deebf7',
                '#c6dbef','#c6dbef','#c6dbef','#c6dbef',
                '#9ecae1','#9ecae1','#9ecae1','#9ecae1',
                '#6baed6','#6baed6','#6baed6','#6baed6',
                '#4292c6','#4292c6','#4292c6','#4292c6',
                '#2171b5','#2171b5','#2171b5','#2171b5',
                '#084594', #29-30
                ], N=30)

def get_ols(x,y):
    "Return an OLS model object of the form y=mx+b based on x and y inputs."
    x = sm.add_constant(x)
    est = sm.OLS(y,x,missing='raise').fit()
    return est
def get_y_ends(x_ends,params):
    "Return y min and y max as a tuple based on an OLS model params and an x min and x max as a tuple."
    y0 = params[0] + params[1]*x_ends[0]
    y1 = params[0] + params[1]*x_ends[1]
    return (y0,y1)

def plot_hexbin(df, groundtruth_colname, patterns_colname = "raw_visit_counts", bestfit = True, hexbin_gridsize = 30):
    """
    Plots a hexbin (2D histogram) using two columns of a pandas dataframe, typically with raw_visit_counts on the x-axis.

    Parameters:
        df (pandas DataFrame): DataFrame containing columns to plot
        groundtruth_colname (str): Column to plot on the y-axis.
    Optional Parameters:
        patterns_colname (str): Column to plot on the y-axis. Defaults to "raw_visit_counts".
        bestfit (bool): Whether or not to add a line of best fit and r2 to the plot. Defaults to True.
        hexbin_gridsize (int): Size of hexagon bins. Defaults to 30.
    """
    x = df[patterns_colname]
    y = df[groundtruth_colname]
    
    #generate plot parameters based on number of data points
    num_points = min(len(x),len(y)) 
    max_bin_color = num_points / 200
    
    #create plot
    hb = plt.hexbin(x,y,gridsize=hexbin_gridsize, cmap=safegraph_cm, vmin=0, vmax=max_bin_color)
    if bestfit:
        #plot bestfit line
        ols = get_ols(x,y)
        fitted = ols.fittedvalues
        x_range = (fitted.min(),fitted.max())
        y_range = get_y_ends(x_range,ols.params)
        plt.plot(x_range,y_range,'k--',lw=3)

        #add r2 text
        rsq = ols.rsquared
        big_x = x_range[0]+(x_range[1]-x_range[0])*0.95 #get positions dynamically
        small_y = y_range[0]+(y_range[1]-y_range[0])*0.05
        plt.text(big_x,small_y,'$r^2$={:0.2f}'.format(rsq),fontweight='bold',ha='right')

    #add plot labels
    plt.xlabel(patterns_colname)
    plt.ylabel(groundtruth_colname)

    #add colorbar axis
    cb = plt.colorbar(hb,orientation='vertical')
    cb.ax.tick_params(direction='out') 
    cb.set_label('Number of observations')
    
    plt.show()

def plot_scatter(df, groundtruth_colname, patterns_colname = "raw_visit_counts", bestfit = True, series_groupings = None):
    """
    Plots an interactive scatterplot using two columns of a pandas dataframe, typically with raw_visit_counts on the x-axis.

    Parameters:
        df (pandas DataFrame): DataFrame containing columns to plot
        groundtruth_colname (str): Column to plot on the y-axis.
    Optional Parameters:
        patterns_colname (str): Column to plot on the y-axis. Defaults to "raw_visit_counts".
        bestfit (bool): Whether or not to add a line of best fit and r2 to the plot. Defaults to True.
        series_groupings (str): Column to separate scatter points by color. Defaults to None (no grouping).
    """
    x = df[patterns_colname]
    y = df[groundtruth_colname]
    
    #create plot
    if bestfit:
        fig = px.scatter(df, x = patterns_colname, y = groundtruth_colname, trendline = 'ols', color = series_groupings)
    else:
        fig = px.scatter(df, x = patterns_colname, y = groundtruth_colname, color = series_groupings)
    
    fig.show()