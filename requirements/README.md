# For developers

#### Prerequisites
pip-tools package must be installed in current virtual env. This can be done:

- by installing dev requirements (for new virtualenvs): `pip install -r requirements/requirements.dev.txt`
- by installing package only (specific version: check version in requirements.dev.txt): `pip install pip-tools==7.5.3`
 
 
### Adding or updating top-level dependencies

1. Update required ".in" files with new top-level dependencies / dependency versions
2. Run `bash requirements/compile.sh` to update ".txt" files
3. See ".txt" files for changes. Added / updated top-level packages and their dependencies are added here
4. Commit changed ".in" and ".txt" files to git