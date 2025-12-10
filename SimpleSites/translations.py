TRANSLATIONS = {
    'en': {
        'meta': {
            'title_suffix': ' | Hope TCM'
        },
        'header': {
            'logo_alt': 'Hope Traditional Chinese Medicine Clinic',
            'title_line1': 'Hope Traditional',
            'title_line2': 'Chinese Medicine Clinic',
            'compact_title_line1': 'Hope Traditional',
            'compact_title_line2': 'Chinese Medicine Clinic',
            'subtitle': '向&nbsp;&nbsp;陽&nbsp;&nbsp;中&nbsp;&nbsp;醫&nbsp;&nbsp;診&nbsp;&nbsp;所'
        },
        'nav': {
            'home': 'Home',
            'therapists': 'Therapists',
            'treatments': 'Treatments',
            'blog': 'Blog',
            'contact': 'Contact',
            'book_now': 'Book Now',
            'lang_switch': '中文',
            'lang_link_prefix': '/cn'  # Link to switch TO
        },
        'footer': {
            'address': '235-889 Carnarvon St, Buzzer 235, New Westminster, BC V3M1G2',
            'rights': 'Copyright © 2023 - 2025. Acupuncture, Facial Rejuvenation, Cupping, Moxibustion, Gua Sha & Hebal treatments at Hope Traditional Chinese Medicine Clinic.'
        }
    },
    'cn': {
        'meta': {
            'title_suffix': ' | Hope TCM' # Example suffix
        },
        'header': {
            'logo_alt': 'Hope Traditional Chinese Medicine Clinic', # Keep English for alt or use CN? keeping EN mostly for file ref but alt text can be CN
             # The design uses English for title lines even in CN template? 
             # Looking at cn/main.html, lines 36-37: "HOPE TRADITIONAL" / "CHINESE MEDICINE CLINIC" are English.
             # Only the subtitle "向 陽 中 醫 診 所" is the same.
             # So actually, the header is identical in both langauges except for semantics?
             # Wait, in the user's previous `cn/main.html`:
             # p tag: "HOPE TRADITIONAL", "CHINESE MEDICINE CLINIC". 
             # So the "title" is English in both sites.
            'title_line1': 'HOPE TRADITIONAL', # Original CN template used uppercase
            'title_line2': 'CHINESE MEDICINE CLINIC',
            'compact_title_line1': 'HOPE TRADITIONAL',
            'compact_title_line2': 'CHINESE MEDICINE CLINIC',
            'subtitle': '向&nbsp;&nbsp;陽&nbsp;&nbsp;中&nbsp;&nbsp;醫&nbsp;&nbsp;診&nbsp;&nbsp;所'
        },
        'nav': {
            'home': '首页', 
            'therapists': '医师',
            'treatments': '治疗项目',
            'blog': '博客',
            'contact': '联系我们',
            'book_now': '网上预约',
            'lang_switch': 'English',
            'lang_link_prefix': '' # Link to switch TO (root for EN)
        },
        'footer': {
            'address': '235-889 Carnarvon St, Buzzer 235, New Westminster, BC V3M1G2',
            'rights': '版权所有 © 2023 - 2025. 针灸, 美容针灸, 拔罐, 艾灸, 刮痧, 中草药治疗等 @Hope Traditional Chinese Medicine Clinic'
        }
    }
}
