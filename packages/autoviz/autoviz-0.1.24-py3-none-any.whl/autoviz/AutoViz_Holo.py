######################### AutoViz New with HoloViews ############################
import numpy as np
import pandas as pd
############# Import from autoviz.AutoViz_Class the following libraries #######
from autoviz.AutoViz_Utils import *
##############   make sure you use: conda install -c pyviz hvplot ###############
import hvplot.pandas  # noqa
import hvplot.dask  # noqa
import copy
import pdb
####################################################################################
#### The warnings from Sklearn are so annoying that I have to shut it off ####
import warnings
warnings.filterwarnings("ignore")
def warn(*args, **kwargs):
    pass
warnings.warn = warn
########################################
import logging
logging.getLogger("param").setLevel(logging.ERROR)
from bokeh.util.warnings import BokehUserWarning 
import warnings 
warnings.simplefilter(action='ignore', category=BokehUserWarning)
warnings.filterwarnings("ignore")
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)
####################################################################################
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
# from matplotlib import io
import io
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)
import re
import pdb
import pprint
import matplotlib
matplotlib.style.use('fivethirtyeight')
from itertools import cycle, combinations
from collections import defaultdict
import copy
import time
import sys
import random
import xlrd
import statsmodels
from io import BytesIO
import base64
from functools import reduce
import traceback
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from xgboost.sklearn import XGBRegressor
import os
##########################################################################################
######## This is where we import HoloViews related libraries  #########
import hvplot.pandas
import holoviews as hv
from holoviews import opts
#hv.notebook_extension('bokeh')
hv.extension('bokeh', 'matplotlib')
#hv.extension('bokeh')
import panel as pn
import panel.widgets as pnw
import holoviews.plotting.bokeh
######################################################################################
######## This is where we store the image data in a dictionary with a list of images #########
def save_image_data(fig, chart_count, chart_format):
    if chart_format == 'svg':
        ###### You have to add these lines to each function that creates charts currently ##
        imgdata = io.StringIO()
        fig.savefig(imgdata, format=chart_format)
        imgdata.seek(0)
        svg_data = imgdata.getvalue()
        return svg_data
    elif chart_format in ['png','jpg']:
        ### You have to do it slightly differently for PNG and JPEG formats
        imgdata = BytesIO()
        fig.savefig(imgdata, format=chart_format, bbox_inches='tight', pad_inches=0.0)
        imgdata.seek(0)
        figdata_png = base64.b64encode(imgdata.getvalue())
        return figdata_png
##############  This is where we
def append_panels(hv_panel, imgdata_list, chart_format):
    imgdata_list.append(hv.output(hv_panel, backend='bokeh', fig=chart_format))
    return imgdata_list
###### Display on Jupyter Notebook or on the Server ########
def display_dmap(dmap):
    renderer = hv.renderer('bokeh')
    #### You must have a Dynamic Map dmap to render these Bokeh objects on Servers
    app = renderer.app(dmap)
    server = renderer.app(dmap, show=True, new_window=True)
    return server
####################################################################################
def display_obj(dmap_in):
    ### This is to render the chart in a web server to display as a dashboard!!
    renderer = hv.renderer('bokeh')
    #### You must have a Dynamic Map dmap to render these Bokeh objects on Servers
    app = renderer.app(dmap_in)
    server = renderer.app(dmap_in, show=True, new_window=True)
    display(server)
####################################################################################
def display_server(dmap):
    #### You must have a Dynamic Map dmap to render these Bokeh objects on Servers
    server = pn.serve(dmap, start=True, show=False)
    return server
