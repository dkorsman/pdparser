const char *s = "/*";

#ifdef GOOD_8
The comment start is part of a string
#endif

const char *s2 = "*/";

fn("asdf", /* "asdf" ...

#ifdef BAD_2

The comment start is not actually part of a string

*/ "asdf");

fn("/*", "*/");

#ifdef GOOD_9

#endif

    locale_list = ExpandOne(&xpc, (char_u *)"$VIMRUNTIME/lang/*",
                              NULL, options, WILD_ALL);

#ifdef GOOD_10
Again, comment start is part of a string
#endif

const char *s3 = "*/";

fn("This string does\" NOT end here! /* NOT a \"comment");

#ifdef GOOD_11
An escaped quote does not end the string
#endif

const char *s4 = "*/";


fn("This is a multiline string which still contains the \
start comment tag /* but this is NOT a comment! \
But this should be pretty easy.");

#ifdef GOOD_12

#endif

const char *s5 = "*/";


fn("This does actually end the string next line \
" /* this IS a comment and NOT a string because the backslash does not escape the "

#ifdef BAD_3

*/
);
const char *s6 = "*/";


/* We start a comment here
"and we suddenly end it here */ "this is a string" // "

#ifdef GOOD_12
That string wasn't real was it?
#endif

const char *s7 = "*/";


fn("", " /* ");

#ifdef GOOD_13
That comment tag was part of a string
#endif

const char *s8 = "*/";

// "this should /* not start a multiline comment"

#ifdef GOOD_14

#endif

// " */ "


fn(/*
 * This should! end the comment " */ "aa");

#ifdef GOOD_15

#endif
