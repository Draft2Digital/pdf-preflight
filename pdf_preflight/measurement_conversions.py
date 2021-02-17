from decimal import Decimal


# convert from inches to pdf points
def in2pt(inch):
    return Decimal(inch) * Decimal("72")


# convert from mm to pdf points
def mm2pt(mm):
    return Decimal(mm) * (Decimal("72") / Decimal("25.4"))


# convert from cm to pdf points
def cm2pt(cm):
    return Decimal(cm) * mm2pt(10)

##########################################################################


# convert from pdf points to inches
def pt2in(pt):
    return Decimal(pt) / in2pt(1)


# convert from pdf points to mm
def pt2mm(pt):
    return Decimal(pt) / mm2pt(1)


# convert from pdf points to cm
def pt2cm(pt):
    return Decimal(pt) / cm2pt(1)