##############################  This is the beginning of the new AutoViz_Holo ###################
def AutoViz_Holo(filename, sep=',', depVar='', dfte=None, header=0, verbose=0,
                        lowess=False,chart_format='svg',max_rows_analyzed=150000,
                            max_cols_analyzed=30):
    """
    ##############################################################################
    ##### AUTOVIZ_HOLO PERFORMS AUTO VISUALIZATION OF ANY DATA SET USING BOKEH. ##
    #####    Give it any input file (CSV, txt or json) and AV will visualize it.##
    ##### INPUTS:                                                            #####
    #####    A FILE NAME OR A DATA FRAME AS INPUT.                           #####
    ##### AutoViz will visualize any sized file using a statistically valid sample.
    #####  - max_rows_analyzed = 150000 ### this limits the max number of rows ###
    #####           that is used to display charts                             ###
    #####  - max_cols_analyzed = 30  ### This limits the number of continuous  ###
    #####           vars that can be analyzed                                 ####
    #####  - COMMA is assumed as default separator in file. But u can change it.##
    #####  - Assumes first row as header in file but you can change it.      #####
    #####  - First instantiate an AutoViz class to  hold output of charts, plots.#
    #####  - Then call the Autoviz program with inputs as defined below.       ###
    ##############################################################################
    ####  If chart_format='bokeh': Bokeh charts are plotted on Jupyter Notebooks##
    ####  This is the default for AutoViz_Holo.                              #####
    ####  If chart_format='server', dashboards will pop up for each kind of    ###
    ####  chart on your browser.                                             #####
    ####  In both cases, all charts are interactive and you can play with them####
    ####  In the next version, I will let you save them in HTML.             #####
    ##############################################################################
    """
    if verbose <= 1:
        # ipython inline magic shouldn't be needed because all plots are
        # being displayed with plt.show() calls
        get_ipython().magic('matplotlib inline')
    ####################################################################################
    corr_limit = 0.7  ### This is needed to remove variables correlated above this limit
    ######### create a directory to save all plots generated by autoviz ############
    mk_dir = os.path.join(".","AutoViz_Plots")
    if verbose == 2 and not os.path.isdir(mk_dir):
        os.mkdir(mk_dir)
    ############   Start the clock here and classify variables in data set first ########
    start_time = time.time()
    try:
        dfin, dep,IDcols,bool_vars,cats,nums,discrete_string_vars,date_vars,classes,problem_type,selected_cols = classify_print_vars(
                                            filename,sep,max_rows_analyzed, max_cols_analyzed,
                                            depVar,dfte,header,verbose)
    except:
        print('Not able to read or load file. Please check your inputs and try again...')
        return None
    #################   This is where the differentiated HoloViews code begins ####
    ls_objects = []
    imgdata_list = list()
    height_size = 400
    width_size = 500
    ##########    Now start drawing the Bokeh Plots ###############################
    if len(nums) > 0:
        drawobj1 = draw_scatters(dfin,nums,chart_format,problem_type,
                      dep, classes, lowess,verbose)
        ls_objects.append(drawobj1)
        
        if len(nums) >= 2:
            drawobj2 = draw_pair_scatters(dfin, nums, problem_type, chart_format, dep,
                           classes, lowess, verbose)
            ls_objects.append(drawobj2)
    drawobj3 = draw_distplot(dfin, cats, nums, chart_format, problem_type, dep, classes, verbose)
    ### This is to render the chart in a web server to display as a dashboard!!
    ls_objects.append(drawobj3)
    if problem_type.endswith('Classification'):
        colors = cycle('brycgkbyrcmgkbyrcmgkbyrcmgkbyr')
        pdf1 = pd.DataFrame(dfin[dep].value_counts().reset_index())
        pdf2 = pd.DataFrame(dfin[dep].value_counts(1).reset_index())
        drawobj41 = pdf1.hvplot(kind='bar', color='r', title='Distribution of Target variable').opts(
                        height=height_size, width=width_size,xrotation=70)
        drawobj42 = pdf2.hvplot(kind='bar', color='g', title='Percent Distribution of Target variable').opts(
                        )
        dmap = hv.DynamicMap((drawobj41+drawobj42).opts(shared_axes=False).opts(title='Histogram and KDE of Target = %s' %dep)).opts(
                            height=height_size, width=width_size)
        dmap.opts(framewise=True,axiswise=True) ## both must be True for your charts to have dynamically varying axes!
        hv_all = pn.pane.HoloViews(dmap)#, sizing_mode="stretch_both")
        if chart_format.lower() in ['server', 'bokeh_server']:
            #### If you want it on a server, you use drawobj.show()
            #(drawobj41+drawobj42).show()
            server = pn.serve(hv_all, start=True, show=True)
        else:
            ### This will display it in a Jupyter Notebook.
            display(hv_all)
        ls_objects.append(drawobj41)
        ls_objects.append(drawobj42)
    else:
        if not isinstance(dep, list):
            ### it means dep is a string ###
            if dep == '':
                pass
            else:
                drawobj41 = dfin[dep].hvplot(kind='bar', color='r', title='Histogram of Target variable').opts(
                                height=height_size,width=width_size,color='lightgreen', xrotation=70)
                drawobj42 = dfin[dep].hvplot(kind='kde', color='g', title='KDE Plot of Target variable').opts(
                                height=height_size,width=width_size,color='lightblue')
                dmap = hv.DynamicMap((drawobj41+drawobj42)).opts(title='Histogram and KDE of Target = %s' %dep, width=width_size)
                dmap.opts(framewise=True,axiswise=True) ## both must be True for your charts to have dynamically varying axes!
                hv_all = pn.pane.HoloViews(dmap)
                if chart_format.lower() in ['server', 'bokeh_server', 'bokeh-server']:
                    ### If you want it on a server, you use drawobj.show()
                    #(drawobj41+drawobj42).show()
                    server = pn.serve(hv_all, start=True, show=True)
                else:
                    ### This will display it in a Jupyter Notebook.
                    display(hv_all)
                ls_objects.append(drawobj41)
                ls_objects.append(drawobj42)
    if len(nums) > 0:
        drawobj5 = draw_violinplot(dfin, dep, nums, chart_format, problem_type, verbose)
        ls_objects.append(drawobj5)
    if len(nums) > 0:
        drawobj6 = draw_heatmap(dfin, nums, verbose,chart_format, date_vars, dep)
        ls_objects.append(drawobj6)
    if len(date_vars) > 0:
        drawobj7 = draw_date_vars(dfin,dep,date_vars, nums, chart_format, problem_type, verbose)
        ls_objects.append(drawobj7)
    if len(nums) > 0 and len(cats) > 0:
        drawobj8 = draw_cat_vars(dfin, dep, nums, cats, chart_format, problem_type, verbose)
    print('Time to run AutoViz (in seconds) = %0.0f' %(time.time()-start_time))
    return dfin
####################################################################################
def draw_cat_vars(dfin, dep, nums, cats, chart_format, problem_type, verbose=0):
    ######## SCATTER PLOTS ARE USEFUL FOR COMPARING NUMERIC VARIABLES
    ##### we are going to modify dfin and classes, so we are making copies to make changes
    dft = copy.deepcopy(dfin)
    image_count = 0
    imgdata_list = list()
    N = len(nums)
    cols = 2
    width_size = 600
    height_size = 400
    jitter = 0.05
    alpha = 0.5
    size = 5
    transparent = 0.5
    colortext = 'brycgkbyrcmgkbyrcmgkbyrcmgkbyr'
    colors = cycle('brycgkbyrcmgkbyrcmgkbyrcmgkbyr')
    #####################################################
    #######  This is where you call the widget and pass it two select_variables to draw a Bar Chart #######
    def load_symbol(each_cat, num, **kwargs):
        """
        This program must take in a variable passed from the widget and turn it into a chart.
        The input is known as each_cat and it is the variable you must use to get the data and build a chart.
        The output must return a HoloViews Chart.
        """
        width_size=15
        #######  This is where you plot the histogram of categorical variable input as each_cat ####
        conti_df = dft[[num,each_cat]].groupby(each_cat).mean().reset_index()
        row_ticks = dft[num].unique().tolist()
        color_list = next(colors)
        #pivotdf = pd.DataFrame(conti_df).set_index(each_cat)
        plot = conti_df.hvplot(kind='bar',stacked=False,use_index=False, color=color_list,
                              title='Average %s by each %s value' %(num,each_cat)).opts(xrotation=70)
        return plot
    ### This is where you create the dynamic map and pass it the variable to load the chart!
    dmap = hv.DynamicMap(load_symbol, kdims=['Select_Cat_Variable','Select_Num_Variable']).redim.values(
                Select_Cat_Variable=cats, Select_Num_Variable=nums).opts(framewise=True)
    ###########  This is where you put the Panel Together ############
    hv_panel = pn.panel(dmap)
    widgets = hv_panel[0]
    hv_panel = pn.Column(pn.Row(*widgets))
    ##### Save all the chart objects here ##############
    if verbose == 2:
        imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
        image_count += 1
    if chart_format in ['server', 'bokeh_server', 'bokeh-server']:
        #server = pn.serve(hv_all, start=True, show=True)
        hv_panel.show()
    else:
        display(hv_panel)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()        
    return imgdata_list
