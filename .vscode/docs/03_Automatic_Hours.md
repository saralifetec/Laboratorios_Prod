# Automatic Hours

## Purpose

The Automatic Hours module is responsible for generating work hour records automatically for Network activities.

The objective is to allocate available hours to eligible users while respecting:

- User calendars
- Available test capacity
- Existing recorded hours
- Configured generation periods
- Automatic hours generation rules

---

# User Notification

When automatic hours generation is pending, an alert is displayed on the Dashboard page.

The alert is visible only to users with the System role.

Example:

Pending Hours Export

Automatic hours have not yet been generated for the current period.

---

# Dashboard Integration

## Route

```python
@app.route('/')
```

## Service

```python
verificar_alerta_horas_auto()
```

The dashboard does not perform any business calculation.

It only requests the status from the service layer and passes the result to the template.

---

# Models

## HorasAuto

Stores automatic generation configuration.

### Fields

#### ativo

```python
ativo = db.Column(db.Boolean)
```

Enables or disables automatic hours generation.

#### frequencia

```python
frequencia = db.Column(db.String(20))
```

Generation frequency.

Current value:

```text
semanal
```

#### repeticao

```python
repeticao = db.Column(db.Integer)
```

Generation day.

Example:

```text
2 = Monday
3 = Tuesday
```

#### dia_inicio

```python
dia_inicio = db.Column(db.Date)
```

Date from which automatic generation becomes active.

---

## HorasAutoExecucao

Stores automatic generation history.

### Fields

#### data_execucao

Date when the generation process was executed.

#### data_inicio

Generated period start date.

#### data_fim

Generated period end date.

---

# Alert Rules

Implemented in:

```python
verificar_alerta_horas_auto()
```

## Rule 1

Only System users may receive the notification.

```python
user.funcao_id == 3
```

---

## Rule 2

Automatic Hours must be enabled.

```python
HorasAuto.ativo == True
```

---

## Rule 3

Current date must be greater than or equal to:

```python
HorasAuto.dia_inicio
```

---

## Rule 4

The system calculates the latest valid generation period.

Function:

```python
calcular_ultimo_fim_valido()
```

---

## Rule 5

The most recent execution is determined using:

```python
HorasAutoExecucao
```

ordered by:

```python
data_fim DESC
```

---

## Rule 6

The alert is displayed when:

```text
No execution exists
```

or

```text
Latest execution end date
<
Latest valid period end date
```

---

# Current Workflow

```text
User opens dashboard
        ↓
verificar_alerta_horas_auto()
        ↓
Alert displayed
        ↓
User clicks Generate
        ↓
Automatic Hours modal opens
        ↓
Preview is generated
        ↓
User confirms generation
        ↓
Hours are created
        ↓
Execution is stored
```

---

# Files

Current implementation:

```text
routes/
    geral.py

services/
    horasauto_service.py

models/
    HorasAuto
    HorasAutoExecucao
```

---

# Refactoring Notes

Future target:

```text
routes/
    horasauto.py

services/
    horasauto_service.py

docs/
    03_Automatic_Hours.md
```

# Preview Generation

## Endpoint

```http
GET /horasauto/preview
```

## Purpose

Generates a preview of all pending Automatic Hours periods.

No records are written to the database.

The preview is used only for analysis and validation before generation.

---

# Flow

```text
Dashboard
    ↓
Open Automatic Hours Modal
    ↓
GET /horasauto/preview
    ↓
Calculate pending periods
    ↓
Generate period summaries
    ↓
Display preview
```

---

# Main Service

```python
obter_preview_horas_auto()
```

Returns:

```json
[
  {
    "start": "2026-07-01",
    "end": "2026-07-07",
    "resumo": {}
  }
]
```

Each element represents one pending generation period.

---

# Pending Period Detection

Function:

```python
obter_periodos_pendentes()
```

Purpose:

Determine which periods still require automatic generation.

---

## Logic

1. Read Automatic Hours configuration.

2. Calculate the latest closed generation cycle.

3. Read the latest execution stored in:

```python
HorasAutoExecucao
```

4. Generate all missing periods between:

```text
Last generated period
and
Last valid period
```

---

# Valid Cycle Calculation

Function:

```python
calcular_ultimo_fim_valido()
```

Purpose:

Determine the latest period that is fully completed.

---

## Example

Configuration:

```text
Generation day = Monday
```

Current date:

```text
Wednesday
```

Result:

```text
Last Monday is considered closed.
```

The system never generates hours for an unfinished cycle.

---

# Period Summary

Function:

```python
gerar_resumo_periodo()
```

Purpose:

Calculate required hours for every eligible user and every day of the selected period.

---

# Included Data Sources

The calculation uses:

## Holidays

Table:

```python
Feriado
```

Purpose:

Remove working hours from holidays unless explicitly overridden.

---

## User Configuration

Table:

```python
ConfHorasAuto
```

Purpose:

Defines:

- Daily hours
- General hours percentage
- Network membership
- Automatic generation eligibility

Only users with:

