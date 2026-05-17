@Repository
public class CriteriaEventGeofeatureRepository
        implements EventGeofeatureRepository {

    @PersistenceContext
    private EntityManager entityManager;

    public List<EventGeofeatureDto> findEventsForMap(
            EventGeofeatureFilter filter) {

        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<EventGeofeatureDto> query =
                cb.createQuery(EventGeofeatureDto.class);
        Root<EventEntity> root = query.from(EventEntity.class);

        List<Predicate> predicates = new ArrayList<>();

        if (filter.getMinLon() != null && filter.getMaxLon() != null) {
            Expression<?> envelope = cb.function(
                    "ST_MakeEnvelope", Object.class,
                    cb.literal(filter.getMinLon()),
                    cb.literal(filter.getMinLat()),
                    cb.literal(filter.getMaxLon()),
                    cb.literal(filter.getMaxLat()),
                    cb.literal(4326));
            predicates.add(cb.isTrue(cb.function(
                    "ST_Intersects", Boolean.class,
                    root.get("epicenter"), envelope)));
        }

        if (filter.getMaxSeverity() != null) {
            predicates.add(cb.lessThanOrEqualTo(
                    root.get("severity").get("severityValue"),
                    filter.getMaxSeverity().getSeverityValue()));
        }

        predicates.add(cb.or(
                cb.isNull(root.get("expiresAt")),
                cb.greaterThan(root.get("expiresAt"),
                        LocalDateTime.now())));

        Expression<String> localizedTitle = cb.function(
                "jsonb_extract_path_text", String.class,
                root.get("title"), cb.literal(filter.getLang()));
        Expression<String> geoJson = cb.function(
                "ST_AsGeoJSON", String.class,
                root.get("epicenter"));

        query.select(cb.construct(EventGeofeatureDto.class,
                root.get("id"),
                localizedTitle,
                root.get("severity").get("severityValue"),
                geoJson));
        query.where(predicates.toArray(new Predicate[0]));

        return entityManager.createQuery(query).getResultList();
    }
}