#####################################################################################################
def draw_scatters(dfin,nums,chart_format,problem_type,
                  dep=None, classes=None, lowess=False,verbose=0):
    ######## SCATTER PLOTS ARE USEFUL FOR COMPARING NUMERIC VARIABLES
    ##### we are going to modify dfin and classes, so we are making copies to make changes
    dfin = copy.deepcopy(dfin)
    dft = copy.deepcopy(dfin)
    image_count = 0
    imgdata_list = list()
    classes = copy.deepcopy(classes)
    N = len(nums)
    cols = 2
    width_size = 600
    height_size = 400
    jitter = 0.05
    alpha = 0.5
    bubble_size = 10
    colortext = 'brycgkbyrcmgkbyrcmgkbyrcmgkbyr'
    colors = cycle('brycgkbyrcmgkbyrcmgkbyrcmgkbyr')
    #####################################################
    if dep == None or dep == '':
        #### There is no need to do a scatter plot with a dep variable when no dependent variable is given
        hv_all = ''
    elif problem_type == 'Regression':
        ####### This is a Regression Problem #### You need to plot a Scatter plot ####
        ####### First, Plot each Continuous variable against the Target Variable ###
        ######   This is a Very Simple Way to build an Scatter Chart with One Variable as a Select Variable #######
        alpha = 0.5
        colors = cycle('brycgkbyrcmgkbyrcmgkbyrcmgkbyr')
        def load_symbol(symbol, **kwargs):
            color = next(colors)
            return hv.Scatter((dft[symbol].values,dft[dep].values)).opts(framewise=True).opts(size=bubble_size,
                    color=color, alpha=alpha, height=height_size, width=width_size).opts(
                    xlabel='%s' %symbol).opts(ylabel='%s' %dep).opts(
                   title='Scatter Plot of %s against %s variable' %(symbol,dep))
        ### This is where you create the dynamic map and pass it the variable to load the chart!
        dmap = hv.DynamicMap(load_symbol, kdims='Select_Variable').redim.values(Select_Variable=nums).opts(framewise=True)
        ###########  This is where you put the Panel Together ############
        hv_panel = pn.panel(dmap)
        widgets = hv_panel[0]
        hv_all = pn.Column(pn.Row(*widgets))
        if verbose == 2:
            imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
            image_count += 1
    else:
        ##################################################################################################################
        ####### This is a Classification Problem #### You need to plot a Scatter plot ####
        #######   This widget based code works well except it does not add jitter. But it changes y-axis so that's good!
        ##################################################################################################################
        target_vars = dft[dep].unique()
        x = pn.widgets.Select(name='x', options=nums)
        y = pn.widgets.Select(name='y', options=nums)
        kind = pn.widgets.Select(name='kind', value='scatter', options=['scatter'])
        #######  This is where you call the widget and pass it the hv_plotto draw a Chart #######
        plot = dft.hvplot(x=dep, y=y, kind=kind, height=height_size, width=width_size, size=bubble_size,
                        title='Scatter Plot of each independent numeric variable against target variable')
        hv_all = pn.Row(pn.WidgetBox(y), plot)

        ##################################################################################################################
        #############   This works well except that the y-axis does not change when you switch y-variable ################
        ##################################################################################################################
        #target_vars = dft[dep].unique().tolist()
        #color_list = list(colortext[:len(target_vars)])
        #def select_widget(Select_numeric_variable):
        #    """
        #    This program must take in a variable passed from the widget and turn it into a chart.
        #    The input is known as select_variable and it is the variable you must use to get the data and build a chart.
        #    The output must return a HoloViews Chart.
        #    """
        #    hv_string = ''
        #    target_list = np.unique(dfin[dep].values)
        #    lowerbound = dfin[Select_numeric_variable].min()
        #    upperbound = dfin[Select_numeric_variable].max()
        #    for each_t in target_list:
        #        if not isinstance(each_t, str):
        #            each_ts = str(each_t) 
        #        else:
        #            each_ts = copy.deepcopy(each_t)
        #        next_color = next(colors)
        #        #add_string = "hv.Scatter((dfin[dfin['"+dep+"']=="+each_ts+"]['"+dep+"'].values,dfin[dfin['"+dep+"']=="+each_ts+"]['"+Select_numeric_variable+"'].values)).opts(color='"+next_color+"',jitter=eval('"+str(jitter)+"'),alpha=eval('"+str(alpha)+"'),size=eval('"+str(bubble_size)+"'),height=eval('"+str(height_size)+"'),width=eval('"+str(width_size)+"'))"
        #        add_string = "hv.Scatter((dfin[dfin['"+dep+"']=="+each_ts+"]['"+dep+"'].values,dfin[dfin['"+dep+"']=="+each_ts+"]['"+Select_numeric_variable+"'].values)).opts(color='"+next_color+"',jitter=eval('"+str(jitter)+"'),alpha=eval('"+str(alpha)+"'),ylim=(eval('"+str(lowerbound)+"'),eval('"+str(upperbound)+"')),height=eval('"+str(height_size)+"'),width=eval('"+str(width_size)+"'))"
        #        hv_string += add_string + " * "
        #    return eval(hv_string[:-2]).opts(
        #            legend_position='top_left',title='Scatter Plot of each Numeric Variable against Target variable')
        #######  This is where you call the widget and pass it the select_variable to draw a Chart #######
        #########   This is for bokeh server only ##############
        #dmap = hv.DynamicMap(select_widget,  kdims=['Select_numeric_variable']).redim.values(Select_numeric_variable=nums).opts(framewise=True)
        ###########  This is where you put the Panel Together ############
        #hv_panel = pn.panel(dmap)
        #widgets = hv_panel[0]
        #hv_all = pn.Column(pn.Row(*widgets))
        ###########  E N D    O F     Y- A X I S    C O D E    ############
        if verbose == 2:
            imgdata_list = append_panels(hv_all, imgdata_list, chart_format)
            image_count += 1
    ####### End of Scatter Plots ######
    if chart_format in ['server', 'bokeh_server', 'bokeh-server']:
        #server = pn.serve(hv_all, start=True, show=True)
        hv_all.show()
    else:
        display(hv_all)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()        
    return hv_all
