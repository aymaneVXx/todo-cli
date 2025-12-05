# Automate execution of static code analysis with pre-commit hooks

This section demonstrates how static code analysis is automatically executed
before each commit using **pre-commit**, **Ruff**, and **Mypy**.

## 🔧 1. Installation of pre-commit

Pre-commit is installed as a development dependency:

```bash
poetry add -D pre-commit
```
then the Git hook is activated: 
```bash
poetry run pre-commit install
```
This creates the file .git/hooks/pre-commit which runs automatically at each commit.

## 🔧 2. Configuratio file

The configuration is located at the root of the repository in: .pre-commit-config.yaml 
Link : https://github.com/aymaneVXx/todo-cli/blob/main/.pre-commit-config.yaml

# Explanation:

- repo: local → uses the tools already installed via Poetry
- ruff hook → runs static linting
- mypy hook → runs type checking
- pass_filenames: false → ensures pre-commit does not append filenames (avoids Mypy duplicate module errors)

## 🔧 3. How to run the hooks

Manually on all files: 
```bash
poetry run pre-commit run --all-files
```
Automatically before every commit:
```bash
git commit -m "Your message"
```
If Ruff or Mypy find issues,
the commit is blocked until the issues are fixed — this ensures code quality.
