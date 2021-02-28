## Usage

To install this hook download the main script, move it to .git/hooks/pre-push and make it executable:

```
curl -fsSL https://raw.githubusercontent.com/igin/circleci-push-warning/main/verify_circle_ci_status.py --output .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

## Development

Use the .devcontainer configuration to develop in vscode. To run the tests  inside the container run:

```
task test
```

To run the pre-push hook against a defined project create a `.env` file and add at least the following two variables:

```
PRE_PUSH_CIRCLE_CI_TOKEN=%YOUR_PERSONAL_CIRCLE_CI_TOKEN%
GIT_URL=%GIT_URL_OF_YOUR_CIRCLE_CI_BASED_PROJECT%
```