const EARTH_R_KM = 6371;

const toRad = (deg) => (deg * Math.PI) / 180;

export function haversineKm(a, b) {
    const dLat = toRad(b.latitude - a.latitude);
    const dLon = toRad(b.longitude - a.longitude);
    const lat1 = toRad(a.latitude);
    const lat2 = toRad(b.latitude);
    const x = Math.sin(dLat / 2) ** 2 +
        Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) ** 2;
    return EARTH_R_KM * 2 * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x));
}

export function pointToSegmentKm(p, a, b) {
    const dx = b.longitude - a.longitude;
    const dy = b.latitude - a.latitude;
    const lenSq = dx * dx + dy * dy;
    let t = lenSq === 0
        ? 0
        : ((p.longitude - a.longitude) * dx +
           (p.latitude  - a.latitude)  * dy) / lenSq;
    t = Math.max(0, Math.min(1, t));
    return haversineKm(p, {
        longitude: a.longitude + t * dx,
        latitude:  a.latitude  + t * dy,
    });
}

export function pointToRouteKm(point, stops) {
    if (!stops || stops.length === 0) return Infinity;
    if (stops.length === 1) return haversineKm(point, stops[0]);
    let min = Infinity;
    for (let i = 0; i < stops.length - 1; i += 1) {
        const d = pointToSegmentKm(point, stops[i], stops[i + 1]);
        if (d < min) min = d;
    }
    return min;
}
