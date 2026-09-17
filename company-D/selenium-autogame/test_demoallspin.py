import requests
import json

urldemo = "https://example.internal/"
urldemophp2 = "https://example.internal/"
urlsta = "https://example.internal/"
urllab = "http://example.internal/"

#ID SPIN DATA
#16 slot
body1601 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1601,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body1602 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1602,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body1603 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1603,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body1604 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1604,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body1605 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1605,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body1606 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1606,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body1607 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1607,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
#scratch
body1700 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1700,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body1701 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1701,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body1811 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1811,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body1812 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1812,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
#18 fruit + 20 fruit
body1817 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1817,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
body1820 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1820,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
body2000 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2000,\"line_bet\":25,\"line_num\":8,\"coin_value\":10,\"bet_credit\":2000}}"
body2001 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2001,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
#18 slot
body1813 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1813,\"line_bet\":50,\"line_num\":15,\"coin_value\":3,\"bet_credit\":2250}}"
body1815 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1815,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
body1816 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1816,\"line_bet\":50,\"line_num\":40,\"coin_value\":1,\"bet_credit\":2000}}"
body1818 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1818,\"line_bet\":50,\"line_num\":9,\"coin_value\":5,\"bet_credit\":2250}}"
body1819 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1819,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body1822 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1822,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
#19 slot
body1900 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1900,\"line_bet\":25,\"line_num\":9,\"coin_value\":10,\"bet_credit\":2250}}"
body1901 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1901,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
body1902 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000}}"
body1903 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1903,\"line_bet\":50,\"line_num\":9,\"coin_value\":5,\"bet_credit\":2250}}"
body1904 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1904,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body1905 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1905,\"line_bet\":25,\"line_num\":15,\"coin_value\":5,\"bet_credit\":1875}}"
body1906 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1906,\"line_bet\":25,\"line_num\":40,\"coin_value\":2,\"bet_credit\":2000}}"
body1907 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1907,\"line_bet\":50,\"line_num\":15,\"coin_value\":3,\"bet_credit\":2250}}"
body1908 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1908,\"line_bet\":25,\"line_num\":25,\"coin_value\":3,\"bet_credit\":1875}}"

#21 medusa
body2100 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2100,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body2101 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2101,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body2102 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2102,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body2103 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2103,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body2104 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2104,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#22 
body2200 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2200,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body2201 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2201,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body2202 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2202,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body2203 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2203,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#23 1 line
body2300 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2300,\"line_bet\":1000,\"line_num\":1,\"coin_value\":2,\"bet_credit\":2000}}"
body2301 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2301,\"line_bet\":1000,\"line_num\":1,\"coin_value\":2,\"bet_credit\":2000}}"
body2302 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2302,\"line_bet\":500,\"line_num\":1,\"coin_value\":4,\"bet_credit\":2000}}"
#24 right + left + buy free
body2400 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body2400buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
body2401 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body2401buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
body2402 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2402,\"line_bet\":25,\"line_num\":18,\"coin_value\":4,\"bet_credit\":1800,\"buy_spin\":0}}"
body2402buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2402,\"line_bet\":25,\"line_num\":18,\"coin_value\":4,\"bet_credit\":1800,\"buy_spin\":1}}"
body2403 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body2403buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
#25 grid
body2500 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body2501 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body2502 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000}}"
body2503 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2503,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body2504 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2504,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
#26 hold and spin 1
body2600 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2600,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body2600buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2600,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body2601 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2601,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body2601buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2601,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body2602 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2602,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body2602buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2602,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"
body2603 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2603,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body2603buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2603,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#27 hold and spin 2
body2700 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2700,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body2700buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2700,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body2701 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2701,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body2701buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2701,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body2702 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2702,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body2702buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2702,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"
body2703 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2703,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body2703buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2703,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#28 medusa 2
body2800 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2800,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body2801 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2801,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body2802 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2802,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body2803 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2803,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body2804 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2804,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#29 grid 2 
body2900 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2900,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body2900buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2900,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body2901 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2901,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body2901buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2901,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body2902 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body2902buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#30 slot aladin
body3000 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3000,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body3000buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3000,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body3001 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3001,\"line_bet\":40,\"line_num\":50,\"coin_value\":1,\"bet_credit\":2000,\"buy_spin\":0}}"
body3001buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3001,\"line_bet\":40,\"line_num\":50,\"coin_value\":1,\"bet_credit\":2000,\"buy_spin\":1}}"
body3002 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3002,\"line_bet\":20,\"line_num\":50,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body3002buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3002,\"line_bet\":20,\"line_num\":50,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#31 slot arthur king
body3100 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3100,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body3100buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3100,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body3101 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3101,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body3101buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3101,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body3102 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3102,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":0}}"
body3102buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3102,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":1}}"

#32 slot
body3200 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3200,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body3200buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3200,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body3201 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3201,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body3201buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3201,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body3202 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3202,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":0}}"
body3202buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3202,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":1}}"

#33 slot
body3300 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3300,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body3300buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3300,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body3301 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3301,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body3301buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3301,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body3302 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3302,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body3302buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3302,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#34 slot
body3400 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3400,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body3400buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3400,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body3401 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3401,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body3401buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3401,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body3402 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3402,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body3402buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3402,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#35 grid
body3500 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body3500buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body3501 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body3501buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body3502 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body3502buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#36 poker
body3600 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3600,\"line_bet\":200,\"line_num\":5,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"

#電竟
body1001 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1001,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"

#37
body3700 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3700,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"

