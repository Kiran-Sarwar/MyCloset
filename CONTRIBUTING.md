# Contributing to MyCloset

Thank you for your interest in contributing to MyCloset! 🎉

MyCloset is an open-source digital wardrobe application built with Python and Flask. Contributions of all kinds are welcome, including bug fixes, improvements, documentation, testing, and new features.

## Getting Started

### 1. Fork the Repository

Fork the MyCloset repository to your own GitHub account.

### 2. Clone Your Fork

Clone your fork to your local machine:

    git clone <your-fork-url>
    cd MyCloset

### 3. Create a Branch

Create a separate branch for your contribution:

    git checkout -b feature/your-feature-name

For bug fixes, you can use:

    git checkout -b fix/your-bug-name

Avoid making changes directly on the `main` branch.

## Running MyCloset

From the project root, run:

    python src/app.py

Then open the local Flask address shown in your terminal.

## Running Tests

Run the test suite with:

    python -m unittest discover tests

Please make sure all existing tests pass before submitting a pull request.

## Project Structure

    MyCloset/
    ├── docs/                  # Project documentation
    ├── src/
    │   ├── app.py             # Flask application
    │   ├── clothing_item.py   # Clothing item model
    │   ├── main.py            # Command-line entry point
    │   ├── wardrobe_manager.py # Wardrobe management logic
    │   ├── wardrobe.txt       # Persistent wardrobe data
    │   ├── static/             # CSS and other static files
    │   └── templates/          # Flask HTML templates
    ├── tests/                  # Automated tests
    ├── .gitignore
    └── CONTRIBUTING.md

## Finding Something to Work On

Check the repository's **Issues** section for available tasks.

Issues labeled:

- `good first issue` — suitable for beginners
- `enhancement` — improvements or new functionality
- `bug` — something that needs fixing
- `documentation` — documentation-related work

If you are interested in working on an issue, comment on it before starting when possible so other contributors know that it is being worked on.

## Making Changes

Keep contributions focused on the issue you are addressing.

When making changes:

- Follow the existing project structure.
- Keep code readable and understandable.
- Avoid unnecessary changes to unrelated files.
- Add or update tests when appropriate.
- Make sure existing functionality continues to work.

## Commit Guidelines

Write clear and meaningful commit messages.

For example:

    Add empty wardrobe state

or:

    Fix clothing item validation

Avoid vague messages such as:

    changes

or:

    stuff

## Pull Requests

Before opening a pull request:

1. Make sure your branch contains only the changes related to your contribution.
2. Run the test suite.
3. Make sure the application still runs correctly.
4. Push your branch to your fork.
5. Open a pull request against the `main` branch.

In your pull request description, explain:

- What you changed
- Why you changed it
- Which issue it addresses
- How you tested the changes

If your pull request fixes an issue, reference it using:

    Closes #1

## Code of Conduct

Please be respectful and constructive when interacting with other contributors.

Different approaches and opinions are welcome. Feedback should focus on improving the project rather than criticizing individuals.

## Questions and Suggestions

If you are unsure about something, open an issue or start a discussion before making a large change.

Thank you for helping improve MyCloset! 💙