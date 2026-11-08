# QUILL GitHub Practice

This repository is somewhere safe to learn GitHub with QUILL and QUILL Lite.
Nothing here matters. You can't break anything, and nobody minds if you get
something wrong.

It's a tiny Python project called `tally`, which counts the words in a piece
of text. The code is small on purpose: what you're here to practise is
everything around it. That means issues, pull requests, reviews, checks,
releases and discussions, all of them already set up and waiting for you.

## Two ways to practise

### Read and explore here

You don't need permission to read anything in this repository. Open GitHub
Items in QUILL or QUILL Lite, choose this repository
(`Community-Access/quill-github-practice`), and look around:

- issues with labels, an assignee and a milestone, including a closed one;
- an open pull request with review comments and a suggested change;
- a draft pull request whose check fails on purpose, so What Failed has
  something to explain;
- a release with a file attached;
- a discussion with replies;
- a security policy, a code of conduct, and issue and pull request templates.

You can also comment, react and open new issues here. Please keep it friendly,
because other people practise here too.

### Make your own copy

To practise the things that change a repository (merging, closing, labelling,
pushing), make a copy of your own:

1. On this repository's page on GitHub, choose **Use this template**, then
   **Create a new repository**. Pick your own account as the owner. The copy
   can be private.
2. GitHub copies the files, but not the issues or pull requests. To add those,
   open your copy's **Actions** tab, choose the **Set up practice** workflow,
   and choose **Run workflow**. In QUILL you can do this without the browser:
   the GitHub Guide's chapter 6, "Running a workflow by hand", shows how.
3. When the run finishes, its summary lists everything it made. Run it again
   at any time to put back anything you've closed or deleted. It never makes a
   second copy of something that's already there.

The setup needs two settings in your copy. If either is off, the run's summary
says which one, and you can run it again after turning it on.

- **Pull requests:** Settings > Actions > General > Workflow permissions. Check
  **Allow GitHub Actions to create and approve pull requests**, then Save.
- **Discussions:** Settings > General > Features. Check **Discussions**.

## Where to start

[PRACTICE.md](PRACTICE.md) has an exercise for each chapter of the GitHub
Guide, in the order the guide teaches them. Each one says whether you can do
it here or need your own copy.

The GitHub Guide comes with both editors. In QUILL it's in the User Guide, and
in QUILL Lite it's a chapter run of its own. It's also on the web at
<https://quillforall.org/docs.html>.

## Running the tests

You don't need to, but if you'd like to:

```
python -m unittest discover -s tests
```

It needs Python 3.9 or later and nothing else.

## Help

If something here doesn't work the way PRACTICE.md says, email
support@community-access.org and say which exercise you were on.

This repository is maintained by Community Access and licensed under the MIT
License.