#######################################################################################
def draw_pair_scatters(dfin,nums,problem_type,chart_format, dep=None,
                       classes=None, lowess=False,verbose=0):
    """
    #### PAIR SCATTER PLOTS ARE NEEDED ONLY FOR CLASSIFICATION PROBLEMS IN NUMERIC VARIABLES
    ### This is where you plot a pair-wise scatter plot of Independent Variables against each other####
    """
    
    dft = dfin[:]
    image_count = 0
    imgdata_list = list()
    if len(nums) <= 1:
        return
    classes = copy.deepcopy(classes)
    height_size = 400
    width_size = 600
    alpha = 0.5
    bubble_size = 10
    cmap_list = ['rainbow', 'viridis', 'plasma', 'inferno', 'magma', 'cividis']
    if problem_type == 'Regression' or problem_type == 'Clustering':
        ########## This is for Regression problems ##########
        #########  Here we plot a pair-wise scatter plot of Independent Variables ####
        ### Only 1 color is needed since only 2 vars are plotted against each other ##
        ################################################################################################
        #####  This widgetbox code works but it doesn't change the x- and y-axis when you change variables
        ################################################################################################
        #x = pn.widgets.Select(name='x', options=nums)
        #y = pn.widgets.Select(name='y', options=nums)
        #kind = pn.widgets.Select(name='kind', value='scatter', options=['bivariate', 'scatter'])
        ### Let us say you want to change the range of the x axis 
        ## - Then you can explicitly set the limits and it works!
        #xlimi = (dft[x.value].min(), dft[x.value].max())
        #ylimi = (dft[y.value].min(), dft[y.value].max())
        #plot = dft.hvplot(x=x, y=y, kind=kind,  color=next(colors), alpha=0.5, xlim=xlimi, ylim=ylimi,
        #            title='Pair-wise Scatter Plot of two Independent Numeric variables')
        #hv_panel = pn.Row(pn.WidgetBox(x, y, kind),plot)
        ########################   This is the new way of drawing scatter   ###############################
        
        quantileable = [x for x in nums if len(dft[x].unique()) > 20]

        x = pnw.Select(name='X-Axis', value=quantileable[0], options=quantileable)
        y = pnw.Select(name='Y-Axis', value=quantileable[1], options=quantileable)
        size = pnw.Select(name='Size', value='None', options=['None'] + quantileable)
        color = pnw.Select(name='Color', value='None', options=['None', dep])

        @pn.depends(x.param.value, y.param.value, color.param.value) 
        def create_figure(x, y, color):
            opts = dict(cmap=cmap_list[0], width=width_size, height=height_size, line_color='black')
            if color != 'None':
                opts['color'] = color 
            opts['size'] = bubble_size
            opts['alpha'] = alpha
            opts['tools'] = ['hover']
            opts['toolbar'] = 'above'
            opts['colorbar'] = True
            return hv.Points(dft, [x, y], label="%s vs %s" % (x.title(), y.title()),
                title='Pair-wise Scatter Plot of two Independent Numeric variables').opts(**opts)

        widgets = pn.WidgetBox(x, y, color)

        hv_panel = pn.Row(widgets, create_figure).servable('Cross-selector')
        ########################   This is the old way of drawing scatter  ################################
        #colors = cycle('brycgkbyrcmgkbyrcmgkbyrcmgkbyr')
        #def load_symbol(symbol, variable, **kwargs):
        #    color = next(colors)
        #    return hv.Scatter((dft[symbol].values,dft[variable].values)).opts(framewise=True).opts(size=5,
        #            color=color, alpha=alpha, height=height_size, width=width_size).opts(
        #            xlabel='%s' %symbol).opts(ylabel='%s' %variable).opts(
        #           title='Scatter Plot of %s against %s variable' %(symbol,variable))
        ### This is where you create the dynamic map and pass it the variable to load the chart!
        #dmap = hv.DynamicMap(load_symbol, kdims=['Select_X','Select_Y']).redim.values(Select_X=nums, Select_Y=nums).opts(framewise=True)
        ###########  This is where you put the Panel Together ############
        #hv_panel = pn.panel(dmap)
        #widgets = hv_panel[0]
        #hv_panel = pn.Column(pn.Row(*widgets))
        ########################   End of the old way of drawing scatter  ################################
        if verbose == 2:
            imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
            image_count += 1
    else:
        ########## This is for Classification problems ##########
        #########  This is the new way to plot a pair-wise scatter plot ####
        quantileable = [x for x in nums if len(dft[x].unique()) > 20]

        x = pnw.Select(name='X-Axis', value=quantileable[0], options=quantileable)
        y = pnw.Select(name='Y-Axis', value=quantileable[1], options=quantileable)
        size = pnw.Select(name='Size', value='None', options=['None'] + quantileable)
        color = pnw.Select(name='Color', value='None', options=['None',dep])

        @pn.depends(x.param.value, y.param.value, color.param.value) 
        def create_figure(x, y, color):
            opts = dict(cmap=cmap_list[0], width=width_size, height=height_size, line_color='black')
            if color != 'None':
                opts['color'] = color 
            opts['size'] = bubble_size
            opts['alpha'] = alpha
            opts['tools'] = ['hover']
            opts['toolbar'] = 'above'
            opts['colorbar'] = True
            return hv.Points(dft, [x, y], label="%s vs %s" % (x.title(), y.title()),
                title='Pair-wise Scatter Plot of two Independent Numeric variables').opts(**opts)

        widgets = pn.WidgetBox(x, y, color)

        hv_panel = pn.Row(widgets, create_figure).servable('Cross-selector')
        #########  This is an old way to plot a pair-wise scatter plot ####
        #target_vars = dft[dep].unique()
        #x = pn.widgets.Select(name='x', options=nums)
        #y = pn.widgets.Select(name='y', options=nums)
        #kind = pn.widgets.Select(name='kind', value='scatter', options=['bivariate', 'scatter'])

        #plot = dft.hvplot(x=x, y=y, kind=kind, by=dep, height=height_size, alpha=0.5,
        #                title='Pair-wise Scatter Plot of two Independent Numeric variables')
        #hv_panel = pn.Row(pn.WidgetBox(x, y, kind), plot)
        if verbose == 2:
            imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
            image_count += 1
    ####### End of Pair Scatter Plots ######
    if chart_format in ['server', 'bokeh_server', 'bokeh-server']:
        #server = pn.serve(hv_panel, start=True, show=True)
        hv_panel.show()
    else:
        display(hv_panel)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()        
    return hv_panel
