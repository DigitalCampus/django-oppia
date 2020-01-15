#!/bin/sh
#
# A git hook script to find and fix trailing whitespace in your commits. Bypass
# it with the --no-verify option to git-commit.
#
# Original source: http://web.archive.org/web/20120605081123/http://blog.yesmeck.com/archives/make-git-automatically-remove-trailing-whitespace-before-committing/
#
# What's distinct about this version, as opposed to several I've seen, is that
# it only fixes the whitespace on lines you've actually changed, so avoids
# making you the blamee of code you didn't change.

# Find files with trailing whitespace
for file in `git diff --check --cached | grep '^[^+-]' | grep -o '^.*[0-9]\+:'` ; do
    file_name=`echo ${file} | grep -o '^[^:]\+'`
    # Uses perl because "grep -P" doesn't work on OS X
    line_number=`echo ${file} | perl -nle'print $& if m{(?<=:)[0-9]+(?=:)}'`
    # Different OSes have different sed's; try the one that works.
    (sed -i "${line_number}s/\s*$//" "${file_name}" > /dev/null 2>&1 \
        || sed -i '' -E "${line_number}s/[[:space:]]*$//" "${file_name}")
    git add ${file_name}
    echo "Re-wrote ${file_name} to trim whitespace."
done

# Now we can commit
exit
