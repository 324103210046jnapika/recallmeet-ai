"""
Seed realistic demo data demonstrating evolution across multiple client meetings.

All meetings are:
1. Retained into Hindsight memory.
2. Saved into the local resilient store.

This script is intended to be run manually from the backend directory.
"""

import sys
import os
import asyncio


# Add backend directory to sys.path so app modules can be imported.
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__)))
)


from app.schemas.meeting import MeetingCreate
from app.services.meeting_service import meeting_service
from app.services.hindsight_service import hindsight_service


DEMO_MEETINGS = [

    # ============================================================
    # ACME CORPORATION — MEETING 1
    # ============================================================

    MeetingCreate(
        client="Acme Corporation",
        contact="Sarah Chen, CTO",
        date="2026-08-15",
        title="Initial Discovery: Analytics Platform Modernization",

        meeting_notes=(
            "Met with Sarah Chen (CTO) to explore upgrading Acme Corporation's "
            "legacy reporting infrastructure into a modern AI-powered analytics "
            "engine. Sarah emphasized that time-to-market is the #1 company "
            "metric. They currently have an allocated budget of around $20,000 "
            "for this discovery & implementation phase. Discussion was positive "
            "and exploratory."
        ),

        decisions=[
            "Agreed to move forward with a technical feasibility assessment",
            "Target budget benchmark capped around $20,000 for initial phase"
        ],

        concerns=[
            "Deployment speed is critical — cannot tolerate months of engineering ramp-up"
        ],

        commitments=[
            "Team promised to return with preliminary deployment architecture by next week"
        ],

        follow_ups=[
            "Send follow-up deck on analytics platform architecture options"
        ]
    ),

    # ============================================================
    # ACME CORPORATION — MEETING 2
    # ============================================================

    MeetingCreate(
        client="Acme Corporation",
        contact="Sarah Chen, CTO",
        date="2026-08-25",
        title="Cloud Architecture & Timeline Alignment",

        meeting_notes=(
            "Sarah confirmed Acme's strong preference for native AWS deployment "
            "(they run all production workloads in AWS us-east-1). She established "
            "a firm six-week delivery target for the MVP to align with their Q4 "
            "board demo. Sarah explicitly asked for an architecture proposal "
            "showing containerization and VPC isolation."
        ),

        decisions=[
            "Selected AWS as the mandatory cloud deployment target",
            "Locked six-week MVP delivery window"
        ],

        concerns=[
            "Strict six-week deadline must be adhered to without slipping"
        ],

        commitments=[
            "Team committed to draft detailed architecture proposal detailing AWS microservices"
        ],

        follow_ups=[
            "Deliver AWS architecture proposal document before the next sync"
        ]
    ),

    # ============================================================
    # ACME CORPORATION — MEETING 3
    # ============================================================

    MeetingCreate(
        client="Acme Corporation",
        contact="Sarah Chen, CTO",
        date="2026-09-08",
        title="Security & Governance Deep Dive",

        meeting_notes=(
            "Reviewed the AWS architecture proposal with Sarah. While pleased "
            "with the AWS infrastructure choices, Sarah raised serious security "
            "concerns regarding enterprise data governance. She stated that "
            "Role-Based Access Control (RBAC) with granular tenant isolation "
            "is a non-negotiable prerequisite. She requested comprehensive "
            "security documentation and compliance validation before any "
            "production deployment."
        ),

        decisions=[
            "RBAC confirmed as mandatory technical requirement for user access"
        ],

        concerns=[
            "CTO raised significant security concerns regarding data isolation and access controls",
            "Multi-tenant security compliance review must be cleared before contract execution"
        ],

        commitments=[
            "Team committed to provide in-depth security documentation and RBAC architecture matrix"
        ],

        follow_ups=[
            "Schedule joint architecture review with Acme security compliance team"
        ]
    ),

    # ============================================================
    # ACME CORPORATION — MEETING 4
    # ============================================================

    MeetingCreate(
        client="Acme Corporation",
        contact="Sarah Chen, CTO",
        date="2026-09-22",
        title="Architecture Review & Pending Security Sign-Off",

        meeting_notes=(
            "Presented updated microservice architecture incorporating granular "
            "RBAC and AWS KMS encryption. Sarah noted progress is aligned with "
            "the six-week timeline, but emphasized that their internal security "
            "review remains open and unresolved. She cannot greenlight production "
            "rollout until Acme's InfoSec team validates the security plan. "
            "Our engineering team committed to deliver the finalized, signed "
            "security and governance specification by next Friday."
        ),

        decisions=[
            "RBAC model accepted in principle, subject to final InfoSec review"
        ],

        concerns=[
            "Security review remains pending and is the single blocking gate to contract execution and deployment",
            "CTO will not sign off until formal InfoSec approval is granted"
        ],

        commitments=[
            "Engineering team committed to deliver finalized security plan and audit documentation by Friday"
        ],

        follow_ups=[
            "Deliver final security plan documentation",
            "Prepare for upcoming meeting with Sarah Chen and security auditors"
        ]
    ),

    # ============================================================
    # NOVAHEALTH SYSTEMS — MEETING 1
    # ============================================================

    MeetingCreate(
        client="NovaHealth Systems",
        contact="Dr. Marcus Vance, VP of Health Informatics",
        date="2026-09-05",
        title="Clinical Workflow AI Exploration",

        meeting_notes=(
            "Initial meeting with Dr. Marcus Vance to discuss clinical transcript "
            "summarization. Paramount requirement is strict HIPAA compliance and "
            "zero data retention for model retraining. Marcus highlighted that "
            "all patient data must undergo de-identification before AI processing."
        ),

        decisions=[
            "Agreed to explore HIPAA-compliant pipeline"
        ],

        concerns=[
            "Zero patient data leakage risk permitted; strictly non-negotiable"
        ],

        commitments=[
            "Provide overview of HIPAA data processing guarantees and encryption standards"
        ],

        follow_ups=[
            "Share compliance whitepaper with NovaHealth legal team"
        ]
    ),

    # ============================================================
    # NOVAHEALTH SYSTEMS — MEETING 2
    # ============================================================

    MeetingCreate(
        client="NovaHealth Systems",
        contact="Dr. Marcus Vance, VP of Health Informatics",
        date="2026-09-18",
        title="Infrastructure & BAA Contract Discussion",

        meeting_notes=(
            "Follow-up with Dr. Vance. NovaHealth prefers private cloud deployment "
            "on Microsoft Azure or on-prem VPC. Marcus requested a formal Business "
            "Associate Agreement (BAA) draft before running a pilot on synthetic "
            "patient records."
        ),

        decisions=[
            "Agreed that pilot will use synthetic data only"
        ],

        concerns=[
            "BAA execution timeline cannot delay hospital pilot schedule"
        ],

        commitments=[
            "Legal team committed to provide standard BAA draft within 5 business days"
        ],

        follow_ups=[
            "Deliver BAA draft to Dr. Vance's legal counsel"
        ]
    )
]


