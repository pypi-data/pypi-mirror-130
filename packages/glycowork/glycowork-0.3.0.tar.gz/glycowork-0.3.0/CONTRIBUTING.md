# How to contribute

## How to get started

Before anything else, please install the git hooks that run automatic scripts during each commit and merge to strip the notebooks of superfluous metadata (and avoid merge conflicts). After cloning the repository, run the following command inside it:
```
nbdev_install_git_hooks
```

## Did you find a bug?

* Ensure the bug was not already reported by searching on GitHub under Issues.
* If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.
* Be sure to add the complete error messages.

#### Did you write a patch that fixes a bug?

* Open a new GitHub pull request with the patch.
* Ensure that your PR includes a test that fails without your patch, and pass with it.
* Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.

## PR submission guidelines

* Keep each PR focused. While it's more convenient, do not combine several unrelated fixes together. Create as many branches as needing to keep each PR focused.
* Do not mix style changes/fixes with "functional" changes. It's very difficult to review such PRs and it most likely get rejected.
* Do not add/remove vertical whitespace. Preserve the original style of the file you edit as much as you can.
* Do not turn an already submitted PR into your development playground. If after you submitted PR, you discovered that more work is needed - close the PR, do the required work and then submit a new PR. Otherwise each of your commits requires attention from maintainers of the project.
* If, however, you submitted a PR and received a request for changes, you should proceed with commits inside that PR, so that the maintainer can see the incremental fixes and won't need to review the whole PR again. In the exception case where you realize it'll take many many commits to complete the requests, then it's probably best to close the PR, do the work and then submit it again. Use common sense where you'd choose one way over another.

## Do you want to contribute to the documentation?

* Docs are automatically created from the notebooks in the nbs folder.


## Wishlist for future glycowork updates (last update: 2021-07-28)
#### Urgent
* Currently, annotation functions convert glycans to graphs on the fly, which is potentially wasteful computation. Rather, subgraph_isomorphism and related functions should be able to take pre-computed graphs (either provided or calculated in the wrapper functions)
* get_trisaccharides needs to be reworked to ensure 100% completeness (and probably better efficiency)
* ideally, we’d have a better heuristic than estimate_lower_bound for speeding up annotation

#### At some point
* split motif_list into ‘core’ motifs (occurring frequently) and ‘extended’ motifs (that are rare / niche) for performance reasons
* Currently, the glycan graph objects have, as node labels, numbers that indicate the glycoletters (which can be retrieved by indexing lib with this number). In the future, it might be more intuitive to provide the actual glycoletters as strings in the node labels. This would require a slight rewrite of all functions that currently work with the node labels.
* characterize_monosaccharide only factors in subsequent sequence context; make it possible (as an option) to also consider upstream sequence context
* add the possibility of drawing glycans on plots (e.g., have SNFG glycans on x-axis for a bar plot etc.)

#### Not sure whether a good idea
* instead of stemifying rare monosaccharide modifications, consider masking them with a ‘monosaccharide’ token
