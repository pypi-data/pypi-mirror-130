"""BRAILE CODES

This script defines a list of list (matrix) whos entries
give the corresponding braile unicode character that represents
a binary number.

Each braile character contains two 4-bit binary numbers, each binary number
is used with the MSB being the bottom dot such that
BRAILE[n][k] is the braile code form by a 4-bit binary number n
(left column) and another 4-bit binary number k (right column)
"""

#All characters that contain the number 0 on the left column
C0 = ["\u2800", "\u2808", "\u2810", "\u2818",
      "\u2820", "\u2828", "\u2830", "\u2838",
      "\u2880", "\u2888", "\u2890", "\u2898",
      "\u28a0", "\u28a8", "\u28b0", "\u28b8"]

C1 = ["\u2801", "\u2809", "\u2811", "\u2819",
      "\u2821", "\u2829", "\u2831", "\u2839",
      "\u2881", "\u2889", "\u2891", "\u2899",
      "\u28a1", "\u28a9", "\u28b1", "\u28b9"]

C2 = ["\u2802", "\u280a", "\u2812", "\u281a",
      "\u2822", "\u282a", "\u2832", "\u283a",
      "\u2882", "\u288a", "\u2892", "\u289a",
      "\u28a2", "\u28aa", "\u28b2", "\u28ba"]

C3 = ["\u2803", "\u280b", "\u2813", "\u281b",
      "\u2823", "\u282b", "\u2833", "\u283b",
      "\u2883", "\u288b", "\u2893", "\u289b",
      "\u28a3", "\u28ab", "\u28b3", "\u28bb"]

C4 = ["\u2804", "\u280c", "\u2814", "\u281c",
      "\u2824", "\u282c", "\u2834", "\u283c",
      "\u2884", "\u288c", "\u2894", "\u289c",
      "\u28a4", "\u28ac", "\u28b4", "\u28bc"]

C5 = ["\u2805", "\u280d", "\u2815", "\u281d",
      "\u2825", "\u282d", "\u2835", "\u283d",
      "\u2885", "\u288d", "\u2895", "\u289d",
      "\u28a5", "\u28ad", "\u28b5", "\u28bd"]

C6 = ["\u2806", "\u280e", "\u2816", "\u281e",
      "\u2826", "\u282e", "\u2836", "\u283e",
      "\u2886", "\u288e", "\u2896", "\u289e",
      "\u28a6", "\u28ae", "\u28b6", "\u28be"]

C7 = ["\u2807", "\u280f", "\u2817", "\u281f",
      "\u2827", "\u282f", "\u2837", "\u283f",
      "\u2887", "\u288f", "\u2897", "\u289f",
      "\u28a7", "\u28af", "\u28b7", "\u28bf"]

C8 = ["\u2840", "\u2848", "\u2850", "\u2858",
      "\u2860", "\u2868", "\u2870", "\u2878",
      "\u28c0", "\u28c8", "\u28d0", "\u28d8",
      "\u28e0", "\u28e8", "\u28f0", "\u28f8"]

C9 = ["\u2841", "\u2849", "\u2851", "\u2859",
      "\u2861", "\u2869", "\u2871", "\u2879",
      "\u28c1", "\u28c9", "\u28d1", "\u28d9",
      "\u28e1", "\u28e9", "\u28f1", "\u28f9"]

C10 = ["\u2842", "\u284a", "\u2852", "\u285a",
       "\u2862", "\u286a", "\u2872", "\u287a",
       "\u28c2", "\u28ca", "\u28d2", "\u28da",
       "\u28e2", "\u28ea", "\u28f2", "\u28fa"]

C11 = ["\u2843", "\u284b", "\u2853", "\u285b",
       "\u2863", "\u286b", "\u2873", "\u287b",
       "\u28c3", "\u28cb", "\u28d3", "\u28db",
       "\u28e3", "\u28eb", "\u28f3", "\u28fb"]

C12 = ["\u2844", "\u284c", "\u2854", "\u285c",
       "\u2864", "\u286c", "\u2874", "\u287c",
       "\u28c4", "\u28cc", "\u28d4", "\u28dc",
       "\u28e4", "\u28ec", "\u28f4", "\u28fc"]

C13 = ["\u2845", "\u284d", "\u2855", "\u285d",
       "\u2865", "\u286d", "\u2875", "\u287d",
       "\u28c5", "\u28cd", "\u28d5", "\u28dd",
       "\u28e5", "\u28ed", "\u28f5", "\u28fd"]

C14 = ["\u2846", "\u284e", "\u2856", "\u285e",
       "\u2866", "\u286e", "\u2876", "\u287e",
       "\u28c6", "\u28ce", "\u28d6", "\u28de",
       "\u28e6", "\u28ee", "\u28f6", "\u28fe"]

C15 = ["\u2847", "\u284f", "\u2857", "\u285f",
       "\u2867", "\u286f", "\u2877", "\u287f",
       "\u28c7", "\u28cf", "\u28d7", "\u28df",
       "\u28e7", "\u28ef", "\u28f7", "\u28ff"]

BRAILE = [C0, C1, C2, C3, C4, C5, C6, C7,
          C8, C9, C10, C11, C12, C13, C14, C15]