async def seed():
    """
    Seed all demo meetings asynchronously.

    Hindsight SDK calls are asynchronous, so this function must
    be executed through asyncio.
    """

    print("=" * 60)
    print("SEEDING RECALLMEET AI WITH HINDSIGHT")
    print("=" * 60)

    # ------------------------------------------------------------
    # Check Hindsight connection
    # ------------------------------------------------------------

    conn = await hindsight_service.check_connection()

    if conn.get("connected"):

        print(
            f"[OK] Hindsight connected at "
            f"{conn.get('base_url')} "
            f"(v{conn.get('version')})"
        )

        await hindsight_service.ensure_bank()

    else:

        print(
            f"[NOTE] Hindsight server offline "
            f"({conn.get('error')}). "
            f"Using resilient local memory layer."
        )

    # ------------------------------------------------------------
    # Retain demo meetings
    # ------------------------------------------------------------

    for idx, meeting in enumerate(DEMO_MEETINGS, 1):

        custom_id = f"demo_{idx}"

        saved = await meeting_service.create_meeting(
            meeting,
            custom_id=custom_id
        )

        print(
            f"[{saved.hindsight_status}] "
            f"Retained: {saved.client} - "
            f"{saved.title} ({saved.date})"
        )

    # ------------------------------------------------------------
    # Final summary
    # ------------------------------------------------------------

    print("=" * 60)

    print(
        f"Successfully seeded "
        f"{len(DEMO_MEETINGS)} meetings "
        f"across 2 enterprise clients."
    )

    print(
        "Clients available: "
        "Acme Corporation (4 meetings), "
        "NovaHealth Systems (2 meetings)"
    )

    print("=" * 60)

    hindsight_service.close()


if __name__ == "__main__":
    asyncio.run(seed())