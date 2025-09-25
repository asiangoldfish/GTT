# Contributing to The YAGI Project

## How to write commit messages?
While there are many commit conventions out there and I have previously had many different commit standards within this project, the following standards should be followed:

1. Leave a blank line between the subject and the body.
This helps git log and git rebase work nicely and allows for smooth generation of release notes.
2. Try to keep the subject line below 72 characters, ideally 50.
3. Prefer to not capitalize the subject line.
4. Do not end the subject line with a period.
5. Use the imperative mood in the subject line (e.g., `bug: fix particles not spawning`).
6. Wrap the commit body at 80 characters.
7. Use semantic line feeds to separate different ideas, improving readability.
8. Be concise but thorough: If significant alternative solutions were available, explain why they were discarded.
9. Reference related discussions or issues: If the commit refers to a topic discussed on the project forum or fixes a regression test, provide the link. If it fixes a compiler error, include a minimal verbatim message of the compiler error. If the commit closes an issue, use the [GitHub issue closing keywords](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

The title of a commit message should start with one of the following tags:
| Commit Type | Title                    | Description                                                                                                 |
|:-----------:|--------------------------|-------------------------------------------------------------------------------------------------------------|
|   `feat`    | Features                 | A new feature                                                                                               |
|    `bug`    | Bug Fixes                | A bug fix                                                                                                   |
|   `docs`    | Documentation            | Documentation only changes. This may also include comments/docstrings                                       |
|   `style`   | Styles                   | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)      |
| `refactor`  | Code Refactoring         | A code change that neither fixes a bug nor adds a feature                                                   |
|   `test`    | Tests                    | Adding missing tests or correcting existing tests                                                           |
|   `chore`   | Chores                   | Other changes that don't modify src or test files                                                           |
|  `revert`   | Reverts                  | Reverts a previous commit                                                                                   |

The guidelines are inspired by those found at [SystoleOS/guix-systole](https://github.com/SystoleOS/guix-systole/blob/main/CONTRIBUTING.md), [pvdlg/conventional-changelog-metahub](https://github.com/pvdlg/conventional-changelog-metahub?tab=readme-ov-file), and Chris Beam's [How to Write a Git Commit Message](https://cbea.ms/git-commit/) post.