import re
import smtplib
import dns.resolver
from email_validator import validate_email, EmailNotValidError

class EmailValidator:
    @staticmethod
    def is_valid_syntax(email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None

    @staticmethod
    def get_mx_record(domain):
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            mx_records = [str(rdata.exchange).rstrip('.') for rdata in answers]
            return mx_records
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout) as e:
            print(f"Failed to get MX record for domain {domain}: {e}")
            return None

    @staticmethod
    def verify_email_via_smtp(email):
        domain = email.split('@')[1]
        mx_records = EmailValidator.get_mx_record(domain)
        if not mx_records:
            return False

        for mx_record in mx_records:
            try:
                server = smtplib.SMTP(mx_record, timeout=10)
                server.set_debuglevel(0)
                server.helo()
                server.mail('test@example.com')
                code, message = server.rcpt(email)
                server.quit()
                if code == 250:
                    return True
            except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError, smtplib.SMTPHeloError, smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused, smtplib.SMTPDataError) as e:
                print(f"SMTP verification failed for {email} at {mx_record}: {e}")
                continue

        return False

    def validate_and_verify_email(self, email):
        try:
            validation = validate_email(email, check_deliverability=True)
            email = validation.email
        except EmailNotValidError as e:
            return False, str(e)

        # SMTP check
        if not self.verify_email_via_smtp(email):
            return False, "Email failed SMTP verification"

        return True, "Email is valid and can receive messages"
