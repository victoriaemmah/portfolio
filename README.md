# Portfolio

As I don't write code intended for anyone else to look at/work on, I had to create this github for the application. As such, I've uploaded some examples of my work across different projects. 

A brief explination of them:

seq_dep_all_plot.py: This is an example of data visualisation. It plots three different parameters relevant to my work on DNA and was written to plot data for my PhD thesis.

charlson_analysis.ipynb: This is a Jupyter Notebook that reads a dataset of raw data from my NHS project and makes it suitable for analytics. The raw data contains discharge codes that (ICD-10 codes in the format Xnnn where X is a letter and n are numbers) that are used to calculate Comorbidity scores. An example of the analytics is included - a logistic regression to look at the effect of the comorbidities on the outcome of patients. 

merging.ipynb: This is a Jupyter Notebook that takes raw, NHS data from multiple sources and merges them together based on patient identity and admission date, ensuring that they are matched on an episode-by-episode basis. NHS data is inherently messy and there are inconsistencies across the datasets, as such the code is messy and repetitive to deal with this. I have noted these in the comments.

ntpro_analysis.ipynb: This is a Jupyter Notebook for looking at the link between a blood biomarker and frailty score. As the paper is still currently under review, I have had to remove a lot of the analysis; however, I have shown here the initial exploratory analysis. 

I would like to note that these were written intended for my own use and for specific datasets. As such, I acknowledge that they cannot easily be applied to other datasets.
