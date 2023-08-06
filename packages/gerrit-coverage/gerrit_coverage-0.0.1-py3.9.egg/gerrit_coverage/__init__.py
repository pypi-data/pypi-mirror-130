from gerrit_coverage.gerrit_coverage import CommentMissingLinesBot

def main():
    import argparse
    parser = argparse.ArgumentParser(description='comment_missing_lines_bot: A bot, that thakes a coverage-run result, checks if any missing lines are in the current diff and commends them in Gerrit.')
    parser.add_argument('--gerrit_domain', type=str, help='The domain where gerrit is installed.', required=True)
    parser.add_argument('--project', type=str, help='The project-name on the gerrit server.', required=True)
    parser.add_argument('--username', type=str, help='The Gerrit-Username for the user that creates the comments.', required=True)
    parser.add_argument('--http_password', type=str, help='It is not the normal password of the user, but the one you generate in the settings.', required=True)
    parser.add_argument('--project_path', type=str, help='The path where the git project resides (a local path)', required=True)
    parser.add_argument('--change_id', type=str, help='The change_id for which the covered lines are analyzed. The current patchset of that change is used.', required=True)

    args = parser.parse_args()

    bot = CommentMissingLinesBot(
        args.gerrit_domain, args.project, 
        args.username, args.http_password)
    bot.review(args.project_path, args.change_id)



    # bot = CommentMissingLinesBot(
    #     'http://review.firmenessen.de', 'firmenessen', 
    #     't.deniffel', '6OJyEXkb3G8cvGfv6oy/+AqS7RIxqpQbZrm2GMVNzg')

    # bot.review('/home/tom/tmp/firmenessen', 'Iec7d8d43351d71215e6c155cc3cb0dbd10ce3214')
