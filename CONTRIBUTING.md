# Contributing to MyGravatar

Thank you for your interest in contributing to **MyGravatar**!

We welcome contributions that improve clarity, test coverage, documentation, simulation fidelity, or the static GitHub Pages site, while keeping the project self-contained and honest about its scope.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).  
By participating, you are expected to uphold this code.  
Reports can be sent to the repository maintainer via GitHub (@AnticipatedD).

## How Can I Contribute?

### Reporting Bugs / Issues
- Search existing issues first.
- Open a new issue with a clear title and description.
- Include steps to reproduce, expected vs actual behavior, Python version, and OS.
- For the static site (https://anticipatedd.github.io/MyGravatar), note browser and any console errors.

### Suggesting Enhancements
- Open an issue describing the enhancement and why it fits a demonstration project.
- Keep suggestions aligned with the simulated, dependency-light nature of the toolkit.

### Pull Requests
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name` or `fix/issue-number-description`.
3. Make your changes.
4. Ensure the project still works:
   bash
   python -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   pytest --cov=. --cov-report=term-missing --cov-fail-under=60
   python vane_space_init.py

5. Follow the existing code style (clean, readable Python; no hardcoded secrets).
6. Update documentation (README.md, docstrings, or comments) if needed.
7. Commit with clear, conventional messages (e.g., feat: improve grounding strength validation, test: add edge case for soft mode, docs: clarify simulation scope).
8. Push to your fork and open a Pull Request against the main branch.
9. Link any related issues in the PR description.
10. The GitHub Actions CI must pass (tests + coverage ≥ 60%).

**Development Setup**  
Exact steps from the README: 
```bash
git clone https://github.com/AnticipatedD/MyGravatar.git
cd VANE-SPACE-SLA
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
pytest --cov=. --cov-report=term
python vane_space_init.py
```
---

Key files: 
- `vane_space_init.py` – main entry / simulation orchestration
- `strict_prompt_builder.py` – strict / moderate / soft grounding logic
- `tests/ – pytest suite`
- `.github/workflows/ci.yml` – continuous integration
- Static HTML/JS/CSS for the GitHub Pages website

**Style & Quality Guidelines** 
- Prefer clear, readable Python over clever one-liners.
- Use environment variables via `.env / python-dotenv` (never commit real secrets).
- Maintain or improve the existing test coverage.
- Keep the project fully runnable offline (no real external API calls).
- Do not introduce production claims or remove the “demonstration / simulated” language from the README.
- For HTML/JS changes on the Pages site, keep the design consistent and accessible.


**Commit Messages**
Use conventional commits where possible:
- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation only
- `test`: adding or updating tests
- `chore`: tooling, CI, dependencies
- `refactor`: code change that neither fixes a bug nor adds a feature

**License** 
By contributing, you agree that your contributions will be licensed under the same MIT License (LICENSE) that covers the project. 

**Questions?** 
Open an issue or reach out via the repository. Thank you for helping keep VANE-SPACE-SLA accurate, useful, and honest as a demonstration toolkit! 

---
**Author / Maintainer** 
MD ABUL HOSSAIN 
Repository: https://github.com/AnticipatedD/MyGravatar
Live Telemetry Monitor: https://anticipatedd.github.io/MyGravatar

### Alerts
Alerts, also sometimes known as callouts or admonitions, are a Markdown extension based on the blockquote syntax that you can use to emphasize critical information. On GitHub, they are displayed with distinctive colors and icons to indicate the significance of the content.

Use alerts only when they are crucial for user success and limit them to one or two per article to prevent overloading the reader. Additionally, you should avoid placing alerts consecutively. Alerts cannot be nested within other elements.

To add an alert, use a special blockquote line specifying the alert type, followed by the alert information in a standard blockquote. Five types of alerts are available:

> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.
