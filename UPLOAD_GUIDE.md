# Publish this project on GitHub

First review `README.md`, the two written reports, and the source code. Confirm
that the attribution describes your work accurately. Publish only material you
are permitted to share. This folder excludes the copied simulation resources.

## Create the GitHub repository

Sign in to GitHub and choose **New repository**. Use:

- Name: `coffee-derivatives-pricing`
- Description: `Coffee futures and European option pricing with analytical models and Monte Carlo validation.`
- Visibility: Public, when you are ready to showcase it.

Leave the options to add a README, .gitignore, or license unchecked for this
initial import. The prepared project already has the first two. Choose a license
later only for material you have the right to license.

## Upload using Git

Open a terminal inside the prepared `coffee-derivatives-pricing` folder. Replace
`RyanWang1114` below with your actual GitHub username:

```shell
git init -b main
git add README.md requirements.txt .gitignore pricing.py compare_models.py tests docs UPLOAD_GUIDE.md
git diff --cached --stat
git diff --cached
git commit -m "Add coffee derivatives pricing case study"
git remote add origin https://github.com/RyanWang1114/coffee-derivatives-pricing.git
git push -u origin main
```

Review the staged diff before committing. Git may open a browser for sign-in.
If Git requests your identity, set your chosen author name and GitHub verified
email or GitHub-provided noreply email with repository-local `git config
user.name` and `git config user.email`, then repeat the commit.

This delivery folder has no Git repository initialized yet. If you initialize
one before following this guide, skip `git init`.

## Finish the portfolio presentation

In the repository's About settings, add topics such as `python`,
`quantitative-finance`, `derivatives`, `option-pricing`, and `monte-carlo`.
Pin the repository from your GitHub profile. Check that the README renders
properly and that the example instructions work after cloning.

For later edits, change the local files, run the tests, review `git diff`, commit
the specific changed files, and push. Avoid editing the same file simultaneously
in the GitHub website and locally; pull remote changes before further work.

Official reference:
https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github

