function renderMarrowfenMap() {
    const mapElement = document.getElementById("marrowfen-map");
    if (!mapElement) return; // Avoid crashing on pages without the map

    const map = L.map("marrowfen-map", {
        crs: L.CRS.Simple,
        minZoom: 0.25,
        maxZoom: 4,
        zoom: 1,
    });

    const bounds = [
        [0, 0],
        [1344, 1357],
    ];
    const image = L.imageOverlay("/assets/img/marrowfen-map.png", bounds).addTo(map);
    map.fitBounds(bounds);

    const markers = [
        { coords: [700, 505], label: "Stone and Copper ore mine" },
        { coords: [725, 710], label: "Clay and reeds" },
        { coords: [635, 550], label: "Bridge #1 - Log 1 and 2" },
        { coords: [600, 575], label: "The Starry Crossing tavern - Log 1 and 2" },
    ];

    markers.forEach((m) => {
        L.marker(m.coords).addTo(map).bindPopup(m.label);
    });

    // Optional: add click debug tool
    map.on("click", function (e) {
        const { lat, lng } = e.latlng;
        console.log(`🧭 Clicked at Y: ${lat.toFixed(0)}, X: ${lng.toFixed(0)}`);
    });
}

// Hook into MkDocs Material's navigation events
if (typeof document$ !== "undefined") {
    document$.subscribe(() => renderMarrowfenMap());
} else {
    // Fallback for non-MkDocs
    if (document.readyState !== "loading") {
        renderMarrowfenMap();
    } else {
        document.addEventListener("DOMContentLoaded", renderMarrowfenMap);
    }
}
