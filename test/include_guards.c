#ifndef INCLUDE_GUARD_H
#define INCLUDE_GUARD_H

#define FEATURE

#if defined(FEATURE)
code
#endif

#if defined(INCLUDE_GUARD)
#define INCLUDE_GUARD
#endif

#if defined(NOT_INCLUDE_GUARD_A)
#define NOT_INCLUDE_GUARD_A
#endif

#define NOT_INCLUDE_GUARD_A
#define NOT_INCLUDE_GUARD_B

#if defined(NOT_INCLUDE_GUARD_B)
#define NOT_INCLUDE_GUARD_B
#endif

#if defined(NOT_INCLUDE_GUARD_C)
#define NOT_INCLUDE_GUARD_C 1
#endif

#endif /* INCLUDE_GUARD_H */