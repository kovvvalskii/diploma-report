@RestController
@RequestMapping("/api/v1/geoserver")
@CrossOrigin(origins = "*")
public class GeoServerController {

    private final Map<String, GeofeatureProvider<?, ?>> layerProviders;

    public GeoServerController(List<GeofeatureProvider<?, ?>> providers) {
        this.layerProviders = providers.stream().collect(
                Collectors.toMap(GeofeatureProvider::getLayerName, p -> p));
    }

    @PostMapping("/batch")
    public ResponseEntity<Map<String, GeoJsonFeatureCollection>>
            getFeaturesForMap(
                    @RequestBody BatchGeofeatureRequestDto request,
                    @RequestParam(defaultValue = "en") String lang) {

        if (!List.of("en", "ru").contains(lang)) {
            throw new BadRequestException(
                    "lang %s is not supported".formatted(lang));
        }
        Map<String, Object> common = new HashMap<>(request.getCommon());
        common.put("lang", lang);

        Map<String, GeoJsonFeatureCollection> result = new HashMap<>();
        for (var layer : request.getLayers().entrySet()) {
            var provider = layerProviders.get(layer.getKey());
            if (provider == null) {
                throw new BadRequestException(
                        "layer " + layer.getKey() + " not found");
            }
            var layerProps = new HashMap<>(common);
            layerProps.putAll(layer.getValue());
            result.put(layer.getKey(),
                    new GeoJsonFeatureCollection(
                            fetchFeatures(provider, layerProps)));
        }
        return ResponseEntity.ok(result);
    }

    private <D extends GeofeatureDto, F extends GeofeatureFilter>
            List<D> fetchFeatures(GeofeatureProvider<D, F> provider,
                                  Map<String, Object> props) {
        return provider.getGeofeatures(provider.buildFilter(props));
    }
}