##################################################################################
##### Draw the Distribution of each variable using Distplot
##### Must do this only for Continuous Variables
def draw_distplot(dft, cats, conti, chart_format,problem_type,dep=None, classes=None,verbose=0):
    image_count = 0
    imgdata_list = list()
    #### Since we are making changes to dft and classes, we will be making copies of it here
    conti = list(set(conti))
    nums = copy.deepcopy(conti)
    dft = dft[:]
    classes = copy.deepcopy(classes)
    colors = cycle('brycgkbyrcmgkbyrcmgkbyrcmgkbyr')
    imgdata_list = list()
    width_size = 600  #### this is to control the width of chart as well as number of categories to display
    height_size = 400
    gap = 0.4 #### This controls the space between rows  ######
    if dep==None or dep=='' or problem_type == 'Regression':
        ######### This is for Regression problems only ########
        transparent = 0.7
        binsize = 30
        ### Be very careful with the next 2 lines: we want to fill NA with 0 in numeric vars
        for each_conti,k in zip(conti,range(len(conti))):
            if dft[each_conti].isnull().sum() > 0:
                dft[each_conti].fillna(0, inplace=True)
        ## In this case, we perform this only if we have Cat variables
        if not isinstance(dep, list):
            ### it means dep is a string ###
            if dep == '':
                pass
            elif len(cats) > 0:
                colors = cycle('brycgkbyrcmgkbyrcmgkbyrcmgkbyr')
                def select_widget(each_cat):
                    """
                    This program must take in a variable passed from the widget and turn it into a chart.
                    The input is known as each_cat and it is the variable you must use to get the data and build a chart.
                    The output must return a HoloViews Chart.
                    """
                    width_size=15
                    #######  This is where you plot the histogram of categorical variable input as each_cat ####
                    conti_df = dft[[dep,each_cat]].groupby(each_cat).mean().reset_index()
                    row_ticks = dft[dep].unique().tolist()
                    color_list = next(colors)
                    pivotdf = pd.DataFrame(conti_df.to_records()).set_index(each_cat)
                    plot = pivotdf.hvplot(kind='bar',stacked=False,use_index=False, color=color_list,
                                          title='Mean Target = %s by each Categorical Variable' %dep).opts(xrotation=70)
                    return plot
                #######  This is where you call the widget and pass it the select_variable to draw a Chart #######
                dmap = hv.DynamicMap(select_widget,  kdims=['Select_Cat_Variable']).redim.values(Select_Cat_Variable=cats)
                dmap.opts(framewise=True,axiswise=True) ## both must be True for your charts to have dynamically varying axes!
                ###########  This is where you put the Panel Together ############
                hv_panel = pn.panel(dmap)
                widgets = hv_panel[0]
                hv_all = pn.Column(pn.Row(*widgets))
                if verbose == 2:
                    imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
                    image_count += 1
                if chart_format in ['server', 'bokeh_server', 'bokeh-server']:
                    #server = pn.serve(hv_all, start=True, show=True)
                    hv_all.show()
                else:
                    display(hv_all)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()        
                    #display_obj(hv_all)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()
        if len(conti) > 0:
            try:
                ######   This is a Very Complex Way to build an ND Overlay Chart with One Variable as a Select Variable #######
                jitter = 0.5
                colors = cycle('brycgkbyrcmgkbyrcmgkbyrcmgkbyr')
                transparent = 0.5
                def select_variable_to_plot(num_var):
                    """
                    This program must take in a variable passed from the widget and turn it into a chart.
                    The input is known as num_var and it is the variable you must use to get the data and build a chart.
                    The output must return a HoloViews Chart.
                    """
                    color = next(colors)
                    xlimi = (dft[num_var].min(), dft[num_var].max())
                    hv_look = hv.Distribution(np.histogram(dft[num_var]), num_var).opts(color=color,
                                        height=height_size, width=width_size, alpha=transparent,
                                    title='KDE (Distribution) Plot of Numeric Variables').redim.range(num_var=xlimi)
                    return hv_look
                #######  This is where you call the widget and pass it the select_variable to draw a Chart #######
                dmap = hv.DynamicMap(select_variable_to_plot,  kdims=['Select_Variable']).redim.values(Select_Variable=nums)
                dmap.opts(framewise=True,axiswise=True) ## both must be True for your charts to have dynamically varying axes!
                ###########  This is where you put the Panel Together ############
                hv_panel = pn.panel(dmap)
                widgets = hv_panel[0]
                hv_all = pn.Column(pn.Row(*widgets))
            except:
                print('Error in Distribution Plot')
        if verbose == 2:
            imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
            image_count += 1
        if chart_format in ['server', 'bokeh_server', 'bokeh-server']:
            #server = pn.serve(hv_all, start=True, show=True)
            hv_all.show()
        else:
            display(hv_all)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()        
            #display_obj(hv_all)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()
    else:
        ######### This is for Classification problems only ########
        transparent = 0.7
        binsize = 30
        alpha = 0.5
        height_size = 400
        width_size = 600
        ### Be very careful with the next 2 lines: we want to fill NA with 0 in numeric vars
        target_vars = dft[dep].unique().tolist()
        if type(classes[0])==int:
            classes = [str(x) for x in classes]
        for each_conti,k in zip(conti,range(len(conti))):
            if dft[each_conti].isnull().sum() > 0:
                dft[each_conti].fillna(0, inplace=True)
        if len(cats) > 0:
            def select_widget(Select_categorical_var):
                """
                This program must take in a variable passed from the widget and turn it into a chart.
                The input is known as num_var and it is the variable you must use to get the data and build a chart.
                The output must return a HoloViews Chart.
                """
                colors = cycle('brycgkbyrcmgkbyrcmgkbyrcmgkbyr')
                #######  This is where you plot the histogram of categorical variable input as each_cat ####
                conti_df = dft[[dep,Select_categorical_var]].groupby([dep,Select_categorical_var]).size().nlargest(
                                    width_size).reset_index(name='Values')
                pivot_df = conti_df.pivot(index=Select_categorical_var, columns=dep, values='Values').fillna(0)
                row_ticks = dft[dep].unique().tolist()
                color_list = []
                for i in range(len(row_ticks)):
                    color_list.append(next(colors))
                pivotdf = pd.DataFrame(pivot_df.to_records()).set_index(Select_categorical_var)
                plot = pivotdf.hvplot(kind='bar',stacked=True,use_index=True,
                            title='Target = %s Histogram by each Categorical Variable' %dep).opts(
                                height=height_size,width=width_size, xrotation=70)
                return plot
            #######  This is where you call the widget and pass it the select_variable to draw a Chart #######
            dmap = hv.DynamicMap(select_widget,  kdims=['Select_categorical_var']).redim.values(
                                                Select_categorical_var=cats)
            ###########  This is where you put the Panel Together ############
            hv_panel = pn.panel(dmap)
            widgets = hv_panel[0]
            hv_all = pn.Column(pn.Row(*widgets))
            if verbose == 2:
                imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
                image_count += 1
            if chart_format in ['server', 'bokeh_server', 'bokeh-server']:
                #server = pn.serve(hv_all, start=True, show=True)
                hv_all.show()
            else:
                display(hv_all)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()        
                #display_obj(hv_all)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()
        if len(conti) > 0:
            try:
                ######   This is a Very Complex Way to build an ND Overlay Chart with One Variable as a Select Variable #######
                colortext = 'brycgkbyrcmgkbyrcmgkbyrcmgkbyr'
                target_vars = dft[dep].unique().tolist()
                color_list = list(colortext[:len(target_vars)])
                jitter = 0.5
                colors = cycle('brycgkbyrcmgkbyrcmgkbyrcmgkbyr')
                transparent = 0.5
                def select_widget(Select_numeric_variable):
                    """
                    This program must take in a variable passed from the widget and turn it into a chart.
                    The input is known as num_var and it is the variable you must use to get the data and build a chart.
                    The output must return a HoloViews Chart.
                    """
                    color = next(colors)
                    overlay = hv.NdOverlay({group: hv.Distribution(np.histogram(dft[dft[dep]==group][Select_numeric_variable].values)) for i,group in enumerate(target_vars)})
                    hv_look = overlay.opts(opts.Distribution(alpha=0.5, height=height_size, width=width_size)).opts(
                        title='KDE (Distribution) Plots of all Numeric Variables by Classes').opts(
                        xlabel='%s' %dep).opts(ylabel='%s' %Select_numeric_variable)
                    return hv_look
                #######  This is where you call the widget and pass it the select_variable to draw a Chart #######
                dmap = hv.DynamicMap(select_widget,  kdims=['Select_numeric_variable']).redim.values(Select_numeric_variable=nums)
                ###########  This is where you put the Panel Together ############
                hv_panel = pn.panel(dmap)
                widgets = hv_panel[0]
                hv_all = pn.Column(pn.Row(*widgets))
            except:
                print('Error in Distribution Plot')
            if verbose == 2:
                imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
                image_count += 1
            if chart_format in ['server', 'bokeh_server', 'bokeh-server']:
                #server = pn.serve(hv_all, start=True, show=True)
                hv_all.show()
            else:
                display(hv_all)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()        
                #display_obj(hv_all)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()
    ####### End of Distplots ###########
    return hv_all
