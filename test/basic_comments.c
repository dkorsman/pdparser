#ifdef GOOD_4
/*
 * Simple multiline test
*/
#endif


/* These are the build-in archivers. We list them all as "extern" here without
   #ifdefs to keep it tidy, but obviously you need to make sure these are
   wrapped in PHYSFS_SUPPORTS_* checks before actually referencing them. */


#ifdef GOOD_5
// May have been set by compiler/*.hpp, but "long long" without library
// support is useless.
#endif


#ifdef GOOD_6 /* comment
#endif */
#endif // the real one

/*
#ifdef BAD_0
*/

/* If we're using clang + glibc, we have to get hacky.
 * See http://llvm.org/bugs/show_bug.cgi?id=6907 */

#ifdef GOOD_7

#endif /*

#ifdef BAD_1

*/

#if 0
This is not actually code! But this comment is real: /* this
#endif
#endif
aa */ aa
#endif
