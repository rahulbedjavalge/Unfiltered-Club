# Contributing to Unfiltered Club

👋 First off, thanks for taking the time to contribute!

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/yourusername/unfiltered/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/yourusername/unfiltered/issues/new).

### Suggesting Enhancements

- First, read the documentation and make sure the enhancement isn't already available.
- Open a new issue with the "enhancement" label.
- Describe your idea in detail.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code follows the existing style.
5. Issue that pull request!

## Development Process

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your credentials
5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Style Guide

- Use Black for Python code formatting
- Follow PEP 8 guidelines
- Write descriptive commit messages
- Comment your code when necessary

## Questions?

Feel free to open an issue with the "question" label if you need help!
