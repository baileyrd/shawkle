# Shawkle - rule-based processing of plain-text lists #

This Python script is designed to process plain-text files,
composed of "lines" of screen width (e.g., 120 columns)
or Tweet width (140 columns), by automatically relocating
individual lines into various files based on pattern matching.
The patterns to be matched, along with the source and target
files to which the patterns refer, are expressed in a set of
"rules" that are processed in order.  This Python script
replaces [earlier incarnations of the script in Korn shell](http://www.lifehacker.com/software/command-line/getting-things-done-with-rulebased-list-processing-217063.php)
that I have been continuously using to manage my to-do lists,
activity logs, and browser favorites for the past eighteen
years.

## Running Shawkle with test data ##

The [SVN project](http://code.google.com/p/shawkle/) includes a directory of test data.  In order
to run Shawkle using test data:
  * Install the SVN project, https://shawkle.googlecode.com/svn/trunk, under your home directory ("~/shawkle").
  * Uncomment the first three lines of the "if name == main" block, which run shawkle using the test data included in the SVN project (~/shawkle/testdata/a).

[![](http://wingware.com/images/coded-with-logo-129x66.png)](http://wingware.com)