##################################################################################
def draw_violinplot(dft, dep, nums,chart_format, modeltype='Regression',verbose=0):
    dft = dft[:]
    image_count = 0
    imgdata_list = list()
    number_in_each_row = 7
    imgdata_list = list()
    width_size = 600
    height_size = 400
    if type(dep) == str:
        nums = [x for x in nums if x not in [dep]]
    else:
        nums = [x for x in nums if x not in dep]
    if modeltype == 'Regression' or dep == None or dep == '':
        ###### This is for Regression and Clustering problems only ##########################
        if modeltype == 'Regression':
            nums = nums + [dep]
        ###### This is for looping over variables 10 at a time only ##########################
        df_p = dft[nums]
        if df_p.shape[1] < number_in_each_row:
            iter_limit = number_in_each_row
        else:
            iter_limit = max(number_in_each_row, int(df_p.shape[1]/5+0.5))
        print('Current number of Numeric Variables = %d ' %(df_p.shape[1],))
        ###### This is for looping over variables 10 at a time only ##########################
        drawobjv_list = [] ## this keeps track of the actual values
        drawobj_list = [] ## this keeps track of the names
        counter = 0
        for i in range(0,df_p.shape[1],iter_limit):
            new_end = i+iter_limit
            #print('i = ',i,"new end = ", new_end)
            if i == 0:
                title_string = 'using first %d variables...' %(iter_limit)
                #print(title_string )
            else:
                title_string = 'using next %d variables...' %(iter_limit)
                #print(title_string )
            conti = nums[i:new_end]
            ######################### Add Standard Scaling here ##################################
            from sklearn.preprocessing import StandardScaler
            SS = StandardScaler()
            data = pd.DataFrame(SS.fit_transform(dft[conti]),columns=conti)
            var_name = 'drawobjv_list['+str(counter)+']'
            drawobj_list.append(var_name)
            drawobjv_list.append(var_name)
            drawobj = data.hvplot(kind='violin', label='Violin Plot %s (Standard Scaled)' %title_string,)
                                     #height=height_size,width=width_size)
            drawobjv_list[counter] = drawobj
            counter += 1
        ######### After collecting all the drawobjv's put them in a dynamic map and display them ###
        combined_charts = "("+"".join([x+'+' for x in drawobj_list])[:-1]+")"
        if chart_format.lower() in ['server', 'bokeh_server', 'bokeh-server']:
            ### If you want it on a server, you use drawobj.show()
            #(drawobj41+drawobj42).show()
            dmap = hv.DynamicMap(eval(combined_charts).opts(title='Violin Plots of all Numeric Variables', width=width_size))
            dmap = pn.pane.HoloViews(dmap, sizing_mode="stretch_both")
        else:
            ### This will display it in a Jupyter Notebook.
            dmap = hv.DynamicMap(eval(combined_charts).opts(title='Violin Plots of all Numeric Variables', width=width_size))
        ###########  This is where you put the Panel Together ############
        hv_panel = pn.panel(dmap)
        widgets = hv_panel[0]
        hv_all = pn.Column(pn.Row(*widgets))
        #### This is where we add them to the list ######        
        if verbose == 2:
            imgdata_list = append_panels(hv_all, imgdata_list, chart_format)
            image_count += 1
        #### In the case of violin plots, you have to create multiple tabs or plots ###
        if chart_format in ['server', 'bokeh_server', 'bokeh-server']:
            server = pn.serve(hv_all, start=True, show=True)
            #hv_all.show()  ### for some reason .show errors in violin plots
        else:
            display(hv_all)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()        
            #display_obj(hv_all)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()
    else :
        df_p = dft[nums]
        if df_p.shape[1] < number_in_each_row:
            iter_limit = number_in_each_row
        else:
            iter_limit = max(number_in_each_row, int(df_p.shape[1]/5+0.5))
        print('Current number of Numeric Variables = %d ' %(df_p.shape[1],))
        ###### This is for looping over variables 10 at a time only ##########################
        target_vars = np.unique(dft[dep])
        for symbol in target_vars:
            print('    Drawing Violin plots for %s class = %s' %(dep,symbol))
            drawobjv_list = [] ## this keeps track of the actual values
            drawobj_list = [] ## this keeps track of the names
            counter = 0
            for i in range(0,df_p.shape[1],iter_limit):
                new_end = i+iter_limit
                if i == 0:
                    title_string = 'using first %d variables...' %(iter_limit)
                else:
                    title_string = 'using next %d variables...' %(iter_limit)
                conti = nums[i:new_end]
                ######################### Add Standard Scaling here ##################################
                from sklearn.preprocessing import StandardScaler
                SS = StandardScaler()
                data = pd.DataFrame(SS.fit_transform(dft[conti]),columns=conti)
                data[dep] = dft[dep].values
                dft_sym = data[data[dep] == symbol][conti]
                var_name = 'drawobjv_list['+str(counter)+']'
                drawobj_list.append(var_name)
                drawobjv_list.append(var_name)
                drawobj =  dft_sym.hvplot(kind='violin').opts(framewise=True).opts(
                        #height=height_size, width=width_size).opts(
                       title='Violin Plot %s (Standard Scaled):' %title_string)
                drawobjv_list[counter] = drawobj
                counter += 1
            ######### After collecting all the drawobjv's put them in a dynamic map and display them ###
            combined_charts = "("+"".join([x+'+' for x in drawobj_list])[:-1]+")"
            dmap = hv.DynamicMap(eval(combined_charts).opts(title='Violin Plots for %s target class' %symbol, width=width_size))
            dmap = pn.pane.HoloViews(dmap, sizing_mode="stretch_both")
            ###########  This is where you put the Panel Together ############
            hv_panel = pn.panel(dmap)
            widgets = hv_panel[0]
            hv_all = pn.Column(pn.Row(*widgets))
            if chart_format.lower() in ['server', 'bokeh_server', 'bokeh-server']:
                ### If you want it on a server, you use drawobj.show()
                server = pn.serve(hv_all, start=True, show=True)
            else:
                ### This will display it in a Jupyter Notebook.
                display(dmap)
            #### This is where we add them to the list ######        
            if verbose == 2:
                imgdata_list = append_panels(hv_all, imgdata_list, chart_format)
                image_count += 1
    ########## End of Violin Plots #########
    return hv_all
