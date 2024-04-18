var map = L.map('map').setView([52, 19.0], 7);
var filtersList = []

L.tileLayer('https://tile-c.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    attribution: 'made by Wojciech Linowski'
}).addTo(map);

map.zoomControl.remove();

var overlay = L.DomUtil.create('div', 'overlay', map.getPane('overlayPane'));
overlay.style.position = 'absolute';
overlay.style.width = '100%';
overlay.style.height = '100%';
overlay.style.backgroundColor = 'rgba(207,178,156,0.6)'; // Semi-transparent white


var overlay2 = L.DomUtil.create('div', 'overlay2', map.getPane('overlayPane'));
overlay2.style.position = 'absolute';
overlay2.style.width = '1000vw !important';
overlay2.style.height = '1000vh !important';
overlay2.style.left = "-100 vw";
overlay2.style.top= "-100 vh";
overlay2.style.backgroundImage = 'url(/static/images/dots.svg")'; // Path to your semi-transparent tile image
overlay2.style.backgroundRepeat = 'repeat'; // This makes the image repeat across the space
overlay2.style.pointerEvents = 'none';

var currentZoom = null;
var currentLevel = 0;
var currentId = ["", "", "", ""];
var currentName = ["Lasy Polskie", "", "", ""];

function setRibbonName(name)
{
    document.getElementById("map-title-text").innerHTML = name;
}

function go_back()
{
    console.log("go back!");
    currentLevel -= 1;
    console.log(currentZoom);
    if(currentLevel < 0)
    {
        currentLevel = 0;
        console.log("cannot go back futher!")
        return;
    }
    else if(currentLevel == 0)
    {
        clearMap();
        map.setView([52, 19.0], 7);
        setRibbonName(currentName[0]);
        get("/get_rdlp", drawRDLP);
    }
    else if(currentLevel == 1)
    {
        clearMap();
        var z = map.getBoundsZoom(currentZoom);
        map.fitBounds(currentZoom, true);
        map.setZoom(z);
        setRibbonName(currentName[1]);
        get("/get_district_from_rdlp/" + currentId[0], drawDistrict);
    }
    else if(currentLevel == 2)
    {
        clearMap();
        var z = map.getBoundsZoom(currentZoom);
        map.fitBounds(currentZoom, true);
        map.setZoom(z);
        setRibbonName(currentName[2]);
        get("/get_forestry_from_district/" + currentId[0] + "/" +  + currentId[1], drawForestry);
    }
    else
    {
        console.log("too high level!")
    }



}

function get(url, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", url, true); // true for asynchronous
    xmlHttp.send(null);
}


