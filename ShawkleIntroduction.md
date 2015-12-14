# Introduction #

This Python script is designed to process plain-text files,
composed of "lines" of screen width (e.g., 120 columns)
or Tweet width (140 columns), by automatically relocating
individual lines into various files based on pattern matching.
The patterns to be matched, along with the source and target
files to which the patterns refer, are expressed in a set of
"rules" that are processed in order.  This Python script
replaces earlier incarnations of the script in Korn shell
that I have been continuously using to manage my to-do lists,
activity logs, and browser favorites for the past sixteen
years.

# Details #

The SVN project includes a directory of test data.  In order
to run Shawkle using test data:
  * Install the SVN project under your home directory ("~").
  * Uncomment the first three lines of the "if name == main" block, which point shawkle at the test data.