##################################################################################
def draw_date_vars(df,dep,datevars, num_vars, chart_format, modeltype='Regression',verbose=0):
    #### Now you want to display 2 variables at a time to see how they change over time
    ### Don't change the number of cols since you will have to change rows formula as well
    df = df[:]
    imgdata_list = list()
    image_count = 0
    N = len(num_vars)
    dft = df.set_index(pd.to_datetime(df.pop(datevars[0])))
    if N < 2:
        var1 = num_vars[0]
        width_size = 5
        height_size = 5
        fig = plt.figure(figsize=(width_size,height_size))
        dft[var1].plot(title=var1, label=var1)
        fig.suptitle('Time Series Plot of %s' %var1, fontsize=20,y=1.08)
        if verbose == 2:
            imgdata_list.append(save_image_data(fig, image_count, chart_format))
            image_count += 1
        return imgdata_list
    if isinstance(dft.index, pd.DatetimeIndex) :
        dft =  dft[:]
        pass
    else:
        dft = dft[:]
        try:
            col = datevars[0]
            if dft[col].map(lambda x: 0 if len(str(x)) == 4 else 1).sum() == 0:
                if dft[col].min() > 1900 or dft[col].max() < 2100:
                    dft[col] = dft[col].map(lambda x: '01-01-'+str(x) if len(str(x)) == 4 else x)
                    dft.index = pd.to_datetime(dft.pop(col), infer_datetime_format=True)
                else:
                    print('%s could not be indexed. Could not draw date_vars.' %col)
                    return imgdata_list
            else:
                dft.index = pd.to_datetime(dft.pop(col), infer_datetime_format=True)
        except:
            print('%s could not be indexed. Could not draw date_vars.' %col)
            return imgdata_list
    ####### Draw the time series for Regression and DepVar
    if modeltype == 'Regression' or dep == None or dep == '':
        kind = 'line'
        plot = dft[num_vars+[dep]].hvplot( height=400, width=600,kind=kind,
                        title='Time Series Plot of all Numeric variables and Target').opts(legend_position='top_left')
        hv_panel = pn.Row(pn.WidgetBox( kind), plot)
        if verbose == 2:
            imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
            image_count += 1
    else:
        ######## This is for Classification problems only
        kind = 'line'
        plot = dft[num_vars+[dep]].hvplot(groupby=dep, height=400, width=600,kind=kind,
                        title='Time Series Plot of all Numeric variables by Target').opts(legend_position='top_left')
        hv_panel = pn.Row(pn.WidgetBox( kind), plot)
        if verbose == 2:
            imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
            image_count += 1
    ############# End of Date vars plotting #########################
    if chart_format in ['server', 'bokeh_server', 'bokeh-server']:
        #server = pn.serve(hv_panel, start=True, show=True)
        hv_panel.show()
    else:
        display(hv_panel)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()        
        #display_obj(hv_panel)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()
    return hv_panel
