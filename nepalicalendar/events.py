# -*- coding: utf-8 -*-

"""
Defines different constant events in nepali and english calendar
"""

from collections import defaultdict


NEPALI_EVENTS = defaultdict(lambda: [])

# The events are represented as below
# NEPALI_EVENTS[(month, day)] = (Event name, holiday)
# Holiday represents if there is a holiday in that day


NEPALI_EVENTS[(1, 1)] = [("नेपाली नयाँ वर्ष", 1)]
NEPALI_EVENTS[(1, 8)] = [("छन्द दिवस", 0)]
NEPALI_EVENTS[(1, 24)] = [("किरात समाजसुधार दिवस", 0)]
NEPALI_EVENTS[(1, 11)] = [("लोकतन्त्र दिवस", 1)]
NEPALI_EVENTS[(2, 15)] = [("गणतन्त्र दिवस", 1)]
NEPALI_EVENTS[(3, 15)] = [("दहि-चिउरा खाने दिन", 0)]
NEPALI_EVENTS[(4, 15)] = [("खिर खाने दिन", 0)]
NEPALI_EVENTS[(5, 1)] = [("भाद्र सङ्क्रान्ति", 0)]
NEPALI_EVENTS[(5, 29)] = [("राष्ट्रिय बाल दिवस", 0)]
NEPALI_EVENTS[(9, 27)] = [("पृथ्वी जयन्ती", 0)]
NEPALI_EVENTS[(10, 1)] = [("माघे सङ्क्रान्ति", 0)]
NEPALI_EVENTS[(10, 16)] = [("शहीद दिवस", 1)]
NEPALI_EVENTS[(11, 7)] = [("प्रजातन्त्र दिवस", 1)]

ENGLISH_EVENTS = defaultdict(lambda: [])

ENGLISH_EVENTS[(1, 1)] = [("अंग्रेजी नयाँ वर्ष", 0)]
ENGLISH_EVENTS[(2, 14)] = [("भ्यालेन्टाईन डे", 0)]
ENGLISH_EVENTS[(3, 22)] = [("विश्व पानी दिवस", 0)]
ENGLISH_EVENTS[(3, 24)] = [("विश्व क्षयरोग बिरुद्ध दिवस", 0)]
ENGLISH_EVENTS[(4, 1)] = [("विश्व मूर्ख दिवस", 0)]
ENGLISH_EVENTS[(4, 7)] = [("विश्व स्वास्थ्य दिवस", 0)]
ENGLISH_EVENTS[(5, 1)] = [("मजदुर दिवस", 0)]
ENGLISH_EVENTS[(5, 3)] = [("प्रेस स्वतन्त्रता दिवस", 0)]
ENGLISH_EVENTS[(5, 1)] = [("विश्व दुरसंचार दिवस", 0)]
ENGLISH_EVENTS[(5, 31)] = [("विश्व धुम्रपानरहित दिवस", 0)]
ENGLISH_EVENTS[(6, 5)] = [("विश्व वातावरण दिवस", 0)]
ENGLISH_EVENTS[(6, 20)] = [("विश्व शरणार्थी दिवस", 0)]
ENGLISH_EVENTS[(7, 11)] = [("अन्तराष्टिय जनसङ्ख्या दिवस", 0)]
ENGLISH_EVENTS[(8, 12)] = [("विश्व युवा दिवस", 0)]
ENGLISH_EVENTS[(9, 8)] = [("शिक्षा तथा साक्षरता दिवस", 0)]
ENGLISH_EVENTS[(9, 27)] = [("विश्व पर्यटन दिवस", 0)]
ENGLISH_EVENTS[(10, 1)] = [("अन्तराष्टिय जेष्ठ नागरिक दिवस", 0)]
ENGLISH_EVENTS[(10, 9)] = [("विश्व हुलाक दिवस", 0)]
ENGLISH_EVENTS[(10, 13)] = [("प्राकृतिक विपत्ति न्यूनिकरण दिवस", 0)]
ENGLISH_EVENTS[(10, 14)] = [("विश्व गुणस्तर दिवस", 0)]
ENGLISH_EVENTS[(10, 16)] = [("विश्व खाद्य दिवस", 0)]
ENGLISH_EVENTS[(10, 16)] = [("विश्व गरिबी निवारण दिवस", 0)]
ENGLISH_EVENTS[(10, 24)] = [("संयुक्त राष्ट्रसंघ दिवस", 0)]
ENGLISH_EVENTS[(11, 14)] = [("विश्व मधुमेह दिवस", 0)]
ENGLISH_EVENTS[(11, 17)] = [("अन्तराष्टिय विद्यार्थी दिवस", 0)]
ENGLISH_EVENTS[(11, 20)] = [("विश्व बाल अधिकार दिवस", 0)]
ENGLISH_EVENTS[(11, 21)] = [("विश्व टेलिभिजन दिवस", 0)]
ENGLISH_EVENTS[(12, 1)] = [("विश्व एड्स दिवस", 0)]
ENGLISH_EVENTS[(12, 7)] = [("अन्तर्राष्ट्रीय नागरिक उड्डयन दिवस", 0)]
ENGLISH_EVENTS[(12, 9)] = [("विश्व भ्रष्टाचारविरुद्द दिवस", 0)]
ENGLISH_EVENTS[(12, 10)] = [("विश्व मानव अधिकार दिवस", 0)]
