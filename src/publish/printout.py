from utils.helper import articles_to_message


def printout(articles, dry_run=False):
    # dry_run is ignored. printout can always be called
    print(articles_to_message(articles, add_footer=True))
