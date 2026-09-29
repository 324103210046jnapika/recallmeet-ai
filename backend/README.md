# RecallMeet AI — Backend

The backend of RecallMeet AI is built with FastAPI and provides the meeting intelligence, client history, memory, and preparation APIs.

## Responsibilities

- Record and persist client meetings
- Track decisions, concerns, commitments, and follow-ups
- Store meeting experience through the memory service
- Recall relevant historical context
- Reflect on recalled context
- Generate structured meeting preparation briefs
- Provide client and meeting insights
- Expose health and diagnostic information

## Memory Architecture

RecallMeet follows the memory-driven workflow:

```text
RETAIN → RECALL → REFLECT → PREPARE