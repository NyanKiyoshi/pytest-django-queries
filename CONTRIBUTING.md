# Contribution Guide
1. To contribute, you can fork us!
1. But please be on one of the latest master versions.
1. Always put and commit your change sets into a new and meaningful branch in your fork.
1. Update the changelog file with the changes you made. Otherwise,
   unless your contribution is minor, it won’t get accepted.
1. You can run `pre-commit` inside your changes to check if they respect our code style.
1. Your contributions will get reviewed and will receive comments, remarks and suggestion.
   Please respect them, discuss them and be happy! The open source is great!
1. It may take time, days or even weeks before you get a review from us. But don’t worry,
   we won’t forget about it, it just mean it is in a backlog because we are too busy
   for now.
1. You will get reviews from bots (CIs) that will succeed or fail. Mostly from travis-ci
   and codecov. Please be careful about them, they are important checks that we get your
   contribution denied as long as those checks are not passing.
1. Travis-ci is there to check that your changes work (tests and linters). If travis fails,
   it means something is wrong with your changes. Look at the logs, it will tell you
   what’s going on!
1. Codecov is there to report the test coverage of your changes. We have a strict 100%
   coverage, meaning that all the code is covered by automatic tests. Please test
   all your changes and test them hastily, don’t test just for the sake of testing
   and to get a proper coverage... it’s wrong. We want the tests to prevent any error and
   any potential breaking from changes!
1. Finally, make sure you are using the latest version of the dependencies and that
   you have read our documentations.
