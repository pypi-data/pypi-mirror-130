from missing_diff_lines import missing_diff_lines
from gerrit_coverage.condense import condense
from gerrit_robo import Review

from missing_diff_lines import missing_diff_lines
from gerrit_coverage.condense import condense
from gerrit_robo import Review, Gerrit
import subprocess

class ReviewBot:
    
    def __init__(self, gerrit_url, gerrit_project, username, http_credentials):
        self.gerrit_url = gerrit_url
        self.gerrit_project = gerrit_project
        self.username = username
        self.http_credentials = http_credentials
        self.gerrit = Gerrit(gerrit_url, gerrit_project).with_auth(username, http_credentials)
        

    def review(self, path, change_id):
        self._bring_repo_up_to_date(path, change_id)
        review = self._do_review(path)
        self._send_review(change_id, review)

    def _bring_repo_up_to_date(self, path, change_id):
        output = self.__run(
            f'git-review -d {change_id}',
            cwd=path
        )
        return output

    def _do_review(self, path):
        raise NotImplementedError

    def _send_review(self, change_id, review):
        self.gerrit.send_review(change_id, review)

    def __run(self, command, cwd):
        return subprocess.check_output(command.split(), cwd=cwd).decode()


class CommentMissingLinesBot(ReviewBot):

    def _do_review(self, path):
        lines = missing_diff_lines(path)
        condensed_lines = condense(lines)
        review = self._condensed_lines_to_review(condensed_lines)
        return review

    def _condensed_lines_to_review(self, lines):
        review = Review('test-coverage found some untested files')
        for filename, line_range in lines:
            message = 'These lines are'
            if line_range[0] == line_range[1]:
                message = 'This line is'
            message += ' not covered by any test'
            review.comment(filename, line_range, message)
        return review


def condensed_lines_to_review(lines):
    review = Review('test-coverage found some untested files')
    for filename, line_range in lines:
        message = 'These lines are'
        if line_range[0] == line_range[1]:
            message = 'This line is'
        message += ' not covered by any test'
        review.comment(filename, line_range)

# lines = missing_diff_lines()
# condensed_lines = condense(lines)
# review = condensed_lines_to_review(condensed_lines)