function title(str) {
    if (str.length === 0) return str; // Handle empty string
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function displaySector(data)
{
    data = JSON.parse(data);
    console.log(data);

    let info = document.getElementById("info");
    info.style.display = "block";

    let table = document.getElementById("info-table").rows;

    let coords = "N " + data["coordinates"]["N"].toString().substring(0,10) + ",<br> E " + data["coordinates"]["E"].toString().substring(0,10)

    table[0].cells[1].innerHTML = title(data["rdlp"]);
    table[1].cells[1].innerHTML = title(data["district"]);
    table[2].cells[1].innerHTML = title(data["forestry"]);
    table[3].cells[1].innerHTML = coords;
    table[4].cells[1].innerHTML = data["id"];
    table[5].cells[1].innerHTML = data["address"];
    table[6].cells[1].innerHTML = data["silvicult"];
    table[7].cells[1].innerHTML = data["area_type"];
    table[8].cells[1].innerHTML = data["site_type"];
    table[9].cells[1].innerHTML = data["stand_structure"];
    table[10].cells[1].innerHTML = data["forest_function"];
    table[11].cells[1].innerHTML = data["spiecies"];
    table[12].cells[1].innerHTML = data["species_age"];
    table[13].cells[1].innerHTML = data["rotation_age"];
    table[14].cells[1].innerHTML = data["year"];



}

function drawSector(data)
{
    data = JSON.parse(data);

    console.log(data);

    var style =  {
        fillColor: '#e6c16c',
        weight: 2,
        opacity: 0.3,
        color: 'black',
        dashArray: '1',
        fillOpacity: 0.6
    };

    var tooltipStyle =
    {
        permanent: true,
        direction:"center",
        className: 'forest-tooltip'
    };


    for (const [key, value] of Object.entries(data))
    {


        for(let i = 0; i < value["geometry"].length; i++)
        {
            let save = value["geometry"][i][0];
            value["geometry"][i][0] = value["geometry"][i][1];
            value["geometry"][i][1] = save;
        }



        let polygon = L.polygon(value["geometry"], style).addTo(map);


        polygon.on('click', function(e)
        {
            //map.fitBounds(e.target.getBounds());
            //clearMap();
            //currentLevel = 3;
            console.log(value);
            get("/display_sector/"+value["address"].toString(), displaySector)
        });

        polygon.on('mouseover', function(e)
        {
            let layer = e.target;
            let newStyle = {};
            Object.assign(newStyle, style);
            newStyle.fillOpacity = 0.9;
            layer.setStyle(newStyle);

        });

        polygon.on('mouseout', function(e)
        {
            var layer = e.target;
            layer.setStyle(style);

        });

    }
}

function drawForestry(data)
{
    data = JSON.parse(data);

    console.log(data);

    var style =  {
        fillColor: '#e6c16c',
        weight: 2,
        opacity: 0.3,
        color: 'black',
        dashArray: '1',
        fillOpacity: 0.6
    };

    var tooltipStyle =
    {
        permanent: true,
        direction:"center",
        className: 'forest-tooltip'
    };


    for (const [key, value] of Object.entries(data))
    {


        for(let i = 0; i < value["geometry"].length; i++)
        {
            let save = value["geometry"][i][0];
            value["geometry"][i][0] = value["geometry"][i][1];
            value["geometry"][i][1] = save;
        }

        let name = value["name"];
        let html = '<svg class="curved-text" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n';
        html += '<path class="text-path" id="curve" fill="none" stroke="black" d="M73.2,148.6c4-6.1,65.5-96.8,178.6-95.6c111.3,1.2,170.8,90.3,175.1,97" />\n';
        html += '<text class="text-text" width="500" style="text-anchor: middle;">\n';
        html += '<textPath xlink:href="#curve" startOffset="50%">\n';
        html += name + '\n';
        html += '</textPath>\n';
        html += '</text>\n';
        html += '</svg>\n';

        let polygon = L.polygon(value["geometry"], style).addTo(map);
        polygon.bindTooltip(html, tooltipStyle);

        polygon.on('click', function(e)
        {
            map.fitBounds(e.target.getBounds());
            clearMap();
            currentLevel = 3;
            setRibbonName(value["name"]);
            currentName[3] = value["name"];
            currentId[0] = value["rdlp_id"].toString();
            currentId[1] = value["district_id"].toString();
            currentId[2] = value["forestry_id"].toString();
            get("/get_sector_from_forestry/"+value["rdlp_id"].toString()+"/"+value["district_id"].toString()+"/"+value["forestry_id"].toString(), drawSector)
        });

        polygon.on('mouseover', function(e)
        {
            let layer = e.target;
            let newStyle = {};
            Object.assign(newStyle, style);
            newStyle.fillOpacity = 0.9;
            layer.setStyle(newStyle);


            let tooltip =  e.target.getTooltip()._container;
            tooltip.classList.add('forest-tooltip-scaled');
        });

        polygon.on('mouseout', function(e)
        {
            var layer = e.target;
            layer.setStyle(style);

            let tooltip =  e.target.getTooltip()._container;
            tooltip.classList.remove('forest-tooltip-scaled');

        });

    }
}


function drawDistrict(data)
{
    data = JSON.parse(data);
    console.log(data)
    var style =  {
        fillColor: '#e6c16c',
        weight: 2,
        opacity: 0.3,
        color: 'black',
        dashArray: '1',
        fillOpacity: 0.6
    };

    var tooltipStyle =
    {
        permanent: true,
        direction:"center",
        className: 'forest-tooltip'
    };


    for (const [key, value] of Object.entries(data))
    {


        for(let i = 0; i < value["geometry"].length; i++)
        {
            let save = value["geometry"][i][0];
            value["geometry"][i][0] = value["geometry"][i][1];
            value["geometry"][i][1] = save;
        }

        let name = value["name"];
        let html = '<svg class="curved-text" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n';
        html += '<path class="text-path" id="curve" fill="none" stroke="black" d="M73.2,148.6c4-6.1,65.5-96.8,178.6-95.6c111.3,1.2,170.8,90.3,175.1,97" />\n';
        html += '<text class="text-text" width="500" style="text-anchor: middle;">\n';
        html += '<textPath xlink:href="#curve" startOffset="50%">\n';
        html += name + '\n';
        html += '</textPath>\n';
        html += '</text>\n';
        html += '</svg>\n';

        let polygon = L.polygon(value["geometry"], style).addTo(map);
        polygon.bindTooltip(html, tooltipStyle);

        polygon.on('click', function(e)
        {
            map.fitBounds(e.target.getBounds());
            clearMap();
            currentLevel = 2;
            setRibbonName(value["name"]);
            currentName[2] = value["name"];
            currentId[0] = value["rdlp_id"].toString();
            currentId[1] = value["district_id"].toString();
            get("/get_forestry_from_district/"+value["rdlp_id"].toString()+"/"+value["district_id"].toString(), drawForestry)
        });

        polygon.on('mouseover', function(e)
        {
            let layer = e.target;
            let newStyle = {};
            Object.assign(newStyle, style);
            newStyle.fillOpacity = 0.9;
            layer.setStyle(newStyle);


            let tooltip =  e.target.getTooltip()._container;
            tooltip.classList.add('forest-tooltip-scaled');
        });

        polygon.on('mouseout', function(e)
        {
            var layer = e.target;
            layer.setStyle(style);

            let tooltip =  e.target.getTooltip()._container;
            tooltip.classList.remove('forest-tooltip-scaled');

        });

    }
}

function drawRDLP(data)
{
    data = JSON.parse(data);

    var style =  {
        fillColor: '#e6c16c',
        weight: 2,
        opacity: 0.3,
        color: 'black',
        dashArray: '1',
        fillOpacity: 0.6
    };

    var tooltipStyle =
    {
        permanent: true,
        direction:"center",
        className: 'forest-tooltip'
    };


    for (const [key, value] of Object.entries(data))
    {


        for(let i = 0; i < value["geometry"].length; i++)
        {
            let save = value["geometry"][i][0];
            value["geometry"][i][0] = value["geometry"][i][1];
            value["geometry"][i][1] = save;
        }

        let name = value["name"];
        let html = '<svg class="curved-text" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n';
        html += '<path class="text-path" id="curve" fill="none" stroke="black" d="M73.2,148.6c4-6.1,65.5-96.8,178.6-95.6c111.3,1.2,170.8,90.3,175.1,97" />\n';
        html += '<text class="text-text" width="500" style="text-anchor: middle;">\n';
        html += '<textPath xlink:href="#curve" startOffset="50%">\n';
        html += name + '\n';
        html += '</textPath>\n';
        html += '</text>\n';
        html += '</svg>\n';

        let polygon = L.polygon(value["geometry"], style).addTo(map);
        polygon.bindTooltip(html, tooltipStyle);

        polygon.on('click', function(e)
        {
            currentZoom = e.target.getBounds();
            map.fitBounds(e.target.getBounds());
            clearMap();
            currentId[0] = value["id"].toString();
            currentLevel = 1;
            setRibbonName(value["name"]);
            currentName[1] = value["name"];
            get("/get_district_from_rdlp/"+value["id"].toString(), drawDistrict)
        });

        polygon.on('mouseover', function(e)
        {
            let layer = e.target;
            let newStyle = {};
            Object.assign(newStyle, style);
            newStyle.fillOpacity = 0.9;
            layer.setStyle(newStyle);


            let tooltip =  e.target.getTooltip()._container;
            tooltip.classList.add('forest-tooltip-scaled');
        });

        polygon.on('mouseout', function(e)
        {
            var layer = e.target;
            layer.setStyle(style);

            let tooltip =  e.target.getTooltip()._container;
            tooltip.classList.remove('forest-tooltip-scaled');

        });

    }


}

function clearMap() {
    for(i in map._layers) {
        if(map._layers[i]._path != undefined) {
            try {
                map.removeLayer(map._layers[i]);
            }
            catch(e) {
                console.log("problem with " + e + map._layers[i]);
            }
        }
    }
}


var filterState = false;

function toggleFilters()
{
    if(!filterState)
    {
        filterState = true;
        get("/get_filters", drawFilters);
    }
    else
    {
        filterState = false;
        document.getElementById("filters-panel").style.display = "none";
    }

}

function toggleGroup(element)
{

    if(element.dataset.state == "show")
    {
        let id = element.id.split('-')[0] + "-content";
        let content = document.getElementById(id);
        content.style.display = "none";
        element.dataset.state = "hide";
        let arrow = element.getElementsByClassName("groupExpand")[0];
        arrow.innerHTML = '▼';
    }
    else
    {
        let id = element.id.split('-')[0] + "-content";
        let content = document.getElementById(id);
        content.style.display = "block";
        element.dataset.state = "show";
        let arrow = element.getElementsByClassName("groupExpand")[0];
        arrow.innerHTML = '▲';

    }
}

function selectAll()
{
    console.log("all filters selected!");
    let checkboxes = document.getElementsByClassName("checkbox");
    for(let i = 0; i < checkboxes.length; i++)
    {
        checkboxes[i].checked = true;
    }
}

function deselectAll()
{
    console.log("all filters deselected!");
    let checkboxes = document.getElementsByClassName("checkbox");
    for(let i = 0; i < checkboxes.length; i++)
    {
        checkboxes[i].checked = false;
    }
}

function applyFilters()
{
    console.log("filters applied!");

    for(let i = 0; i < filtersList.length; i++)
    {
        console.log(filtersList[i]);
    }
}

function drawFilters(filters)
{
    filters = JSON.parse(filters);

    document.getElementById("filters-panel").style.display = "block";

    let box = document.createElement("div");
    box.id = 'filter-box';

    for (const [key, value] of Object.entries(filters))
    {
        let group = document.createElement('div');
        let groupRibbon = document.createElement('div');
        groupRibbon.id =  key + "-ribbon";
        groupRibbon.classList.add('filter-ribbon');
        groupRibbon.onclick = function() { toggleGroup(groupRibbon); };
        let groupName = document.createElement('p');
        groupName.classList.add('filter-group-title');

        let newKey = "";

        if(key == "species")
        {
            newKey = "gatunki";
        }
        else if(key == "site_types")
        {
            newKey = "typ siedliskowy";
        }
        else if(key == "silvicults")
        {
            newKey = "rodzaj lasu";
        }
        else if(key == "forest_functions")
        {
            newKey = "funkcja lasu";
        }
        else if(key == "area_types")
        {
            newKey = "rodzaj powierzchni";
        }

        groupName.innerHTML = newKey;

        let groupExpand = document.createElement('div');
        groupExpand.classList.add("groupExpand");
        groupExpand.innerHTML = "▼";


        groupRibbon.appendChild(groupName);
        groupRibbon.appendChild(groupExpand);
        group.appendChild(groupRibbon);

        let groupContent = document.createElement('div');
        groupContent.id =  key + "-content";
        groupContent.style.display = "none";

        for (const [entryKey, entryValue] of Object.entries(value))
        {

            let entry = document.createElement('div');

            let entryNameBox = document.createElement('div');
            entryNameBox.classList.add("entryNameBox");

            let entryName = document.createElement('span');
            entryName.innerHTML = entryValue + ": ";
            entryName.classList.add("entryName");

            if(entryValue.length > 28)
            {
                entryName.classList.add("entryNameAnimation");
            }


            let check = document.createElement("input");
            check.value = entryValue;
            check.type="checkbox";
            check.id=value;
            check.classList.add("checkbox");
            check.checked = true;
            filtersList.push(check);

            entryNameBox.appendChild(entryName);
            entry.appendChild(entryNameBox);
            entry.appendChild(check);
            groupContent.appendChild(entry);

        }

        group.appendChild(groupContent);

        box.appendChild(group);


    }

    if(document.getElementById("filters-box"))
    {
        document.getElementById("filters-box").innerHTML = "";
    }

    document.getElementById("filters-panel").appendChild(box);

}

get("/get_rdlp", drawRDLP);

document.querySelector('[title="A JavaScript library for interactive maps"]').style.display = "none";
