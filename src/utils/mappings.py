from publish.mailgun import mailgun_digest, mailgun_warning
from publish.mailjet import mailjet_digest, mailjet_warning
from publish.printout import printout

PUBLISH_TYPES = {
    'printout': printout,
    'mailgun_digest': mailgun_digest,
    'mailgun_warning': mailgun_warning,
    'mailjet_digest': mailjet_digest,
    'mailjet_warning': mailjet_warning,
}
