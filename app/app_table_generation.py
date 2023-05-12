# Python modules
import pandas as pd
import numpy as np

# From local files
from app_data_processing import data_processing, get_columns_from_categories
import app_data_processing
from app_variables import diagnoses_categories_map_aggregates

styled_table_cached = None

# Builds a dataframe with classes names to apply to each "td" table cell element
def get_table_cell_classes(df, aggregate_index_names):
    classes = df.transform(lambda row: 
                           ["summary-row"]*len(row) 
                           if row.name in aggregate_index_names 
                           else ["normal-row"]*len(row), 
                           axis=1)
    return pd.DataFrame(classes, index=df.index, columns=df.columns)

# Created a styled table from raw data with default styling
def initialise_table(df):
    oecd_df = df.copy()

    # Process the data - keeping summary columns. 
    # No need for scaling
    countries, numeric_data = data_processing(oecd_df, 
                                              scaling=False, 
                                              include_category_summary=True,
                                              ) 

    # Re-shape the table and indexes
    table = pd.concat([countries,numeric_data], axis=1)    
    table = table.set_index('country')
    table.index.name = None
    table = table.T    

    # List of names which are the summary/aggregate columns 
    aggregate_index_names = list(diagnoses_categories_map_aggregates.values())+\
        ["Diseases of the ear and mastoid process_Per 100 000 population", 
         "Congenital malformations, deformations and chromosomal abnormalities_Per 100 000 population"]

    # General styling to the whole table
    styles_table = [
        {'selector': 'thead', 'props': 'border-bottom: 2px solid black; text-align: center'},
        {'selector': 'td', 'props': 'width: 200px'},
        {'selector': 'table', 'props': 'border-spacing: 5px;'},
        {'selector': 'th', 'props': 'padding: 6px'},
        {'selector': 'td', 'props': 'text-align: center'},
    ]

    # Row specific styling, adding hover styles
    summary_row_styles = [{'selector': 'tr:hover td', 'props': 'background-color: #d9fff6 !important; cursor: pointer'},
                    {'selector': 'tr:hover th', 'props': 'background-color: #d9fff6 !important; cursor: pointer;'},
                    {'selector': 'tr td', 'props': 'background-color: #78f4ff;'},
                    {'selector': 'td','props': 'border-bottom: 1px solid grey;'},
                    {'selector': 'th','props': 'border-bottom: 1px solid grey; min_width: 150px; width: 250px'}]

    other_row_styles = [{'selector': 'tr:hover td', 'props': 'background-color: #dbdbdb !important;'},
                    {'selector': 'tr:hover th', 'props': 'background-color: #dbdbdb !important;'},
                    ]

    styles_rows = {
        row_name : summary_row_styles
            if row_name in aggregate_index_names else
            other_row_styles            
        for row_name in table.index
    }

    # Apply styling
    styled = table.style\
        .format(precision=1, thousands=",", decimal=".")\
        .format_index(lambda index_name: index_name.replace("_"," "))\
        .set_table_styles(styles_table)\
        .set_table_styles(styles_rows, axis=1, overwrite=False)\
        .apply_index(lambda names: np.where(names.isin(aggregate_index_names), "background-color: #78f4ff;", ""))\
        .set_sticky(axis = 1)\
        .set_td_classes(get_table_cell_classes(table, aggregate_index_names))\
        .set_table_attributes("class='interactive-table'") # Allows JavaScript selection

    return styled

def create_table(categories, countries_selected, country_to_color, rows_hidden_state):
    global styled_table_cached 
    
    data_df_cached = app_data_processing.data_df_cached

    # If data not available or no countries/categories selected, don't do anything
    if data_df_cached is None or len(categories)==0 or len(countries_selected)==0:
        return

    styled = styled_table_cached

    # For the display table, only need to process the underlying data once
    # Because the underlying numbers do not change only what to show (i.e. the style)
    if styled is None:
        styled = initialise_table(data_df_cached)
        styled_table_cached = styled # update the cached table

    # Update the styled table depending on country and category selections:
    # Update header colors
    styles_columns = {
            country: [{'selector': '.col_heading',
                       'props': f'background: linear-gradient(0deg,{country_to_color[country]} 0%, rgba(255,255,255,1) 30%)'}]
            for country in countries_selected
        }

    # Hide columns and rows depending on selection
    all_cols = list(styled.columns)
    all_rows = list(styled.index)
    cols_to_hide = [col for col in all_cols if col not in countries_selected]
    rows_to_hide = [row 
                    for row in all_rows
                    if row not in get_columns_from_categories(categories,include_category_summary=True)
                   ]

    # The state of which row is collapsed is saved in a hidden ui checkbox component. 
    # Sets display of the table cell (<td> or <th>) of the relevant row (<tr>)
    # Note: "display: none" on tr fails
    rows_to_collapse = {
        all_rows[int(index)] : [{'selector': 'tr td', 'props': 'display: none'},
                                {'selector': 'tr th', 'props': 'display: none'}]
        for index in rows_hidden_state
    }

    # Apply/update styling in response to reactive inputs.
    styled\
        .hide(cols_to_hide, axis = 1)\
        .hide(rows_to_hide, axis = 0)\
        .set_table_styles(styles_columns, overwrite=False)\
        .set_table_styles(rows_to_collapse, axis =1, overwrite=False)\

    return styled
