info_html = "\
<h6> How the Dashboard works </h6>\
<p>\
This dashboard application allows visualisation of a subset of OECD member countries based on \
how similar or dissimilar they are in terms of diagnoses made on hospital discharge (based on numbers of diagnoses per 100,000 population or female population). \
There are 20 categories of diagnoses available to be filtered. In addition, the number of clusters to group the countries \
may be adjusted. These processes of reducing the dataset into two axes to allow visualisation, and the learning of groups/clusters are \
both unsupervised Machine Learning algorithms.\
</p>\
<p>\
To view the underlying numerical data and to compare between countries, simply click on the datapoint or country in the plot. \
This will create a table with the selected countries and diagnostic categories. To collapse or show the sub-categories - \
click on the main category row.\
</p>\
<hr/>\
<h6> Methodology </h6>\
<p>\
This dashboard uses the OECD Health Care Utilisation dataset and the latest discharge diagnosis numbers for each country. \
After removing countries with unavailable data for discharge diagnoses, 26 countries remained which were mostly OECD member countries. \
There were over 100 numerical columns of different diagnoses. Depending on user selection of categories to show, these numerical columns were \
normalised and processed into two dimensions to allow plotting. This was performed using Spectral Embedding, an unsupervised machine learning process. \
Following this, the countries were clustered/ grouped depending on the two reduced dimensions using another unsupervised machine learning process called Agglomerative Clustering. \
These data processing and learning steps are dynamic and respond reactively to changes in user input.\
</p>\
"