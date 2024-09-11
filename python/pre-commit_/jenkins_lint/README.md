This is a script for linting job files written for [Jenkins](https://www.jenkins.io/)
using the [built-in validator](https://www.jenkins.io/doc/book/pipeline/development/#linter). The syntax of pipeline
files is frequently obtuse and I got sick of the commit-push-wait cycle to work through the simple problems with my jobs.

I built this for use as a [pre-commit](https://pre-commit.com/) hook, but it can also be used as a standalone script.

`pre-commit` workflow of this tool looks like:

```
$ vim Jenkinsfile secondJob.jenkinsfile  # making changes to two jobs
$ git add Jenkinsfile secondJob.jenkinsfile
$ git commit -m "Add amazing new feature to CI"  # triggers pre-commit if `pre-commit install` has been run
 
Lint Jenkinsfile(s)......................................................Failed
- hook id: jenkins-lint
- duration: 0.48s
- exit code: 1

Jenkins lint OK     for 'Jenkinsfile'
Jenkins lint failed for file 'secondJob.jenkinsfile':
  > Errors encountered validating Jenkinsfile:
  > WorkflowScript: 133: unexpected token: IS @ line 133, column 6.
  >    THIS IS A SYNTAX ERROR
  >         ^
```
