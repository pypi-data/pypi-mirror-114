# Installation
pip install [pnu-strfile](https://pypi.org/project/pnu-strfile/)

# STRFILE(8), UNSTR(8)

## NAME
strfile, unstr — create a random access file for storing strings

## SYNOPSIS
**strfile**
\[-Ciorsx\]
\[-c char\]
\[--debug\]
\[--help|-?\]
\[--version\]
\[--\]
source_file \[output_file\]

**unstr**
\[--debug\]
\[--help|-?\]
\[--version\]
\[--\]
source_file

## DESCRIPTION
The **strfile** utility reads a file containing groups of lines separated by a line containing a single percent ‘%’ sign and creates a data file which contains a header structure and a table of file offsets for each group of lines.
This allows random access of the strings.

The output file, if not specified on the command line, is named *source_file.dat*.

The options are as follows:

Options | Use
------- | ---
-C|Flag the file as containing comments. This option cases the STR_COMMENTS bit in the header str_flags field to be set. Comments are designated by two delimiter characters at the beginning of the line, though strfile does not give any special treatment to comment lines.
-c char|Change the delimiting character from the percent sign to char.
-i|Ignore case when ordering the strings.
-o|Order the strings in alphabetical order. The offset table will be sorted in the alphabetical order of the groups of lines referenced. Any initial non-alphanumeric characters are ignored. This option causes the STR_ORDERED bit in the header str_flags field to be set.
-r|Randomize access to the strings. Entries in the offset table will be randomly ordered. This option causes the STR_RANDOM bit in the header str_flags field to be set. The *-o* option has precedence over the *-r* option.
-s|Run silently; do not give a summary message when finished.
-x|Note that each alphabetic character in the groups of lines is rotated 13 positions in a simple caesar cypher. This option causes the STR_ROTATED bit in the header str_flags field to be set.
--debug|Enable debug mode
--help\|-?|Print usage and a short help message and exit
--version|Print version and exit
--|Options processing terminator

The format of the header is:

```C
#define VERSION 1
uint32_t        str_version;    /* version number */
uint32_t        str_numstr;     /* # of strings in the file */
uint32_t        str_longlen;    /* length of longest string */
uint32_t        str_shortlen;   /* length of shortest string */
#define STR_RANDOM      0x1     /* randomized pointers */
#define STR_ORDERED     0x2     /* ordered pointers */
#define STR_ROTATED     0x4     /* rot-13'd text */
#define STR_COMMENTS    0x8     /* embedded comments */
uint32_t        str_flags;      /* bit field for flags */
char            str_delim;      /* delimiting character */
```

All fields are written in network byte order.

The purpose of **unstr** is to undo the work of **strfile**.
It prints out the strings contained in the file *source_file* in the order that they are listed in the header file *source_file.dat* to standard output.
It is possible to create sorted versions of input files by using *-o* when **strfile** is run and then using **unstr** to dump them out in the table order.

## ENVIRONMENT
The STRFILE_DEBUG and UNSTR_DEBUG environment variables can also be set to any value to enable debug mode.

## SEE ALSO
[byteorder(3)](https://www.freebsd.org/cgi/man.cgi?query=byteorder),
[fortune(6)](https://www.freebsd.org/cgi/man.cgi?query=fortune&apropos=0&sektion=0&manpath=FreeBSD+14.0-current&arch=default&format=html)

## STANDARDS
This implementation is fully compatible with the FreeBSD version.

It tries to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for [Python](https://www.python.org/) code.

## HISTORY
Contributed by [Ken Arnold](https://en.wikipedia.org/wiki/Ken_Arnold), the **strfile** utility first appeared in 2.9BSD.

This implementation was made for [The PNU project](https://github.com/HubTou/PNU).

## LICENSE
This utility is available under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).

## AUTHORS
This version was written by [Hubert Tournier](https://github.com/HubTou).

The man page is derived from the FreeBSD project's one.

