# Release Guide and Checklist

## Choosing the right version number
### The Release Type
Following the [PEP 440](https://www.python.org/dev/peps/pep-0440/#pre-releases), if you
want to do a pre-release, you will choose between:

    Pre releases:
        X.YaN   # Alpha release
        X.YbN   # Beta release
        X.YrcN  # Release Candidate
        X.Y     # Final release

    Post releases:
        X.Y.postN     # Post-release
        X.YaN.postM   # Post-release of an alpha release
        X.YbN.postM   # Post-release of a beta release
        X.YrcN.postM  # Post-release of a release candidate

    Development releases:
        X.Y.devN         # Developmental release
        X.YaN.devM       # Developmental release of an alpha release
        X.YbN.devM       # Developmental release of a beta release
        X.YrcN.devM      # Developmental release of a release candidate
        X.Y.postN.devM   # Developmental release of a post-release

### The Release Version Number
1. If your changes are fixing a big and changing in no way the behavior of any component,
you will bump the patch version number (`X.Y.PatchNumber`). This should only be used
for minor patches and should in no case break anything for anyone.
1. If your changes are minor, you will bump the minor version number (`X.Minor.Z`).
The changes should stay as minor as possible, they should not change the behavior of
the software and shouldn't break the current logic. The user should not get anything
broken from upgrading or applying the minor patch.
1. If your changes are logic changes, structure changes, big changes, etc. they are major.
Thus should change the major version number (`Major.Y.Z`). Those changes should be stashed
and properly planned for the big next release that introduce a given load of breaking changes.
1. A breaking change should be documented in the upgrade section of the documentation, in
addition of in the changelog.

### The Release Number Checklist

- [ ] Choose a release type
- [ ] Bump the major, minor or patch version number

## Bumping the version
- [ ] Make sure to bump the `setup.py`'s version to the correct newest version.
- [ ] Update the `README.md` file's comparison tag version (look for `Commits since latest release`).
- [ ] Commit with the message "Bump version for new release" and push it to a new branch
- [ ] Prepare the final changelog and notes

## Creating the release
- [ ] Merge the branch
- [ ] Create a tag through GitHub or `git tag vX.Y.Z && git push --tag`; the tag should be `vX.Y.Z`
- [ ] Create a release and put the change logs and any information that may be useful.
