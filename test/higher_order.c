#ifdef HIGHER_ORDER_0_A
A

#ifdef HIGHER_ORDER_0_B
AB

#ifdef HIGHER_ORDER_0_C
ABC
#endif

AB
#endif

A
#endif



#if defined(HIGHER_ORDER_1_A) && defined(HIGHER_ORDER_1_B)
AB

#if defined(HIGHER_ORDER_1_C)
ABC
#endif

AB
#endif



#if defined(HIGHER_ORDER_2_A)
A

#if defined(HIGHER_ORDER_2_B) && defined(HIGHER_ORDER_2_C)
ABC
#endif

A
#endif



#if defined(HIGHER_ORDER_3_A) && defined(HIGHER_ORDER_3_B)
AB

#if defined(HIGHER_ORDER_3_C) && defined(HIGHER_ORDER_3_D)
ABCD
#endif

AB
#endif



#if defined(HIGHER_ORDER_4_A) && defined(HIGHER_ORDER_4_B)
AB

#if defined(HIGHER_ORDER_4_C)
ABC

#if defined(HIGHER_ORDER_4_D) && defined(HIGHER_ORDER_4_E)
ABCDE
#endif

ABC
#endif

AB
#endif