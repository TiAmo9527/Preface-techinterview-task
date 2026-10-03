# Domain glossary

Version: 0.2

Revised: 2026-10-03

This is the shared glossary for the repository documentation. The product specification defines the required behavior.

| Term | Meaning |
|---|---|
| Property | One fictional hotel in a portfolio location. |
| Room | One identified room within one property. |
| Asset record | One stable record for one room/category combination. Its identity continues through purchases and replacements. |
| Category | Lighting, Water supply, or Air conditioning. Each room has one asset record in each category. |
| Invoice item | One identified purchase or replacement entry. It supplies a full snapshot for one existing asset record. |
| Snapshot | The asset name, purchase date, installation date, useful life, acquisition cost, and currency supplied together. |
| Baseline | The original property, room, observation, and asset information accepted from Assets. |
| Source evidence | Preserved baseline information, accepted invoice items, and their provenance. |
| Provenance | The upload reference, source filename, sheet, row coordinates, and actual import timestamp. |
| Source values | The latest applied invoice cost/currency pair. The baseline pair applies before any invoice update. |
| Current operational values | The current asset name, dates, and useful life. Manager edits can differ from source evidence. |
| Effective financial values | The active override cost/currency pair, or source values when no override exists. |
| Financial override | A manager's paired cost/currency correction with a reason, recorder, timestamp, and history. |
| Observation | The latest manual assessment of one room system. It has condition information separate from maintenance tickets. |
| Unassessed Unknown | No recorded assessment. The observation has no date, recorder, or note. |
| Recorded Unknown | An assessment that could not establish condition. It requires an observation date and recorder. |
| Maintenance ticket | One manually created maintenance record for a room, with an optional same-room asset link. |
| Ticket owner | A fictional person assigned to maintenance work. This person is not an authenticated permission role. |
| Recorder | A self-declared person attributed to a manual change or assessment. This name does not prove authenticated identity. |
| History | Persistent before/after information for invoice updates, overrides, or maintenance changes. Observations have no history. |
| Financial reporting date | The session date used for depreciation and replacement results. It does not select a historical portfolio snapshot. |
| Operational date | The actual current date in Asia/Hong_Kong. Maintenance overdue checks use this date. |
| Service anchor | The current installation date, or current purchase date when installation is absent. |
| Month anniversary | The original service day in a destination month, clamped to that month's last day when necessary. |
| Book value | Effective acquisition cost minus accumulated depreciation. |
| Spending proxy | Effective acquisition cost used for replacement planning. It is not a quotation or predicted repair expense. |
| FX | Currency conversion through a complete, dated, fixed fictional rate table. |
| Local mode | Display in each asset record's effective transaction currency. Mixed totals remain separate by currency. |
| Blocker | A validation error that prevents every write in an upload. |
| Warning | A diagnostic that does not prevent confirmation of an otherwise valid upload. |
| Conflict | Changed evidence under an existing identity, or different snapshots at a target's controlling invoice date. |
| Skip | An identical source identity that requires no evidence rewrite or operational update. |
| Historical-only item | New invoice evidence that does not apply an asset update. |
| Atomic commit | All writes for one confirmed upload succeed together. A failed commit preserves the previous saved state. |
| Preview | Proposed upload effects and diagnostics. Preview does not save records, evidence, or histories. |
| Demo data store | Shared local SQLite state for this prototype. Explicit reset clears its saved domain data to empty. |
| Reset data | Confirmed atomic deletion of domain records, evidence, and histories. Browser preferences and configuration remain. |
| Store generation | An identity changed on reset. Commands from the previous generation cannot mutate the new store. |
| Submission receipt | An atomic record of a successful command response. Identical retries do not repeat the mutation. |
| Normal restart | Stop and start the application with the same selected data store. |
| Owner approval | Alex's product or design decision. It does not mean client acceptance or passing application tests. |
| Inherited | A UI requirement already defined by a product requirement. |
| Confirmed | A UI choice that Alex confirmed. |
| Proposed | A detail without owner approval. Writing it does not make it required. |
| Specified | A requirement documented with a defining section and acceptance coverage. It is not execution evidence. |
