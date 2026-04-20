# AI Agents Multi-API - PA-ECOZERO

Projeto end-to-end para consolidar múltiplos HubSpots via API/script, unificar dados com deduplicação e expor uma API final com dashboard intuitivo.

## O que este projeto entrega
- Pipeline E2E replicável para outros públicos/setores.
- Schema padrão interno para contatos e empresas.
- Deduplicação inteligente (determinística + fuzzy com RapidFuzz).
- API FastAPI para executar sincronização e consultar KPIs.
- Dashboard web simples e intuitivo para time comercial/gestão.
- Base para LGPD: consentimento e rastreio de origem.

## Arquitetura resumida
```
HubSpot A ─┐
HubSpot B ─┼──> Extract ─> Normalize ─> Deduplicate ─> Warehouse ─> API/Dashboard
HubSpot C ─┘
```

## Estrutura
- `app/main.py`: API FastAPI + endpoints de pipeline e dashboard.
- `app/pipeline.py`: lógica de extração (simulada), normalização e deduplicação.
- `app/schemas.py`: schema interno padrão.
- `app/storage.py`: storage local JSON (substituível por PostgreSQL/BigQuery).
- `templates/dashboard.html`: dashboard.
- `static/style.css`: estilos do dashboard.
- `docs/architecture.md`: visão técnica e governança LGPD.

## Rodando local
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Acesse:
- Dashboard: `http://localhost:8000/dashboard`
- Health: `http://localhost:8000/health`

## Endpoints principais
- `POST /pipeline/run`: executa pipeline completo e persiste dados unificados.
- `GET /api/dashboard`: retorna KPIs consolidados.

## Como adaptar para produção (roadmap)
1. Trocar extractor simulado por clientes HubSpot reais (tokens por conta).
2. Adicionar tabelas SQL (PostgreSQL) para histórico incremental.
3. Criar jobs agendados (Airflow/Cron/K8s CronJob).
4. Modelagem analítica com dbt + BI (Power BI / Looker).
5. Sincronização reversa para HubSpot master/ERP.

## Script comercial reutilizável (PA-ECOZERO)
### Pitch de alta conversão (resumo)
- **Dor:** alto consumo de água, custo operacional elevado e inconsistência de qualidade.
- **Mudança:** processamento com zero efluente líquido, menor custo por saca e mais previsibilidade.
- **Prova:** métricas reais de água economizada, custos reduzidos e aumento de lotes especiais.
- **Ação:** diagnóstico técnico + simulação de payback + plano de implantação.

### Objeções prontas
1. "Investimento inicial é alto"
   - Resposta: comparar TCO e payback por safra, não apenas CAPEX.
2. "Não sei se funciona para meu café"
   - Resposta: executar piloto com lotes e maturações diferentes; medir score e rendimento.
3. "Tecnologia nova"
   - Resposta: mostrar casos de operação completa de safra com menos paradas e manutenção.

### Canais de uso
- Campo: roteiro de visita com diagnóstico e ROI.
- WhatsApp: mensagens curtas com prova social e CTA para demonstração.
- Feiras: narrativa visual focada em água, custo/saca e qualidade de xícara.
