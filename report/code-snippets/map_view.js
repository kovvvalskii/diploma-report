export default function MapView() {
    const dispatch = useDispatch();
    const mapRef = useRef(null);
    const { i18n } = useTranslation();

    const { viewState, tileProvider, projection, isPlacingStops } =
        useSelector((state) => state.map);
    const { data: layerData, activeLayers, filter } =
        useSelector((state) => state.layers);
    const { routeGeoJson, stops } = useSelector((state) => state.travel);
    const { selectedEvent } = useSelector((state) => state.events);

    const loadDataForCurrentBounds = useCallback(() => {
        if (mapRef.current) {
            const bounds = mapRef.current.getMap().getBounds();
            dispatch(fetchLayerData({ bounds, lang: i18n.language }));
        }
    }, [dispatch, i18n.language]);

    const onMapClick = useCallback((event) => {
        const { features, lngLat } = event;
        if (isPlacingStops) {
            dispatch(addStop({
                longitude: lngLat.lng,
                latitude: lngLat.lat,
            }));
            return;
        }
        const clicked = features?.find(
            (f) => f.layer.id === 'events-layer');
        if (clicked) {
            dispatch(setSelectedEvent({
                longitude: lngLat.lng,
                latitude: lngLat.lat,
                properties: clicked.properties,
            }));
            dispatch(openEventDetails());
        }
    }, [dispatch, isPlacingStops]);

    return (
        <Map ref={mapRef} {...viewState}
             mapStyle={TILE_PROVIDERS[tileProvider]}
             projection={projection}
             interactiveLayerIds={['events-layer']}
             onMove={(e) => dispatch(setViewState(e.viewState))}
             onMoveEnd={loadDataForCurrentBounds}
             onClick={onMapClick}
             onLoad={loadDataForCurrentBounds}
             cursor={isPlacingStops ? 'crosshair' : 'default'}>
            {activeLayers.includes('events') && layerData.events && (
                <Source id="events-source" type="geojson"
                        data={layerData.events}>
                    <Layer {...eventsHaloStyle} />
                    <Layer {...eventsLayerStyle} />
                </Source>
            )}
            {selectedEvent && <EventPopup
                selectedEvent={selectedEvent} />}
        </Map>
    );
}
