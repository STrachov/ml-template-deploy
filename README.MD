Command to Clean the Workspace but Keep venv
bash

git clean -fdx --exclude="venv/"

Options Explanation:

-f: Force the clean operation.

-d: Remove untracked directories.

-x: Remove ignored and untracked files.

--exclude="venv/": Exclude the venv folder from the clean operation.