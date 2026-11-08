# QUILL GitHub Practice

This repository is somewhere safe to learn GitHub with QUILL and QUILL Lite.

It's a tiny Python project called `tally`, which counts the words in a piece
of text. The code is small on purpose: what you're here to practise is
everything around it. That means issues, pull requests, reviews, checks,
releases and discussions, all of them already set up and waiting for you.

## Read here, practise in your own copy

This repository is the example everyone reads, so it stays as it is. Its
issues, pull requests and discussion are locked, and only Community Access can
change anything here. Everything you do that writes something (a comment, a
reaction, a label, a merge) happens in a copy of your own, where nothing you
do can bother anyone else.

### Reading here

You don't need permission to read anything. Open GitHub Items in QUILL or
QUILL Lite, choose `Community-Access/quill-github-practice`, and look around:

- six issues with labels, an assignee and a milestone, one of them closed;
- the pull request "Add a line count", with a review, a line comment and a
  suggested change;
- the draft pull request "Speed up word counting", whose check fails on
  purpose, so What Failed has something to explain;
- the release `v0.1.0`, with a file attached;
- the discussion "Welcome: say hello and ask anything", with replies;
- a security policy, a code of conduct, and issue and pull request templates.

### Making your own copy

You can make the copy without leaving the GitHub Workbench:

1. In GitHub Items, open Explore and find this repository.
2. Open its context menu (the Applications key, or `Shift+F10`), then choose
   **Repository Actions for Community-Access/quill-github-practice > Create
   Repository from This Template...**.
3. Give your copy a name and choose your own account as its owner. It can be
   private.

You can also do it on the web: on this repository's page, choose **Use this
template**, then **Create a new repository**.

GitHub copies the files, but not the issues or pull requests. To add those:

1. Open your copy in GitHub Items and go to its workflows.
2. Choose **Set up practice**, then **Run Workflow on Branch...**, and run it
   on `main`. On the web, it's on your copy's **Actions** tab.
3. When the run finishes, its summary lists everything it made. Run it again
   at any time to put back anything you've closed or deleted. It never makes a
   second copy of something that's already there.

Setting up needs two settings in your copy. If either is off, the run fails
and its summary says which one to turn on. Turn it on, then run Set up practice
again.

- **Pull requests:** Settings > Actions > General > Workflow permissions. Check
  **Allow GitHub Actions to create and approve pull requests**, then Save.
- **Discussions:** Settings > General > Features. Check **Discussions**.

In your copy, the checks on the two practice pull requests may wait for your
approval before they run, because a workflow opened those pull requests rather
than a person. Approving them is the first exercise in chapter 6.

## Where to start

[PRACTICE.md](PRACTICE.md) has an exercise for each chapter of the GitHub
Guide, in the order the guide teaches them. The tutorial "Practise GitHub
Safely" on the QUILL website walks through the same steps:
<https://quillforall.org/docs.html>.

The GitHub Guide comes with both editors. In QUILL it's part of the User
Guide, and in QUILL Lite it's a chapter run of its own.

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
