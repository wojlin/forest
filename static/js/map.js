var map = L.map('map').setView([52, 19.0], 7);


L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
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




function drawRDLP(data)
{
    data = JSON.parse(data);

    var style =  {
        fillColor: '#eba85b',
        weight: 2,
        opacity: 0.3,
        color: 'black',
        dashArray: '1',
        fillOpacity: 0.6
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
        polygon.bindTooltip(value["name"], {permanent: true, direction:"center", className: 'forest-tooltip' });

        polygon.on('click', function(e)
        {
            map.fitBounds(e.target.getBounds());
        });

        polygon.on('mouseover', function(e)
        {
            var layer = e.target;
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

get("/get_rdlp", drawRDLP)

