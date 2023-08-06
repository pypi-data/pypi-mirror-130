#Expected file: '../data/gardner_time_to_catastrophe_dic_tidy.csv' or 'C:data/gardner_time_to_catastrophe_dic_tidy.csv'
def ecdf_tubulin (file):  
    """
    This function will allow you to create an ECDF plot with confidence intervals for labeled and unlabeled tubulin data
    Expected file: '../data/gardner_time_to_catastrophe_dic_tidy.csv' or 'C:data/gardner_time_to_catastrophe_dic_tidy.csv'
    For ease of us set up folders so that the data folder containing the folder containing the notebook are on the same  
    level.        

    """
    #Import packages
    import pandas as pd; import numpy as np; 

    import iqplot; import bokeh.io; import bokeh.plotting; import colorcet; import holoviews as hv

    bokeh.io.output_notebook()
    hv.extension("bokeh")  

    #import data
    data = pd.read_csv(file, header=[0])
    
    #Create new dataframes that contain either only labeled or unlabeled data
    labeled = data.loc[data["labeled"] == True, "time to catastrophe (s)"].values
    unlabeled = data.loc[data["labeled"] == False, "time to catastrophe (s)"].values

    #Plot time to catastrophe with an ECDF plot with confidence intervals
    p = iqplot.ecdf(
        data=data, cats="labeled", q="time to catastrophe (s)", conf_int=True
    )

    p.legend.title = "labeled"
    
    return bokeh.io.show(p)