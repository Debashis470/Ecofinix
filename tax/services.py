from decimal import Decimal, ROUND_HALF_UP


def compute_tax(income, deductions, regime):

    income = Decimal(income)
    deductions = Decimal(deductions)

    # ----- TAXABLE -----
    if regime == "old":
        taxable = max(income - deductions, Decimal("0"))
    else:
        taxable = income

    tax = Decimal("0")

    # ----- SLABS -----
    if regime == "old":
        slabs = [
            (250000, Decimal("0.00")),
            (500000, Decimal("0.05")),
            (1000000, Decimal("0.20")),
            (Decimal("99999999"), Decimal("0.30")),
        ]
    else:
        slabs = [
            (300000, Decimal("0.00")),
            (600000, Decimal("0.05")),
            (900000, Decimal("0.10")),
            (1200000, Decimal("0.15")),
            (1500000, Decimal("0.20")),
            (Decimal("99999999"), Decimal("0.30")),
        ]

    prev_limit = Decimal("0")

    for limit, rate in slabs:
        if taxable > prev_limit:
            slab_amount = min(taxable, Decimal(limit)) - prev_limit
            tax += slab_amount * rate
            prev_limit = Decimal(limit)

    # ----- CESS -----
    cess = tax * Decimal("0.04")
    total = tax + cess

    return {
        "taxable": taxable.quantize(Decimal("1."), rounding=ROUND_HALF_UP),
        "tax": tax.quantize(Decimal("1."), rounding=ROUND_HALF_UP),
        "cess": cess.quantize(Decimal("1."), rounding=ROUND_HALF_UP),
        "total": total.quantize(Decimal("1."), rounding=ROUND_HALF_UP),
    }