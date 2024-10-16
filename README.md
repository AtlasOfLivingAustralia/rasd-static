# RASD static site and assets

Welcome! This project contains the infrastructure, code and the deployment pipeline to launch and develop the RASD static site and automated user pool backups.

- [Static Page README](cicd/static-page/README.md)
- [Backups README](cicd/backups/README.md)

## Environments
There are 2 environments: testing, and production. the CICD framework also allows for development and staging environments, these are not currently used in this project. The environment is determined by the branch.

|git branch|environment|
|--|--|
|main|production|
|main|staging ( not used ) |
|testing|testing|
|feature* (e.g. feature/issue-121-new-logo) |development ( not used )|

The production environment runs in our production AWS account and is available on https://rasd.org.au/. Testing runs in the testing account and is available on https://testing.rasd.org.au/

## Configuration
All configuration for the project is handled in the `config.ini` file. The file format is of a standard ini file with different sections corresponding to the different environments. there is a [default] section that includes values common to all environments such as the code repo details. Default values can be overridden in an environment section

## Git branching and deployment
The branching model for this project is very similar to [gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
The `main` branch is a faithful representation of what is running in production, the `testing` branch represents what is deployed to the testing environment. Both of these branches are protected and can only be altered through PRs. 
The `main` and `testing` branches are CICD enabled with auto deployment, any commits to these will result in a deployment to the corresponding environment

## Development workflow
The `main` and `testing` branches are protected and cant be committed to directly. To begin development on a feature or enhancement:
- Create a branch off `main` that includes a short description of the feature e.g. `feature/update-footer`
- Make all your changes and commit them to your branch. Test locally.
- Once it's ready for deployment create a PR to merge your branch into `testing` Include at least one reviewer. It can be left up to the PR author if they want to wait for an approval, at the very least the reviewer receives a notification that we are getting ready for a testing deploy.
- Once the PR is merged it will be automatically deployed to the `testing` environment. Delete the feature branch
- Do any required UAT testing on the testing environment
- When UAT is passed create a PR to merge `testing` into `main` including at least one reviewer. Again it can be left up to the author if they want to wait for an approval
- When the PR is merged the changed will be automatically deployed to production


## Rollback
To rollback to any previous revision go to CodePipeline and after selecting "Release Change" choose the commit to release. [Detailed instructions here](https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-trigger-source-overrides.html#pipelines-trigger-source-overrides-console)
