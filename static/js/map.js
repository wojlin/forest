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
    console.log(data);
    for (const [key, value] of Object.entries(data))
    {
        console.log(value)
        let polygon = L.polygon(value["geometry"]).addTo(map);
        polygon.bindTooltip(value["name"], {permanent: true, direction:"center"});
    }


}

get("/get_rdlp", drawRDLP)

