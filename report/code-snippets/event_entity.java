@Entity
@Table(name = "event")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class EventEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "source_id")
    private SourceEntity source;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "type_id")
    private EventTypeEntity type;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "title", columnDefinition = "jsonb", nullable = false)
    private Map<String, String> title;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "description", columnDefinition = "jsonb")
    private Map<String, String> description;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "severity_id")
    private EventSeverityEntity severity;

    @Column(columnDefinition = "geometry(Point,4326)")
    private Point epicenter;

    @Column(columnDefinition = "geometry(Polygon,4326)")
    private Polygon impactArea;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "expires_at")
    private LocalDateTime expiresAt;

    @OneToMany(mappedBy = "event",
               cascade = CascadeType.ALL,
               orphanRemoval = true)
    @Builder.Default
    private List<MentionEntity> mentions = new ArrayList<>();
}
