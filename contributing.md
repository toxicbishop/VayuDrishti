# Contributing to VayuDrishti

Thank you for your interest in contributing to **VayuDrishti**!

Contributions of all kinds are welcome, including bug fixes, new features, improvements to the machine-learning pipeline, frontend improvements, documentation, testing, and research-related work.

VayuDrishti combines software engineering, data processing, geospatial/satellite data, machine learning, and visualization. Contributions should therefore prioritize **correctness, reproducibility, maintainability, and clear documentation**.

## Table of Contents

- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Branch Naming](#branch-naming)
- [Commit Guidelines](#commit-guidelines)
- [Development Requirements](#development-requirements)
- [Research and Model Contributions](#research-and-model-contributions)
- [Data and Security Guidelines](#data-and-security-guidelines)
- [Pull Requests](#pull-requests)
- [Code Quality](#code-quality)
- [Code of Conduct](#code-of-conduct)
- [Questions and Discussions](#questions-and-discussions)

---

## Getting Started

Before contributing, make sure you have:

- Git installed
- Python installed
- Node.js and `pnpm` installed if working on the frontend
- The required project dependencies installed
- A local copy of the repository

Fork the repository and clone your fork:

```bash
git clone https://github.com/toxicbishop/VayuDrishti.git
cd VayuDrishti
````

Create a new branch before making changes:

```bash
git checkout -b feature/your-feature-name
```

Make your changes, test them locally, and push the branch to your fork:

```bash
git add .
git commit -m "describe your changes"
git push origin feature/your-feature-name
```

Then open a Pull Request against the main VayuDrishti repository.

---

## How to Contribute

Anyone is welcome to contribute to VayuDrishti.

You can contribute by:

* Forking the repository and submitting a Pull Request
* Fixing bugs
* Adding new features
* Improving the frontend
* Improving backend functionality
* Improving data-processing pipelines
* Adding or improving tests
* Improving documentation
* Improving machine-learning models
* Adding reproducible experiments
* Improving performance
* Reporting bugs
* Suggesting improvements

If you are unsure whether a change is appropriate, you can open an issue first and discuss the idea before implementing it.

---

## Branch Naming

There is no strict branch naming requirement, but descriptive branch names are encouraged.

Recommended formats include:

```text
feature/<name>
fix/<name>
docs/<name>
model/<name>
test/<name>
refactor/<name>
```

### Examples

```text
feature/air-quality-dashboard
feature/satellite-data-processing
fix/aqi-calculation
model/improve-pm25-prediction
docs/setup-guide
test/data-validation
```

Choose a name that makes it easy to understand what the branch is intended to change.

---

## Commit Guidelines

VayuDrishti does **not** require a specific commit-message convention.

However, commits should be reasonably clear and describe what was changed.

Good examples:

```text
add satellite data preprocessing
fix AQI calculation
improve dashboard responsiveness
add PM2.5 prediction model
update installation instructions
remove unused dependency
```

Avoid extremely vague commit messages such as:

```text
update
changes
stuff
final
final final
```

Try to keep commits logically organized so that changes are easier to understand and review.

---

## Development Requirements

Before submitting a Pull Request, make sure your changes work locally.

### Run Tests

```bash
make test
```

### Run Linting

```bash
make lint
```

### Frontend Changes

If you modify the frontend, also run:

```bash
pnpm build
```

Make sure the build completes successfully before submitting your Pull Request.

If your changes introduce new functionality, add or update tests where appropriate.

---

## Research and Model Contributions

VayuDrishti includes research and machine-learning components.

If you contribute a new model, algorithm, experiment, or data-processing method, document the work clearly enough that another contributor can understand and reproduce it.

Where applicable, include information about the following.

### Dataset

Document:

* Dataset name/source
* Data format
* Relevant features
* Collection period
* Geographic coverage
* Any preprocessing performed

Do **not** commit large raw datasets to the repository.

### Preprocessing

Explain important preprocessing steps such as:

* Data cleaning
* Missing-value handling
* Normalization
* Feature engineering
* Filtering
* Spatial transformations
* Temporal transformations

### Model or Algorithm

Document:

* Model or algorithm used
* Important parameters
* Input features
* Output
* Training procedure
* Relevant assumptions

### Evaluation

Where applicable, provide:

* Evaluation metrics
* Validation methodology
* Test results
* Comparison with relevant baselines
* Important limitations

### Reproducibility

Research contributions should include enough information for another developer or researcher to reproduce the result.

Avoid relying on:

* Undocumented local files
* Absolute paths
* Private datasets
* Machine-specific configuration
* Unavailable dependencies

---

## Data and Security Guidelines

Please keep the repository clean and secure.

### Do Not Commit Large Raw Datasets

Do not add large raw datasets directly to the repository.

Instead, document where the data can be obtained and provide instructions for preparing it locally when appropriate.

### Never Commit Secrets

Do **not** commit:

* API keys
* Passwords
* Access tokens
* Private keys
* `.env` files containing secrets
* Database credentials
* Cloud credentials
* Other sensitive configuration

For example, avoid committing:

```text
API_KEY=your-secret-key
```

Use environment variables or an appropriate local configuration mechanism instead.

If you accidentally expose a secret, revoke or rotate it immediately.

### Avoid Machine-Specific Paths

Do not hard-code paths such as:

```text
C:\Users\YourName\Desktop\project\data
```

or:

```text
/home/username/project/data
```

Use relative paths or configurable environment variables instead.

---

## Pull Requests

When submitting a Pull Request:

1. Make sure your branch contains only the changes relevant to the contribution.
2. Explain what you changed.
3. Explain why the change was needed.
4. Mention any important implementation details.
5. Include relevant testing information.
6. For frontend changes, include screenshots or other useful visual information when appropriate.
7. For research/model changes, explain the methodology and results.
8. Make sure existing functionality has not been unnecessarily broken.

A good Pull Request should allow someone unfamiliar with your changes to understand what was done and why.

### Example Pull Request Description

```text
## What changed?

Added a new satellite-data preprocessing pipeline for PM2.5
prediction.

## Why?

The previous pipeline required manual preprocessing and made
experiments difficult to reproduce.

## Changes

- Added automated preprocessing
- Added missing-value handling
- Added feature normalization
- Added tests for the preprocessing pipeline

## Testing

make test
make lint
```

---

## Code Quality

Contributions should aim to keep VayuDrishti:

* Readable
* Maintainable
* Reproducible
* Testable
* Secure
* Consistent with the existing project structure

Avoid unnecessary changes that are unrelated to your contribution.

If you are refactoring existing code, make sure the refactoring does not unintentionally change existing behavior.

---

## Code of Conduct

We want VayuDrishti to remain a welcoming and constructive project for everyone.

Contributors are expected to:

* Be respectful to other contributors.
* Communicate constructively.
* Focus discussions on the code, research, or technical problem rather than individuals.
* Accept constructive feedback.
* Avoid harassment, discrimination, personal attacks, or deliberately disruptive behavior.
* Give others an opportunity to explain their ideas and reasoning.
* Keep discussions relevant to the project.

### Unacceptable Behavior

The following are not acceptable:

* Harassment or personal attacks
* Threats or intimidation
* Discriminatory or hateful behavior
* Deliberate disruption of project discussions
* Sharing private information about others without permission
* Repeatedly ignoring reasonable project guidelines

Project maintainers may remove or close contributions that violate these expectations.

---

## Questions and Discussions

If you have a question about VayuDrishti, encounter a problem, or have an idea for improving the project, open an issue in the repository with enough information for others to understand the situation.

### Bug Reports

For bugs, include:

* What happened
* What you expected to happen
* Steps to reproduce the issue
* Relevant error messages
* Environment information when useful

### Feature Requests

For feature requests, explain:

* What you want to add or change
* Why it would be useful
* How you expect it to work

---

## Final Note

Every contribution matters.

Whether you are fixing a typo, improving the UI, optimizing a data pipeline, adding a test, or contributing a new machine-learning approach, thank you for taking the time to improve VayuDrishti.

**Happy contributing! 🌱**
