from publish.jekyll import jekyll_post
from publish.mailjet import mailjet_digest, mailjet_warning
from publish.printout import printout
from publish.twitter import tweet

PUBLISH_TYPES = {
    'printout': printout,
    'mailjet_digest': mailjet_digest,
    'mailjet_warning': mailjet_warning,
    'jekyll': jekyll_post,
    'twitter': tweet,
}
