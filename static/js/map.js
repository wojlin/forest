var map = L.map('map').setView([52, 19.0], 7);


L.tileLayer('https://tile-c.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);



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
            //clearMap();
            //get("/get_forestry_from_district/"+value["id"].toString(), drawDistrict)
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
            map.fitBounds(e.target.getBounds());
            clearMap();
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


get("/get_rdlp", drawRDLP);