##### Draw a Heatmap using Pearson Correlation #########################################
def draw_heatmap(dft, conti, verbose,chart_format,datevars=[], dep=None,
                                    modeltype='Regression',classes=None):
    #####
    ### Test if this is a time series data set, then differene the continuous vars to find
    ###  if they have true correlation to Dependent Var. Otherwise, leave them as is
    width_size = 600
    height_size = 400
    cmap_list = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    if len(conti) <= 1:
        return
    elif len(conti) <= 10:
        height_size = 500
        width_size = 600
    else:
        height_size = 800
        width_size = 1200
    if isinstance(dft.index, pd.DatetimeIndex) :
        dft = dft[:]
        timeseries_flag = True
        pass
    else:
        dft = dft[:]
        try:
            dft.index = pd.to_datetime(dft.pop(datevars[0]),infer_datetime_format=True)
            timeseries_flag = True
        except:
            if verbose == 1 and len(datevars) > 0:
                print('No date vars could be found or %s could not be indexed.' %datevars)
            elif verbose == 1 and len(datevars) == 0:
                print('No date vars could be found in data set')
            timeseries_flag = False
    # Add a column: the color depends on target variable but you can use whatever function
    imgdata_list = list()
    if modeltype != 'Regression':
        ########## This is for Classification problems only ###########
        if dft[dep].dtype == object or dft[dep].dtype == np.int64:
            dft[dep] = dft[dep].factorize()[0]
        image_count = 0
        N = len(conti)
        target_vars = dft[dep].unique()
        plotc = 1
        #rows = len(target_vars)
        rows = 1
        cols = 1
        if timeseries_flag:
            dft_target = dft[[dep]+conti].diff()
        else:
            dft_target = dft[:]
        dft_target[dep] = dft[dep].values
        corre = dft_target.corr()
        if timeseries_flag:
            heatmap = corre.hvplot.heatmap(height=height_size, width=width_size, colorbar=True, 
                    cmap=cmap_list, rot=70,
            title='Time Series: Heatmap of all Differenced Continuous vars for target = %s' %dep)
        else:
            heatmap = corre.hvplot.heatmap(height=height_size, width=width_size,  colorbar=True,
                    cmap=cmap_list,
                    rot=70,
            title='Heatmap of all Continuous Variables including target = %s' %dep);
        hv_panel = heatmap * hv.Labels(heatmap).opts(opts.Labels(text_font_size='7pt'))
        if verbose == 2:
            imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
            image_count += 1
    else:
        ### This is for Regression and None Dep variable problems only ##
        image_count = 0
        if dep is None or dep == '':
            pass
        else:
            conti += [dep]
        dft_target = dft[conti]
        if timeseries_flag:
            dft_target = dft_target.diff().dropna()
        else:
            dft_target = dft_target[:]
        N = len(conti)
        corre = dft_target.corr()
        if timeseries_flag:
            heatmap = corre.hvplot.heatmap(height=height_size, width=width_size, colorbar=True, 
                    cmap=cmap_list,
                                           rot=70,
                title='Time Series Data: Heatmap of Differenced Continuous vars including target = %s' %dep).opts(
                        opts.HeatMap(tools=['hover'], toolbar='above'))
        else:
            heatmap = corre.hvplot.heatmap(height=height_size, width=width_size, colorbar=True, 
                    cmap=cmap_list,
                                           rot=70,
            title='Heatmap of all Continuous Variables including target = %s' %dep).opts(
                                    opts.HeatMap(tools=['hover'],  toolbar='above'))
        hv_panel = heatmap * hv.Labels(heatmap).opts(opts.Labels(text_font_size='7pt'))
        if verbose == 2:
            imgdata_list = append_panels(hv_panel, imgdata_list, chart_format)
            image_count += 1
    ############# End of Heat Maps ##############
    if chart_format in ['server', 'bokeh_server', 'bokeh-server']:
        server = pn.serve(hv_panel, start=True, show=True)
        #hv_panel.show() ### dont use show for just heatmap there is some problem with it
    else:
        display(hv_panel)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()        
        #display_obj(hv_panel)  ### This will display it in a Jupyter Notebook. If you want it on a server, you use drawobj.show()
    return hv_panel
#######################################################################################
###########################################################################################
