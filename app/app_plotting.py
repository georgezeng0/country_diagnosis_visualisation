# Python modules
from sklearn.manifold import SpectralEmbedding
from sklearn.cluster import AgglomerativeClustering
import bqplot.pyplot as plt
from bqplot import Tooltip

# Integer group to color mapping
colors_map = {
    0:'#669900', # green
    1:'#cb0b0a', # red
    2:'#6ab6dc', # blue
    3:'#9b9c9b', # grey
    4:'#ff9900', # yellow
    5:'#cc3399', # pink
    6:'#3a0ca3', # purple
}

# Figure Default Styling
animation_speed = 2000 #ms

# Main plotting function that can either create a new figure or update one (using the "fig" and "update_plot" parameters)
def create_plot(X_train, countries, num_groups, fig = None, update_plot=False, selected_countries = [], on_select = None):

    global animation_speed
    
    # Create reduced dimensions for 2D plotting
    X_reduced = SpectralEmbedding(n_components=2, #2 axes
                                   n_neighbors=12,
                                   affinity = "nearest_neighbors",
                                   random_state=42)\
                                   .fit_transform(X_train)

    # Clustering to generate interger labels
    clustering = AgglomerativeClustering(linkage="average", n_clusters=num_groups)
    clustering.fit(X_reduced)

    # Get label colors
    labels_to_color = [colors_map[label] for label in clustering.labels_]

    # Get axis coordinates
    x_axis = X_reduced[:, 0]
    y_axis = X_reduced[:, 1]

    # Create new figure if update_plot is False
    if update_plot==False:
        fig= plt.figure(figsize=(6, 6),animation_duration=animation_speed)

        # Tooltip - hover for name
        tooltip = Tooltip(fields=["name"], formats=[""])

        # Axes
        axes_options = {
            "x":{"label":"Reduced Dimension X","tick_style":{"display":"none"}},
            "y":{"label":"Reduced Dimension Y","tick_style":{"display":"none"}}
        }

        # Scatterplot
        scatterplot = plt.scatter(x_axis, y_axis, 
                    colors=labels_to_color,
                    names=countries,
                    display_names=True,
                    apply_clip=False,
                    tooltip=tooltip,
                    axes_options=axes_options
                    )

        # Register click callback that updates Reactive value in the server
        scatterplot.on_element_click(on_select)

        # Scatterplot - only showing the stroke as a ring highliting selected points
        highlights = plt.scatter(
            x =[],
            y=[],
            default_size=200,
            fill=False,
            stroke="black",
            axes_options=axes_options
        )
        
        return fig

    # Update the plot in-place if update_plot is True
    else:
        if not fig:
            return # Do nothing if no figure object passed
            
        # Figure object passed as fig and the plt.scatter object within "marks" attribute. 
        scatterplot = fig.marks[0]
        highlights = fig.marks[1]
        
        num_points = len(scatterplot.x)

        # Update plot within context manager hold_sync() for simultaneous updating
        with fig.hold_sync():
            # New coordinates after reprocessing and retraining the data
            scatterplot.x = x_axis
            scatterplot.y = y_axis
            
            # New cluster labels and colors
            scatterplot.colors=labels_to_color
            
            # Reset styling
            fig.title=""
            scatterplot.opacities = [1]*num_points
            highlights.opacities = [1]*num_points
            scatterplot.display_names = True
            
            # Update highlight circle positions
            plot_highlight_circle(fig, selected_countries)

# Plots a highlight circle around selected country
def plot_highlight_circle(fig, selected_countries=[]):
    global animation_speed

    # Figure object passed as fig and the plt.scatter object within "marks" attribute. 
    scatterplot = fig.marks[0]
    highlights = fig.marks[1]

    # Index positions in the scatterplot of selected countries
    indexes = [index for index in range(len(scatterplot.x)) 
               if scatterplot.names[index] in selected_countries]

    # Build updated positions
    x_positions, y_positions = [],[]
    for index in indexes:
        x_positions.append(scatterplot.x[index])
        y_positions.append(scatterplot.y[index])

    # Update the plot in-place, within context manager hold_sync() for simultaneous updating.
    # No animation when updating highlights on/off
    fig.animation_duration=0
    
    with fig.hold_sync():
        highlights.x=x_positions
        highlights.y=y_positions
        
    fig.animation_duration=animation_speed

# Toggles display of labels on/off
def toggle_plot_labels(fig):
    scatterplot = fig.marks[0]

    scatterplot.display_names = not scatterplot.display_names
    
        
# Changes a figure in-place to empty plot, and display an error message as the plot title
def empty_plot_with_title(title="Something Went Wrong :(", fig = None):
    if not fig:
        return

    global animation_speed
        
    scatterplot = fig.marks[0]
    highlights = fig.marks[1]

    num_points = len(scatterplot.x)

    # Update the plot in-place, within context manager hold_sync() for simultaneous updating
    # Do not animate the changes
    fig.animation_duration=0
    
    with fig.hold_sync():
        fig.title=title
        scatterplot.opacities = [0]*num_points # Hide current points
        highlights.opacities = [0]*num_points # Hide current highlights
        scatterplot.display_names = False

    fig.animation_duration=animation_speed    