// Script adds interactivity to the created <table> element that displays the Pandas dataframe.
// Difficulty is that HTML elements are repeated created/removed/modified due to shiny reactivity. 
// Therefore cannot statically execute javascript, need to dynamically execute code so that functionality remains when table is recreated. 
// Uses MutationObserver to achieve this. https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver

// The function below was taken from Yong Wang (https://stackoverflow.com/questions/5525071/how-to-wait-until-an-element-exists)
// Waits for a selected element to load and resolves Promise by returning the element
function wait_for_element(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                resolve(document.querySelector(selector));
                observer.disconnect();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
};

// Toggles the hidden checkbox to talk enable persistent state of which rows are collapsed between table renders
function toggle_hidden_checkbox(row){
    
    // Gets list of classes in the row - should contain a class like "row123" where 123 is the row number (0-indexed)
    const row_classlist = Array.from(row.firstElementChild.classList);
    // Regex match "row" + any digit
    const row_class = row_classlist.find(class_name => class_name.match(/row\d/gm)) ;
    // Only keep the number portion to get the row index
    const row_index = row_class.slice(3) ;

    // Get the input checkbox element with value corresponding to the row index
    const checkbox = document.querySelector(`input[name='row_indexes_to_hide'][value='${row_index}']`)
    
    if (checkbox.checked === true || checkbox.checked === "checked") {
        checkbox.checked = false;
    } else {
        checkbox.checked = true;
    };

    // Dispatch event so that backend can pick it up and update its state
    const event = new CustomEvent('change', {bubbles: true});
    checkbox.dispatchEvent(event);
};

// Togles all show/hide of all rows under a clickable summary row 
function toggle_show_hide_rows(row) {
    // Get the next table row <tr> element
    let next_row = row.nextElementSibling;

    // Stops running when next row is another summary row or no more rows
    while (next_row && next_row.querySelector("td.normal-row")) {
        // Get child cells (<td> and <th>) of the row
        const child_cells = Array.from(next_row.children)

        // Toggles collapse by setting display of table cell elements (<td> and <th>) to none or table-cell
        child_cells.forEach(child=>{
            // Gets the computed display (pandas generated styles do not appear in HTML "style" attribute)
            computed_display = window.getComputedStyle(child, null).display;
            if (computed_display === "none") {
                child.style.display = "table-cell";
            } else {
                child.style.display = "none";
            };
        })

        // Update a checkbox group to update state and allow backend to read it
        toggle_hidden_checkbox(next_row)

        // Iterate
        next_row = next_row.nextElementSibling;
    };
};

// Adds onclick function to each summary row
function make_table_clickable(table) {
    // Use "has" CSS pseudo-class to select the table row (tr) that contains a cell (td) with class "summary-row"
    // Table cells (td) were classed during table styling in app_data_processing.py
    const summary_rows = table.querySelectorAll("tr:has(td.summary-row)"); // List of <tr> elements to be made clickable

    // Add onclick for each row
    summary_rows.forEach((row)=>{
        row.onclick = ()=>{toggle_show_hide_rows(row)}
    });
    
};

// Observes the table div for reactive changes. If table exists, make its summary rows clickable
async function observe_table() {    
    // Retrieve the <div> corresponding to the shiny ui element: ui.output_table("table_output"). 
    // This is not available on page start - so need to listen for it using wait_for_element
    const target_node = await wait_for_element("#table_output"); 

    // Callback function to execute when mutations are observed
    const callback = (mutationList, observer) => {
      for (const mutation of mutationList) {
        if (mutation.type === "childList") {
            table_element = target_node.querySelector('.interactive-table'); // "interactive-table" class was added during table styling in app_data_processing.py
            
            if (table_element) {
                make_table_clickable(table_element);
            }
        }
      }
    };
    
    // Create an observer instance linked to the callback function
    const observer = new MutationObserver(callback);
    
    // Indefinitely observe the target node for mutations - in this case changes to child nodes (i.e. the <table> HTML elemnt)
    observer.observe(target_node, { childList: true });
};

observe_table();
