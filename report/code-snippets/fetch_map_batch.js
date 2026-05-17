import { API_BASE_URL } from '../config/apiConfig.js';
import { requestJson } from './httpClient.js';

export async function fetchMapBatch({ bounds, lang, maxSeverity,
                                       includeTravellerRoutes }) {
    const body = {
        common: {
            minLon: bounds._sw.lng,
            minLat: bounds._sw.lat,
            maxLon: bounds._ne.lng,
            maxLat: bounds._ne.lat,
        },
        layers: {
            events: { maxSeverity },
        },
    };

    if (includeTravellerRoutes) {
        body.layers.travellerRoutes = {};
    }

    return requestJson(`${API_BASE_URL}/geoserver/batch?lang=${lang}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept-Language': lang,
        },
        body: JSON.stringify(body),
    });
}