#38
body3800 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3800,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body3800buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3800,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#ID agent-01 SPIN DATA
#16 slot
body21601 = "{\"command\":\"spin\",\"token\":\"test2token1601\",\"data\":{\"game_id\":1601,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body21602 = "{\"command\":\"spin\",\"token\":\"test2token1602\",\"data\":{\"game_id\":1602,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body21603 = "{\"command\":\"spin\",\"token\":\"test2token1603\",\"data\":{\"game_id\":1603,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body21604 = "{\"command\":\"spin\",\"token\":\"test2token1604\",\"data\":{\"game_id\":1604,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body21605 = "{\"command\":\"spin\",\"token\":\"test2token1605\",\"data\":{\"game_id\":1605,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body21606 = "{\"command\":\"spin\",\"token\":\"test2token1606\",\"data\":{\"game_id\":1606,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body21607 = "{\"command\":\"spin\",\"token\":\"test2token1607\",\"data\":{\"game_id\":1607,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
#scratch
body21700 = "{\"command\":\"spin\",\"token\":\"test2token1700\",\"data\":{\"game_id\":1700,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body21701 = "{\"command\":\"spin\",\"token\":\"test2token1701\",\"data\":{\"game_id\":1701,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body21811 = "{\"command\":\"spin\",\"token\":\"test2token1811\",\"data\":{\"game_id\":1811,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body21812 = "{\"command\":\"spin\",\"token\":\"test2token1812\",\"data\":{\"game_id\":1812,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
#18 fruit + 20 fruit
body21817 = "{\"command\":\"spin\",\"token\":\"test2token1817\",\"data\":{\"game_id\":1817,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
body21820 = "{\"command\":\"spin\",\"token\":\"test2token1820\",\"data\":{\"game_id\":1820,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
body22000 = "{\"command\":\"spin\",\"token\":\"test2token2000\",\"data\":{\"game_id\":2000,\"line_bet\":25,\"line_num\":8,\"coin_value\":10,\"bet_credit\":2000}}"
body22001 = "{\"command\":\"spin\",\"token\":\"test2token2001\",\"data\":{\"game_id\":2001,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
#18 slot
body21813 = "{\"command\":\"spin\",\"token\":\"test2token1813\",\"data\":{\"game_id\":1813,\"line_bet\":50,\"line_num\":15,\"coin_value\":3,\"bet_credit\":2250}}"
body21815 = "{\"command\":\"spin\",\"token\":\"test2token1815\",\"data\":{\"game_id\":1815,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
body21816 = "{\"command\":\"spin\",\"token\":\"test2token1816\",\"data\":{\"game_id\":1816,\"line_bet\":50,\"line_num\":40,\"coin_value\":1,\"bet_credit\":2000}}"
body21818 = "{\"command\":\"spin\",\"token\":\"test2token1818\",\"data\":{\"game_id\":1818,\"line_bet\":50,\"line_num\":9,\"coin_value\":5,\"bet_credit\":2250}}"
body21819 = "{\"command\":\"spin\",\"token\":\"test2token1819\",\"data\":{\"game_id\":1819,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body21822 = "{\"command\":\"spin\",\"token\":\"test2token1822\",\"data\":{\"game_id\":1822,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
#19 slot
body21900 = "{\"command\":\"spin\",\"token\":\"test2token1900\",\"data\":{\"game_id\":1900,\"line_bet\":25,\"line_num\":9,\"coin_value\":10,\"bet_credit\":2250}}"
body21901 = "{\"command\":\"spin\",\"token\":\"test2token1901\",\"data\":{\"game_id\":1901,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
body21902 = "{\"command\":\"spin\",\"token\":\"test2token1902\",\"data\":{\"game_id\":1902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000}}"
body21903 = "{\"command\":\"spin\",\"token\":\"test2token1903\",\"data\":{\"game_id\":1903,\"line_bet\":50,\"line_num\":9,\"coin_value\":5,\"bet_credit\":2250}}"
body21904 = "{\"command\":\"spin\",\"token\":\"test2token1904\",\"data\":{\"game_id\":1904,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body21905 = "{\"command\":\"spin\",\"token\":\"test2token1905\",\"data\":{\"game_id\":1905,\"line_bet\":25,\"line_num\":15,\"coin_value\":5,\"bet_credit\":1875}}"
body21906 = "{\"command\":\"spin\",\"token\":\"test2token1906\",\"data\":{\"game_id\":1906,\"line_bet\":25,\"line_num\":40,\"coin_value\":2,\"bet_credit\":2000}}"
body21907 = "{\"command\":\"spin\",\"token\":\"test2token1907\",\"data\":{\"game_id\":1907,\"line_bet\":50,\"line_num\":15,\"coin_value\":3,\"bet_credit\":2250}}"
body21908 = "{\"command\":\"spin\",\"token\":\"test2token1908\",\"data\":{\"game_id\":1908,\"line_bet\":25,\"line_num\":25,\"coin_value\":3,\"bet_credit\":1875}}"

#21 medusa
body22100 = "{\"command\":\"spin\",\"token\":\"test2token2100\",\"data\":{\"game_id\":2100,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body22101 = "{\"command\":\"spin\",\"token\":\"test2token2101\",\"data\":{\"game_id\":2101,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body22102 = "{\"command\":\"spin\",\"token\":\"test2token2102\",\"data\":{\"game_id\":2102,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body22103 = "{\"command\":\"spin\",\"token\":\"test2token2103\",\"data\":{\"game_id\":2103,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body22104 = "{\"command\":\"spin\",\"token\":\"test2token2104\",\"data\":{\"game_id\":2104,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#22 
body22200 = "{\"command\":\"spin\",\"token\":\"test2token2200\",\"data\":{\"game_id\":2200,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body22201 = "{\"command\":\"spin\",\"token\":\"test2token2201\",\"data\":{\"game_id\":2201,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body22202 = "{\"command\":\"spin\",\"token\":\"test2token2202\",\"data\":{\"game_id\":2202,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body22203 = "{\"command\":\"spin\",\"token\":\"test2token2203\",\"data\":{\"game_id\":2203,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#23 1 line
body22300 = "{\"command\":\"spin\",\"token\":\"test2token2300\",\"data\":{\"game_id\":2300,\"line_bet\":1000,\"line_num\":1,\"coin_value\":2,\"bet_credit\":2000}}"
body22301 = "{\"command\":\"spin\",\"token\":\"test2token2301\",\"data\":{\"game_id\":2301,\"line_bet\":1000,\"line_num\":1,\"coin_value\":2,\"bet_credit\":2000}}"
body22302 = "{\"command\":\"spin\",\"token\":\"test2token2302\",\"data\":{\"game_id\":2302,\"line_bet\":500,\"line_num\":1,\"coin_value\":4,\"bet_credit\":2000}}"
#24 right + left + buy free
body22400 = "{\"command\":\"spin\",\"token\":\"test2token2400\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body22400buy = "{\"command\":\"spin\",\"token\":\"test2token2400\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
body22401 = "{\"command\":\"spin\",\"token\":\"test2token2401\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body22401buy = "{\"command\":\"spin\",\"token\":\"test2token2401\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
body22402 = "{\"command\":\"spin\",\"token\":\"test2token2402\",\"data\":{\"game_id\":2402,\"line_bet\":25,\"line_num\":18,\"coin_value\":4,\"bet_credit\":1800,\"buy_spin\":0}}"
body22402buy = "{\"command\":\"spin\",\"token\":\"test2token2402\",\"data\":{\"game_id\":2402,\"line_bet\":25,\"line_num\":18,\"coin_value\":4,\"bet_credit\":1800,\"buy_spin\":1}}"
body22403 = "{\"command\":\"spin\",\"token\":\"test2token2403\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body22403buy = "{\"command\":\"spin\",\"token\":\"test2token2403\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
#25 grid
body22500 = "{\"command\":\"spin\",\"token\":\"test2token2500\",\"data\":{\"game_id\":2500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body22501 = "{\"command\":\"spin\",\"token\":\"test2token2501\",\"data\":{\"game_id\":2501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body22502 = "{\"command\":\"spin\",\"token\":\"test2token2502\",\"data\":{\"game_id\":2502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000}}"
body22503 = "{\"command\":\"spin\",\"token\":\"test2token2503\",\"data\":{\"game_id\":2503,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body22504 = "{\"command\":\"spin\",\"token\":\"test2token2504\",\"data\":{\"game_id\":2504,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
#26 hold and spin 1
body22600 = "{\"command\":\"spin\",\"token\":\"test2token2600\",\"data\":{\"game_id\":2600,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body22600buy = "{\"command\":\"spin\",\"token\":\"test2token2600\",\"data\":{\"game_id\":2600,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body22601 = "{\"command\":\"spin\",\"token\":\"test2token2601\",\"data\":{\"game_id\":2601,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body22601buy = "{\"command\":\"spin\",\"token\":\"test2token2601\",\"data\":{\"game_id\":2601,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body22602 = "{\"command\":\"spin\",\"token\":\"test2token2602\",\"data\":{\"game_id\":2602,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body22602buy = "{\"command\":\"spin\",\"token\":\"test2token2602\",\"data\":{\"game_id\":2602,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"
body22603 = "{\"command\":\"spin\",\"token\":\"test2token2603\",\"data\":{\"game_id\":2603,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body22603buy = "{\"command\":\"spin\",\"token\":\"test2token2603\",\"data\":{\"game_id\":2603,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#27 hold and spin 2
body22700 = "{\"command\":\"spin\",\"token\":\"test2token2700\",\"data\":{\"game_id\":2700,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body22700buy = "{\"command\":\"spin\",\"token\":\"test2token2700\",\"data\":{\"game_id\":2700,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body22701 = "{\"command\":\"spin\",\"token\":\"test2token2701\",\"data\":{\"game_id\":2701,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body22701buy = "{\"command\":\"spin\",\"token\":\"test2token2701\",\"data\":{\"game_id\":2701,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body22702 = "{\"command\":\"spin\",\"token\":\"test2token2702\",\"data\":{\"game_id\":2702,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body22702buy = "{\"command\":\"spin\",\"token\":\"test2token2702\",\"data\":{\"game_id\":2702,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"
body22703 = "{\"command\":\"spin\",\"token\":\"test2token2703\",\"data\":{\"game_id\":2703,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body22703buy = "{\"command\":\"spin\",\"token\":\"test2token2703\",\"data\":{\"game_id\":2703,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#28 medusa 2
body22800 = "{\"command\":\"spin\",\"token\":\"test2token2800\",\"data\":{\"game_id\":2800,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body22801 = "{\"command\":\"spin\",\"token\":\"test2token2801\",\"data\":{\"game_id\":2801,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body22802 = "{\"command\":\"spin\",\"token\":\"test2token2802\",\"data\":{\"game_id\":2802,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body22803 = "{\"command\":\"spin\",\"token\":\"test2token2803\",\"data\":{\"game_id\":2803,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body22804 = "{\"command\":\"spin\",\"token\":\"test2token2804\",\"data\":{\"game_id\":2804,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#29 grid 2 
body22900 = "{\"command\":\"spin\",\"token\":\"test2token2900\",\"data\":{\"game_id\":2900,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body22900buy = "{\"command\":\"spin\",\"token\":\"test2token2900\",\"data\":{\"game_id\":2900,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body22901 = "{\"command\":\"spin\",\"token\":\"test2token2901\",\"data\":{\"game_id\":2901,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body22901buy = "{\"command\":\"spin\",\"token\":\"test2token2901\",\"data\":{\"game_id\":2901,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body22902 = "{\"command\":\"spin\",\"token\":\"test2token2902\",\"data\":{\"game_id\":2902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body22902buy = "{\"command\":\"spin\",\"token\":\"test2token2902\",\"data\":{\"game_id\":2902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#30 slot aladin
body23000 = "{\"command\":\"spin\",\"token\":\"test2token3000\",\"data\":{\"game_id\":3000,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body23000buy = "{\"command\":\"spin\",\"token\":\"test2token3000\",\"data\":{\"game_id\":3000,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body23001 = "{\"command\":\"spin\",\"token\":\"test2token3001\",\"data\":{\"game_id\":3001,\"line_bet\":40,\"line_num\":50,\"coin_value\":1,\"bet_credit\":2000,\"buy_spin\":0}}"
body23001buy = "{\"command\":\"spin\",\"token\":\"test2token3001\",\"data\":{\"game_id\":3001,\"line_bet\":40,\"line_num\":50,\"coin_value\":1,\"bet_credit\":2000,\"buy_spin\":1}}"
body23002 = "{\"command\":\"spin\",\"token\":\"test2token3002\",\"data\":{\"game_id\":3002,\"line_bet\":20,\"line_num\":50,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body23002buy = "{\"command\":\"spin\",\"token\":\"test2token3002\",\"data\":{\"game_id\":3002,\"line_bet\":20,\"line_num\":50,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#31 slot arthur king
body23100 = "{\"command\":\"spin\",\"token\":\"test2token3100\",\"data\":{\"game_id\":3100,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body23100buy = "{\"command\":\"spin\",\"token\":\"test2token3100\",\"data\":{\"game_id\":3100,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body23101 = "{\"command\":\"spin\",\"token\":\"test2token3101\",\"data\":{\"game_id\":3101,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body23101buy = "{\"command\":\"spin\",\"token\":\"test2token3101\",\"data\":{\"game_id\":3101,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body23102 = "{\"command\":\"spin\",\"token\":\"test2token3102\",\"data\":{\"game_id\":3102,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":0}}"
body23102buy = "{\"command\":\"spin\",\"token\":\"test2token3102\",\"data\":{\"game_id\":3102,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":1}}"

#32 slot
body23200 = "{\"command\":\"spin\",\"token\":\"test2token3200\",\"data\":{\"game_id\":3200,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body23200buy = "{\"command\":\"spin\",\"token\":\"test2token3200\",\"data\":{\"game_id\":3200,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body23201 = "{\"command\":\"spin\",\"token\":\"test2token3201\",\"data\":{\"game_id\":3201,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body23201buy = "{\"command\":\"spin\",\"token\":\"test2token3201\",\"data\":{\"game_id\":3201,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body23202 = "{\"command\":\"spin\",\"token\":\"test2token3202\",\"data\":{\"game_id\":3202,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":0}}"
body23202buy = "{\"command\":\"spin\",\"token\":\"test2token3202\",\"data\":{\"game_id\":3202,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":1}}"

#33 slot
body23300 = "{\"command\":\"spin\",\"token\":\"test2token3300\",\"data\":{\"game_id\":3300,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body23300buy = "{\"command\":\"spin\",\"token\":\"test2token3300\",\"data\":{\"game_id\":3300,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body23301 = "{\"command\":\"spin\",\"token\":\"test2token3301\",\"data\":{\"game_id\":3301,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body23301buy = "{\"command\":\"spin\",\"token\":\"test2token3301\",\"data\":{\"game_id\":3301,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body23302 = "{\"command\":\"spin\",\"token\":\"test2token3302\",\"data\":{\"game_id\":3302,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body23302buy = "{\"command\":\"spin\",\"token\":\"test2token3302\",\"data\":{\"game_id\":3302,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#34 slot
body23400 = "{\"command\":\"spin\",\"token\":\"test2token3400\",\"data\":{\"game_id\":3400,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body23400buy = "{\"command\":\"spin\",\"token\":\"test2token3400\",\"data\":{\"game_id\":3400,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body23401 = "{\"command\":\"spin\",\"token\":\"test2token3401\",\"data\":{\"game_id\":3401,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body23401buy = "{\"command\":\"spin\",\"token\":\"test2token3401\",\"data\":{\"game_id\":3401,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body23402 = "{\"command\":\"spin\",\"token\":\"test2token3402\",\"data\":{\"game_id\":3402,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body23402buy = "{\"command\":\"spin\",\"token\":\"test2token3402\",\"data\":{\"game_id\":3402,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#35 grid
body23500 = "{\"command\":\"spin\",\"token\":\"test2token3500\",\"data\":{\"game_id\":3500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body23500buy = "{\"command\":\"spin\",\"token\":\"test2token3500\",\"data\":{\"game_id\":3500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body23501 = "{\"command\":\"spin\",\"token\":\"test2token3501\",\"data\":{\"game_id\":3501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body23501buy = "{\"command\":\"spin\",\"token\":\"test2token3501\",\"data\":{\"game_id\":3501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body23502 = "{\"command\":\"spin\",\"token\":\"test2token3502\",\"data\":{\"game_id\":3502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body23502buy = "{\"command\":\"spin\",\"token\":\"test2token3502\",\"data\":{\"game_id\":3502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#36 poker
body23600 = "{\"command\":\"spin\",\"token\":\"test2token3600\",\"data\":{\"game_id\":3600,\"line_bet\":200,\"line_num\":5,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"

#電竟
body21001 = "{\"command\":\"spin\",\"token\":\"test2token1001\",\"data\":{\"game_id\":1001,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"

#37
body23700 = "{\"command\":\"spin\",\"token\":\"test2token3700\",\"data\":{\"game_id\":3700,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"

#38
body23800 = "{\"command\":\"spin\",\"token\":\"test2token3800\",\"data\":{\"game_id\":3800,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body23800buy = "{\"command\":\"spin\",\"token\":\"test2token3800\",\"data\":{\"game_id\":3800,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#ID agent-02 SPIN DATA
#16 slot
body31601 = "{\"command\":\"spin\",\"token\":\"test3token1601\",\"data\":{\"game_id\":1601,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body31602 = "{\"command\":\"spin\",\"token\":\"test3token1602\",\"data\":{\"game_id\":1602,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body31603 = "{\"command\":\"spin\",\"token\":\"test3token1603\",\"data\":{\"game_id\":1603,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body31604 = "{\"command\":\"spin\",\"token\":\"test3token1604\",\"data\":{\"game_id\":1604,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body31605 = "{\"command\":\"spin\",\"token\":\"test3token1605\",\"data\":{\"game_id\":1605,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body31606 = "{\"command\":\"spin\",\"token\":\"test3token1606\",\"data\":{\"game_id\":1606,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body31607 = "{\"command\":\"spin\",\"token\":\"test3token1607\",\"data\":{\"game_id\":1607,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
#scratch
body31700 = "{\"command\":\"spin\",\"token\":\"test3token1700\",\"data\":{\"game_id\":1700,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body31701 = "{\"command\":\"spin\",\"token\":\"test3token1701\",\"data\":{\"game_id\":1701,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body31811 = "{\"command\":\"spin\",\"token\":\"test3token1811\",\"data\":{\"game_id\":1811,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body31812 = "{\"command\":\"spin\",\"token\":\"test3token1812\",\"data\":{\"game_id\":1812,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
#18 fruit + 20 fruit
body31817 = "{\"command\":\"spin\",\"token\":\"test3token1817\",\"data\":{\"game_id\":1817,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
body31820 = "{\"command\":\"spin\",\"token\":\"test3token1820\",\"data\":{\"game_id\":1820,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
body32000 = "{\"command\":\"spin\",\"token\":\"test3token2000\",\"data\":{\"game_id\":2000,\"line_bet\":25,\"line_num\":8,\"coin_value\":10,\"bet_credit\":2000}}"
body32001 = "{\"command\":\"spin\",\"token\":\"test3token2001\",\"data\":{\"game_id\":2001,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
#18 slot
body31813 = "{\"command\":\"spin\",\"token\":\"test3token1813\",\"data\":{\"game_id\":1813,\"line_bet\":50,\"line_num\":15,\"coin_value\":3,\"bet_credit\":2250}}"
body31815 = "{\"command\":\"spin\",\"token\":\"test3token1815\",\"data\":{\"game_id\":1815,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
body31816 = "{\"command\":\"spin\",\"token\":\"test3token1816\",\"data\":{\"game_id\":1816,\"line_bet\":50,\"line_num\":40,\"coin_value\":1,\"bet_credit\":2000}}"
body31818 = "{\"command\":\"spin\",\"token\":\"test3token1818\",\"data\":{\"game_id\":1818,\"line_bet\":50,\"line_num\":9,\"coin_value\":5,\"bet_credit\":2250}}"
body31819 = "{\"command\":\"spin\",\"token\":\"test3token1819\",\"data\":{\"game_id\":1819,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body31822 = "{\"command\":\"spin\",\"token\":\"test3token1822\",\"data\":{\"game_id\":1822,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
#19 slot
body31900 = "{\"command\":\"spin\",\"token\":\"test3token1900\",\"data\":{\"game_id\":1900,\"line_bet\":25,\"line_num\":9,\"coin_value\":10,\"bet_credit\":2250}}"
body31901 = "{\"command\":\"spin\",\"token\":\"test3token1901\",\"data\":{\"game_id\":1901,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
body31902 = "{\"command\":\"spin\",\"token\":\"test3token1902\",\"data\":{\"game_id\":1902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000}}"
body31903 = "{\"command\":\"spin\",\"token\":\"test3token1903\",\"data\":{\"game_id\":1903,\"line_bet\":50,\"line_num\":9,\"coin_value\":5,\"bet_credit\":2250}}"
body31904 = "{\"command\":\"spin\",\"token\":\"test3token1904\",\"data\":{\"game_id\":1904,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body31905 = "{\"command\":\"spin\",\"token\":\"test3token1905\",\"data\":{\"game_id\":1905,\"line_bet\":25,\"line_num\":15,\"coin_value\":5,\"bet_credit\":1875}}"
body31906 = "{\"command\":\"spin\",\"token\":\"test3token1906\",\"data\":{\"game_id\":1906,\"line_bet\":25,\"line_num\":40,\"coin_value\":2,\"bet_credit\":2000}}"
body31907 = "{\"command\":\"spin\",\"token\":\"test3token1907\",\"data\":{\"game_id\":1907,\"line_bet\":50,\"line_num\":15,\"coin_value\":3,\"bet_credit\":2250}}"
body31908 = "{\"command\":\"spin\",\"token\":\"test3token1908\",\"data\":{\"game_id\":1908,\"line_bet\":25,\"line_num\":25,\"coin_value\":3,\"bet_credit\":1875}}"

#21 medusa
body32100 = "{\"command\":\"spin\",\"token\":\"test3token2100\",\"data\":{\"game_id\":2100,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body32101 = "{\"command\":\"spin\",\"token\":\"test3token2101\",\"data\":{\"game_id\":2101,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body32102 = "{\"command\":\"spin\",\"token\":\"test3token2102\",\"data\":{\"game_id\":2102,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body32103 = "{\"command\":\"spin\",\"token\":\"test3token2103\",\"data\":{\"game_id\":2103,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body32104 = "{\"command\":\"spin\",\"token\":\"test3token2104\",\"data\":{\"game_id\":2104,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#22 
body32200 = "{\"command\":\"spin\",\"token\":\"test3token2200\",\"data\":{\"game_id\":2200,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body32201 = "{\"command\":\"spin\",\"token\":\"test3token2201\",\"data\":{\"game_id\":2201,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body32202 = "{\"command\":\"spin\",\"token\":\"test3token2202\",\"data\":{\"game_id\":2202,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body32203 = "{\"command\":\"spin\",\"token\":\"test3token2203\",\"data\":{\"game_id\":2203,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#23 1 line
body32300 = "{\"command\":\"spin\",\"token\":\"test3token2300\",\"data\":{\"game_id\":2300,\"line_bet\":1000,\"line_num\":1,\"coin_value\":2,\"bet_credit\":2000}}"
body32301 = "{\"command\":\"spin\",\"token\":\"test3token2301\",\"data\":{\"game_id\":2301,\"line_bet\":1000,\"line_num\":1,\"coin_value\":2,\"bet_credit\":2000}}"
body32302 = "{\"command\":\"spin\",\"token\":\"test3token2302\",\"data\":{\"game_id\":2302,\"line_bet\":500,\"line_num\":1,\"coin_value\":4,\"bet_credit\":2000}}"
#24 right + left + buy free
body32400 = "{\"command\":\"spin\",\"token\":\"test3token2400\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body32400buy = "{\"command\":\"spin\",\"token\":\"test3token2400\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
body32401 = "{\"command\":\"spin\",\"token\":\"test3token2401\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body32401buy = "{\"command\":\"spin\",\"token\":\"test3token2401\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
body32402 = "{\"command\":\"spin\",\"token\":\"test3token2402\",\"data\":{\"game_id\":2402,\"line_bet\":25,\"line_num\":18,\"coin_value\":4,\"bet_credit\":1800,\"buy_spin\":0}}"
body32402buy = "{\"command\":\"spin\",\"token\":\"test3token2402\",\"data\":{\"game_id\":2402,\"line_bet\":25,\"line_num\":18,\"coin_value\":4,\"bet_credit\":1800,\"buy_spin\":1}}"
body32403 = "{\"command\":\"spin\",\"token\":\"test3token2403\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body32403buy = "{\"command\":\"spin\",\"token\":\"test3token2403\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
#25 grid
body32500 = "{\"command\":\"spin\",\"token\":\"test3token2500\",\"data\":{\"game_id\":2500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body32501 = "{\"command\":\"spin\",\"token\":\"test3token2501\",\"data\":{\"game_id\":2501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body32502 = "{\"command\":\"spin\",\"token\":\"test3token2502\",\"data\":{\"game_id\":2502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000}}"
body32503 = "{\"command\":\"spin\",\"token\":\"test3token2503\",\"data\":{\"game_id\":2503,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body32504 = "{\"command\":\"spin\",\"token\":\"test3token2504\",\"data\":{\"game_id\":2504,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
#26 hold and spin 1
body32600 = "{\"command\":\"spin\",\"token\":\"test3token2600\",\"data\":{\"game_id\":2600,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body32600buy = "{\"command\":\"spin\",\"token\":\"test3token2600\",\"data\":{\"game_id\":2600,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body32601 = "{\"command\":\"spin\",\"token\":\"test3token2601\",\"data\":{\"game_id\":2601,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body32601buy = "{\"command\":\"spin\",\"token\":\"test3token2601\",\"data\":{\"game_id\":2601,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body32602 = "{\"command\":\"spin\",\"token\":\"test3token2602\",\"data\":{\"game_id\":2602,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body32602buy = "{\"command\":\"spin\",\"token\":\"test3token2602\",\"data\":{\"game_id\":2602,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"
body32603 = "{\"command\":\"spin\",\"token\":\"test3token2603\",\"data\":{\"game_id\":2603,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body32603buy = "{\"command\":\"spin\",\"token\":\"test3token2603\",\"data\":{\"game_id\":2603,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#27 hold and spin 2
body32700 = "{\"command\":\"spin\",\"token\":\"test3token2700\",\"data\":{\"game_id\":2700,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body32700buy = "{\"command\":\"spin\",\"token\":\"test3token2700\",\"data\":{\"game_id\":2700,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body32701 = "{\"command\":\"spin\",\"token\":\"test3token2701\",\"data\":{\"game_id\":2701,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body32701buy = "{\"command\":\"spin\",\"token\":\"test3token2701\",\"data\":{\"game_id\":2701,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body32702 = "{\"command\":\"spin\",\"token\":\"test3token2702\",\"data\":{\"game_id\":2702,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body32702buy = "{\"command\":\"spin\",\"token\":\"test3token2702\",\"data\":{\"game_id\":2702,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"
body32703 = "{\"command\":\"spin\",\"token\":\"test3token2703\",\"data\":{\"game_id\":2703,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body32703buy = "{\"command\":\"spin\",\"token\":\"test3token2703\",\"data\":{\"game_id\":2703,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#28 medusa 2
body32800 = "{\"command\":\"spin\",\"token\":\"test3token2800\",\"data\":{\"game_id\":2800,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body32801 = "{\"command\":\"spin\",\"token\":\"test3token2801\",\"data\":{\"game_id\":2801,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body32802 = "{\"command\":\"spin\",\"token\":\"test3token2802\",\"data\":{\"game_id\":2802,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body32803 = "{\"command\":\"spin\",\"token\":\"test3token2803\",\"data\":{\"game_id\":2803,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body32804 = "{\"command\":\"spin\",\"token\":\"test3token2804\",\"data\":{\"game_id\":2804,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#29 grid 2 
body32900 = "{\"command\":\"spin\",\"token\":\"test3token2900\",\"data\":{\"game_id\":2900,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body32900buy = "{\"command\":\"spin\",\"token\":\"test3token2900\",\"data\":{\"game_id\":2900,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body32901 = "{\"command\":\"spin\",\"token\":\"test3token2901\",\"data\":{\"game_id\":2901,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body32901buy = "{\"command\":\"spin\",\"token\":\"test3token2901\",\"data\":{\"game_id\":2901,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body32902 = "{\"command\":\"spin\",\"token\":\"test3token2902\",\"data\":{\"game_id\":2902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body32902buy = "{\"command\":\"spin\",\"token\":\"test3token2902\",\"data\":{\"game_id\":2902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#30 slot aladin
body33000 = "{\"command\":\"spin\",\"token\":\"test3token3000\",\"data\":{\"game_id\":3000,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body33000buy = "{\"command\":\"spin\",\"token\":\"test3token3000\",\"data\":{\"game_id\":3000,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body33001 = "{\"command\":\"spin\",\"token\":\"test3token3001\",\"data\":{\"game_id\":3001,\"line_bet\":40,\"line_num\":50,\"coin_value\":1,\"bet_credit\":2000,\"buy_spin\":0}}"
body33001buy = "{\"command\":\"spin\",\"token\":\"test3token3001\",\"data\":{\"game_id\":3001,\"line_bet\":40,\"line_num\":50,\"coin_value\":1,\"bet_credit\":2000,\"buy_spin\":1}}"
body33002 = "{\"command\":\"spin\",\"token\":\"test3token3002\",\"data\":{\"game_id\":3002,\"line_bet\":20,\"line_num\":50,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body33002buy = "{\"command\":\"spin\",\"token\":\"test3token3002\",\"data\":{\"game_id\":3002,\"line_bet\":20,\"line_num\":50,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#31 slot arthur king
body33100 = "{\"command\":\"spin\",\"token\":\"test3token3100\",\"data\":{\"game_id\":3100,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body33100buy = "{\"command\":\"spin\",\"token\":\"test3token3100\",\"data\":{\"game_id\":3100,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body33101 = "{\"command\":\"spin\",\"token\":\"test3token3101\",\"data\":{\"game_id\":3101,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body33101buy = "{\"command\":\"spin\",\"token\":\"test3token3101\",\"data\":{\"game_id\":3101,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body33102 = "{\"command\":\"spin\",\"token\":\"test3token3102\",\"data\":{\"game_id\":3102,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":0}}"
body33102buy = "{\"command\":\"spin\",\"token\":\"test3token3102\",\"data\":{\"game_id\":3102,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":1}}"

#32 slot
body33200 = "{\"command\":\"spin\",\"token\":\"test3token3200\",\"data\":{\"game_id\":3200,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body33200buy = "{\"command\":\"spin\",\"token\":\"test3token3200\",\"data\":{\"game_id\":3200,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body33201 = "{\"command\":\"spin\",\"token\":\"test3token3201\",\"data\":{\"game_id\":3201,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body33201buy = "{\"command\":\"spin\",\"token\":\"test3token3201\",\"data\":{\"game_id\":3201,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body33202 = "{\"command\":\"spin\",\"token\":\"test3token3202\",\"data\":{\"game_id\":3202,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":0}}"
body33202buy = "{\"command\":\"spin\",\"token\":\"test3token3202\",\"data\":{\"game_id\":3202,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":1}}"

#33 slot
body33300 = "{\"command\":\"spin\",\"token\":\"test3token3300\",\"data\":{\"game_id\":3300,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body33300buy = "{\"command\":\"spin\",\"token\":\"test3token3300\",\"data\":{\"game_id\":3300,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body33301 = "{\"command\":\"spin\",\"token\":\"test3token3301\",\"data\":{\"game_id\":3301,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body33301buy = "{\"command\":\"spin\",\"token\":\"test3token3301\",\"data\":{\"game_id\":3301,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body33302 = "{\"command\":\"spin\",\"token\":\"test3token3302\",\"data\":{\"game_id\":3302,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body33302buy = "{\"command\":\"spin\",\"token\":\"test3token3302\",\"data\":{\"game_id\":3302,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#34 slot
body33400 = "{\"command\":\"spin\",\"token\":\"test3token3400\",\"data\":{\"game_id\":3400,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body33400buy = "{\"command\":\"spin\",\"token\":\"test3token3400\",\"data\":{\"game_id\":3400,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body33401 = "{\"command\":\"spin\",\"token\":\"test3token3401\",\"data\":{\"game_id\":3401,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body33401buy = "{\"command\":\"spin\",\"token\":\"test3token3401\",\"data\":{\"game_id\":3401,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body33402 = "{\"command\":\"spin\",\"token\":\"test3token3402\",\"data\":{\"game_id\":3402,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body33402buy = "{\"command\":\"spin\",\"token\":\"test3token3402\",\"data\":{\"game_id\":3402,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#35 grid
body33500 = "{\"command\":\"spin\",\"token\":\"test3token3500\",\"data\":{\"game_id\":3500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body33500buy = "{\"command\":\"spin\",\"token\":\"test3token3500\",\"data\":{\"game_id\":3500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body33501 = "{\"command\":\"spin\",\"token\":\"test3token3501\",\"data\":{\"game_id\":3501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body33501buy = "{\"command\":\"spin\",\"token\":\"test3token3501\",\"data\":{\"game_id\":3501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body33502 = "{\"command\":\"spin\",\"token\":\"test3token3502\",\"data\":{\"game_id\":3502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body33502buy = "{\"command\":\"spin\",\"token\":\"test3token3502\",\"data\":{\"game_id\":3502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#36 poker
body33600 = "{\"command\":\"spin\",\"token\":\"test3token3600\",\"data\":{\"game_id\":3600,\"line_bet\":200,\"line_num\":5,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"

#電竟
body31001 = "{\"command\":\"spin\",\"token\":\"test3token1001\",\"data\":{\"game_id\":1001,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"

#37
body33700 = "{\"command\":\"spin\",\"token\":\"test3token3700\",\"data\":{\"game_id\":3700,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"

#38
body33800 = "{\"command\":\"spin\",\"token\":\"test3token3800\",\"data\":{\"game_id\":3800,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body33800buy = "{\"command\":\"spin\",\"token\":\"test3token3800\",\"data\":{\"game_id\":3800,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#ID agent-03 SPIN DATA
#16 slot
body41601 = "{\"command\":\"spin\",\"token\":\"test4token1601\",\"data\":{\"game_id\":1601,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body41602 = "{\"command\":\"spin\",\"token\":\"test4token1602\",\"data\":{\"game_id\":1602,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body41603 = "{\"command\":\"spin\",\"token\":\"test4token1603\",\"data\":{\"game_id\":1603,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body41604 = "{\"command\":\"spin\",\"token\":\"test4token1604\",\"data\":{\"game_id\":1604,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body41605 = "{\"command\":\"spin\",\"token\":\"test4token1605\",\"data\":{\"game_id\":1605,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body41606 = "{\"command\":\"spin\",\"token\":\"test4token1606\",\"data\":{\"game_id\":1606,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body41607 = "{\"command\":\"spin\",\"token\":\"test4token1607\",\"data\":{\"game_id\":1607,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
#scratch
body41700 = "{\"command\":\"spin\",\"token\":\"test4token1700\",\"data\":{\"game_id\":1700,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body41701 = "{\"command\":\"spin\",\"token\":\"test4token1701\",\"data\":{\"game_id\":1701,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body41811 = "{\"command\":\"spin\",\"token\":\"test4token1811\",\"data\":{\"game_id\":1811,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
body41812 = "{\"command\":\"spin\",\"token\":\"test4token1812\",\"data\":{\"game_id\":1812,\"line_bet\":500,\"line_num\":7,\"coin_value\":1,\"bet_credit\":3500}}"
#18 fruit + 20 fruit
body41817 = "{\"command\":\"spin\",\"token\":\"test4token1817\",\"data\":{\"game_id\":1817,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
body41820 = "{\"command\":\"spin\",\"token\":\"test4token1820\",\"data\":{\"game_id\":1820,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
body42000 = "{\"command\":\"spin\",\"token\":\"test4token2000\",\"data\":{\"game_id\":2000,\"line_bet\":25,\"line_num\":8,\"coin_value\":10,\"bet_credit\":2000}}"
body42001 = "{\"command\":\"spin\",\"token\":\"test4token2001\",\"data\":{\"game_id\":2001,\"line_bet\":50,\"line_num\":8,\"coin_value\":5,\"bet_credit\":2000}}"
#18 slot
body41813 = "{\"command\":\"spin\",\"token\":\"test4token1813\",\"data\":{\"game_id\":1813,\"line_bet\":50,\"line_num\":15,\"coin_value\":3,\"bet_credit\":2250}}"
body41815 = "{\"command\":\"spin\",\"token\":\"test4token1815\",\"data\":{\"game_id\":1815,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
body41816 = "{\"command\":\"spin\",\"token\":\"test4token1816\",\"data\":{\"game_id\":1816,\"line_bet\":50,\"line_num\":40,\"coin_value\":1,\"bet_credit\":2000}}"
body41818 = "{\"command\":\"spin\",\"token\":\"test4token1818\",\"data\":{\"game_id\":1818,\"line_bet\":50,\"line_num\":9,\"coin_value\":5,\"bet_credit\":2250}}"
body41819 = "{\"command\":\"spin\",\"token\":\"test4token1819\",\"data\":{\"game_id\":1819,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body41822 = "{\"command\":\"spin\",\"token\":\"test4token1822\",\"data\":{\"game_id\":1822,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
#19 slot
body41900 = "{\"command\":\"spin\",\"token\":\"test4token1900\",\"data\":{\"game_id\":1900,\"line_bet\":25,\"line_num\":9,\"coin_value\":10,\"bet_credit\":2250}}"
body41901 = "{\"command\":\"spin\",\"token\":\"test4token1901\",\"data\":{\"game_id\":1901,\"line_bet\":50,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2500}}"
body41902 = "{\"command\":\"spin\",\"token\":\"test4token1902\",\"data\":{\"game_id\":1902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000}}"
body41903 = "{\"command\":\"spin\",\"token\":\"test4token1903\",\"data\":{\"game_id\":1903,\"line_bet\":50,\"line_num\":9,\"coin_value\":5,\"bet_credit\":2250}}"
body41904 = "{\"command\":\"spin\",\"token\":\"test4token1904\",\"data\":{\"game_id\":1904,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body41905 = "{\"command\":\"spin\",\"token\":\"test4token1905\",\"data\":{\"game_id\":1905,\"line_bet\":25,\"line_num\":15,\"coin_value\":5,\"bet_credit\":1875}}"
body41906 = "{\"command\":\"spin\",\"token\":\"test4token1906\",\"data\":{\"game_id\":1906,\"line_bet\":25,\"line_num\":40,\"coin_value\":2,\"bet_credit\":2000}}"
body41907 = "{\"command\":\"spin\",\"token\":\"test4token1907\",\"data\":{\"game_id\":1907,\"line_bet\":50,\"line_num\":15,\"coin_value\":3,\"bet_credit\":2250}}"
body41908 = "{\"command\":\"spin\",\"token\":\"test4token1908\",\"data\":{\"game_id\":1908,\"line_bet\":25,\"line_num\":25,\"coin_value\":3,\"bet_credit\":1875}}"

#21 medusa
body42100 = "{\"command\":\"spin\",\"token\":\"test4token2100\",\"data\":{\"game_id\":2100,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body42101 = "{\"command\":\"spin\",\"token\":\"test4token2101\",\"data\":{\"game_id\":2101,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body42102 = "{\"command\":\"spin\",\"token\":\"test4token2102\",\"data\":{\"game_id\":2102,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body42103 = "{\"command\":\"spin\",\"token\":\"test4token2103\",\"data\":{\"game_id\":2103,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body42104 = "{\"command\":\"spin\",\"token\":\"test4token2104\",\"data\":{\"game_id\":2104,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#22 
body42200 = "{\"command\":\"spin\",\"token\":\"test4token2200\",\"data\":{\"game_id\":2200,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body42201 = "{\"command\":\"spin\",\"token\":\"test4token2201\",\"data\":{\"game_id\":2201,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body42202 = "{\"command\":\"spin\",\"token\":\"test4token2202\",\"data\":{\"game_id\":2202,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body42203 = "{\"command\":\"spin\",\"token\":\"test4token2203\",\"data\":{\"game_id\":2203,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#23 1 line
body42300 = "{\"command\":\"spin\",\"token\":\"test4token2300\",\"data\":{\"game_id\":2300,\"line_bet\":1000,\"line_num\":1,\"coin_value\":2,\"bet_credit\":2000}}"
body42301 = "{\"command\":\"spin\",\"token\":\"test4token2301\",\"data\":{\"game_id\":2301,\"line_bet\":1000,\"line_num\":1,\"coin_value\":2,\"bet_credit\":2000}}"
body42302 = "{\"command\":\"spin\",\"token\":\"test4token2302\",\"data\":{\"game_id\":2302,\"line_bet\":500,\"line_num\":1,\"coin_value\":4,\"bet_credit\":2000}}"
#24 right + left + buy free
body42400 = "{\"command\":\"spin\",\"token\":\"test4token2400\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body42400buy = "{\"command\":\"spin\",\"token\":\"test4token2400\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
body42401 = "{\"command\":\"spin\",\"token\":\"test4token2401\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body42401buy = "{\"command\":\"spin\",\"token\":\"test4token2401\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
body42402 = "{\"command\":\"spin\",\"token\":\"test4token2402\",\"data\":{\"game_id\":2402,\"line_bet\":25,\"line_num\":18,\"coin_value\":4,\"bet_credit\":1800,\"buy_spin\":0}}"
body42402buy = "{\"command\":\"spin\",\"token\":\"test4token2402\",\"data\":{\"game_id\":2402,\"line_bet\":25,\"line_num\":18,\"coin_value\":4,\"bet_credit\":1800,\"buy_spin\":1}}"
body42403 = "{\"command\":\"spin\",\"token\":\"test4token2403\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":0}}"
body42403buy = "{\"command\":\"spin\",\"token\":\"test4token2403\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":2,\"bet_credit\":1800,\"buy_spin\":1}}"
#25 grid
body42500 = "{\"command\":\"spin\",\"token\":\"test4token2500\",\"data\":{\"game_id\":2500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body42501 = "{\"command\":\"spin\",\"token\":\"test4token2501\",\"data\":{\"game_id\":2501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body42502 = "{\"command\":\"spin\",\"token\":\"test4token2502\",\"data\":{\"game_id\":2502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000}}"
body42503 = "{\"command\":\"spin\",\"token\":\"test4token2503\",\"data\":{\"game_id\":2503,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
body42504 = "{\"command\":\"spin\",\"token\":\"test4token2504\",\"data\":{\"game_id\":2504,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"
#26 hold and spin 1
body42600 = "{\"command\":\"spin\",\"token\":\"test4token2600\",\"data\":{\"game_id\":2600,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body42600buy = "{\"command\":\"spin\",\"token\":\"test4token2600\",\"data\":{\"game_id\":2600,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body42601 = "{\"command\":\"spin\",\"token\":\"test4token2601\",\"data\":{\"game_id\":2601,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body42601buy = "{\"command\":\"spin\",\"token\":\"test4token2601\",\"data\":{\"game_id\":2601,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body42602 = "{\"command\":\"spin\",\"token\":\"test4token2602\",\"data\":{\"game_id\":2602,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body42602buy = "{\"command\":\"spin\",\"token\":\"test4token2602\",\"data\":{\"game_id\":2602,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"
body42603 = "{\"command\":\"spin\",\"token\":\"test4token2603\",\"data\":{\"game_id\":2603,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body42603buy = "{\"command\":\"spin\",\"token\":\"test4token2603\",\"data\":{\"game_id\":2603,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#27 hold and spin 2
body42700 = "{\"command\":\"spin\",\"token\":\"test4token2700\",\"data\":{\"game_id\":2700,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body42700buy = "{\"command\":\"spin\",\"token\":\"test4token2700\",\"data\":{\"game_id\":2700,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body42701 = "{\"command\":\"spin\",\"token\":\"test4token2701\",\"data\":{\"game_id\":2701,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body42701buy = "{\"command\":\"spin\",\"token\":\"test4token2701\",\"data\":{\"game_id\":2701,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body42702 = "{\"command\":\"spin\",\"token\":\"test4token2702\",\"data\":{\"game_id\":2702,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body42702buy = "{\"command\":\"spin\",\"token\":\"test4token2702\",\"data\":{\"game_id\":2702,\"line_bet\":20,\"line_num\":25,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"
body42703 = "{\"command\":\"spin\",\"token\":\"test4token2703\",\"data\":{\"game_id\":2703,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body42703buy = "{\"command\":\"spin\",\"token\":\"test4token2703\",\"data\":{\"game_id\":2703,\"line_bet\":40,\"line_num\":25,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#28 medusa 2
body42800 = "{\"command\":\"spin\",\"token\":\"test4token2800\",\"data\":{\"game_id\":2800,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body42801 = "{\"command\":\"spin\",\"token\":\"test4token2801\",\"data\":{\"game_id\":2801,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body42802 = "{\"command\":\"spin\",\"token\":\"test4token2802\",\"data\":{\"game_id\":2802,\"line_bet\":50,\"line_num\":5,\"coin_value\":8,\"bet_credit\":2000}}"
body42803 = "{\"command\":\"spin\",\"token\":\"test4token2803\",\"data\":{\"game_id\":2803,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
body42804 = "{\"command\":\"spin\",\"token\":\"test4token2804\",\"data\":{\"game_id\":2804,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"
#29 grid 2 
body42900 = "{\"command\":\"spin\",\"token\":\"test4token2900\",\"data\":{\"game_id\":2900,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body42900buy = "{\"command\":\"spin\",\"token\":\"test4token2900\",\"data\":{\"game_id\":2900,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body42901 = "{\"command\":\"spin\",\"token\":\"test4token2901\",\"data\":{\"game_id\":2901,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body42901buy = "{\"command\":\"spin\",\"token\":\"test4token2901\",\"data\":{\"game_id\":2901,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body42902 = "{\"command\":\"spin\",\"token\":\"test4token2902\",\"data\":{\"game_id\":2902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body42902buy = "{\"command\":\"spin\",\"token\":\"test4token2902\",\"data\":{\"game_id\":2902,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#30 slot aladin
body43000 = "{\"command\":\"spin\",\"token\":\"test4token3000\",\"data\":{\"game_id\":3000,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body43000buy = "{\"command\":\"spin\",\"token\":\"test4token3000\",\"data\":{\"game_id\":3000,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body43001 = "{\"command\":\"spin\",\"token\":\"test4token3001\",\"data\":{\"game_id\":3001,\"line_bet\":40,\"line_num\":50,\"coin_value\":1,\"bet_credit\":2000,\"buy_spin\":0}}"
body43001buy = "{\"command\":\"spin\",\"token\":\"test4token3001\",\"data\":{\"game_id\":3001,\"line_bet\":40,\"line_num\":50,\"coin_value\":1,\"bet_credit\":2000,\"buy_spin\":1}}"
body43002 = "{\"command\":\"spin\",\"token\":\"test4token3002\",\"data\":{\"game_id\":3002,\"line_bet\":20,\"line_num\":50,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body43002buy = "{\"command\":\"spin\",\"token\":\"test4token3002\",\"data\":{\"game_id\":3002,\"line_bet\":20,\"line_num\":50,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#31 slot arthur king
body43100 = "{\"command\":\"spin\",\"token\":\"test4token3100\",\"data\":{\"game_id\":3100,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body43100buy = "{\"command\":\"spin\",\"token\":\"test4token3100\",\"data\":{\"game_id\":3100,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body43101 = "{\"command\":\"spin\",\"token\":\"test4token3101\",\"data\":{\"game_id\":3101,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body43101buy = "{\"command\":\"spin\",\"token\":\"test4token3101\",\"data\":{\"game_id\":3101,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body43102 = "{\"command\":\"spin\",\"token\":\"test4token3102\",\"data\":{\"game_id\":3102,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":0}}"
body43102buy = "{\"command\":\"spin\",\"token\":\"test4token3102\",\"data\":{\"game_id\":3102,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":1}}"

#32 slot
body43200 = "{\"command\":\"spin\",\"token\":\"test4token3200\",\"data\":{\"game_id\":3200,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body43200buy = "{\"command\":\"spin\",\"token\":\"test4token3200\",\"data\":{\"game_id\":3200,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body43201 = "{\"command\":\"spin\",\"token\":\"test4token3201\",\"data\":{\"game_id\":3201,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":0}}"
body43201buy = "{\"command\":\"spin\",\"token\":\"test4token3201\",\"data\":{\"game_id\":3201,\"line_bet\":40,\"line_num\":50,\"coin_value\":2,\"bet_credit\":4000,\"buy_spin\":1}}"
body43202 = "{\"command\":\"spin\",\"token\":\"test4token3202\",\"data\":{\"game_id\":3202,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":0}}"
body43202buy = "{\"command\":\"spin\",\"token\":\"test4token3202\",\"data\":{\"game_id\":3202,\"line_bet\":20,\"line_num\":50,\"coin_value\":4,\"bet_credit\":4000,\"buy_spin\":1}}"

#33 slot
body43300 = "{\"command\":\"spin\",\"token\":\"test4token3300\",\"data\":{\"game_id\":3300,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body43300buy = "{\"command\":\"spin\",\"token\":\"test4token3300\",\"data\":{\"game_id\":3300,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body43301 = "{\"command\":\"spin\",\"token\":\"test4token3301\",\"data\":{\"game_id\":3301,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body43301buy = "{\"command\":\"spin\",\"token\":\"test4token3301\",\"data\":{\"game_id\":3301,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body43302 = "{\"command\":\"spin\",\"token\":\"test4token3302\",\"data\":{\"game_id\":3302,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body43302buy = "{\"command\":\"spin\",\"token\":\"test4token3302\",\"data\":{\"game_id\":3302,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#34 slot
body43400 = "{\"command\":\"spin\",\"token\":\"test4token3400\",\"data\":{\"game_id\":3400,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body43400buy = "{\"command\":\"spin\",\"token\":\"test4token3400\",\"data\":{\"game_id\":3400,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body43401 = "{\"command\":\"spin\",\"token\":\"test4token3401\",\"data\":{\"game_id\":3401,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body43401buy = "{\"command\":\"spin\",\"token\":\"test4token3401\",\"data\":{\"game_id\":3401,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body43402 = "{\"command\":\"spin\",\"token\":\"test4token3402\",\"data\":{\"game_id\":3402,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body43402buy = "{\"command\":\"spin\",\"token\":\"test4token3402\",\"data\":{\"game_id\":3402,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#35 grid
body43500 = "{\"command\":\"spin\",\"token\":\"test4token3500\",\"data\":{\"game_id\":3500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body43500buy = "{\"command\":\"spin\",\"token\":\"test4token3500\",\"data\":{\"game_id\":3500,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body43501 = "{\"command\":\"spin\",\"token\":\"test4token3501\",\"data\":{\"game_id\":3501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body43501buy = "{\"command\":\"spin\",\"token\":\"test4token3501\",\"data\":{\"game_id\":3501,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"
body43502 = "{\"command\":\"spin\",\"token\":\"test4token3502\",\"data\":{\"game_id\":3502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":0}}"
body43502buy = "{\"command\":\"spin\",\"token\":\"test4token3502\",\"data\":{\"game_id\":3502,\"line_bet\":25,\"line_num\":20,\"coin_value\":4,\"bet_credit\":2000,\"buy_spin\":1}}"

#36 poker
body43600 = "{\"command\":\"spin\",\"token\":\"test4token3600\",\"data\":{\"game_id\":3600,\"line_bet\":200,\"line_num\":5,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"

#電竟
body41001 = "{\"command\":\"spin\",\"token\":\"test4token1001\",\"data\":{\"game_id\":1001,\"line_bet\":100,\"line_num\":5,\"coin_value\":4,\"bet_credit\":2000}}"

#37
body43700 = "{\"command\":\"spin\",\"token\":\"test4token3700\",\"data\":{\"game_id\":3700,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"

#38
body43800 = "{\"command\":\"spin\",\"token\":\"test4token3800\",\"data\":{\"game_id\":3800,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
body43800buy = "{\"command\":\"spin\",\"token\":\"test4token3800\",\"data\":{\"game_id\":3800,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":1}}"

#PHP SPIN DATA
#21
bodyph2100 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2100,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.004,\"bet_credit\":4}}"
bodyph2101 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2101,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.004,\"bet_credit\":4}}"
bodyph2102 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2102,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.004,\"bet_credit\":4}}"
bodyph2103 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2103,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.004,\"bet_credit\":4}}"
bodyph2104 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2104,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.004,\"bet_credit\":4}}"

#22 
bodyph2200 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2200,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.002,\"bet_credit\":2}}"
bodyph2201 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2201,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.002,\"bet_credit\":2}}"
bodyph2202 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2202,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.002,\"bet_credit\":2}}"
bodyph2203 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2203,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.002,\"bet_credit\":2}}"

#23 1 line
bodyph2300 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2300,\"line_bet\":1000,\"line_num\":1,\"coin_value\":0.002,\"bet_credit\":2}}"
bodyph2301 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2301,\"line_bet\":1000,\"line_num\":1,\"coin_value\":0.002,\"bet_credit\":2}}"
bodyph2302 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2302,\"line_bet\":1000,\"line_num\":1,\"coin_value\":0.002,\"bet_credit\":2}}"

#24 right + left + buy free
bodyph2400 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":0}}"
bodyph2400buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":1}}"
bodyph2401 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":0}}"
bodyph2401buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":1}}"
bodyph2402 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2402,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":0}}"
bodyph2402buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2402,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":1}}"
bodyph2403 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":0}}"
bodyph2403buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":1}}"

#25 grid
bodyph2500 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2500,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2}}"
bodyph2501 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2501,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2}}"
bodyph2502 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2502,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2}}"
bodyph2503 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2503,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2}}"
bodyph2504 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2504,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2}}"

#26 hold and spin 1
bodyph2600 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2600,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph2600buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2600,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"
bodyph2601 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2601,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph2601buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2601,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"
bodyph2602 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2602,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph2602buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2602,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"
bodyph2603 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2603,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph2603buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2603,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"

#27 hold and spin 2
bodyph2700 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2700,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph2700buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2700,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"
bodyph2701 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2701,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph2701buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2701,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"
bodyph2702 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2702,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph2702buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2702,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"
bodyph2703 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2703,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph2703buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2703,\"line_bet\":40,\"line_num\":25,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"

#28 medusa 2
bodyph2800 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2800,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.004,\"bet_credit\":4}}"
bodyph2801 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2801,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.004,\"bet_credit\":4}}"
bodyph2802 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2802,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.004,\"bet_credit\":4}}"
bodyph2803 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2803,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.004,\"bet_credit\":4}}"
bodyph2804 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2804,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.004,\"bet_credit\":4}}"

#29 grid 2 
bodyph2900 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2900,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph2900buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2900,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"
bodyph2901 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2901,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph2901buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2901,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"
bodyph2902 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2902,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph2902buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2902,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"

#30 slot aladin
bodyph3000 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3000,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3000buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3000,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"
bodyph3001 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3001,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3001buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3001,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"
bodyph3002 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3002,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3002buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3002,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"

#31 slot arthur king
bodyph3100 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3100,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3100buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3100,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"
bodyph3101 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3101,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3101buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3101,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"
bodyph3102 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3102,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3102buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3102,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"

#32 slot
bodyph3200 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3200,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3200buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3200,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"
bodyph3201 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3201,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3201buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3201,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"
bodyph3202 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3202,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3202buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3202,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"

#33 slot
bodyph3300 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3300,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph3300buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3300,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"
bodyph3301 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3301,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph3301buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3301,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"
bodyph3302 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3302,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph3302buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3302,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"

#34 slot
bodyph3400 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3400,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph3400buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3400,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"
bodyph3401 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3401,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph3401buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3401,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"
bodyph3402 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3402,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph3402buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3402,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"

#35 grid
bodyph3500 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3500,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3500buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3500,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"
bodyph3501 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3501,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3501buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3501,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"
bodyph3502 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3502,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
bodyph3502buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3502,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":1}}"

#36 poker
bodyph3600 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3600,\"line_bet\":200,\"line_num\":5,\"coin_value\":0.002,\"bet_credit\":2,\"buy_spin\":0}}"
#37
bodyph3700 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3700,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000,\"buy_spin\":0}}"
#38
bodyph3800 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3800,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":0}}"
bodyph3800buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3800,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.004,\"bet_credit\":4,\"buy_spin\":1}}"

#KO SPIN DATA
#21
bodykr2100 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2100,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2101 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2101,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2102 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2102,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2103 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2103,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2104 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2104,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
#22 
bodykr2200 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2200,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2201 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2201,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2202 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2202,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2203 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2203,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
#23 1 line
bodykr2300 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2300,\"line_bet\":400,\"line_num\":1,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2301 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2301,\"line_bet\":400,\"line_num\":1,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2302 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2302,\"line_bet\":400,\"line_num\":1,\"coin_value\":5,\"bet_credit\":2000}}"
#24 right + left + buy free
bodykr2400 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":0}}"
bodykr2400buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2400,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":1}}"
bodykr2401 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":0}}"
bodykr2401buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2401,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":1}}"
bodykr2402 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2402,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":0}}"
bodykr2402buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2402,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":1}}"
bodykr2403 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":0}}"
bodykr2403buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2403,\"line_bet\":50,\"line_num\":18,\"coin_value\":0.002,\"bet_credit\":1.8,\"buy_spin\":1}}"
#25 grid
bodykr2500 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2500,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2}}"
bodykr2501 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2501,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2}}"
bodykr2502 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2502,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2}}"
bodykr2503 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2503,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2}}"
bodykr2504 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2504,\"line_bet\":50,\"line_num\":20,\"coin_value\":0.002,\"bet_credit\":2}}"
#26 hold and spin 1
bodykr2600 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2600,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr2600buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2600,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr2601 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2601,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr2601buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2601,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr2602 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2602,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr2602buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2602,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr2603 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2603,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr2603buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2603,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
#27 hold and spin 2
bodykr2700 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2700,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr2700buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2700,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr2701 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2701,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr2701buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2701,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr2702 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2702,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr2702buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2702,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr2703 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2703,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr2703buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2703,\"line_bet\":16,\"line_num\":25,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
#28 medusa 2
bodykr2800 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2800,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2801 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2801,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2802 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2802,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2803 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2803,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
bodykr2804 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2804,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000}}"
#29 grid 2 
bodykr2900 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2900,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr2900buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2900,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr2901 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2901,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr2901buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2901,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr2902 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2902,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr2902buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2902,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
#30 slot aladin
bodykr3000 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3000,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3000buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3000,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3001 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3001,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3001buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3001,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3002 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3002,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3002buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3002,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"

#31 slot arthur king
bodykr3100 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3100,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3100buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3100,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3101 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3101,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3101buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3101,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3102 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3102,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3102buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3102,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"

#32 slot
bodykr3200 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3200,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3200buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3200,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3201 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3201,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3201buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3201,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3202 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3202,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3202buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3202,\"line_bet\":8,\"line_num\":50,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"

#33 slot
bodykr3300 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3300,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3300buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3300,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3301 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3301,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3301buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3301,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3302 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3302,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3302buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3302,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"

#34 slot
bodykr3400 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3400,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3400buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3400,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3401 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3401,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3401buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3401,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3402 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3402,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3402buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3402,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"

#35 grid
bodykr3500 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3500,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3500buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3500,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3501 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3501,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3501buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3501,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"
bodykr3502 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3502,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"
bodykr3502buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3502,\"line_bet\":20,\"line_num\":20,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":1}}"

#36 poker
bodykr3600 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3600,\"line_bet\":80,\"line_num\":5,\"coin_value\":5,\"bet_credit\":2000,\"buy_spin\":0}}"

#th SPIN DATA
#16 slot
bodyth1601 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1601,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth1602 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1602,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth1603 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1603,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth1604 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1604,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth1605 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1605,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth1606 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1606,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth1607 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":1607,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5}}"

#20 fruit
bodyth2001 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2001,\"line_bet\":50,\"line_num\":8,\"coin_value\":0.01,\"bet_credit\":4}}"

#21 medusa
bodyth2100 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2100,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2101 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2101,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2102 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2102,\"line_bet\":50,\"line_num\":5,\"coin_value\":0.02,\"bet_credit\":5}}"
bodyth2103 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2103,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2104 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2104,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5}}"
#22 
bodyth2200 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2200,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2201 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2201,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2202 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2202,\"line_bet\":50,\"line_num\":5,\"coin_value\":0.02,\"bet_credit\":5}}"
bodyth2203 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2203,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5}}"
#23 1 line
bodyth2300 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2300,\"line_bet\":500,\"line_num\":1,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2301 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2301,\"line_bet\":500,\"line_num\":1,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2302 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2302,\"line_bet\":250,\"line_num\":1,\"coin_value\":0.02,\"bet_credit\":5}}"
#24 right + left + buy free
bodyth2400 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2400,\"line_bet\":25,\"line_num\":18,\"coin_value\":0.01,\"bet_credit\":4.5,\"buy_spin\":0}}"
bodyth2400buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2400,\"line_bet\":25,\"line_num\":18,\"coin_value\":0.01,\"bet_credit\":4.5,\"buy_spin\":1}}"
bodyth2401 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2401,\"line_bet\":25,\"line_num\":18,\"coin_value\":0.01,\"bet_credit\":4.5,\"buy_spin\":0}}"
bodyth2401buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2401,\"line_bet\":25,\"line_num\":18,\"coin_value\":0.01,\"bet_credit\":4.5,\"buy_spin\":1}}"
bodyth2402 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2402,\"line_bet\":10,\"line_num\":18,\"coin_value\":0.01,\"bet_credit\":1.8,\"buy_spin\":0}}"
bodyth2402buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2402,\"line_bet\":10,\"line_num\":18,\"coin_value\":0.01,\"bet_credit\":1.8,\"buy_spin\":1}}"
bodyth2403 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2403,\"line_bet\":25,\"line_num\":18,\"coin_value\":0.01,\"bet_credit\":4.5,\"buy_spin\":0}}"
bodyth2403buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2403,\"line_bet\":25,\"line_num\":18,\"coin_value\":0.01,\"bet_credit\":4.5,\"buy_spin\":1}}"
#25 grid
bodyth2500 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2500,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2501 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2501,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2502 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2502,\"line_bet\":10,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":2}}"
bodyth2503 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2503,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2504 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2504,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5}}"
#26 hold and spin 1
bodyth2600 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2600,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth2600buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2600,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth2601 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2601,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth2601buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2601,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth2602 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2602,\"line_bet\":10,\"line_num\":25,\"coin_value\":0.02,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth2602buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2602,\"line_bet\":10,\"line_num\":25,\"coin_value\":0.02,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth2603 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2603,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth2603buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2603,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"

#27 hold and spin 2
bodyth2700 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2700,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth2700buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2700,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth2701 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2701,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth2701buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2701,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth2702 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2702,\"line_bet\":10,\"line_num\":25,\"coin_value\":0.02,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth2702buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2702,\"line_bet\":10,\"line_num\":25,\"coin_value\":0.02,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth2703 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2703,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth2703buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2703,\"line_bet\":20,\"line_num\":25,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"

#28 medusa 2
bodyth2800 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2800,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2801 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2801,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2802 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2802,\"line_bet\":50,\"line_num\":5,\"coin_value\":0.02,\"bet_credit\":5}}"
bodyth2803 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2803,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5}}"
bodyth2804 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2804,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5}}"
#29 grid 2 
bodyth2900 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2900,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth2900buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2900,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth2901 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2901,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth2901buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2901,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth2902 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2902,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth2902buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":2902,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"

#30 slot aladin
bodyth3000 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3000,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3000buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3000,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth3001 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3001,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3001buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3001,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth3002 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3002,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3002buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3002,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"

#31 slot arthur king
bodyth3100 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3100,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3100buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3100,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth3101 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3101,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3101buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3101,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth3102 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3102,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3102buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3102,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"

#32 slot
bodyth3200 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3200,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.01,\"bet_credit\":10,\"buy_spin\":0}}"
bodyth3200buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3200,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.01,\"bet_credit\":10,\"buy_spin\":1}}"
bodyth3201 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3201,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.01,\"bet_credit\":10,\"buy_spin\":0}}"
bodyth3201buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3201,\"line_bet\":20,\"line_num\":50,\"coin_value\":0.01,\"bet_credit\":10,\"buy_spin\":1}}"
bodyth3202 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3202,\"line_bet\":10,\"line_num\":50,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3202buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3202,\"line_bet\":10,\"line_num\":50,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"

#33 slot
bodyth3300 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3300,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3300buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3300,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth3301 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3301,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3301buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3301,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth3302 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3302,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3302buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3302,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"

#34 slot
bodyth3400 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3400,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3400buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3400,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth3401 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3401,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3401buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3401,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth3402 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3402,\"line_bet\":10,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":3,\"buy_spin\":0}}"
bodyth3402buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3402,\"line_bet\":10,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":3,\"buy_spin\":1}}"

#35 grid
bodyth3500 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3500,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3500buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3500,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth3501 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3501,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3501buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3501,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"
bodyth3502 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3502,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3502buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3502,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"

#36 poker
bodyth3600 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3600,\"line_bet\":100,\"line_num\":5,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"

#37
bodyth3700 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3700,\"line_bet\":50,\"line_num\":20,\"coin_value\":2,\"bet_credit\":2000}}"

#38
bodyth3800 = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3800,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":0}}"
bodyth3800buy = "{\"command\":\"spin\",\"token\":\"<ACCOUNT>\",\"data\":{\"game_id\":3800,\"line_bet\":25,\"line_num\":20,\"coin_value\":0.01,\"bet_credit\":5,\"buy_spin\":1}}"

headerdemo = {
  'Host': 'example.internal',
  'Accept': '*/*',
  'Content-Type': 'text/plain;charset=UTF-8',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

headerdemothx2 = {
  'Host': 'example.internal',
  'Accept': '*/*',
  'Content-Type': 'text/plain;charset=UTF-8',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

headerdemophp2 = {
  'Host': 'example.internal',
  'Accept': '*/*',
  'Content-Type': 'text/plain;charset=UTF-8',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

headersta = {
  'Host': 'example.internal',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
  'Accept': '*/*',
  'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-Type': 'text/plain;charset=UTF-8',
  'Content-Length': '178',
  'DNT': '1',
  'Connection': 'keep-alive',
  'TE': 'Trailers'
}

headerlab = {
  'Host': 'example.internal',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
  'Accept': '*/*',
  'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-Type': 'text/plain;charset=UTF-8',
  'Content-Length': '178',
  'DNT': '1',
  'Connection': 'keep-alive',
  'TE': 'Trailers'
}

url = urldemo
#使用lab game server
headers = headerdemo
#使用lab request

def IDspin (spintime) : 
  for i in range(spintime):
    rclose = requests.request("POST", url, headers={'Connection':'close'},verify=False)
    r1 = requests.request("POST", url, headers=headers, data = body1601)
    print(r1.text.encode('utf8'))
    r2 = requests.request("POST", url, headers=headers, data = body1602)
    r3 = requests.request("POST", url, headers=headers, data = body1603)
    r4 = requests.request("POST", url, headers=headers, data = body1604)
    r5 = requests.request("POST", url, headers=headers, data = body1605)
    r6 = requests.request("POST", url, headers=headers, data = body1606)
    r7 = requests.request("POST", url, headers=headers, data = body1607)
    r8 = requests.request("POST", url, headers=headers, data = body1700)
    r9 = requests.request("POST", url, headers=headers, data = body1701)
    r10 = requests.request("POST", url, headers=headers, data = body1811)
    r11 = requests.request("POST", url, headers=headers, data = body1812)
    r12 = requests.request("POST", url, headers=headers, data = body1817)
    r13 = requests.request("POST", url, headers=headers, data = body1820)
    r14 = requests.request("POST", url, headers=headers, data = body2000)
    r15 = requests.request("POST", url, headers=headers, data = body2001)
    r16 = requests.request("POST", url, headers=headers, data = body1813)
    r17 = requests.request("POST", url, headers=headers, data = body1815)
    r18 = requests.request("POST", url, headers=headers, data = body1816)
    r19 = requests.request("POST", url, headers=headers, data = body1818)
    r20 = requests.request("POST", url, headers=headers, data = body1819)
    r21 = requests.request("POST", url, headers=headers, data = body1822)
    r22 = requests.request("POST", url, headers=headers, data = body1900)
    r23 = requests.request("POST", url, headers=headers, data = body1901)
    r24 = requests.request("POST", url, headers=headers, data = body1902)
    r25 = requests.request("POST", url, headers=headers, data = body1903)
    r26 = requests.request("POST", url, headers=headers, data = body1904)
    r27 = requests.request("POST", url, headers=headers, data = body1905)
    r28 = requests.request("POST", url, headers=headers, data = body1906)
    r29 = requests.request("POST", url, headers=headers, data = body1907)
    r30 = requests.request("POST", url, headers=headers, data = body1908)
    r31 = requests.request("POST", url, headers=headers, data = body2100)
    r32 = requests.request("POST", url, headers=headers, data = body2101)
    r33 = requests.request("POST", url, headers=headers, data = body2102)
    r34 = requests.request("POST", url, headers=headers, data = body2103)
    r35 = requests.request("POST", url, headers=headers, data = body2104)
    r36 = requests.request("POST", url, headers=headers, data = body2200)
    r37 = requests.request("POST", url, headers=headers, data = body2201)
    r38 = requests.request("POST", url, headers=headers, data = body2202)
    r39 = requests.request("POST", url, headers=headers, data = body2203)
    r40 = requests.request("POST", url, headers=headers, data = body2300)
    r41 = requests.request("POST", url, headers=headers, data = body2301)
    r42 = requests.request("POST", url, headers=headers, data = body2302)
    r43 = requests.request("POST", url, headers=headers, data = body2400)
    r44 = requests.request("POST", url, headers=headers, data = body2400buy)
    r45 = requests.request("POST", url, headers=headers, data = body2401)
    r46 = requests.request("POST", url, headers=headers, data = body2401buy)
    r47 = requests.request("POST", url, headers=headers, data = body2402)
    r48 = requests.request("POST", url, headers=headers, data = body2402buy)
    r49 = requests.request("POST", url, headers=headers, data = body2403)
    r50 = requests.request("POST", url, headers=headers, data = body2403buy)
    r51 = requests.request("POST", url, headers=headers, data = body2500)
    r52 = requests.request("POST", url, headers=headers, data = body2501)
    r53 = requests.request("POST", url, headers=headers, data = body2502)
    r54 = requests.request("POST", url, headers=headers, data = body2503)
    r55 = requests.request("POST", url, headers=headers, data = body2504)
    r56 = requests.request("POST", url, headers=headers, data = body2600)
    r57 = requests.request("POST", url, headers=headers, data = body2600buy)
    r58 = requests.request("POST", url, headers=headers, data = body2601)
    r59 = requests.request("POST", url, headers=headers, data = body2601buy)
    r60 = requests.request("POST", url, headers=headers, data = body2602)
    r61 = requests.request("POST", url, headers=headers, data = body2602buy)
    r62 = requests.request("POST", url, headers=headers, data = body2603)
    r63 = requests.request("POST", url, headers=headers, data = body2603buy)
    r64 = requests.request("POST", url, headers=headers, data = body2700)
    r65 = requests.request("POST", url, headers=headers, data = body2700buy)
    r66 = requests.request("POST", url, headers=headers, data = body2701)
    r67 = requests.request("POST", url, headers=headers, data = body2701buy)
    r68 = requests.request("POST", url, headers=headers, data = body2702)
    r69 = requests.request("POST", url, headers=headers, data = body2702buy)
    r70 = requests.request("POST", url, headers=headers, data = body2703)
    r71 = requests.request("POST", url, headers=headers, data = body2703buy)
    r72 = requests.request("POST", url, headers=headers, data = body2800)
    r73 = requests.request("POST", url, headers=headers, data = body2801)
    r74 = requests.request("POST", url, headers=headers, data = body2802)
    r75 = requests.request("POST", url, headers=headers, data = body2803)
    r76 = requests.request("POST", url, headers=headers, data = body2804)
    r77 = requests.request("POST", url, headers=headers, data = body2900)
    r78 = requests.request("POST", url, headers=headers, data = body2900buy)
    r79 = requests.request("POST", url, headers=headers, data = body2901)
    r80 = requests.request("POST", url, headers=headers, data = body2901buy)
    r81 = requests.request("POST", url, headers=headers, data = body2902)
    r82 = requests.request("POST", url, headers=headers, data = body2902buy)
    r83 = requests.request("POST", url, headers=headers, data = body3000)
    r84 = requests.request("POST", url, headers=headers, data = body3000buy)
    r85 = requests.request("POST", url, headers=headers, data = body3001)
    r86 = requests.request("POST", url, headers=headers, data = body3001buy)
    r87 = requests.request("POST", url, headers=headers, data = body3002)
    r88 = requests.request("POST", url, headers=headers, data = body3002buy)
    r89 = requests.request("POST", url, headers=headers, data = body3100)
    r90 = requests.request("POST", url, headers=headers, data = body3100buy)
    r91 = requests.request("POST", url, headers=headers, data = body3101)
    r92 = requests.request("POST", url, headers=headers, data = body3101buy)
    r93 = requests.request("POST", url, headers=headers, data = body3102)
    r94 = requests.request("POST", url, headers=headers, data = body3102buy)
    r95 = requests.request("POST", url, headers=headers, data = body3200)
    r96 = requests.request("POST", url, headers=headers, data = body3200buy)
    r97 = requests.request("POST", url, headers=headers, data = body3201)
    r98 = requests.request("POST", url, headers=headers, data = body3201buy)
    r99 = requests.request("POST", url, headers=headers, data = body3202)
    r100 = requests.request("POST", url, headers=headers, data = body3202buy)
    r101 = requests.request("POST", url, headers=headers, data = body3300)
    r102 = requests.request("POST", url, headers=headers, data = body3300buy)
    r103 = requests.request("POST", url, headers=headers, data = body3301)
    r104 = requests.request("POST", url, headers=headers, data = body3301buy)
    r105 = requests.request("POST", url, headers=headers, data = body3302)
    r106 = requests.request("POST", url, headers=headers, data = body3302buy)
    r107 = requests.request("POST", url, headers=headers, data = body3400)
    r108 = requests.request("POST", url, headers=headers, data = body3400buy)
    r109 = requests.request("POST", url, headers=headers, data = body3401)
    r110 = requests.request("POST", url, headers=headers, data = body3401buy)
    r111 = requests.request("POST", url, headers=headers, data = body3402)
    r112 = requests.request("POST", url, headers=headers, data = body3402buy)
    r113 = requests.request("POST", url, headers=headers, data = body3500)
    r114 = requests.request("POST", url, headers=headers, data = body3500buy)
    r115 = requests.request("POST", url, headers=headers, data = body3501)
    r116 = requests.request("POST", url, headers=headers, data = body3501buy)
    r117 = requests.request("POST", url, headers=headers, data = body3502)
    r118 = requests.request("POST", url, headers=headers, data = body3502buy)
    r119 = requests.request("POST", url, headers=headers, data = body3600)
    r120 = requests.request("POST", url, headers=headers, data = body1001)
    r121 = requests.request("POST", url, headers=headers, data = body3700)
    r122 = requests.request("POST", url, headers=headers, data = body3800)
    r123 = requests.request("POST", url, headers=headers, data = body3800buy)

    print(str(i)+"end")

def ID_ACCOUNT01_spin (spintime) : 
  for i in range(spintime):
    rclose = requests.request("POST", url, headers={'Connection':'close'},verify=False)
    r1 = requests.request("POST", url, headers=headers, data = body21601)
    print(r1.text.encode('utf8'))
    r2 = requests.request("POST", url, headers=headers, data = body21602)
    r3 = requests.request("POST", url, headers=headers, data = body21603)
    r4 = requests.request("POST", url, headers=headers, data = body21604)
    r5 = requests.request("POST", url, headers=headers, data = body21605)
    r6 = requests.request("POST", url, headers=headers, data = body21606)
    r7 = requests.request("POST", url, headers=headers, data = body21607)
    r8 = requests.request("POST", url, headers=headers, data = body21700)
    r9 = requests.request("POST", url, headers=headers, data = body21701)
    r10 = requests.request("POST", url, headers=headers, data = body21811)
    r11 = requests.request("POST", url, headers=headers, data = body21812)
    r12 = requests.request("POST", url, headers=headers, data = body21817)
    r13 = requests.request("POST", url, headers=headers, data = body21820)
    r14 = requests.request("POST", url, headers=headers, data = body22000)
    r15 = requests.request("POST", url, headers=headers, data = body22001)
    r16 = requests.request("POST", url, headers=headers, data = body21813)
    r17 = requests.request("POST", url, headers=headers, data = body21815)
    r18 = requests.request("POST", url, headers=headers, data = body21816)
    r19 = requests.request("POST", url, headers=headers, data = body21818)
    r20 = requests.request("POST", url, headers=headers, data = body21819)
    r21 = requests.request("POST", url, headers=headers, data = body21822)
    r22 = requests.request("POST", url, headers=headers, data = body21900)
    r23 = requests.request("POST", url, headers=headers, data = body21901)
    r24 = requests.request("POST", url, headers=headers, data = body21902)
    r25 = requests.request("POST", url, headers=headers, data = body21903)
    r26 = requests.request("POST", url, headers=headers, data = body21904)
    r27 = requests.request("POST", url, headers=headers, data = body21905)
    r28 = requests.request("POST", url, headers=headers, data = body21906)
    r29 = requests.request("POST", url, headers=headers, data = body21907)
    r30 = requests.request("POST", url, headers=headers, data = body21908)
    r31 = requests.request("POST", url, headers=headers, data = body22100)
    r32 = requests.request("POST", url, headers=headers, data = body22101)
    r33 = requests.request("POST", url, headers=headers, data = body22102)
    r34 = requests.request("POST", url, headers=headers, data = body22103)
    r35 = requests.request("POST", url, headers=headers, data = body22104)
    r36 = requests.request("POST", url, headers=headers, data = body22200)
    r37 = requests.request("POST", url, headers=headers, data = body22201)
    r38 = requests.request("POST", url, headers=headers, data = body22202)
    r39 = requests.request("POST", url, headers=headers, data = body22203)
    r40 = requests.request("POST", url, headers=headers, data = body22300)
    r41 = requests.request("POST", url, headers=headers, data = body22301)
    r42 = requests.request("POST", url, headers=headers, data = body22302)
    r43 = requests.request("POST", url, headers=headers, data = body22400)
    r44 = requests.request("POST", url, headers=headers, data = body22400buy)
    r45 = requests.request("POST", url, headers=headers, data = body22401)
    r46 = requests.request("POST", url, headers=headers, data = body22401buy)
    r47 = requests.request("POST", url, headers=headers, data = body22402)
    r48 = requests.request("POST", url, headers=headers, data = body22402buy)
    r49 = requests.request("POST", url, headers=headers, data = body22403)
    r50 = requests.request("POST", url, headers=headers, data = body22403buy)
    r51 = requests.request("POST", url, headers=headers, data = body22500)
    r52 = requests.request("POST", url, headers=headers, data = body22501)
    r53 = requests.request("POST", url, headers=headers, data = body22502)
    r54 = requests.request("POST", url, headers=headers, data = body22503)
    r55 = requests.request("POST", url, headers=headers, data = body22504)
    r56 = requests.request("POST", url, headers=headers, data = body22600)
    r57 = requests.request("POST", url, headers=headers, data = body22600buy)
    r58 = requests.request("POST", url, headers=headers, data = body22601)
    r59 = requests.request("POST", url, headers=headers, data = body22601buy)
    r60 = requests.request("POST", url, headers=headers, data = body22602)
    r61 = requests.request("POST", url, headers=headers, data = body22602buy)
    r62 = requests.request("POST", url, headers=headers, data = body22603)
    r63 = requests.request("POST", url, headers=headers, data = body22603buy)
    r64 = requests.request("POST", url, headers=headers, data = body22700)
    r65 = requests.request("POST", url, headers=headers, data = body22700buy)
    r66 = requests.request("POST", url, headers=headers, data = body22701)
    r67 = requests.request("POST", url, headers=headers, data = body22701buy)
    r68 = requests.request("POST", url, headers=headers, data = body22702)
    r69 = requests.request("POST", url, headers=headers, data = body22702buy)
    r70 = requests.request("POST", url, headers=headers, data = body22703)
    r71 = requests.request("POST", url, headers=headers, data = body22703buy)
    r72 = requests.request("POST", url, headers=headers, data = body22800)
    r73 = requests.request("POST", url, headers=headers, data = body22801)
    r74 = requests.request("POST", url, headers=headers, data = body22802)
    r75 = requests.request("POST", url, headers=headers, data = body22803)
    r76 = requests.request("POST", url, headers=headers, data = body22804)
    r77 = requests.request("POST", url, headers=headers, data = body22900)
    r78 = requests.request("POST", url, headers=headers, data = body22900buy)
    r79 = requests.request("POST", url, headers=headers, data = body22901)
    r80 = requests.request("POST", url, headers=headers, data = body22901buy)
    r81 = requests.request("POST", url, headers=headers, data = body22902)
    r82 = requests.request("POST", url, headers=headers, data = body22902buy)
    r83 = requests.request("POST", url, headers=headers, data = body23000)
    r84 = requests.request("POST", url, headers=headers, data = body23000buy)
    r85 = requests.request("POST", url, headers=headers, data = body23001)
    r86 = requests.request("POST", url, headers=headers, data = body23001buy)
    r87 = requests.request("POST", url, headers=headers, data = body23002)
    r88 = requests.request("POST", url, headers=headers, data = body23002buy)
    r89 = requests.request("POST", url, headers=headers, data = body23100)
    r90 = requests.request("POST", url, headers=headers, data = body23100buy)
    r91 = requests.request("POST", url, headers=headers, data = body23101)
    r92 = requests.request("POST", url, headers=headers, data = body23101buy)
    r93 = requests.request("POST", url, headers=headers, data = body23102)
    r94 = requests.request("POST", url, headers=headers, data = body23102buy)
    r95 = requests.request("POST", url, headers=headers, data = body23200)
    r96 = requests.request("POST", url, headers=headers, data = body23200buy)
    r97 = requests.request("POST", url, headers=headers, data = body23201)
    r98 = requests.request("POST", url, headers=headers, data = body23201buy)
    r99 = requests.request("POST", url, headers=headers, data = body23202)
    r100 = requests.request("POST", url, headers=headers, data = body23202buy)
    r101 = requests.request("POST", url, headers=headers, data = body23300)
    r102 = requests.request("POST", url, headers=headers, data = body23300buy)
    r103 = requests.request("POST", url, headers=headers, data = body23301)
    r104 = requests.request("POST", url, headers=headers, data = body23301buy)
    r105 = requests.request("POST", url, headers=headers, data = body23302)
    r106 = requests.request("POST", url, headers=headers, data = body23302buy)
    r107 = requests.request("POST", url, headers=headers, data = body23400)
    r108 = requests.request("POST", url, headers=headers, data = body23400buy)
    r109 = requests.request("POST", url, headers=headers, data = body23401)
    r110 = requests.request("POST", url, headers=headers, data = body23401buy)
    r111 = requests.request("POST", url, headers=headers, data = body23402)
    r112 = requests.request("POST", url, headers=headers, data = body23402buy)
    r113 = requests.request("POST", url, headers=headers, data = body23500)
    r114 = requests.request("POST", url, headers=headers, data = body23500buy)
    r115 = requests.request("POST", url, headers=headers, data = body23501)
    r116 = requests.request("POST", url, headers=headers, data = body23501buy)
    r117 = requests.request("POST", url, headers=headers, data = body23502)
    r118 = requests.request("POST", url, headers=headers, data = body23502buy)
    r119 = requests.request("POST", url, headers=headers, data = body23600)
    r120 = requests.request("POST", url, headers=headers, data = body21001)
    r121 = requests.request("POST", url, headers=headers, data = body23700)
    r122 = requests.request("POST", url, headers=headers, data = body23800)
    r123 = requests.request("POST", url, headers=headers, data = body23800buy)

    print(str(i)+"end")

def ID_ACCOUNT02_spin (spintime) : 
  for i in range(spintime):
    rclose = requests.request("POST", url, headers={'Connection':'close'},verify=False)
    r1 = requests.request("POST", url, headers=headers, data = body31601)
    print(r1.text.encode('utf8'))
    r2 = requests.request("POST", url, headers=headers, data = body31602)
    r3 = requests.request("POST", url, headers=headers, data = body31603)
    r4 = requests.request("POST", url, headers=headers, data = body31604)
    r5 = requests.request("POST", url, headers=headers, data = body31605)
    r6 = requests.request("POST", url, headers=headers, data = body31606)
    r7 = requests.request("POST", url, headers=headers, data = body31607)
    r8 = requests.request("POST", url, headers=headers, data = body31700)
    r9 = requests.request("POST", url, headers=headers, data = body31701)
    r10 = requests.request("POST", url, headers=headers, data = body31811)
    r11 = requests.request("POST", url, headers=headers, data = body31812)
    r12 = requests.request("POST", url, headers=headers, data = body31817)
    r13 = requests.request("POST", url, headers=headers, data = body31820)
    r14 = requests.request("POST", url, headers=headers, data = body32000)
    r15 = requests.request("POST", url, headers=headers, data = body32001)
    r16 = requests.request("POST", url, headers=headers, data = body31813)
    r17 = requests.request("POST", url, headers=headers, data = body31815)
    r18 = requests.request("POST", url, headers=headers, data = body31816)
    r19 = requests.request("POST", url, headers=headers, data = body31818)
    r20 = requests.request("POST", url, headers=headers, data = body31819)
    r21 = requests.request("POST", url, headers=headers, data = body31822)
    r22 = requests.request("POST", url, headers=headers, data = body31900)
    r23 = requests.request("POST", url, headers=headers, data = body31901)
    r24 = requests.request("POST", url, headers=headers, data = body31902)
    r25 = requests.request("POST", url, headers=headers, data = body31903)
    r26 = requests.request("POST", url, headers=headers, data = body31904)
    r27 = requests.request("POST", url, headers=headers, data = body31905)
    r28 = requests.request("POST", url, headers=headers, data = body31906)
    r29 = requests.request("POST", url, headers=headers, data = body31907)
    r30 = requests.request("POST", url, headers=headers, data = body31908)
    r31 = requests.request("POST", url, headers=headers, data = body32100)
    r32 = requests.request("POST", url, headers=headers, data = body32101)
    r33 = requests.request("POST", url, headers=headers, data = body32102)
    r34 = requests.request("POST", url, headers=headers, data = body32103)
    r35 = requests.request("POST", url, headers=headers, data = body32104)
    r36 = requests.request("POST", url, headers=headers, data = body32200)
    r37 = requests.request("POST", url, headers=headers, data = body32201)
    r38 = requests.request("POST", url, headers=headers, data = body32202)
    r39 = requests.request("POST", url, headers=headers, data = body32203)
    r40 = requests.request("POST", url, headers=headers, data = body32300)
    r41 = requests.request("POST", url, headers=headers, data = body32301)
    r42 = requests.request("POST", url, headers=headers, data = body32302)
    r43 = requests.request("POST", url, headers=headers, data = body32400)
    r44 = requests.request("POST", url, headers=headers, data = body32400buy)
    r45 = requests.request("POST", url, headers=headers, data = body32401)
    r46 = requests.request("POST", url, headers=headers, data = body32401buy)
    r47 = requests.request("POST", url, headers=headers, data = body32402)
    r48 = requests.request("POST", url, headers=headers, data = body32402buy)
    r49 = requests.request("POST", url, headers=headers, data = body32403)
    r50 = requests.request("POST", url, headers=headers, data = body32403buy)
    r51 = requests.request("POST", url, headers=headers, data = body32500)
    r52 = requests.request("POST", url, headers=headers, data = body32501)
    r53 = requests.request("POST", url, headers=headers, data = body32502)
    r54 = requests.request("POST", url, headers=headers, data = body32503)
    r55 = requests.request("POST", url, headers=headers, data = body32504)
    r56 = requests.request("POST", url, headers=headers, data = body32600)
    r57 = requests.request("POST", url, headers=headers, data = body32600buy)
    r58 = requests.request("POST", url, headers=headers, data = body32601)
    r59 = requests.request("POST", url, headers=headers, data = body32601buy)
    r60 = requests.request("POST", url, headers=headers, data = body32602)
    r61 = requests.request("POST", url, headers=headers, data = body32602buy)
    r62 = requests.request("POST", url, headers=headers, data = body32603)
    r63 = requests.request("POST", url, headers=headers, data = body32603buy)
    r64 = requests.request("POST", url, headers=headers, data = body32700)
    r65 = requests.request("POST", url, headers=headers, data = body32700buy)
    r66 = requests.request("POST", url, headers=headers, data = body32701)
    r67 = requests.request("POST", url, headers=headers, data = body32701buy)
    r68 = requests.request("POST", url, headers=headers, data = body32702)
    r69 = requests.request("POST", url, headers=headers, data = body32702buy)
    r70 = requests.request("POST", url, headers=headers, data = body32703)
    r71 = requests.request("POST", url, headers=headers, data = body32703buy)
    r72 = requests.request("POST", url, headers=headers, data = body32800)
    r73 = requests.request("POST", url, headers=headers, data = body32801)
    r74 = requests.request("POST", url, headers=headers, data = body32802)
    r75 = requests.request("POST", url, headers=headers, data = body32803)
    r76 = requests.request("POST", url, headers=headers, data = body32804)
    r77 = requests.request("POST", url, headers=headers, data = body32900)
    r78 = requests.request("POST", url, headers=headers, data = body32900buy)
    r79 = requests.request("POST", url, headers=headers, data = body32901)
    r80 = requests.request("POST", url, headers=headers, data = body32901buy)
    r81 = requests.request("POST", url, headers=headers, data = body32902)
    r82 = requests.request("POST", url, headers=headers, data = body32902buy)
    r83 = requests.request("POST", url, headers=headers, data = body33000)
    r84 = requests.request("POST", url, headers=headers, data = body33000buy)
    r85 = requests.request("POST", url, headers=headers, data = body33001)
    r86 = requests.request("POST", url, headers=headers, data = body33001buy)
    r87 = requests.request("POST", url, headers=headers, data = body33002)
    r88 = requests.request("POST", url, headers=headers, data = body33002buy)
    r89 = requests.request("POST", url, headers=headers, data = body33100)
    r90 = requests.request("POST", url, headers=headers, data = body33100buy)
    r91 = requests.request("POST", url, headers=headers, data = body33101)
    r92 = requests.request("POST", url, headers=headers, data = body33101buy)
    r93 = requests.request("POST", url, headers=headers, data = body33102)
    r94 = requests.request("POST", url, headers=headers, data = body33102buy)
    r95 = requests.request("POST", url, headers=headers, data = body33200)
    r96 = requests.request("POST", url, headers=headers, data = body33200buy)
    r97 = requests.request("POST", url, headers=headers, data = body33201)
    r98 = requests.request("POST", url, headers=headers, data = body33201buy)
    r99 = requests.request("POST", url, headers=headers, data = body33202)
    r100 = requests.request("POST", url, headers=headers, data = body33202buy)
    r101 = requests.request("POST", url, headers=headers, data = body33300)
    r102 = requests.request("POST", url, headers=headers, data = body33300buy)
    r103 = requests.request("POST", url, headers=headers, data = body33301)
    r104 = requests.request("POST", url, headers=headers, data = body33301buy)
    r105 = requests.request("POST", url, headers=headers, data = body33302)
    r106 = requests.request("POST", url, headers=headers, data = body33302buy)
    r107 = requests.request("POST", url, headers=headers, data = body33400)
    r108 = requests.request("POST", url, headers=headers, data = body33400buy)
    r109 = requests.request("POST", url, headers=headers, data = body33401)
    r110 = requests.request("POST", url, headers=headers, data = body33401buy)
    r111 = requests.request("POST", url, headers=headers, data = body33402)
    r112 = requests.request("POST", url, headers=headers, data = body33402buy)
    r113 = requests.request("POST", url, headers=headers, data = body33500)
    r114 = requests.request("POST", url, headers=headers, data = body33500buy)
    r115 = requests.request("POST", url, headers=headers, data = body33501)
    r116 = requests.request("POST", url, headers=headers, data = body33501buy)
    r117 = requests.request("POST", url, headers=headers, data = body33502)
    r118 = requests.request("POST", url, headers=headers, data = body33502buy)
    r119 = requests.request("POST", url, headers=headers, data = body33600)
    r120 = requests.request("POST", url, headers=headers, data = body31001)
    r121 = requests.request("POST", url, headers=headers, data = body33700)
    r122 = requests.request("POST", url, headers=headers, data = body33800)
    r123 = requests.request("POST", url, headers=headers, data = body33800buy)

    print(str(i)+"end")

def ID_ACCOUNT03_spin (spintime) : 
  for i in range(spintime):
    rclose = requests.request("POST", url, headers={'Connection':'close'},verify=False)
    r1 = requests.request("POST", url, headers=headers, data = body41601)
    print(r1.text.encode('utf8'))
    r2 = requests.request("POST", url, headers=headers, data = body41602)
    r3 = requests.request("POST", url, headers=headers, data = body41603)
    r4 = requests.request("POST", url, headers=headers, data = body41604)
    r5 = requests.request("POST", url, headers=headers, data = body41605)
    r6 = requests.request("POST", url, headers=headers, data = body41606)
    r7 = requests.request("POST", url, headers=headers, data = body41607)
    r8 = requests.request("POST", url, headers=headers, data = body41700)
    r9 = requests.request("POST", url, headers=headers, data = body41701)
    r10 = requests.request("POST", url, headers=headers, data = body41811)
    r11 = requests.request("POST", url, headers=headers, data = body41812)
    r12 = requests.request("POST", url, headers=headers, data = body41817)
    r13 = requests.request("POST", url, headers=headers, data = body41820)
    r14 = requests.request("POST", url, headers=headers, data = body42000)
    r15 = requests.request("POST", url, headers=headers, data = body42001)
    r16 = requests.request("POST", url, headers=headers, data = body41813)
    r17 = requests.request("POST", url, headers=headers, data = body41815)
    r18 = requests.request("POST", url, headers=headers, data = body41816)
    r19 = requests.request("POST", url, headers=headers, data = body41818)
    r20 = requests.request("POST", url, headers=headers, data = body41819)
    r21 = requests.request("POST", url, headers=headers, data = body41822)
    r22 = requests.request("POST", url, headers=headers, data = body41900)
    r23 = requests.request("POST", url, headers=headers, data = body41901)
    r24 = requests.request("POST", url, headers=headers, data = body41902)
    r25 = requests.request("POST", url, headers=headers, data = body41903)
    r26 = requests.request("POST", url, headers=headers, data = body41904)
    r27 = requests.request("POST", url, headers=headers, data = body41905)
    r28 = requests.request("POST", url, headers=headers, data = body41906)
    r29 = requests.request("POST", url, headers=headers, data = body41907)
    r30 = requests.request("POST", url, headers=headers, data = body41908)
    r31 = requests.request("POST", url, headers=headers, data = body42100)
    r32 = requests.request("POST", url, headers=headers, data = body42101)
    r33 = requests.request("POST", url, headers=headers, data = body42102)
    r34 = requests.request("POST", url, headers=headers, data = body42103)
    r35 = requests.request("POST", url, headers=headers, data = body42104)
    r36 = requests.request("POST", url, headers=headers, data = body42200)
    r37 = requests.request("POST", url, headers=headers, data = body42201)
    r38 = requests.request("POST", url, headers=headers, data = body42202)
    r39 = requests.request("POST", url, headers=headers, data = body42203)
    r40 = requests.request("POST", url, headers=headers, data = body42300)
    r41 = requests.request("POST", url, headers=headers, data = body42301)
    r42 = requests.request("POST", url, headers=headers, data = body42302)
    r43 = requests.request("POST", url, headers=headers, data = body42400)
    r44 = requests.request("POST", url, headers=headers, data = body42400buy)
    r45 = requests.request("POST", url, headers=headers, data = body42401)
    r46 = requests.request("POST", url, headers=headers, data = body42401buy)
    r47 = requests.request("POST", url, headers=headers, data = body42402)
    r48 = requests.request("POST", url, headers=headers, data = body42402buy)
    r49 = requests.request("POST", url, headers=headers, data = body42403)
    r50 = requests.request("POST", url, headers=headers, data = body42403buy)
    r51 = requests.request("POST", url, headers=headers, data = body42500)
    r52 = requests.request("POST", url, headers=headers, data = body42501)
    r53 = requests.request("POST", url, headers=headers, data = body42502)
    r54 = requests.request("POST", url, headers=headers, data = body42503)
    r55 = requests.request("POST", url, headers=headers, data = body42504)
    r56 = requests.request("POST", url, headers=headers, data = body42600)
    r57 = requests.request("POST", url, headers=headers, data = body42600buy)
    r58 = requests.request("POST", url, headers=headers, data = body42601)
    r59 = requests.request("POST", url, headers=headers, data = body42601buy)
    r60 = requests.request("POST", url, headers=headers, data = body42602)
    r61 = requests.request("POST", url, headers=headers, data = body42602buy)
    r62 = requests.request("POST", url, headers=headers, data = body42603)
    r63 = requests.request("POST", url, headers=headers, data = body42603buy)
    r64 = requests.request("POST", url, headers=headers, data = body42700)
    r65 = requests.request("POST", url, headers=headers, data = body42700buy)
    r66 = requests.request("POST", url, headers=headers, data = body42701)
    r67 = requests.request("POST", url, headers=headers, data = body42701buy)
    r68 = requests.request("POST", url, headers=headers, data = body42702)
    r69 = requests.request("POST", url, headers=headers, data = body42702buy)
    r70 = requests.request("POST", url, headers=headers, data = body42703)
    r71 = requests.request("POST", url, headers=headers, data = body42703buy)
    r72 = requests.request("POST", url, headers=headers, data = body42800)
    r73 = requests.request("POST", url, headers=headers, data = body42801)
    r74 = requests.request("POST", url, headers=headers, data = body42802)
    r75 = requests.request("POST", url, headers=headers, data = body42803)
    r76 = requests.request("POST", url, headers=headers, data = body42804)
    r77 = requests.request("POST", url, headers=headers, data = body42900)
    r78 = requests.request("POST", url, headers=headers, data = body42900buy)
    r79 = requests.request("POST", url, headers=headers, data = body42901)
    r80 = requests.request("POST", url, headers=headers, data = body42901buy)
    r81 = requests.request("POST", url, headers=headers, data = body42902)
    r82 = requests.request("POST", url, headers=headers, data = body42902buy)
    r83 = requests.request("POST", url, headers=headers, data = body43000)
    r84 = requests.request("POST", url, headers=headers, data = body43000buy)
    r85 = requests.request("POST", url, headers=headers, data = body43001)
    r86 = requests.request("POST", url, headers=headers, data = body43001buy)
    r87 = requests.request("POST", url, headers=headers, data = body43002)
    r88 = requests.request("POST", url, headers=headers, data = body43002buy)
    r89 = requests.request("POST", url, headers=headers, data = body43100)
    r90 = requests.request("POST", url, headers=headers, data = body43100buy)
    r91 = requests.request("POST", url, headers=headers, data = body43101)
    r92 = requests.request("POST", url, headers=headers, data = body43101buy)
    r93 = requests.request("POST", url, headers=headers, data = body43102)
    r94 = requests.request("POST", url, headers=headers, data = body43102buy)
    r95 = requests.request("POST", url, headers=headers, data = body43200)
    r96 = requests.request("POST", url, headers=headers, data = body43200buy)
    r97 = requests.request("POST", url, headers=headers, data = body43201)
    r98 = requests.request("POST", url, headers=headers, data = body43201buy)
    r99 = requests.request("POST", url, headers=headers, data = body43202)
    r100 = requests.request("POST", url, headers=headers, data = body43202buy)
    r101 = requests.request("POST", url, headers=headers, data = body43300)
    r102 = requests.request("POST", url, headers=headers, data = body43300buy)
    r103 = requests.request("POST", url, headers=headers, data = body43301)
    r104 = requests.request("POST", url, headers=headers, data = body43301buy)
    r105 = requests.request("POST", url, headers=headers, data = body43302)
    r106 = requests.request("POST", url, headers=headers, data = body43302buy)
    r107 = requests.request("POST", url, headers=headers, data = body43400)
    r108 = requests.request("POST", url, headers=headers, data = body43400buy)
    r109 = requests.request("POST", url, headers=headers, data = body43401)
    r110 = requests.request("POST", url, headers=headers, data = body43401buy)
    r111 = requests.request("POST", url, headers=headers, data = body43402)
    r112 = requests.request("POST", url, headers=headers, data = body43402buy)
    r113 = requests.request("POST", url, headers=headers, data = body43500)
    r114 = requests.request("POST", url, headers=headers, data = body43500buy)
    r115 = requests.request("POST", url, headers=headers, data = body43501)
    r116 = requests.request("POST", url, headers=headers, data = body43501buy)
    r117 = requests.request("POST", url, headers=headers, data = body43502)
    r118 = requests.request("POST", url, headers=headers, data = body43502buy)
    r119 = requests.request("POST", url, headers=headers, data = body43600)
    r120 = requests.request("POST", url, headers=headers, data = body41001)
    r121 = requests.request("POST", url, headers=headers, data = body43700)
    r122 = requests.request("POST", url, headers=headers, data = body43800)
    r123 = requests.request("POST", url, headers=headers, data = body43800buy)

    print(str(i)+"end")

def phspin (spintime) : 
  for i in range(spintime):
      rclose = requests.request("POST", url, headers={'Connection':'close'},verify=False)
      r1 = requests.request("POST", url, headers=headers, data = bodyph2100)
      print(r1.text.encode('utf8'))
      r2 = requests.request("POST", url, headers=headers, data = bodyph2101)
      r3 = requests.request("POST", url, headers=headers, data = bodyph2102)
      r4 = requests.request("POST", url, headers=headers, data = bodyph2103)
      r5 = requests.request("POST", url, headers=headers, data = bodyph2104)
      r6 = requests.request("POST", url, headers=headers, data = bodyph2200)
      r7 = requests.request("POST", url, headers=headers, data = bodyph2201)
      r8 = requests.request("POST", url, headers=headers, data = bodyph2202)
      r9 = requests.request("POST", url, headers=headers, data = bodyph2203)
      r10 = requests.request("POST", url, headers=headers, data = bodyph2300)
      r11 = requests.request("POST", url, headers=headers, data = bodyph2301)
      r12 = requests.request("POST", url, headers=headers, data = bodyph2302)
      r13 = requests.request("POST", url, headers=headers, data = bodyph2400)
      r14 = requests.request("POST", url, headers=headers, data = bodyph2400buy)
      r15 = requests.request("POST", url, headers=headers, data = bodyph2401)
      r16 = requests.request("POST", url, headers=headers, data = bodyph2401buy)
      r17 = requests.request("POST", url, headers=headers, data = bodyph2402)
      r18 = requests.request("POST", url, headers=headers, data = bodyph2402buy)
      r19 = requests.request("POST", url, headers=headers, data = bodyph2403)
      r20 = requests.request("POST", url, headers=headers, data = bodyph2403buy)
      r21 = requests.request("POST", url, headers=headers, data = bodyph2500)
      r22 = requests.request("POST", url, headers=headers, data = bodyph2501)
      r23 = requests.request("POST", url, headers=headers, data = bodyph2502)
      r24 = requests.request("POST", url, headers=headers, data = bodyph2503)
      r25 = requests.request("POST", url, headers=headers, data = bodyph2504)
      r26 = requests.request("POST", url, headers=headers, data = bodyph2600)
      r27 = requests.request("POST", url, headers=headers, data = bodyph2600buy)
      r28 = requests.request("POST", url, headers=headers, data = bodyph2601)
      r29 = requests.request("POST", url, headers=headers, data = bodyph2601buy)
      r30 = requests.request("POST", url, headers=headers, data = bodyph2602)
      r31 = requests.request("POST", url, headers=headers, data = bodyph2602buy)
      r32 = requests.request("POST", url, headers=headers, data = bodyph2603)
      r33 = requests.request("POST", url, headers=headers, data = bodyph2603buy)
      r34 = requests.request("POST", url, headers=headers, data = bodyph2700)
      r35 = requests.request("POST", url, headers=headers, data = bodyph2700buy)
      r36 = requests.request("POST", url, headers=headers, data = bodyph2701)
      r37 = requests.request("POST", url, headers=headers, data = bodyph2701buy)
      r38 = requests.request("POST", url, headers=headers, data = bodyph2702)
      r39 = requests.request("POST", url, headers=headers, data = bodyph2702buy)
      r40 = requests.request("POST", url, headers=headers, data = bodyph2703)
      r41 = requests.request("POST", url, headers=headers, data = bodyph2703buy)
      r42 = requests.request("POST", url, headers=headers, data = bodyph2800)
      r43 = requests.request("POST", url, headers=headers, data = bodyph2801)
      r44 = requests.request("POST", url, headers=headers, data = bodyph2802)
      r45 = requests.request("POST", url, headers=headers, data = bodyph2803)
      r46 = requests.request("POST", url, headers=headers, data = bodyph2804)
      r47 = requests.request("POST", url, headers=headers, data = bodyph2900)
      r48 = requests.request("POST", url, headers=headers, data = bodyph2900buy)
      r49 = requests.request("POST", url, headers=headers, data = bodyph2901)
      r50 = requests.request("POST", url, headers=headers, data = bodyph2901buy)
      r51 = requests.request("POST", url, headers=headers, data = bodyph2902)
      r52 = requests.request("POST", url, headers=headers, data = bodyph2902buy)
      r53 = requests.request("POST", url, headers=headers, data = bodyph3000)
      r54 = requests.request("POST", url, headers=headers, data = bodyph3000buy)
      r55 = requests.request("POST", url, headers=headers, data = bodyph3001)
      r56 = requests.request("POST", url, headers=headers, data = bodyph3001buy)
      r57 = requests.request("POST", url, headers=headers, data = bodyph3002)
      r58 = requests.request("POST", url, headers=headers, data = bodyph3002buy)
      r59 = requests.request("POST", url, headers=headers, data = bodyph3100)
      r60 = requests.request("POST", url, headers=headers, data = bodyph3100buy)
      r61 = requests.request("POST", url, headers=headers, data = bodyph3101)
      r62 = requests.request("POST", url, headers=headers, data = bodyph3101buy)
      r63 = requests.request("POST", url, headers=headers, data = bodyph3102)
      r64 = requests.request("POST", url, headers=headers, data = bodyph3102buy)
      r65 = requests.request("POST", url, headers=headers, data = bodyph3200)
      r66 = requests.request("POST", url, headers=headers, data = bodyph3200buy)
      r67 = requests.request("POST", url, headers=headers, data = bodyph3201)
      r68 = requests.request("POST", url, headers=headers, data = bodyph3201buy)
      r69 = requests.request("POST", url, headers=headers, data = bodyph3202)
      r70 = requests.request("POST", url, headers=headers, data = bodyph3202buy)
      r71 = requests.request("POST", url, headers=headers, data = bodyph3300)
      r72 = requests.request("POST", url, headers=headers, data = bodyph3300buy)
      r73 = requests.request("POST", url, headers=headers, data = bodyph3301)
      r74 = requests.request("POST", url, headers=headers, data = bodyph3301buy)
      r75 = requests.request("POST", url, headers=headers, data = bodyph3302)
      r76 = requests.request("POST", url, headers=headers, data = bodyph3302buy)
      r77 = requests.request("POST", url, headers=headers, data = bodyph3400)
      r78 = requests.request("POST", url, headers=headers, data = bodyph3400buy)
      r79 = requests.request("POST", url, headers=headers, data = bodyph3401)
      r80 = requests.request("POST", url, headers=headers, data = bodyph3401buy)
      r81 = requests.request("POST", url, headers=headers, data = bodyph3402)
      r82 = requests.request("POST", url, headers=headers, data = bodyph3402buy)
      r83 = requests.request("POST", url, headers=headers, data = bodyph3500)
      r84 = requests.request("POST", url, headers=headers, data = bodyph3500buy)
      r85 = requests.request("POST", url, headers=headers, data = bodyph3501)
      r86 = requests.request("POST", url, headers=headers, data = bodyph3501buy)
      r87 = requests.request("POST", url, headers=headers, data = bodyph3502)
      r88 = requests.request("POST", url, headers=headers, data = bodyph3502buy)
      r89 = requests.request("POST", url, headers=headers, data = bodyph3600)
      r89 = requests.request("POST", url, headers=headers, data = bodyph3700)
      r89 = requests.request("POST", url, headers=headers, data = bodyph3800)
      r90 = requests.request("POST", url, headers=headers, data = bodyph3800buy)

      print(str(i)+"end")

def php2spin (spintime) : 
  for i in range(spintime):
      rclose = requests.request("POST", url, headers={'Connection':'close'},verify=False)
      r1 = requests.request("POST", url, headers=headers, data = bodyph2100)
      print(r1.text.encode('utf8'))
      r2 = requests.request("POST", url, headers=headers, data = bodyph2101)
      r3 = requests.request("POST", url, headers=headers, data = bodyph2102)
      r4 = requests.request("POST", url, headers=headers, data = bodyph2103)
      r5 = requests.request("POST", url, headers=headers, data = bodyph2104)
      r6 = requests.request("POST", url, headers=headers, data = bodyph2200)
      r7 = requests.request("POST", url, headers=headers, data = bodyph2201)
      r8 = requests.request("POST", url, headers=headers, data = bodyph2202)
      r9 = requests.request("POST", url, headers=headers, data = bodyph2203)
      r10 = requests.request("POST", url, headers=headers, data = bodyph2300)
      r11 = requests.request("POST", url, headers=headers, data = bodyph2301)
      r12 = requests.request("POST", url, headers=headers, data = bodyph2302)
      r13 = requests.request("POST", url, headers=headers, data = bodyph2400)
      r14 = requests.request("POST", url, headers=headers, data = bodyph2400buy)
      r15 = requests.request("POST", url, headers=headers, data = bodyph2401)
      r16 = requests.request("POST", url, headers=headers, data = bodyph2401buy)
      r17 = requests.request("POST", url, headers=headers, data = bodyph2402)
      r18 = requests.request("POST", url, headers=headers, data = bodyph2402buy)
      r19 = requests.request("POST", url, headers=headers, data = bodyph2403)
      r20 = requests.request("POST", url, headers=headers, data = bodyph2403buy)
      r21 = requests.request("POST", url, headers=headers, data = bodyph2500)
      r22 = requests.request("POST", url, headers=headers, data = bodyph2501)
      r23 = requests.request("POST", url, headers=headers, data = bodyph2502)
      r24 = requests.request("POST", url, headers=headers, data = bodyph2503)
      r25 = requests.request("POST", url, headers=headers, data = bodyph2504)
      r26 = requests.request("POST", url, headers=headers, data = bodyph2600)
      r27 = requests.request("POST", url, headers=headers, data = bodyph2600buy)
      r28 = requests.request("POST", url, headers=headers, data = bodyph2601)
      r29 = requests.request("POST", url, headers=headers, data = bodyph2601buy)
      r30 = requests.request("POST", url, headers=headers, data = bodyph2602)
      r31 = requests.request("POST", url, headers=headers, data = bodyph2602buy)
      r32 = requests.request("POST", url, headers=headers, data = bodyph2603)
      r33 = requests.request("POST", url, headers=headers, data = bodyph2603buy)
      r34 = requests.request("POST", url, headers=headers, data = bodyph2700)
      r35 = requests.request("POST", url, headers=headers, data = bodyph2700buy)
      r36 = requests.request("POST", url, headers=headers, data = bodyph2701)
      r37 = requests.request("POST", url, headers=headers, data = bodyph2701buy)
      r38 = requests.request("POST", url, headers=headers, data = bodyph2702)
      r39 = requests.request("POST", url, headers=headers, data = bodyph2702buy)
      r40 = requests.request("POST", url, headers=headers, data = bodyph2703)
      r41 = requests.request("POST", url, headers=headers, data = bodyph2703buy)
      r42 = requests.request("POST", url, headers=headers, data = bodyph2800)
      r43 = requests.request("POST", url, headers=headers, data = bodyph2801)
      r44 = requests.request("POST", url, headers=headers, data = bodyph2802)
      r45 = requests.request("POST", url, headers=headers, data = bodyph2803)
      r46 = requests.request("POST", url, headers=headers, data = bodyph2804)
      r47 = requests.request("POST", url, headers=headers, data = bodyph2900)
      r48 = requests.request("POST", url, headers=headers, data = bodyph2900buy)
      r49 = requests.request("POST", url, headers=headers, data = bodyph2901)
      r50 = requests.request("POST", url, headers=headers, data = bodyph2901buy)
      r51 = requests.request("POST", url, headers=headers, data = bodyph2902)
      r52 = requests.request("POST", url, headers=headers, data = bodyph2902buy)
      r53 = requests.request("POST", url, headers=headers, data = bodyph3000)
      r54 = requests.request("POST", url, headers=headers, data = bodyph3000buy)
      r55 = requests.request("POST", url, headers=headers, data = bodyph3001)
      r56 = requests.request("POST", url, headers=headers, data = bodyph3001buy)
      r57 = requests.request("POST", url, headers=headers, data = bodyph3002)
      r58 = requests.request("POST", url, headers=headers, data = bodyph3002buy)
      r59 = requests.request("POST", url, headers=headers, data = bodyph3100)
      r60 = requests.request("POST", url, headers=headers, data = bodyph3100buy)
      r61 = requests.request("POST", url, headers=headers, data = bodyph3101)
      r62 = requests.request("POST", url, headers=headers, data = bodyph3101buy)
      r63 = requests.request("POST", url, headers=headers, data = bodyph3102)
      r64 = requests.request("POST", url, headers=headers, data = bodyph3102buy)
      r65 = requests.request("POST", url, headers=headers, data = bodyph3200)
      r66 = requests.request("POST", url, headers=headers, data = bodyph3200buy)
      r67 = requests.request("POST", url, headers=headers, data = bodyph3201)
      r68 = requests.request("POST", url, headers=headers, data = bodyph3201buy)
      r69 = requests.request("POST", url, headers=headers, data = bodyph3202)
      r70 = requests.request("POST", url, headers=headers, data = bodyph3202buy)
      r71 = requests.request("POST", url, headers=headers, data = bodyph3300)
      r72 = requests.request("POST", url, headers=headers, data = bodyph3300buy)
      r73 = requests.request("POST", url, headers=headers, data = bodyph3301)
      r74 = requests.request("POST", url, headers=headers, data = bodyph3301buy)
      r75 = requests.request("POST", url, headers=headers, data = bodyph3302)
      r76 = requests.request("POST", url, headers=headers, data = bodyph3302buy)
      r77 = requests.request("POST", url, headers=headers, data = bodyph3400)
      r78 = requests.request("POST", url, headers=headers, data = bodyph3400buy)
      r79 = requests.request("POST", url, headers=headers, data = bodyph3401)
      r80 = requests.request("POST", url, headers=headers, data = bodyph3401buy)
      r81 = requests.request("POST", url, headers=headers, data = bodyph3402)
      r82 = requests.request("POST", url, headers=headers, data = bodyph3402buy)
      r83 = requests.request("POST", url, headers=headers, data = bodyph3500)
      r84 = requests.request("POST", url, headers=headers, data = bodyph3500buy)
      r85 = requests.request("POST", url, headers=headers, data = bodyph3501)
      r86 = requests.request("POST", url, headers=headers, data = bodyph3501buy)
      r87 = requests.request("POST", url, headers=headers, data = bodyph3502)
      r88 = requests.request("POST", url, headers=headers, data = bodyph3502buy)
      r89 = requests.request("POST", url, headers=headers, data = bodyph3600)

      print(str(i)+"end")

def kospin (spintime) : 
  for i in range(spintime):
      rclose = requests.request("POST", url, headers={'Connection':'close'},verify=False)
      r1 = requests.request("POST", url, headers=headers, data = bodykr2100)
      print(r1.text.encode('utf8'))
      r2 = requests.request("POST", url, headers=headers, data = bodykr2101)
      r3 = requests.request("POST", url, headers=headers, data = bodykr2102)
      r4 = requests.request("POST", url, headers=headers, data = bodykr2103)
      r5 = requests.request("POST", url, headers=headers, data = bodykr2104)
      r6 = requests.request("POST", url, headers=headers, data = bodykr2200)
      r7 = requests.request("POST", url, headers=headers, data = bodykr2201)
      r8 = requests.request("POST", url, headers=headers, data = bodykr2202)
      r9 = requests.request("POST", url, headers=headers, data = bodykr2203)
      r10 = requests.request("POST", url, headers=headers, data = bodykr2300)
      r11 = requests.request("POST", url, headers=headers, data = bodykr2301)
      r12 = requests.request("POST", url, headers=headers, data = bodykr2302)
      r13 = requests.request("POST", url, headers=headers, data = bodykr2400)
      r14 = requests.request("POST", url, headers=headers, data = bodykr2400buy)
      r15 = requests.request("POST", url, headers=headers, data = bodykr2401)
      r16 = requests.request("POST", url, headers=headers, data = bodykr2401buy)
      r17 = requests.request("POST", url, headers=headers, data = bodykr2402)
      r18 = requests.request("POST", url, headers=headers, data = bodykr2402buy)
      r19 = requests.request("POST", url, headers=headers, data = bodykr2403)
      r20 = requests.request("POST", url, headers=headers, data = bodykr2403buy)
      r21 = requests.request("POST", url, headers=headers, data = bodykr2500)
      r22 = requests.request("POST", url, headers=headers, data = bodykr2501)
      r23 = requests.request("POST", url, headers=headers, data = bodykr2502)
      r24 = requests.request("POST", url, headers=headers, data = bodykr2503)
      r25 = requests.request("POST", url, headers=headers, data = bodykr2504)
      r26 = requests.request("POST", url, headers=headers, data = bodykr2600)
      r27 = requests.request("POST", url, headers=headers, data = bodykr2600buy)
      r28 = requests.request("POST", url, headers=headers, data = bodykr2601)
      r29 = requests.request("POST", url, headers=headers, data = bodykr2601buy)
      r30 = requests.request("POST", url, headers=headers, data = bodykr2602)
      r31 = requests.request("POST", url, headers=headers, data = bodykr2602buy)
      r32 = requests.request("POST", url, headers=headers, data = bodykr2603)
      r33 = requests.request("POST", url, headers=headers, data = bodykr2603buy)
      r34 = requests.request("POST", url, headers=headers, data = bodykr2700)
      r35 = requests.request("POST", url, headers=headers, data = bodykr2700buy)
      r36 = requests.request("POST", url, headers=headers, data = bodykr2701)
      r37 = requests.request("POST", url, headers=headers, data = bodykr2701buy)
      r38 = requests.request("POST", url, headers=headers, data = bodykr2702)
      r39 = requests.request("POST", url, headers=headers, data = bodykr2702buy)
      r40 = requests.request("POST", url, headers=headers, data = bodykr2703)
      r41 = requests.request("POST", url, headers=headers, data = bodykr2703buy)
      r42 = requests.request("POST", url, headers=headers, data = bodykr2800)
      r43 = requests.request("POST", url, headers=headers, data = bodykr2801)
      r44 = requests.request("POST", url, headers=headers, data = bodykr2802)
      r45 = requests.request("POST", url, headers=headers, data = bodykr2803)
      r46 = requests.request("POST", url, headers=headers, data = bodykr2804)
      r47 = requests.request("POST", url, headers=headers, data = bodykr2900)
      r48 = requests.request("POST", url, headers=headers, data = bodykr2900buy)
      r49 = requests.request("POST", url, headers=headers, data = bodykr2901)
      r50 = requests.request("POST", url, headers=headers, data = bodykr2901buy)
      r51 = requests.request("POST", url, headers=headers, data = bodykr2902)
      r52 = requests.request("POST", url, headers=headers, data = bodykr2902buy)
      r53 = requests.request("POST", url, headers=headers, data = bodykr3000)
      r54 = requests.request("POST", url, headers=headers, data = bodykr3000buy)
      r55 = requests.request("POST", url, headers=headers, data = bodykr3001)
      r56 = requests.request("POST", url, headers=headers, data = bodykr3001buy)
      r57 = requests.request("POST", url, headers=headers, data = bodykr3002)
      r58 = requests.request("POST", url, headers=headers, data = bodykr3002buy)
      r59 = requests.request("POST", url, headers=headers, data = bodykr3100)
      r60 = requests.request("POST", url, headers=headers, data = bodykr3100buy)
      r61 = requests.request("POST", url, headers=headers, data = bodykr3101)
      r62 = requests.request("POST", url, headers=headers, data = bodykr3101buy)
      r63 = requests.request("POST", url, headers=headers, data = bodykr3102)
      r64 = requests.request("POST", url, headers=headers, data = bodykr3102buy)
      r65 = requests.request("POST", url, headers=headers, data = bodykr3200)
      r66 = requests.request("POST", url, headers=headers, data = bodykr3200buy)
      r67 = requests.request("POST", url, headers=headers, data = bodykr3201)
      r68 = requests.request("POST", url, headers=headers, data = bodykr3201buy)
      r69 = requests.request("POST", url, headers=headers, data = bodykr3202)
      r70 = requests.request("POST", url, headers=headers, data = bodykr3202buy)
      r71 = requests.request("POST", url, headers=headers, data = bodykr3300)
      r72 = requests.request("POST", url, headers=headers, data = bodykr3300buy)
      r73 = requests.request("POST", url, headers=headers, data = bodykr3301)
      r74 = requests.request("POST", url, headers=headers, data = bodykr3301buy)
      r75 = requests.request("POST", url, headers=headers, data = bodykr3302)
      r76 = requests.request("POST", url, headers=headers, data = bodykr3302buy)
      r77 = requests.request("POST", url, headers=headers, data = bodykr3400)
      r78 = requests.request("POST", url, headers=headers, data = bodykr3400buy)
      r79 = requests.request("POST", url, headers=headers, data = bodykr3401)
      r80 = requests.request("POST", url, headers=headers, data = bodykr3401buy)
      r81 = requests.request("POST", url, headers=headers, data = bodykr3402)
      r82 = requests.request("POST", url, headers=headers, data = bodykr3402buy)
      r83 = requests.request("POST", url, headers=headers, data = bodykr3500)
      r84 = requests.request("POST", url, headers=headers, data = bodykr3500buy)
      r85 = requests.request("POST", url, headers=headers, data = bodykr3501)
      r86 = requests.request("POST", url, headers=headers, data = bodykr3501buy)
      r87 = requests.request("POST", url, headers=headers, data = bodykr3502)
      r88 = requests.request("POST", url, headers=headers, data = bodykr3502buy)
      r89 = requests.request("POST", url, headers=headers, data = bodykr3600)

      print(str(i)+"end")
    
def thspin (spintime) : 
  headers = headerdemothx2
  #只有demo才能跑
  
  for i in range(spintime):
    rclose = requests.request("POST", url, headers={'Connection':'close'},verify=False)
    r1 = requests.request("POST", url, headers=headers, data = bodyth1601)
    print(r1.text.encode('utf8'))
    r2 = requests.request("POST", url, headers=headers, data = bodyth1602)
    r3 = requests.request("POST", url, headers=headers, data = bodyth1603)
    r4 = requests.request("POST", url, headers=headers, data = bodyth1604)
    r5 = requests.request("POST", url, headers=headers, data = bodyth1605)
    r6 = requests.request("POST", url, headers=headers, data = bodyth1606)
    r7 = requests.request("POST", url, headers=headers, data = bodyth1607)
    # r8 = requests.request("POST", url, headers=headers, data = body1700)
    # r9 = requests.request("POST", url, headers=headers, data = body1701)
    # r10 = requests.request("POST", url, headers=headers, data = body1811)
    # r11 = requests.request("POST", url, headers=headers, data = body1812)
    # r12 = requests.request("POST", url, headers=headers, data = body1817)
    # r13 = requests.request("POST", url, headers=headers, data = body1820)
    # r14 = requests.request("POST", url, headers=headers, data = body2000)
    r15 = requests.request("POST", url, headers=headers, data = bodyth2001)
    # r16 = requests.request("POST", url, headers=headers, data = body1813)
    # r17 = requests.request("POST", url, headers=headers, data = body1815)
    # r18 = requests.request("POST", url, headers=headers, data = body1816)
    # r19 = requests.request("POST", url, headers=headers, data = body1818)
    # r20 = requests.request("POST", url, headers=headers, data = body1819)
    # r21 = requests.request("POST", url, headers=headers, data = body1822)
    # r22 = requests.request("POST", url, headers=headers, data = body1900)
    # r23 = requests.request("POST", url, headers=headers, data = body1901)
    # r24 = requests.request("POST", url, headers=headers, data = body1902)
    # r25 = requests.request("POST", url, headers=headers, data = body1903)
    # r26 = requests.request("POST", url, headers=headers, data = body1904)
    # r27 = requests.request("POST", url, headers=headers, data = body1905)
    # r28 = requests.request("POST", url, headers=headers, data = body1906)
    # r29 = requests.request("POST", url, headers=headers, data = body1907)
    # r30 = requests.request("POST", url, headers=headers, data = body1908)
    r31 = requests.request("POST", url, headers=headers, data = bodyth2100)
    r32 = requests.request("POST", url, headers=headers, data = bodyth2101)
    r33 = requests.request("POST", url, headers=headers, data = bodyth2102)
    r34 = requests.request("POST", url, headers=headers, data = bodyth2103)
    r35 = requests.request("POST", url, headers=headers, data = bodyth2104)
    r36 = requests.request("POST", url, headers=headers, data = bodyth2200)
    r37 = requests.request("POST", url, headers=headers, data = bodyth2201)
    r38 = requests.request("POST", url, headers=headers, data = bodyth2202)
    r39 = requests.request("POST", url, headers=headers, data = bodyth2203)
    r40 = requests.request("POST", url, headers=headers, data = bodyth2300)
    r41 = requests.request("POST", url, headers=headers, data = bodyth2301)
    r42 = requests.request("POST", url, headers=headers, data = bodyth2302)
    r43 = requests.request("POST", url, headers=headers, data = bodyth2400)
    r44 = requests.request("POST", url, headers=headers, data = bodyth2400buy)
    r45 = requests.request("POST", url, headers=headers, data = bodyth2401)
    r46 = requests.request("POST", url, headers=headers, data = bodyth2401buy)
    r47 = requests.request("POST", url, headers=headers, data = bodyth2402)
    r48 = requests.request("POST", url, headers=headers, data = bodyth2402buy)
    r49 = requests.request("POST", url, headers=headers, data = bodyth2403)
    r50 = requests.request("POST", url, headers=headers, data = bodyth2403buy)
    r51 = requests.request("POST", url, headers=headers, data = bodyth2500)
    r52 = requests.request("POST", url, headers=headers, data = bodyth2501)
    r53 = requests.request("POST", url, headers=headers, data = bodyth2502)
    r54 = requests.request("POST", url, headers=headers, data = bodyth2503)
    r55 = requests.request("POST", url, headers=headers, data = bodyth2504)
    r56 = requests.request("POST", url, headers=headers, data = bodyth2600)
    r57 = requests.request("POST", url, headers=headers, data = bodyth2600buy)
    r58 = requests.request("POST", url, headers=headers, data = bodyth2601)
    r59 = requests.request("POST", url, headers=headers, data = bodyth2601buy)
    r60 = requests.request("POST", url, headers=headers, data = bodyth2602)
    r61 = requests.request("POST", url, headers=headers, data = bodyth2602buy)
    r62 = requests.request("POST", url, headers=headers, data = bodyth2603)
    r63 = requests.request("POST", url, headers=headers, data = bodyth2603buy)
    r64 = requests.request("POST", url, headers=headers, data = bodyth2700)
    r65 = requests.request("POST", url, headers=headers, data = bodyth2700buy)
    r66 = requests.request("POST", url, headers=headers, data = bodyth2701)
    r67 = requests.request("POST", url, headers=headers, data = bodyth2701buy)
    r68 = requests.request("POST", url, headers=headers, data = bodyth2702)
    r69 = requests.request("POST", url, headers=headers, data = bodyth2702buy)
    r70 = requests.request("POST", url, headers=headers, data = bodyth2703)
    r71 = requests.request("POST", url, headers=headers, data = bodyth2703buy)
    r72 = requests.request("POST", url, headers=headers, data = bodyth2800)
    r73 = requests.request("POST", url, headers=headers, data = bodyth2801)
    r74 = requests.request("POST", url, headers=headers, data = bodyth2802)
    r75 = requests.request("POST", url, headers=headers, data = bodyth2803)
    r76 = requests.request("POST", url, headers=headers, data = bodyth2804)
    r77 = requests.request("POST", url, headers=headers, data = bodyth2900)
    r78 = requests.request("POST", url, headers=headers, data = bodyth2900buy)
    r79 = requests.request("POST", url, headers=headers, data = bodyth2901)
    r80 = requests.request("POST", url, headers=headers, data = bodyth2901buy)
    r81 = requests.request("POST", url, headers=headers, data = bodyth2902)
    r82 = requests.request("POST", url, headers=headers, data = bodyth2902buy)
    r83 = requests.request("POST", url, headers=headers, data = bodyth3000)
    r84 = requests.request("POST", url, headers=headers, data = bodyth3000buy)
    r85 = requests.request("POST", url, headers=headers, data = bodyth3001)
    r86 = requests.request("POST", url, headers=headers, data = bodyth3001buy)
    r87 = requests.request("POST", url, headers=headers, data = bodyth3002)
    r88 = requests.request("POST", url, headers=headers, data = bodyth3002buy)
    r89 = requests.request("POST", url, headers=headers, data = bodyth3100)
    r90 = requests.request("POST", url, headers=headers, data = bodyth3100buy)
    r91 = requests.request("POST", url, headers=headers, data = bodyth3101)
    r92 = requests.request("POST", url, headers=headers, data = bodyth3101buy)
    r93 = requests.request("POST", url, headers=headers, data = bodyth3102)
    r94 = requests.request("POST", url, headers=headers, data = bodyth3102buy)
    r95 = requests.request("POST", url, headers=headers, data = bodyth3200)
    r96 = requests.request("POST", url, headers=headers, data = bodyth3200buy)
    r97 = requests.request("POST", url, headers=headers, data = bodyth3201)
    r98 = requests.request("POST", url, headers=headers, data = bodyth3201buy)
    r99 = requests.request("POST", url, headers=headers, data = bodyth3202)
    r100 = requests.request("POST", url, headers=headers, data = bodyth3202buy)
    r101 = requests.request("POST", url, headers=headers, data = bodyth3300)
    r102 = requests.request("POST", url, headers=headers, data = bodyth3300buy)
    r103 = requests.request("POST", url, headers=headers, data = bodyth3301)
    r104 = requests.request("POST", url, headers=headers, data = bodyth3301buy)
    r105 = requests.request("POST", url, headers=headers, data = bodyth3302)
    r106 = requests.request("POST", url, headers=headers, data = bodyth3302buy)
    r107 = requests.request("POST", url, headers=headers, data = bodyth3400)
    r108 = requests.request("POST", url, headers=headers, data = bodyth3400buy)
    r109 = requests.request("POST", url, headers=headers, data = bodyth3401)
    r110 = requests.request("POST", url, headers=headers, data = bodyth3401buy)
    r111 = requests.request("POST", url, headers=headers, data = bodyth3402)
    r112 = requests.request("POST", url, headers=headers, data = bodyth3402buy)
    r113 = requests.request("POST", url, headers=headers, data = bodyth3500)
    r114 = requests.request("POST", url, headers=headers, data = bodyth3500buy)
    r115 = requests.request("POST", url, headers=headers, data = bodyth3501)
    r116 = requests.request("POST", url, headers=headers, data = bodyth3501buy)
    r117 = requests.request("POST", url, headers=headers, data = bodyth3502)
    r118 = requests.request("POST", url, headers=headers, data = bodyth3502buy)
    r119 = requests.request("POST", url, headers=headers, data = bodyth3600)
    # r120 = requests.request("POST", url, headers=headers, data = body1001)
    r121 = requests.request("POST", url, headers=headers, data = bodyth3700)
    r122 = requests.request("POST", url, headers=headers, data = bodyth3800)
    r123 = requests.request("POST", url, headers=headers, data = bodyth3800buy)

    print(str(i)+"end")

if __name__ == "__main__":
    spintime = 1
    #IDspin(spintime)
    #ID_ACCOUNT01_spin(spintime)
    #ID_ACCOUNT02_spin(spintime)
    #ID_ACCOUNT03_spin(spintime)
    #phspin(spintime)
    #php2spin(spintime)
    #kospin(spintime)
    thspin(spintime)
    

