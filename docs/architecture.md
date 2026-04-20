# Arquitetura E2E - Multi HubSpot para PA-ECOZERO

## Objetivo
Consolidar múltiplas bases HubSpot (distribuidores, revendas, operação nacional) em um **schema padrão interno**, com **deduplicação inteligente**, armazenamento central e API para consumo comercial.

## Fluxo
1. **Extract:** conectar em N contas HubSpot via token privado por conta.
2. **Normalize:** mapear campos para schema interno padrão (`contacts`, `companies`).
3. **Deduplicate:** regras determinísticas + fuzzy.
4. **Store:** persistir em warehouse (exemplo local JSON; produção PostgreSQL/BigQuery).
5. **Serve:** API + dashboard para operação e gestão.

## Regras de deduplicação sugeridas
- Contatos: email > telefone > CPF > nome/cidade (fuzzy).
- Empresas: CNPJ > domínio > nome/cidade (fuzzy).

## LGPD
- Manter campo de consentimento por origem.
- Registrar origem (`hub:id`) em todos os registros unificados.
- Minimizar movimentação de dados sensíveis.
- Auditar execuções de pipeline.

## Estratégia de sincronização
- Delta sync a cada 5–15 min.
- Full sync semanal.
- Reprocessamento on-demand por conta HubSpot.
