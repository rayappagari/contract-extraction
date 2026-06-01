REQUIRED_CONTRACT_TYPES = {"MSA", "SOW", "NDA", "Amendment", "PO", "Other"}


def apply_business_rules(data: dict) -> list[str]:
    violations = []
    if data.get("contract_type") not in REQUIRED_CONTRACT_TYPES:
        violations.append(f"Unknown contract_type: {data.get('contract_type')}")
    parties = data.get("parties", [])
    roles = {p.get("role") for p in parties}
    if "buyer" not in roles and "licensee" not in roles:
        violations.append("No buyer or licensee party identified")
    if data.get("auto_renewal") and data.get("renewal_notice_days") is None:
        violations.append("auto_renewal is True but renewal_notice_days is missing")
    return violations
