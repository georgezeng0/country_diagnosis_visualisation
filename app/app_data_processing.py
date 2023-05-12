# Python modules
from pathlib import Path
import pandas as pd
import pyodide.http
from io import StringIO
import bqplot.pyplot as plt

# From local files
from app_variables import diagnoses_categories_map, diagnoses_categories_map_aggregates, data_url
from app_plotting import create_plot, empty_plot_with_title

# Global variable store of raw data
data_df_cached = None

# Fetch csv data from url and avoids additional http requests if cached data exists from previous call to function
async def get_web_data_async(url):
    global data_df_cached

    if data_df_cached is None:
        try:
            response = await pyodide.http.pyfetch(url)
            if response.ok:
                data = await response.string()
                data_df = pd.read_csv(StringIO(data))
                data_df_cached = data_df.copy() # Cache data as global variable
                return data_df
            else:
                raise Exception(f"Fetch Error with STATUS {response.status}. {response.status_text}")
        except:
            raise
    else:
        return data_df_cached
    
# Impute missing values with median of the entire column metric
def impute_median(df):
    from sklearn.impute import SimpleImputer
    
    imputer = SimpleImputer(strategy = "median")                 

    # Impute the remain small numbers (~25) of missing values using median of each column
    df_imputed = pd.DataFrame(imputer.fit_transform(df.iloc[:,1:]), # Without country column
                              columns = df.columns[1:])
    
    countries = df[['country']].reset_index(drop=True)
    
    df_imputed = pd.concat([countries,df_imputed], axis=1)
    
    X_train=df_imputed.drop('country',axis=1)
    
    return countries, X_train

# Get selected column names using diagnoses_categories_map_aggregates from app_variables.py
def get_columns_from_categories(categories, include_category_summary):
    columns_selected = []
    
    for category in categories:
        if include_category_summary:
            # Adds the category summary column
            summary_name = diagnoses_categories_map_aggregates.get(category)
            
            if summary_name:
                columns_selected.append(summary_name)
            
        columns_selected += diagnoses_categories_map[category] # extends the list
        
    return columns_selected

# Performs data processing steps to create a dataframe for training model
def data_processing(df, categories=list(diagnoses_categories_map.keys()), scaling = True, 
                    include_category_summary=False):
    
    df_temp = df.copy()

    # Get selected columns using category to columns map
    columns_selected = get_columns_from_categories(categories, include_category_summary)
    
    # Fills missing values in-place for each country with the latest (by year) value using .ffil()
    df_temp.update(df.groupby("country").ffill())

    # Takes the latest value by using the year 2021, and filters for only the diagnoses columns
    latest_diagnoses = df_temp[df_temp['year']==2021][["country"]+columns_selected]
    
    # Drop countries with many metrics missing - list derived from Pandas exploration not shown here
    to_drop_countries = ["United Kingdom","China (People's Republic of)","Estonia","India",
                         "Indonesia","Russia","South Africa","Brazil","Colombia"]
    latest_diagnoses_dropped = latest_diagnoses[-latest_diagnoses['country'].isin(to_drop_countries)]

    # Impute median for remaining missing values and create training dataframe
    countries, X_train = impute_median(latest_diagnoses_dropped)

    # Normalisation and scaling only required for Machine learning
    if scaling:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_train = pd.DataFrame(scaler.fit_transform(X_train), columns = X_train.columns)

    return countries, X_train

# Loads data and performs data processing and modelling to return a data required for plotting
async def train_and_get_plot(categories = [], num_groups = 3, on_select_callback = None):
    url = data_url
    
    # Load data from url
    # Asynchronous because may not be successful if http request fails e.g. timeout. 
    # Returns an empty figure if fails to fetch data rather than crashing the app
    try:
        oecd_df = await get_web_data_async(url)
    except Exception as e:
        print(e)
        return plt.figure(figsize=(6, 4), title = "Error getting data from URL")

    # Data Processing
    countries, training_data = data_processing(oecd_df, categories, scaling=True)

    # Create bqplot figure object
    fig = create_plot(training_data, countries, num_groups, on_select = on_select_callback)

    return fig

# Retrains and updates figure in-place
def train_and_update_plot(fig, categories = [], num_groups = 3, selected_countries=[]):
    global data_df_cached # Function should only be called after successful initial plot with data, so get data from cache

    # If data not available, don't do anything to the figure (should be displaying error message)
    if data_df_cached is None:
        return 

    # If no cateogires selected - empty the plot and show feedback as the plot title
    if len(categories)==0:
        empty_plot_with_title(title="Please Select At Least One Category...", fig=fig)
        return

    oecd_df = data_df_cached.copy()

    # Reprocess the data on selected categories
    countries, training_data = data_processing(oecd_df, categories, scaling=True)

    # Use create_plot again but pass the figure object and set param update_plot to True. This modifies the fig in-place
    create_plot(training_data, countries, num_groups, fig, selected_countries=selected_countries, update_plot=True)