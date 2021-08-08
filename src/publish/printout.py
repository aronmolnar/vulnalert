from utils.statics import TYPE_WARNING, TYPE_EXPLOIT, TYPE_FEATURED, TYPE_VULNERABILITY


def printout(articles, dry_run=False):
    # dry_run is ignored. printout can always be called
    for article_type in [TYPE_WARNING, TYPE_VULNERABILITY, TYPE_EXPLOIT, TYPE_FEATURED]:
        if any([a['article_type'] == article_type for a in articles]):
            print(f"# {article_type.capitalize()}")
        else:
            # This article type is not present and therefore needs not headline
            continue

        for article in articles:
            if article['article_type'] == article_type:
                print(f'"{article["title"]}": {article["url"]}')

        print('')  # newline
