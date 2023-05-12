# Python modules
from shiny import render, reactive, ui
from shinywidgets import register_widget, reactive_read
import bqplot.pyplot as plt

# From local files
from app_data_processing import train_and_get_plot, train_and_update_plot
from app_table_generation import create_table
from app_plotting import plot_highlight_circle, toggle_plot_labels
from app_ui import left_categories, right_categories
from app_info_text import info_html

def server(input, output, session):
    # Variable store of figure object - allows updating in place (more efficient and allows animation) rather than re-rendering the plot
    fig_object = None
    selected_countries = reactive.Value([])
    country_to_color = reactive.Value({})
    
    # Selects and removes countries when clicking on the plot
    def on_select_callback(*args):
        clicked_name = args[1].get("data").get("name")
        selected_copy = selected_countries.get()[:]

        # Add or remove the clicked country from selected countries
        if clicked_name in selected_copy:
            selected_copy.remove(clicked_name)
        else:
            selected_copy.append(clicked_name)
            
        selected_countries.set(selected_copy)
    
    @reactive.Effect
    @reactive.event(input.diagnosis_categories_left, input.diagnosis_categories_right, input.num_groups)
    # Creates the plot if does not exist, otherwise updates it in-place in response to changes in selection by user
    async def create_and_update_plot():
        nonlocal fig_object
        
        # Reactive inputs
        categories_selected = input.diagnosis_categories_left() + input.diagnosis_categories_right()
        num_groups = input.num_groups()

        # Creates fig object - await because on first call it will fetch the raw data using http request
        if fig_object is None:
            fig = await train_and_get_plot(categories = categories_selected, num_groups = num_groups, on_select_callback = on_select_callback)
            # Register figure to be shown and store figure in variable for in-place modification
            register_widget("plot_output", fig)
            fig_object = fig 
        else:
            # Use stored figure object to update plot in-place
            train_and_update_plot(fig_object, categories = categories_selected, selected_countries=selected_countries.get(), num_groups = num_groups)

        # Retrieve the color mapping from fig and update country_to_color
        colors_list = fig_object.marks[0].colors
        countries = fig_object.marks[0].names
        country_to_color.set(dict(zip(countries,colors_list)))

    @reactive.Effect
    @reactive.event(selected_countries)
    # Toggles the highlight circle on/off for selected countries
    def update_plot_selections():
        nonlocal fig_object
        selected = selected_countries.get()

        plot_highlight_circle(fig_object, selected_countries=selected)

    @reactive.Effect
    @reactive.event(input.select_all_button)
    def select_all_checkboxes():
        ui.update_checkbox_group("diagnosis_categories_left", selected = left_categories)
        ui.update_checkbox_group("diagnosis_categories_right", selected = right_categories)

    @reactive.Effect
    @reactive.event(input.select_none_button)
    def select_no_checkboxes():
        ui.update_checkbox_group("diagnosis_categories_left", selected = [])
        ui.update_checkbox_group("diagnosis_categories_right", selected = [])

    @reactive.Effect
    @reactive.event(input.open_categories_button, input.close_categories_button)
    def toggle_show_categories():
        ui.update_switch("show_categories", value= not input.show_categories())

    @reactive.Effect
    @reactive.event(input.toggle_labels_button)
    def toggle_labels():
        toggle_plot_labels(fig_object)

    @reactive.Effect
    @reactive.event(input.clear_country_selection_button)
    def clear_country_selection():
        selected_countries.set([])     

    @output
    @render.table(index=True)
    @reactive.event(input.diagnosis_categories_left,input.diagnosis_categories_right,selected_countries,country_to_color)
    def table_output():
        # Reactive inputs
        categories_selected = input.diagnosis_categories_left() + input.diagnosis_categories_right()
        countries = selected_countries.get()
        rows_hidden_state = input.row_indexes_to_hide()

        # Table is a Styler object from pandas
        table = create_table(categories = categories_selected, 
                             countries_selected = countries, 
                             country_to_color = country_to_color.get(),
                             rows_hidden_state = rows_hidden_state)
        return table

    @reactive.Effect
    @reactive.event(input.show_info_button)
    def open_info_modal():
        modal = ui.modal(ui.HTML(info_html),
                         title="Instructions and Methodoloy",
                        easy_close=True,
                        )
        ui.modal_show(modal)