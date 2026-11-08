# Practice exercises

There's one set of exercises for each chapter of the GitHub Guide, in the
order the guide teaches them.

- **Read here** exercises only read, so you can do them in
  `Community-Access/quill-github-practice` itself.
- **In your copy** exercises change things, so they need a copy of your own,
  made from this template and set up with the Set up practice workflow. The
  README says how.

The exercises name issues and pull requests by title rather than number,
because the numbers in your copy may differ.

## Chapter 1: Getting started

Read here:

1. Sign in with Manage GitHub Accounts. In QUILL it's on File > Open from
   Remote. In QUILL Lite it's File > Manage GitHub Accounts.
2. Open GitHub Items and choose this repository.
3. Find the issue "Word count is off by one when text ends with a space" and
   read it from the top.

In your copy:

1. Make your copy, as the README describes, and run Set up practice.
2. Open your copy in GitHub Items and check that the same issue is there.

## Chapter 2: Getting around

Read here:

1. In GitHub Items, move between the Issues and Pull requests lists.
2. Filter the issues by the label `good first issue`. There should be one.
3. Open "Add a line count to the summary" and move from comment to comment.
   Then go back to the list without losing your place.

## Chapter 3: Your inbox and your work

In your copy:

1. Comment on "Question: what counts as a word?". Commenting subscribes you.
2. Ask a friend to reply, or reply yourself from a second account. Then find
   the notification in your inbox and mark it Done.
3. Look at My Work. The issue assigned to you should be there.

## Chapter 4: Issues

Read here:

1. Read "Question: what counts as a word?" and hear the summary of the
   discussion.
2. Move through its timeline.

In your copy:

1. Add a reaction to the first comment on that issue.
2. Write a new issue using the **Bug report** template. It doesn't have to be
   a real bug.
3. Add the label `accessibility` to "CONTRIBUTING should explain how to write
   a test".
4. Put your new issue in the milestone "Practice milestone 1".
5. Close "Typo in the module docstring" and then reopen it.
6. Select three issues and add the `question` label to all of them at once.

## Chapter 5: Pull requests and review

Read here:

1. Open the pull request "Add a line count". Hear its one-sentence summary.
2. Open it in the review window. Move through the outline, then from thread
   to thread.
3. Find the suggested change on `line_count`. Read what it would change.

In your copy:

1. Reply to the review thread, then resolve it.
2. Comment on a single line of the diff, then on a range of lines.
3. Merge the pull request. If you'd like to take the suggested change first,
   use **Commit suggestion** on GitHub's website: QUILL reads suggestions but
   doesn't commit them.
4. Mark the draft pull request "Speed up word counting" as ready for review.

## Chapter 6: Actions and checks

Read here:

1. Open the draft pull request "Speed up word counting". Its check fails.
2. Use What Failed. It should name the failing test,
   `test_counts_hyphenated_words`, and quote the assertion.
3. Read the job log, step by step.

In your copy:

1. Use What Failed on the failed Tests run for the branch
   `practice/speed-up-word-counting`. Set up practice started it for you. (The
   draft pull request's own check may be waiting for approval, because a
   workflow opened the pull request. On the web, the pull request page can
   approve it.)
2. Run the **Tests** workflow by hand on `main`. It should pass.
3. Rerun the failed jobs on the draft pull request. They'll fail again, which
   is the point.
4. Run the Tests workflow again, cancel it while it's still going, then delete
   the run.

## Chapter 7: Code and repositories

Read here:

1. Browse the files. Open `src/tally/__init__.py`.
2. Look at the blame for that file. You'll hear who changed which lines, in
   runs.
3. Search the code for `def word_count`.
4. Open the release `v0.1.0`, read its notes and download its attached file.

In your copy:

1. Edit the release notes for `v0.1.0`.
2. Set two topics on your copy, such as `practice` and `python`.

## Chapter 8: Discussions and security

Read here:

1. Open the discussion "Welcome: say hello and ask anything" and read the
   thread.
2. Read the security policy. There are no security alerts here, so Security
   Alerts should tell you so.

In your copy:

1. Reply to the discussion.
2. Reply to one of its comments, to start a thread of its own.

## Chapter 9: Codespaces and the command line

In your copy:

1. Create a codespace, then stop it and delete it. Codespaces count against
   your free monthly hours, so don't leave one running.
2. If you have the GitHub command-line tool, clone your copy and push a small
   change to a new branch.

## Chapter 10: Troubleshooting

1. Open Manage GitHub Accounts and check which account is active.
2. Look at the rate-limit readout. Reading this repository uses very little of
   it.

## Chapter 11: Keyboard reference

There's nothing to do here. Keep chapter 11 open while you work through the
others, and give a key to any command you find yourself using often.

## When you're done

Delete your copy from its Repository Actions submenu (Delete Repository...),
or keep it and run Set up practice again whenever you want a fresh start.
