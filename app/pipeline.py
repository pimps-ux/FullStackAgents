from __future__ import annotations

from collections import defaultdict
from hashlib import md5
from rapidfuzz import fuzz

from app.schemas import (
    HubSpotCompany,
    HubSpotContact,
    PipelineRunResult,
    UnifiedCompany,
    UnifiedContact,
)


def extract_from_hubspot_simulated() -> tuple[list[HubSpotContact], list[HubSpotCompany]]:
    """Simula extração de múltiplos hubs HubSpot via API."""
    contacts = [
        HubSpotContact(source_hub="hub_a", id="1", email="joao@fazenda.com", phone="35999990000", cpf="12345678901", first_name="João", last_name="Silva", city="Varginha", consent=True),
        HubSpotContact(source_hub="hub_b", id="99", email="joao@fazenda.com", phone="35999990000", cpf="12345678901", first_name="Joao", last_name="Silva", city="Varginha", consent=True),
        HubSpotContact(source_hub="hub_c", id="501", email="compras@serraverde.com", phone="31988887777", first_name="Ana", last_name="Lima", city="Três Pontas", consent=False),
    ]

    companies = [
        HubSpotCompany(source_hub="hub_a", id="c10", name="Fazenda Serra Verde", cnpj="12345678000190", domain="serraverde.com", city="Três Pontas"),
        HubSpotCompany(source_hub="hub_b", id="c77", name="Faz. Serra Verde", cnpj="12345678000190", domain="serraverde.com", city="Tres Pontas"),
        HubSpotCompany(source_hub="hub_c", id="c01", name="Coop Sul de Minas", cnpj="98765432000110", domain="coopsm.com", city="Varginha"),
    ]
    return contacts, companies


def _hash_key(seed: str) -> str:
    return md5(seed.encode("utf-8")).hexdigest()[:12]


def deduplicate_contacts(contacts: list[HubSpotContact]) -> list[UnifiedContact]:
    groups: dict[str, list[HubSpotContact]] = defaultdict(list)

    for c in contacts:
        key = c.email or c.phone or c.cpf or f"{c.first_name}-{c.last_name}-{c.city}"
        groups[key.lower()].append(c)

    unified: list[UnifiedContact] = []
    for key, rows in groups.items():
        base = rows[0]
        canonical_name = " ".join(filter(None, [base.first_name, base.last_name])).strip() or "Sem Nome"

        # fallback de similaridade para nomes (fuzzy)
        for r in rows[1:]:
            candidate = " ".join(filter(None, [r.first_name, r.last_name])).strip()
            if candidate and fuzz.ratio(canonical_name.lower(), candidate.lower()) > 80:
                canonical_name = canonical_name if len(canonical_name) >= len(candidate) else candidate

        unified.append(
            UnifiedContact(
                unified_id=_hash_key(key),
                canonical_name=canonical_name,
                email=base.email,
                phone=base.phone,
                cpf=base.cpf,
                city=base.city,
                origins=[f"{r.source_hub}:{r.id}" for r in rows],
                consent_any_source=any(r.consent for r in rows),
            )
        )
    return unified


def deduplicate_companies(companies: list[HubSpotCompany]) -> list[UnifiedCompany]:
    groups: dict[str, list[HubSpotCompany]] = defaultdict(list)

    for c in companies:
        key = c.cnpj or c.domain or f"{c.name}-{c.city}"
        groups[key.lower()].append(c)

    unified: list[UnifiedCompany] = []
    for key, rows in groups.items():
        base = rows[0]
        canonical_name = base.name
        for r in rows[1:]:
            if fuzz.ratio(canonical_name.lower(), r.name.lower()) > 85:
                canonical_name = canonical_name if len(canonical_name) >= len(r.name) else r.name
        unified.append(
            UnifiedCompany(
                unified_id=_hash_key(key),
                canonical_name=canonical_name,
                cnpj=base.cnpj,
                domain=base.domain,
                city=base.city,
                origins=[f"{r.source_hub}:{r.id}" for r in rows],
            )
        )

    return unified


def run_pipeline() -> tuple[PipelineRunResult, list[UnifiedContact], list[UnifiedCompany]]:
    contacts, companies = extract_from_hubspot_simulated()
    unified_contacts = deduplicate_contacts(contacts)
    unified_companies = deduplicate_companies(companies)

    result = PipelineRunResult(
        extracted_contacts=len(contacts),
        extracted_companies=len(companies),
        unified_contacts=len(unified_contacts),
        unified_companies=len(unified_companies),
        duplicate_contacts_removed=len(contacts) - len(unified_contacts),
        duplicate_companies_removed=len(companies) - len(unified_companies),
    )
    return result, unified_contacts, unified_companies
