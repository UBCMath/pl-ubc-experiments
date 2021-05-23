# SCIE 001 PrairieLearn Repo

Instructors and TAs use this repo to coordinate homework assignments over multiple instances of the course.

Please file issues or pull requests to improve the homework questions.

### :gear: Development Workflow

#### Getting Started
* Clone this repo to your local machine.
* Follow instructions in [here](https://prairielearn.readthedocs.io/en/latest/installing/) to set up a local instance of PrairieLearn.

#### Making Changes
1. Create a new branch off of the `master` branch. If you are fixing an issue, name it with the number of the issue you'll be working on (e.g. `ISSUE-101`). If you are adding a new lesson, name it the same thing as the created question's QID (e.g. `FreeBodyDiagramsQ1`).
2. Make changes and commit your changes to your branch with [Conventional Commit Messages](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13).
3. Once you're satisfied with your changes, open a new pull request for your branch with the corresponding issue number or QID and description as the PR title (e.g. ISSUE-61: Fix Colin's code) 
4. Fill out [PR template](https://learning.github.ubc.ca/PrairieLearn/pl-ubc-scie001/blob/master/.github/pr_template.md) when you post a PR.
5. Resolve all merge conflicts as needed.
6. Assign at least one member to review your PR and be open and available to address feedback.
7. Comment the PR link in the issue ticket, if your PR addresses an issue.
8. After approval from the team member, confirm the PR and merge your branch into the `master` branch.
9. Confirm that your changes are reflected in the `master` branch, and then delete your branch.

## Notes

  * The current live instance of this course pulls from the master
    branch (but this does not currently happen automatically).

  * During term, all non-trivial changes should go through merge
    requests.

## Caution

  * **Student data should not be present in this repo.**

  * **Students should not be discussed here.**