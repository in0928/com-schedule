//get tableId
function getTableId() {
    var tableId = "people-list-full";
    var path_name = window.location.pathname;
    switch(path_name){
        case "/ba":
            tableId = "ba-list-full";
            break;
        case "/dreams":
            tableId = "dream-list-full";
            break;
        case "/places":
            tableId = "place-list-full";
            break;
        case "/schedule":
            tableId = "com-schedule";
            break;
        default:
            tableId = "people-list-full"
    };
    return tableId;
    };

var tableId = getTableId();

document.addEventListener("DOMContentLoaded", fill_dropdown(tableId));
document.querySelector("#table-search").oninput = applySearch;

function applySearch() {
    search(tableId);
    alternate(tableId);
}


function fill_dropdown(tableId) {
//    get col names
    var table = document.getElementById(tableId);
    var thead = table.getElementsByTagName("thead")[0];
    var th = thead.getElementsByTagName("th");
//    get dropdown menu
    var dropdown = document.getElementById("search-by-col-name");
    dropdown.options.length = 0;

    for(i = 0; i < th.length; i++) {
        opt = document.createElement("option")
        opt.appendChild(document.createTextNode(th[i].innerText))
        opt.value = th[i].innerText;
        dropdown.appendChild(opt)
    }
}


function search(tableId) {
    // Declare variables
    var input, filter, table, tr, td, th, i, txtValue;
    input = document.getElementById("table-search");
    filter = input.value.toUpperCase();
    table = document.getElementById(tableId);
    tr = table.getElementsByTagName("tr");
//    for the fixed first column
    var thead = table.getElementsByTagName("thead")[0];
    var th = thead.getElementsByTagName("th");
    var dropdown = document.getElementById("search-by-col-name");
    var index = dropdown.selectedIndex;
//    Because the first col is frozen
    if (tableId == "ba-list-full" || tableId == "people-list-full"){
            index = index - 1;
    }
             console.log(index);


    // Loop through all table rows, and hide those who don't match the search query
    for (i = 1; i < tr.length; i++) {
//        Special case

        if(dropdown.value === "名前"){　
           th = tr[i].getElementsByTagName("th")[0];
           txtValue = th.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
              } else {
                tr[i].style.display = "none";
                }
        }
        else {
            td = tr[i].getElementsByTagName("td")[index];
            if (td) {
                txtValue = td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
}


function alternate(tableId){
  if(document.getElementsByTagName){
    var table = document.getElementById(tableId)
    var rows = table.getElementsByTagName("tr");
    var filteredRows = []
    for(i = 0; i < rows.length; i++) {
        if(rows[i].style.display != 'none'){
            filteredRows.push(rows[i])
        }
    }
    console.log(filteredRows)
    for(i = 1; i < filteredRows.length; i++){
  //manipulate rows
      if(i % 2 == 0){
        filteredRows[i].style.background = "whitesmoke";
      }else {
        filteredRows[i].style.background = "white";
      }
    }
  }
}

