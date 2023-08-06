# micro_cata

The goal of this package is to help analyze data taken from Garner, Zanic and coworkers: https://doi.org/10.1016/j.cell.2011.10.037 

# Data
Relevant data can be access from 
https://s3.amazonaws.com/bebi103.caltech.edu/data/gardner_mt_catastrophe_only_tubulin.csv

and 

https://s3.amazonaws.com/bebi103.caltech.edu/data/gardner_time_to_catastrophe_dic_tidy.csv

# Modules
In this package there are three modules
ecdf_tubulin: Allows you to generates a ECDF plot with confidence intervals for our labeled and unlabeled data
compare_model: Assess the gamma distribution and two-step model with a predictive ECDF and difference predictive ECDF
param_gamma: Generates parameter estimates for different tubulin concentration data and plots them with confidence intervals

# Folder setup
To make your life easier, I recommend that you set up your folders so that the data folder and the folder containing the notebook are on the same level.   