# Python modules
from shiny import ui
from shinywidgets import output_widget

# From local files
from app_variables import diagnoses_categories_map

# Split the list of categories in two for UI purposes
categories = list(diagnoses_categories_map.keys())
split_point = len(categories) // 2
left_categories = categories[:split_point]
right_categories = categories[split_point:]

# App UI element
# Styling is achieved through a mix of in-line CSS, bootstrap class names and external CSS
# This is because not all shiny ui components allow setting style attributes and/or classes
app_ui = ui.page_fluid(
    # Container CSS style
    {
        "style": "margin-top: 20px; margin-bottom: 20px; \
        padding-top: 20px; \
        padding-bottom: 20px; \
        border-radius: 30px; \
        background-color: white; \
        max-width: 1300px"
    },
    
    # CSS Style sheet - to style elements unable to be modified in shiny
    ui.tags.head(
        ui.tags.link({"rel": "stylesheet", "type": "text/css", "href": "style.css"}),
        ui.HTML('<link rel="preconnect" href="https://fonts.googleapis.com">\
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\
                <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">')
    ),
    
    # Javascript
    ui.tags.script({"src": "table_interactivity.js"}),
    
    # Checkbox selection group - show/hide on button press
    ui.panel_conditional(
        "input.show_categories", # Using the hidden switch input
        ui.tags.h4(
            "Hospital Discharge Diagnosis Category Selection", class_="text-center mt-2"
        ),
        # Two columns of checkboxes
        ui.div(
            ui.input_checkbox_group(
                "diagnosis_categories_left",
                " ",
                choices=left_categories,
                selected=left_categories,
                width="50%",
            ),
            ui.input_checkbox_group(
                "diagnosis_categories_right",
                " ",
                choices=right_categories,
                selected=right_categories,
                width="50%",
            ),
            {"style": "display: flex"},
        ),
        # Diagnosis Selection buttons
        ui.div(
            ui.input_action_button(
                "select_all_button", 
                "Select All", 
                width="200px", 
                class_="btn-primary"
            ),
            ui.input_action_button(
                "select_none_button",
                "Remove Selections",
                width="200px",
                class_="btn-danger",
            ),
            class_="d-flex w-100 justify-content-around align-items-center mb-3",
        ),
        {"style": "border-radius: 25px; background: lightgrey; padding: 20px"},
    ),
    
    # Plot options container
    ui.div(
        # Number of groups slider
        ui.div(
            ui.input_slider(
                "num_groups", "Number of Clusters", min=1, max=7, value=3, step=1
            ),
            class_="d-flex justify-content-center text-center",
        ),
        # Toggle category selector panel button
        ui.div(
            ui.panel_conditional(
                "!input.show_categories",
                ui.input_action_button(
                    "open_categories_button",
                    "Categories",
                    icon=ui.img({"src": "down-arrow.svg", "style": "width:20px"}),
                    class_="btn-outline-dark",
                ),
            ),
            ui.panel_conditional(
                "input.show_categories",
                ui.input_action_button(
                    "close_categories_button",
                    "Categories",
                    icon=ui.img({"src": "up-arrow.svg", "style": "width:20px"}),
                    class_="btn-outline-dark",
                ),
            ),
            class_="d-flex justify-content-center mb-1",
        ),
        # Label toggle and clear country selection buttons
        ui.div(
            ui.input_action_button(
                "toggle_labels_button",
                "Toggle Labels",
                class_="btn-primary ",
                width="200px",
            ),
            ui.input_action_button(
                "clear_country_selection_button",
                "Clear Selected Countries",
                class_="btn-outline-secondary ms-1",
                width="200px",
            ),
            class_="d-flex justify-content-center align-items-center mb-2",
        ),
        class_="d-xs-column d-md-flex justify-content-md-around justify-content-center align-items-center w-100 mb-2",
    ),
    
    # Place title in html for responsive wrapping of text
    ui.tags.h4(
        "Visualising the Clustering of Countries Based on Similarity of Hospital Discharge Diagnoses Using Unsupervised Machine Learning",
        class_="text-center mb-0",
    ),
    
    # Plot output
    output_widget("plot_output"),

    ui.div(
        "To view more details about a country including numerical data - click on any of the points above to toggle selection.",
        {"style":"border-radius: 10px; background-color: #bfbfbf; text-align: center; padding: 5px; margin: 10px 20px"}
    ),
    
    # Output table
    ui.div(
        ui.output_table("table_output"),
        class_="d-flex justify-content-center"
    ),

    # Hidden Checkboxes - used to pass state of collapsed table rows from frontend to backend
    ui.div(
        ui.input_checkbox_group(
            "row_indexes_to_hide",
            "This should be hidden",
            [str(x) for x in list(range(148))],  # 0-147 as string
        ),
        {"style": "display: none"},
    ),

    # Hidden switch to show categories - used to pass state between frontend and backend
    ui.div(
        ui.input_switch("show_categories", "This should be hidden", value=False),
        {"style": "display: none"},
    ),

    # Footer
    ui.tags.footer(
        ui.div(
            ui.input_action_button(
                "show_info_button",
                ui.img({"src": "info.svg", "style": "width:40px"}),
                width="40px",
            ),
        class_="d-flex justify-content-center"
        ),
        ui.div("Data Source: OECD Health Care Utilisation Dataset ",
               ui.tags.a("(Link)", 
                         href="https://stats.oecd.org/index.aspx?DataSetCode=HEALTH_proc",
                        target="_blank"),
              {"style":"text-align:center; color: grey"}),
        {"style":"border-top: 1px solid grey; margin-top: 20px"}
    )
)
