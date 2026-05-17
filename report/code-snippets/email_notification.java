@Service
@RequiredArgsConstructor
public class EmailNotificationService {
    private final JavaMailSender mailSender;
    private final TemplateEngine templateEngine;

    public void sendAlert(String to, EventEntity event, String locale) {
        Context context = new Context();
        context.setVariable("event", event);
        context.setVariable("locale", locale);

        String body = templateEngine.process("risk-alert", context);
        String title = event.getTitle()
                .getOrDefault(locale, event.getTitle().get("en"));

        MimeMessage message = mailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message,
                MimeMessageHelper.MULTIPART_MODE_NO,
                StandardCharsets.UTF_8.name());
        helper.setTo(to);
        helper.setSubject("Security Alert: " + title);
        helper.setText(body, true);

        mailSender.send(message);
    }
}