```python
auto = True
```

are considered.

---

## User Calendar

Table:

```python
UserCalendar
```

Purpose:

Apply special day rules.

Supported values:

```text
normal
ferias
falta
parcial
trabalhou
```

---

## Existing Hours

Table:

```python
Horas
```

Purpose:

Prevent duplicate allocation.

Already existing hours reduce the amount to generate.

---

# Working Day Rules

## Vacation

```text
ferias
```

Generated hours:

```text
0
```

---

## Absence

```text
falta
```

Generated hours:

```text
0
```

---

## Partial Day

```text
parcial
```

Generated hours:

```text
Calendar hours value
```

---

## Worked Holiday

```text
trabalhou
```

Generated hours:

```text
Normal daily hours
```

---

## Weekend

Default:

```text
0 hours
```

Exception:

```text
trabalhou
parcial
```

---

# Existing Hours Classification

Existing hours are grouped into:

## Network Hours

```text
n
```

Detected as:

```python
ensaio_id
```

or

```python
manual not starting with E.G
```

---

## General Hours

```text
g
```

Detected as:

```python
codigog_id
```

or

```python
manual starting with E.G
```

---

# Generation Targets

For every user and day:

## Total Required

```python
necessario_total
```

---

## Required Network Hours

```python
necessario_n
```

---

## Required General Hours

```python
necessario_g
```

Calculated using:

```python
horasgerais
```

configuration percentage.

---

# Compensation Rules

If one category exceeds the target:

```text
Network excess
↓
reduces General requirement
```

or

```text
General excess
↓
reduces Network requirement
```

Negative generation values are never allowed.

Final values are always:

```python
max(value, 0)
```

Automatic Hours business logic must remain inside the service layer.
Routes should only receive requests and return responses.

---

# User Detail View

## Purpose

Allows the user to inspect the automatic generation calculations for an individual technician before generating hours.

This view is intended for validation and troubleshooting.

---

# Navigation Flow

```text
Preview
    ↓
User Detail
    ↓
Network Summary
    ↓
Generation
```

---

# User Selection

The user selects a technician from:

```html
selectUserHorasAuto
```

The available users are loaded from:

```python
dadosHorasAuto
```

which is returned by:

```python
GET /horasauto/preview
```

---

# User Summary Table

Function:

```javascript
preencherTabelaUtilizador()
```

Displays one column per day of the selected period.

---

# Total Row

Field:

```python
total
```

Displays planned working hours for each day.

The value already includes:

- Holidays
- Vacations
- Absences
- Partial days
- Weekend rules

---

# Test Hours Section

## Required

Field:

```python
n_necessario
```

Network/Test hours required for that day.

---

## Existing

Field:

```python
n_existente
```

Hours already registered in test activities.

Sources:

```python
Horas.ensaio_id
```

or

```python
Horas.manual
```

when not classified as General hours.

---

# General Hours Section

## Required

Field:

```python
g_necessario
```

General hours target for that day.

Calculated from:

```python
ConfHorasAuto.horasgerais
```

---

## Existing

Field:

```python
g_existente
```

General hours already registered.

Sources:

```python
Horas.codigog_id
```

or

```python
Horas.manual
```

starting with:

```text
E.G
```

---

# Hours To Generate Section

## Tests

Field:

```python
n_gerar
```

Hours that still need to be generated and allocated to tests.

Formula:

```text
Required Test Hours
-
Existing Test Hours
```

after compensation rules are applied.

---

## General

Field:

```python
g_gerar
```

Hours that still need to be generated and allocated to General codes.

Formula:

```text
Required General Hours
-
Existing General Hours
```

after compensation rules are applied.

---

# Compensation Logic

The system allows compensation between categories.

Example:

Required:

```text
Tests   = 6h
General = 2h
```

Existing:

```text
Tests   = 8h
General = 0h
```

Result:

```text
Tests to Generate   = 0h
General to Generate = 0h
```

The excess Test hours compensate the missing General hours.

The same rule applies in the opposite direction.

---

# Objective

This screen allows the administrator to verify:

- Planned hours
- Existing hours
- Missing hours
- Compensation effects

before any automatic generation occurs.

# Historical View

The Automatic Hours History page allows users to inspect previous automatic generations.

## Available Periods

Periods are grouped by:

- Year
- Month
- Week

## Year Selection

Available years:

- Current year
- Previous year (only during January)

## Month Selection

The current month is selected by default.

## Week Definition

Week boundaries are determined by:

```python
HorasAuto.repeticao
```

Examples:

```text
2 = Monday → Sunday

3 = Tuesday → Monday

4 = Wednesday → Tuesday
```

The displayed periods always follow the configured automatic generation cycle.

## Default Selection

When opening the page:

- Current year is selected
- Current month is selected
- Latest completed period is selected

## Historical Period Selection

Periods are selected using three levels:

1. Year
2. Month
3. Week

The Week selector only displays periods belonging to the selected month.

This avoids presenting the user with excessive numbers of periods and simplifies navigation.

The most recent completed week is selected automatically.