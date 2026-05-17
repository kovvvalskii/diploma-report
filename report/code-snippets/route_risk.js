const candidates = useMemo(() => {
    const realPoints = asPoints(events, i18n.language);
    const recentPoints = asPoints(eventsList, i18n.language);
    const fallback = listDemoMode || (!realPoints.length
                                       && !recentPoints.length)
        ? asPoints(MOCK_RECENT_EVENTS, i18n.language)
        : [];
    const map = new Map();
    [...realPoints, ...recentPoints, ...fallback].forEach((p) => {
        if (!p.longitude || !p.latitude || !p.id) return;
        map.set(p.id, p);
    });
    return [...map.values()];
}, [events, eventsList, listDemoMode, i18n.language]);

const intersecting = useMemo(() => {
    if (!stops.length) return [];
    return candidates
        .map((event) => ({
            ...event,
            distanceKm: pointToRouteKm(
                { longitude: event.longitude,
                  latitude: event.latitude },
                stops),
        }))
        .filter((e) => e.distanceKm <= bufferKm)
        .sort((a, b) => a.distanceKm - b.distanceKm)
        .slice(0, 8);
}, [candidates, stops, bufferKm]);
