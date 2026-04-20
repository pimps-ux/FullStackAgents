from datetime import datetime
from pydantic import BaseModel, Field


class HubSpotContact(BaseModel):
    source_hub: str
    id: str
    email: str | None = None
    phone: str | None = None
    cpf: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    city: str | None = None
    consent: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


class HubSpotCompany(BaseModel):
    source_hub: str
    id: str
    name: str
    cnpj: str | None = None
    domain: str | None = None
    city: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UnifiedContact(BaseModel):
    unified_id: str
    canonical_name: str
    email: str | None = None
    phone: str | None = None
    cpf: str | None = None
    city: str | None = None
    origins: list[str]
    consent_any_source: bool


class UnifiedCompany(BaseModel):
    unified_id: str
    canonical_name: str
    cnpj: str | None = None
    domain: str | None = None
    city: str | None = None
    origins: list[str]


class PipelineRunResult(BaseModel):
    extracted_contacts: int
    extracted_companies: int
    unified_contacts: int
    unified_companies: int
    duplicate_contacts_removed: int
    duplicate_companies_removed: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
