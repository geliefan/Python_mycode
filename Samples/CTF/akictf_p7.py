# -*- coding:utf-8
Token = {
    u"Υ":"e", # e
    u"Ζ":"_",
    u"J": "r",
    u"Ο": "_",
    u"Ι":"y", # y
    u"Ν": "_",
    u"Μ": "_",
    u"Δ":"m" , # m
    u"G": "_",
    u"Γ": "_",
    u"Β": "_",
    u"Η": "_",
    u"Α": "_",
    u"Τ": "_",
    u"Q":"_",
    u"Χ": "_",
    u"Ρ": "_",
    u"W":"_",
    u"Π": "_",
    u"Κ": "_",
    u"F": "_",
    u"Σ": "_",
    u' ': "-"
         }

cry = u"ΥΔΗΖΙΝΔJΙ ΧJΙΟΜJGGΔΙΒ ΑJΜΟ ΥJΓ ΓΥΝ ΙJΡ WΖΖΙ ΥΖΗJGΔΝΓΖΥ ΥΙΥ ΟΔΗΖ ΝΟΥΜΟΖΥ ΑGJΡΔΙΒ ΜΖQΖΜΝΖGΤ QΥΠΝ ΗΥΙΥΒΖΥ ΟJ ΖΝΧΥΚΖ ΑΜJΗ ΟΓΖ ΥΔΝΟJΜΟΖΥ ΝΚΥΧΖ WΠΟ ΟΓΖ ΜΖΥG QJΤΥΒΖ JΑ ΥΜFΥΙJΔΥ ΔΙ ΟΓΖ ΒΥGΥΣΤ ΓΥΝ JΙGΤ ΝΟΥΜΟΖΥ"
lists = list(cry)
for x in cry:
    if x:
        print Token[x],
    else:
        pass