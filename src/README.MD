Command to Clean the GIT Workspace but Keep venv
bash
git clean -fdx --exclude="venv/"
Options Explanation:
-f: Force the clean operation.
-d: Remove untracked directories.
-x: Remove ignored and untracked files.
--exclude="venv/": Exclude the venv folder from the clean operation.

Configuring the Project for Proper Module Resolution

Mark backend as Sources Root:
Right-click the backend folder in the PyCharm Project View.
Select Mark Directory as > Sources Root.
This ensures that backend is treated as the starting point for resolving modules.

Add absolute path to the backend to PYTHONPATH:
Go to Run > Edit Configurations.
In your configuration, locate the Environment Variables section.
Add a new variable:
Name: PYTHONPATH
Value: /path/to/model_deploy/src/backend
Restart PyCharm