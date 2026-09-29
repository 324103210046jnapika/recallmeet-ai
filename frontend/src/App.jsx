import React, { useEffect, useMemo, useState } from "react";
import {
  Activity,
  ArrowRight,
  Brain,
  CalendarDays,
  Check,
  CheckCircle2,
  CircleAlert,
  Clock3,
  Database,
  FileText,
  LayoutDashboard,
  MessageSquareText,
  Plus,
  RefreshCw,
  Search,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  Target,
  Users,
  X,
} from "lucide-react";

import {
  getMeetings,
  getHealth,
  prepareMeeting,
  createMeeting,
} from "./api/meetings";

import { getClients } from "./api/clients";

const DEMO_CLIENT = "Acme Corp";

const DEMO_MEETINGS = [
  {
    id: "demo-1",
    client: "Acme Corp",
    contact: "Sarah Chen, CTO",
    title: "Analytics Platform Discovery",
    date: "2026-09-12",
    meeting_notes:
      "Discussed the analytics platform, estimated $20k budget, and deployment architecture.",
    decisions: ["Architecture proposal required"],
    concerns: ["Deployment approach needs clarification"],
    commitments: [
      "Engineering team to prepare architecture proposal",
    ],
    follow_ups: ["Send architecture proposal"],
  },
  {
    id: "demo-2",
    client: "Acme Corp",
    contact: "Sarah Chen, CTO",
    title: "Cloud Deployment Planning",
    date: "2026-09-17",
    meeting_notes:
      "Acme prefers AWS and expects an approximately six-week delivery timeline.",
    decisions: [
      "AWS selected as preferred deployment target",
    ],
    concerns: [
      "Delivery schedule needs technical validation",
    ],
    commitments: ["Schedule technical discussion"],
    follow_ups: ["Confirm six-week delivery plan"],
  },
  {
    id: "demo-3",
    client: "Acme Corp",
    contact: "Sarah Chen, CTO",
    title: "Security Architecture Discussion",
    date: "2026-09-23",
    meeting_notes:
      "The CTO raised security concerns and requested role-based access control.",
    decisions: ["RBAC required"],
    concerns: ["Enterprise security review pending"],
    commitments: ["Provide final security architecture"],
    follow_ups: ["Schedule security review"],
  },
  {
    id: "demo-4",
    client: "Acme Corp",
    contact: "Sarah Chen, CTO",
    title: "Production Readiness Review",
    date: "2026-09-26",
    meeting_notes:
      "Security review remains open before production deployment.",
    decisions: [
      "Security review required before production",
    ],
    concerns: ["Security approval is still pending"],
    commitments: ["Deliver final security plan"],
    follow_ups: ["Complete security review"],
  },
];

function formatDate(value) {
  if (!value) return "No date";

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return String(value);
  }

  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function cleanText(value) {
  if (!value) return "";

  return String(value)
    .replace(/\[DEVELOPMENT FALLBACK\]:?/gi, "")
    .replace(/DEVELOPMENT FALLBACK:?/gi, "")
    .replace(/\s+/g, " ")
    .trim();
}

function isHeadingOnly(value) {
  if (!value) return true;

  const text = String(value).trim().toLowerCase();

  return (
    text === "commitments & promises made to client:" ||
    text === "commitments & promises made to client" ||
    text === "concerns & unresolved objections:" ||
    text === "concerns & unresolved objections" ||
    text === "action items & next steps:" ||
    text === "action items & next steps"
  );
}

function cleanArray(values) {
  if (!Array.isArray(values)) return [];

  return values
    .map((item) => cleanText(item))
    .filter(
      (item) => item && !isHeadingOnly(item)
    );
}

function extractFromMemorySources(
  sources,
  sectionName,
  nextSectionNames = []
) {
  if (!Array.isArray(sources)) return [];

  const output = [];

  for (const source of sources) {
    const content = source?.content || "";

    if (!content) continue;

    const lines = content.split("\n");

    let collecting = false;

    for (const rawLine of lines) {
      const line = rawLine.trim();

      if (!line) continue;

      if (
        line
          .toLowerCase()
          .includes(sectionName.toLowerCase())
      ) {
        collecting = true;
        continue;
      }

      if (
        collecting &&
        nextSectionNames.some((name) =>
          line
            .toLowerCase()
            .includes(name.toLowerCase())
        )
      ) {
        collecting = false;
        continue;
      }

      if (collecting) {
        const cleaned = line
          .replace(/^[-•]\s*/, "")
          .trim();

        if (
          cleaned &&
          !isHeadingOnly(cleaned)
        ) {
          output.push(cleanText(cleaned));
        }
      }
    }
  }

  return [...new Set(output)];
}

function normalizeBrief(brief) {
  if (!brief) return null;

  const memorySources =
    brief.memory_sources || [];

  let commitments = cleanArray(
    brief.previous_commitments
  );

  if (commitments.length === 0) {
    commitments = extractFromMemorySources(
      memorySources,
      "Commitments & Promises Made to Client",
      ["Action Items & Next Steps"]
    );
  }

  let concerns = cleanArray(
    brief.unresolved_concerns
  );

  if (concerns.length === 0) {
    concerns = extractFromMemorySources(
      memorySources,
      "Concerns & Unresolved Objections",
      [
        "Commitments & Promises Made to Client",
        "Action Items & Next Steps",
      ]
    );
  }

  let actions = cleanArray(
    brief.open_action_items
  );

  if (actions.length === 0) {
    actions = extractFromMemorySources(
      memorySources,
      "Action Items & Next Steps",
      []
    );
  }

  return {
    ...brief,

    executive_summary: cleanText(
      brief.executive_summary ||
        "No executive summary was generated."
    ),

    client_priorities: cleanArray(
      brief.client_priorities
    ),

    previous_commitments: commitments,

    open_action_items: actions,

    unresolved_concerns: concerns,

    risks: cleanArray(brief.risks),

    suggested_agenda: cleanArray(
      brief.suggested_agenda
    ),

    talking_points: cleanArray(
      brief.talking_points
    ),

    questions_to_ask: cleanArray(
      brief.questions_to_ask
    ),

    recommended_next_steps: cleanArray(
      brief.recommended_next_steps
    ),

    memory_sources: memorySources,
  };
}

function StatusDot({ active = false }) {
  return (
    <span
      className={`h-2.5 w-2.5 rounded-full ${
        active
          ? "bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,.7)]"
          : "bg-amber-400"
      }`}
    />
  );
}

function StatCard({
  icon: Icon,
  label,
  value,
  detail,
}) {
  return (
    <div className="glass-card p-5">
      <div className="flex items-start justify-between">
        <div className="icon-box">
          <Icon size={19} />
        </div>

        <span className="text-xs text-slate-500">
          LIVE
        </span>
      </div>

      <div className="mt-5 text-3xl font-semibold tracking-tight text-white">
        {value}
      </div>

      <div className="mt-1 text-sm font-medium text-slate-300">
        {label}
      </div>

      <div className="mt-2 text-xs text-slate-500">
        {detail}
      </div>
    </div>
  );
}

/* =========================================================
   HINDSIGHT MEMORY PIPELINE
   ========================================================= */

function MemoryPipeline({
  brief,
  memoryEnabled,
}) {
  const memoryCount =
    brief?.memory_sources?.length || 0;

  const steps = [
    {
      number: "01",
      title: "RETAIN",
      subtitle: "Meeting captured",
      description:
        "Client decisions, concerns, commitments and follow-ups become persistent experience.",
      icon: FileText,
      active: true,
    },
    {
      number: "02",
      title: "RECALL",
      subtitle: `${memoryCount} ${
        memoryCount === 1
          ? "memory"
          : "memories"
      } retrieved`,
      description:
        "Relevant historical interactions are retrieved for the upcoming client context.",
      icon: Database,
      active:
        memoryEnabled && memoryCount > 0,
    },
    {
      number: "03",
      title: "REFLECT",
      subtitle: "Relationship analyzed",
      description:
        "The agent identifies priorities, unresolved issues, risks and commitments.",
      icon: Brain,
      active: memoryEnabled,
    },
    {
      number: "04",
      title: "PREPARE",
      subtitle: "Brief generated",
      description:
        "Historical experience becomes actionable talking points, questions and next steps.",
      icon: Sparkles,
      active: Boolean(brief),
    },
  ];

  return (
    <section className="mt-5 overflow-hidden rounded-2xl border border-indigo-400/15 bg-[#0a1020] p-5 shadow-xl shadow-indigo-950/10">
      <div className="flex flex-col justify-between gap-3 md:flex-row md:items-center">
        <div>
          <div className="text-[10px] font-semibold uppercase tracking-[0.2em] text-indigo-300">
            HINDSIGHT MEMORY PIPELINE
          </div>

          <h3 className="mt-1 text-sm font-semibold text-white">
            How RecallMeet learns from every
            interaction
          </h3>
        </div>

        <div className="inline-flex w-fit items-center gap-2 rounded-full border border-indigo-400/15 bg-indigo-500/[0.07] px-3 py-1.5 text-[10px] font-semibold text-indigo-300">
          <Database size={12} />

          {memoryCount}{" "}
          {memoryCount === 1
            ? "memory"
            : "memories"}{" "}
          recalled
        </div>
      </div>

      <div className="mt-5 grid gap-3 lg:grid-cols-4">
        {steps.map((step, index) => {
          const Icon = step.icon;

          return (
            <React.Fragment key={step.title}>
              <div
                className={`rounded-xl border p-4 transition ${
                  step.active
                    ? "border-indigo-400/15 bg-indigo-500/[0.06]"
                    : "border-white/[0.06] bg-white/[0.02]"
                }`}
              >
                <div className="flex items-start justify-between">
                  <div
                    className={`flex h-9 w-9 items-center justify-center rounded-xl ${
                      step.active
                        ? "bg-indigo-500/15 text-indigo-300"
                        : "bg-white/[0.04] text-slate-600"
                    }`}
                  >
                    <Icon size={16} />
                  </div>

                  <span className="text-[9px] font-semibold tracking-[0.15em] text-slate-600">
                    {step.number}
                  </span>
                </div>

                <div className="mt-4 text-[10px] font-bold tracking-[0.18em] text-slate-400">
                  {step.title}
                </div>

                <div
                  className={`mt-1 text-xs font-medium ${
                    step.active
                      ? "text-indigo-200"
                      : "text-slate-600"
                  }`}
                >
                  {step.subtitle}
                </div>

                <p className="mt-2 text-[11px] leading-5 text-slate-600">
                  {step.description}
                </p>
              </div>

              {index < steps.length - 1 && (
                <div className="hidden items-center justify-center lg:flex">
                  <ArrowRight
                    size={15}
                    className="text-slate-700"
                  />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-2 text-[10px] text-slate-600">
        <span className="rounded-full border border-white/[0.06] px-2.5 py-1">
          Persistent experience
        </span>

        <span>→</span>

        <span className="rounded-full border border-white/[0.06] px-2.5 py-1">
          Relevant recall
        </span>

        <span>→</span>

        <span className="rounded-full border border-white/[0.06] px-2.5 py-1">
          Relationship reasoning
        </span>

        <span>→</span>

        <span className="rounded-full border border-white/[0.06] px-2.5 py-1">
          Actionable preparation
        </span>
      </div>
    </section>
  );
}

/* =========================================================
   PREPARATION SECTION CARD
   ========================================================= */

function SectionCard({
  title,
  eyebrow,
  icon: Icon,
  items = [],
  tone = "default",
}) {
  const toneClasses = {
    default: "text-indigo-300",
    green: "text-emerald-300",
    amber: "text-amber-300",
    red: "text-rose-300",
    cyan: "text-cyan-300",
  };

  return (
    <section className="glass-card p-5">
      <div className="flex items-center justify-between">
        <div>
          <div
            className={`text-[10px] font-semibold uppercase tracking-[0.18em] ${
              toneClasses[tone]
            }`}
          >
            {eyebrow}
          </div>

          <h3 className="mt-1 text-sm font-semibold text-white">
            {title}
          </h3>
        </div>

        {Icon && (
          <div className="icon-box-sm">
            <Icon size={15} />
          </div>
        )}
      </div>

      <div className="mt-4 space-y-2">
        {items.length > 0 ? (
          items.map((item, index) => (
            <div
              key={`${title}-${index}`}
              className="rounded-xl border border-white/[0.06] bg-white/[0.025] px-3 py-2.5 text-sm leading-6 text-slate-300"
            >
              {item}
            </div>
          ))
        ) : (
          <div className="rounded-xl border border-dashed border-white/[0.08] px-3 py-4 text-center text-xs text-slate-600">
            No items identified yet.
          </div>
        )}
      </div>
    </section>
  );
}

/* =========================================================
   MAIN APP
   ========================================================= */

function App() {
  const [meetings, setMeetings] = useState([]);
  const [clients, setClients] = useState([]);
  const [health, setHealth] = useState(null);

  const [selectedClient, setSelectedClient] =
    useState(DEMO_CLIENT);

  const [loading, setLoading] =
    useState(true);

  const [preparing, setPreparing] =
    useState(false);

  const [recording, setRecording] =
    useState(false);

  const [brief, setBrief] =
    useState(null);

  const [showMeetingModal, setShowMeetingModal] =
    useState(false);

  const [memoryEnabled, setMemoryEnabled] =
    useState(true);

  const [search, setSearch] =
    useState("");

  const [activeView, setActiveView] =
    useState("Dashboard");

  const [notice, setNotice] =
    useState(null);

  const [meetingForm, setMeetingForm] =
    useState({
      client: DEMO_CLIENT,
      contact: "Sarah Chen, CTO",
      date: new Date()
        .toISOString()
        .slice(0, 10),
      title: "",
      meeting_notes: "",
      decisions: "",
      concerns: "",
      commitments: "",
      follow_ups: "",
    });

  async function loadDashboard() {
    setLoading(true);

    const [
      meetingResult,
      clientResult,
      healthResult,
    ] = await Promise.allSettled([
      getMeetings(),
      getClients(),
      getHealth(),
    ]);

    if (meetingResult.status === "fulfilled") {
      const value =
        meetingResult.value;

      setMeetings(
        Array.isArray(value)
          ? value
          : Array.isArray(
              value?.meetings
            )
          ? value.meetings
          : []
      );
    }

    if (clientResult.status === "fulfilled") {
      const value =
        clientResult.value;

      const rawClients =
        Array.isArray(value)
          ? value
          : Array.isArray(
              value?.clients
            )
          ? value.clients
          : [];

      setClients(rawClients);
    }

    if (healthResult.status === "fulfilled") {
      setHealth(
        healthResult.value
      );
    }

    setLoading(false);
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  const availableClients =
    useMemo(() => {
      const names = [];

      for (const client of clients) {
        const name =
          typeof client === "string"
            ? client
            : client?.client ||
              client?.name;

        if (name) {
          names.push(name);
        }
      }

      for (const meeting of meetings) {
        if (meeting?.client) {
          names.push(meeting.client);
        }
      }

      names.push(DEMO_CLIENT);

      return [
        ...new Set(names),
      ];
    }, [clients, meetings]);

  useEffect(() => {
    if (
      availableClients.length > 0 &&
      !availableClients.includes(
        selectedClient
      )
    ) {
      setSelectedClient(
        availableClients[0]
      );
    }
  }, [
    availableClients,
    selectedClient,
  ]);

  const sourceMeetings =
    meetings.length > 0
      ? meetings
      : DEMO_MEETINGS;

  const visibleMeetings =
    sourceMeetings.filter(
      (meeting) =>
        `${meeting.client || ""} ${
          meeting.title || ""
        } ${
          meeting.meeting_notes ||
          meeting.summary ||
          ""
        }`
          .toLowerCase()
          .includes(
            search.toLowerCase()
          )
    );

  const clientMeetings =
    sourceMeetings
      .filter(
        (meeting) =>
          meeting.client ===
          selectedClient
      )
      .sort(
        (a, b) =>
          new Date(b.date || 0) -
          new Date(a.date || 0)
      );

  const meetingCount =
    clientMeetings.length;

  const openActions =
    Math.max(
      0,
      clientMeetings.reduce(
        (total, meeting) =>
          total +
          (meeting.follow_ups
            ?.length || 0),
        0
      )
    );

  const concernCount =
    Math.max(
      0,
      clientMeetings.reduce(
        (total, meeting) =>
          total +
          (meeting.concerns
            ?.length || 0),
        0
      )
    );

  const commitmentCount =
    Math.max(
      0,
      clientMeetings.reduce(
        (total, meeting) =>
          total +
          (meeting.commitments
            ?.length || 0),
        0
      )
    );

  const hindsightConnected =
    health?.hindsight
      ?.connected === true &&
    health?.hindsight_reachable !==
      false;

  const memoryProvider =
    health?.hindsight
      ?.provider ||
    health?.memory_provider ||
    "local_fallback";

  const memoryLabel =
    memoryProvider ===
      "hindsight" &&
    hindsightConnected
      ? "HINDSIGHT ACTIVE"
      : memoryProvider ===
        "local_fallback"
      ? "DEVELOPMENT MEMORY"
      : "MEMORY STATUS";

  function showNotice(
    message,
    type = "success"
  ) {
    setNotice({
      message,
      type,
    });

    window.setTimeout(() => {
      setNotice(null);
    }, 4000);
  }

  async function handlePrepare() {
    setPreparing(true);
    setBrief(null);

    try {
      const result =
        await prepareMeeting({
          client: selectedClient,

          upcoming_context:
            `Upcoming meeting with ${selectedClient}. ` +
            "Focus on unresolved commitments, security concerns, " +
            "previous decisions, delivery timeline, risks, " +
            "and questions to ask.",

          user_question:
            `Prepare me for my next meeting with ${selectedClient}. ` +
            "What should I remember, what did we promise, " +
            "what remains unresolved, and what should I ask?",

          memory_enabled:
            memoryEnabled,
        });

      setBrief(
        normalizeBrief(result)
      );

      showNotice(
        memoryEnabled
          ? "Meeting intelligence generated from client memory."
          : "Meeting intelligence generated without memory."
      );
    } catch (error) {
      console.error(error);

      showNotice(
        `Preparation failed: ${error.message}`,
        "error"
      );
    } finally {
      setPreparing(false);
    }
  }

  function updateMeetingForm(
    field,
    value
  ) {
    setMeetingForm(
      (current) => ({
        ...current,
        [field]: value,
      })
    );
  }

  function csvToArray(value) {
    return String(value || "")
      .split("\n")
      .map((item) =>
        item.trim()
      )
      .filter(Boolean);
  }

  async function handleRecordMeeting(
    event
  ) {
    event.preventDefault();

    if (
      !meetingForm.client.trim()
    ) {
      showNotice(
        "Client name is required.",
        "error"
      );
      return;
    }

    if (
      !meetingForm.title.trim()
    ) {
      showNotice(
        "Meeting title is required.",
        "error"
      );
      return;
    }

    if (
      !meetingForm.meeting_notes.trim()
    ) {
      showNotice(
        "Meeting notes are required.",
        "error"
      );
      return;
    }

    setRecording(true);

    try {
      const payload = {
        client:
          meetingForm.client.trim(),

        contact:
          meetingForm.contact.trim(),

        date: meetingForm.date,

        title:
          meetingForm.title.trim(),

        meeting_notes:
          meetingForm.meeting_notes.trim(),

        decisions:
          csvToArray(
            meetingForm.decisions
          ),

        concerns:
          csvToArray(
            meetingForm.concerns
          ),

        commitments:
          csvToArray(
            meetingForm.commitments
          ),

        follow_ups:
          csvToArray(
            meetingForm.follow_ups
          ),
      };

      await createMeeting(
        payload
      );

      setSelectedClient(
        payload.client
      );

      setMeetingForm({
        client: payload.client,
        contact: payload.contact,
        date: new Date()
          .toISOString()
          .slice(0, 10),
        title: "",
        meeting_notes: "",
        decisions: "",
        concerns: "",
        commitments: "",
        follow_ups: "",
      });

      setShowMeetingModal(
        false
      );

      await loadDashboard();

      showNotice(
        "Meeting recorded and added to client memory."
      );
    } catch (error) {
      console.error(error);

      showNotice(
        `Could not record meeting: ${error.message}`,
        "error"
      );
    } finally {
      setRecording(false);
    }
  }

  function openRecordModal() {
    setMeetingForm(
      (current) => ({
        ...current,
        client: selectedClient,
      })
    );

    setShowMeetingModal(true);
  }

  function renderBrief() {
    if (!brief) return null;

    return (
      <div className="mt-8 space-y-5">
        {/* AI Executive Brief */}
        <section className="rounded-2xl border border-indigo-400/20 bg-indigo-500/[0.06] p-6 shadow-xl shadow-indigo-950/20">
          <div className="flex items-start gap-4">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-indigo-500/15 text-indigo-300 ring-1 ring-indigo-400/20">
              <Sparkles size={21} />
            </div>

            <div className="min-w-0">
              <div className="text-[10px] font-semibold uppercase tracking-[0.2em] text-indigo-300">
                AI EXECUTIVE BRIEF
              </div>

              <h2 className="mt-1 text-xl font-semibold text-white">
                {brief.client}
              </h2>

              <p className="mt-3 max-w-4xl text-sm leading-7 text-slate-300">
                {brief.executive_summary}
              </p>
            </div>
          </div>

          <div className="mt-5 grid gap-3 md:grid-cols-3">
            <div className="mini-panel">
              <Clock3 size={15} />

              <span>
                {brief.memory_sources
                  ?.length || 0}{" "}
                memory source
                {brief.memory_sources
                  ?.length === 1
                  ? ""
                  : "s"}
              </span>
            </div>

            <div className="mini-panel">
              <Database size={15} />

              <span>
                {memoryLabel}
              </span>
            </div>

            <div className="mini-panel">
              <Target size={15} />

              <span>
                {brief
                  .open_action_items
                  ?.length || 0}{" "}
                open actions
              </span>
            </div>
          </div>
        </section>

        {/* =================================================
            NEW HINDSIGHT MEMORY PIPELINE
            ================================================= */}

        <MemoryPipeline
          brief={brief}
          memoryEnabled={
            memoryEnabled
          }
        />

        {/* Intelligence Sections */}
        <div className="grid gap-5 xl:grid-cols-2">
          <SectionCard
            title="What matters to the client"
            eyebrow="Client Priorities"
            icon={Target}
            items={
              brief.client_priorities
            }
            tone="cyan"
          />

          <SectionCard
            title="What our team promised"
            eyebrow="Previous Commitments"
            icon={CheckCircle2}
            items={
              brief.previous_commitments
            }
            tone="green"
          />

          <SectionCard
            title="Actions that still need attention"
            eyebrow="Open Action Items"
            icon={Clock3}
            items={
              brief.open_action_items
            }
            tone="amber"
          />

          <SectionCard
            title="Issues that could block progress"
            eyebrow="Unresolved Concerns"
            icon={CircleAlert}
            items={
              brief.unresolved_concerns
            }
            tone="red"
          />

          <SectionCard
            title="What could create delivery risk"
            eyebrow="Risk Signals"
            icon={ShieldAlert}
            items={brief.risks}
            tone="red"
          />

          <SectionCard
            title="Points to bring into the conversation"
            eyebrow="Talking Points"
            icon={
              MessageSquareText
            }
            items={
              brief.talking_points
            }
            tone="default"
          />

          <SectionCard
            title="Questions worth asking"
            eyebrow="Questions to Ask"
            icon={Search}
            items={
              brief.questions_to_ask
            }
            tone="cyan"
          />

          <SectionCard
            title="Recommended follow-through"
            eyebrow="Recommended Next Steps"
            icon={ArrowRight}
            items={
              brief.recommended_next_steps
            }
            tone="green"
          />
        </div>

        {brief.suggested_agenda
          ?.length > 0 && (
          <SectionCard
            title="Suggested Meeting Agenda"
            eyebrow="Conversation Plan"
            icon={
              CalendarDays
            }
            items={
              brief.suggested_agenda
            }
            tone="default"
          />
        )}

        {brief.reflection_summary && (
          <section className="glass-card p-5">
            <div className="flex items-center gap-2">
              <Brain
                size={16}
                className="text-purple-300"
              />

              <span className="text-[10px] font-semibold uppercase tracking-[0.18em] text-purple-300">
                MEMORY REFLECTION
              </span>
            </div>

            <p className="mt-3 text-sm leading-7 text-slate-300">
              {cleanText(
                brief.reflection_summary
              )}
            </p>
          </section>
        )}

        {/* Memory Sources */}
        {brief.memory_sources
          ?.length > 0 && (
          <section className="glass-card p-5">
            <div className="flex items-center gap-2">
              <Database
                size={16}
                className="text-indigo-300"
              />

              <span className="text-[10px] font-semibold uppercase tracking-[0.18em] text-indigo-300">
                MEMORY SOURCES
              </span>
            </div>

            <div className="mt-4 space-y-3">
              {brief.memory_sources.map(
                (
                  source,
                  index
                ) => (
                  <div
                    key={
                      source.id ||
                      index
                    }
                    className="rounded-xl border border-white/[0.06] bg-black/10 p-4"
                  >
                    <div className="flex items-center justify-between gap-3">
                      <span className="text-xs font-medium text-indigo-300">
                        Memory #
                        {index + 1}
                      </span>

                      <span className="text-[10px] text-slate-600">
                        {source.timestamp ||
                          source
                            .metadata
                            ?.date ||
                          "Historical interaction"}
                      </span>
                    </div>

                    <p className="mt-2 line-clamp-5 text-xs leading-6 text-slate-400">
                      {source.content}
                    </p>
                  </div>
                )
              )}
            </div>
          </section>
        )}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100">
      {/* Toast */}
      {notice && (
        <div
          className={`fixed right-5 top-5 z-[100] flex max-w-md items-start gap-3 rounded-xl border px-4 py-3 shadow-2xl ${
            notice.type === "error"
              ? "border-rose-400/20 bg-rose-950/90 text-rose-200"
              : "border-emerald-400/20 bg-emerald-950/90 text-emerald-200"
          }`}
        >
          {notice.type === "error" ? (
            <CircleAlert size={17} />
          ) : (
            <Check size={17} />
          )}

          <span className="text-sm">
            {notice.message}
          </span>
        </div>
      )}

      <div className="flex min-h-screen">
        {/* Sidebar */}
        <aside className="fixed inset-y-0 left-0 z-30 hidden w-64 border-r border-white/[0.06] bg-[#080d18] lg:block">
          <div className="flex h-full flex-col p-4">
            <div className="flex items-center gap-3 px-3 py-2">
              <div className="brand-mark">
                <Brain size={20} />
              </div>

              <div>
                <div className="text-sm font-semibold text-white">
                  RecallMeet
                </div>

                <div className="text-[9px] tracking-[0.22em] text-slate-500">
                  AI MEETING
                  <br />
                  INTELLIGENCE
                </div>
              </div>
            </div>

            <nav className="mt-8 space-y-1">
              {[
                {
                  label: "Dashboard",
                  icon: LayoutDashboard,
                },
                {
                  label: "Clients",
                  icon: Users,
                },
                {
                  label: "Meetings",
                  icon: CalendarDays,
                },
                {
                  label: "Memory Explorer",
                  icon: Database,
                },
                {
                  label: "Insights",
                  icon: Activity,
                },
              ].map(
                ({
                  label,
                  icon: Icon,
                }) => (
                  <button
                    key={label}
                    onClick={() =>
                      setActiveView(
                        label
                      )
                    }
                    className={`sidebar-item ${
                      activeView ===
                      label
                        ? "sidebar-item-active"
                        : ""
                    }`}
                  >
                    <Icon size={17} />

                    <span>
                      {label}
                    </span>
                  </button>
                )
              )}
            </nav>

            <div className="mt-auto rounded-2xl border border-white/[0.07] bg-white/[0.025] p-4">
              <div className="flex items-center gap-2">
                <StatusDot
                  active={
                    memoryProvider ===
                      "hindsight" &&
                    hindsightConnected
                  }
                />

                <span className="text-xs font-semibold text-slate-300">
                  Memory Engine
                </span>
              </div>

              <p className="mt-2 text-[11px] leading-5 text-slate-500">
                {memoryProvider ===
                "local_fallback"
                  ? "Development memory is active while Hindsight Cloud retention is unavailable."
                  : "Persistent client memory is connected."}
              </p>
            </div>
          </div>
        </aside>

        {/* Main */}
        <main className="min-w-0 flex-1 lg:ml-64">
          {/* Header */}
          <header className="sticky top-0 z-20 flex h-[70px] items-center justify-between border-b border-white/[0.06] bg-[#080d18]/90 px-5 backdrop-blur-xl lg:px-8">
            <div>
              <div className="text-sm font-medium text-slate-400">
                Meeting Intelligence Workspace
              </div>

              <div className="mt-1 text-xs text-slate-600">
                {activeView}
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="hidden items-center gap-2 rounded-full border border-white/[0.06] bg-white/[0.025] px-3 py-1.5 text-xs text-slate-500 sm:flex">
                <StatusDot
                  active={
                    memoryProvider ===
                      "hindsight" &&
                    hindsightConnected
                  }
                />

                {memoryLabel}
              </div>

              <button
                onClick={
                  openRecordModal
                }
                className="primary-button"
              >
                <Plus size={16} />

                Record Meeting
              </button>
            </div>
          </header>

          <div className="p-5 lg:p-8">
            {/* Hero */}
            <div className="flex flex-col justify-between gap-5 xl:flex-row xl:items-end">
              <div>
                <div className="eyebrow">
                  <Sparkles size={12} />
                  Client intelligence
                </div>

                <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white">
                  Prepare with context.
                  <br />

                  <span className="text-slate-500">
                    Never walk into a
                    meeting blind.
                  </span>
                </h1>

                <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
                  RecallMeet continuously
                  turns client interactions
                  into structured memory,
                  then uses that memory to
                  prepare you for what comes
                  next.
                </p>
              </div>

              <div className="flex items-center gap-2">
                <select
                  value={
                    selectedClient
                  }
                  onChange={(event) =>
                    setSelectedClient(
                      event.target.value
                    )
                  }
                  className="input !h-10 !w-auto min-w-[190px]"
                >
                  {availableClients.map(
                    (client) => (
                      <option
                        key={client}
                        value={client}
                      >
                        {client}
                      </option>
                    )
                  )}
                </select>

                <button
                  onClick={
                    loadDashboard
                  }
                  disabled={loading}
                  className="secondary-button !px-3"
                  title="Refresh"
                >
                  <RefreshCw
                    size={15}
                    className={
                      loading
                        ? "animate-spin"
                        : ""
                    }
                  />
                </button>
              </div>
            </div>

            {/* Stats */}
            <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <StatCard
                icon={CalendarDays}
                label="Client Meetings"
                value={
                  meetingCount
                }
                detail={`Interactions stored for ${selectedClient}`}
              />

              <StatCard
                icon={Clock3}
                label="Open Actions"
                value={
                  openActions
                }
                detail="Follow-ups across the relationship"
              />

              <StatCard
                icon={ShieldCheck}
                label="Commitments"
                value={
                  commitmentCount
                }
                detail="Promises captured from meetings"
              />

              <StatCard
                icon={CircleAlert}
                label="Open Concerns"
                value={
                  concernCount
                }
                detail="Issues requiring attention"
              />
            </div>

            {/* AI Preparation */}
            <section className="mt-8 overflow-hidden rounded-2xl border border-indigo-400/15 bg-gradient-to-br from-indigo-500/[0.10] via-white/[0.025] to-transparent p-6">
              <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-center">
                <div>
                  <div className="flex items-center gap-2">
                    <div className="icon-box">
                      <Sparkles size={18} />
                    </div>

                    <span className="text-xs font-semibold uppercase tracking-[0.16em] text-indigo-300">
                      AI MEETING PREP
                    </span>
                  </div>

                  <h2 className="mt-4 text-xl font-semibold text-white">
                    Prepare for your next meeting
                  </h2>

                  <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
                    RecallMeet will retrieve
                    relevant client history,
                    identify unresolved
                    commitments and concerns,
                    and turn them into a
                    practical meeting brief.
                  </p>
                </div>

                <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                  <button
                    onClick={() =>
                      setMemoryEnabled(
                        !memoryEnabled
                      )
                    }
                    className={`memory-pill ${
                      memoryEnabled
                        ? "border-indigo-400/20 text-indigo-200"
                        : ""
                    }`}
                  >
                    <Database size={14} />

                    Memory{" "}
                    {memoryEnabled
                      ? "ON"
                      : "OFF"}

                    <span
                      className={`h-2 w-2 rounded-full ${
                        memoryEnabled
                          ? "bg-indigo-400"
                          : "bg-slate-600"
                      }`}
                    />
                  </button>

                  <button
                    onClick={
                      handlePrepare
                    }
                    disabled={
                      preparing
                    }
                    className="primary-button justify-center"
                  >
                    {preparing ? (
                      <>
                        <RefreshCw
                          size={16}
                          className="animate-spin"
                        />

                        Preparing...
                      </>
                    ) : (
                      <>
                        <Sparkles size={16} />

                        Prepare Meeting

                        <ArrowRight
                          size={15}
                        />
                      </>
                    )}
                  </button>
                </div>
              </div>
            </section>

            {/* Preparation result */}
            {brief &&
              renderBrief()}

            {/* Dashboard content */}
            {!brief && (
              <>
                {/* Timeline + Client Memory */}
                <div className="mt-8 grid gap-5 xl:grid-cols-[1.5fr_1fr]">
                  {/* Timeline */}
                  <section className="glass-card p-5">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-[10px] font-semibold uppercase tracking-[0.18em] text-indigo-300">
                          MEMORY EVOLUTION
                        </div>

                        <h2 className="mt-1 text-sm font-semibold text-white">
                          Relationship timeline
                        </h2>
                      </div>

                      <Database
                        size={16}
                        className="text-slate-600"
                      />
                    </div>

                    <div className="mt-5 space-y-5">
                      {clientMeetings
                        .slice(0, 6)
                        .map(
                          (
                            meeting,
                            index
                          ) => (
                            <div
                              key={
                                meeting.id ||
                                `${meeting.date}-${index}`
                              }
                              className="timeline-item"
                            >
                              <div className="timeline-line">
                                <span className="timeline-dot" />

                                {index <
                                  Math.min(
                                    clientMeetings.length,
                                    6
                                  ) -
                                    1 && (
                                  <span className="timeline-connector" />
                                )}
                              </div>

                              <div className="min-w-0 flex-1">
                                <div className="flex flex-wrap items-center justify-between gap-2">
                                  <h3 className="text-sm font-medium text-slate-200">
                                    {meeting.title ||
                                      "Client Meeting"}
                                  </h3>

                                  <span className="text-[10px] text-slate-600">
                                    {formatDate(
                                      meeting.date
                                    )}
                                  </span>
                                </div>

                                <p className="mt-1 text-xs leading-5 text-slate-500">
                                  {cleanText(
                                    meeting.meeting_notes ||
                                      meeting.summary ||
                                      "Meeting interaction recorded."
                                  )}
                                </p>

                                <div className="mt-2 flex flex-wrap gap-2">
                                  {(
                                    meeting.decisions ||
                                    []
                                  )
                                    .slice(
                                      0,
                                      3
                                    )
                                    .map(
                                      (
                                        decision,
                                        decisionIndex
                                      ) => (
                                        <span
                                          key={
                                            decisionIndex
                                          }
                                          className="memory-tag"
                                        >
                                          {
                                            decision
                                          }
                                        </span>
                                      )
                                    )}
                                </div>
                              </div>
                            </div>
                          )
                        )}

                      {clientMeetings.length ===
                        0 && (
                        <div className="rounded-xl border border-dashed border-white/[0.08] p-8 text-center">
                          <CalendarDays
                            size={24}
                            className="mx-auto text-slate-700"
                          />

                          <p className="mt-3 text-sm text-slate-500">
                            No meetings
                            recorded for
                            this client yet.
                          </p>
                        </div>
                      )}
                    </div>
                  </section>

                  {/* Client Memory */}
                  <section className="glass-card p-5">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-[10px] font-semibold uppercase tracking-[0.18em] text-indigo-300">
                          CLIENT MEMORY
                        </div>

                        <h2 className="mt-1 text-sm font-semibold text-white">
                          {
                            selectedClient
                          }
                        </h2>
                      </div>

                      <div className="avatar">
                        {selectedClient
                          .slice(0, 2)
                          .toUpperCase()}
                      </div>
                    </div>

                    <div className="mt-5 space-y-3">
                      <div className="mini-panel">
                        <Users size={15} />

                        <span>
                          {
                            meetingCount
                          }{" "}
                          historical
                          interaction
                          {meetingCount ===
                          1
                            ? ""
                            : "s"}
                        </span>
                      </div>

                      <div className="mini-panel">
                        <CheckCircle2 size={15} />

                        <span>
                          {
                            commitmentCount
                          }{" "}
                          captured
                          commitment
                          {commitmentCount ===
                          1
                            ? ""
                            : "s"}
                        </span>
                      </div>

                      <div className="mini-panel">
                        <CircleAlert size={15} />

                        <span>
                          {
                            concernCount
                          }{" "}
                          open concern
                          {concernCount ===
                          1
                            ? ""
                            : "s"}
                        </span>
                      </div>

                      <div className="rounded-xl border border-indigo-400/10 bg-indigo-500/[0.06] p-4">
                        <div className="flex items-center gap-2 text-xs font-medium text-indigo-300">
                          <Brain size={14} />

                          Memory engine
                        </div>

                        <p className="mt-2 text-xs leading-5 text-slate-500">
                          {memoryProvider ===
                          "local_fallback"
                            ? "Development memory is preserving meeting context locally until Hindsight Cloud retention is available."
                            : "Hindsight is maintaining persistent client memory."}
                        </p>
                      </div>
                    </div>

                    <button
                      onClick={
                        openRecordModal
                      }
                      className="secondary-button mt-5 w-full justify-center"
                    >
                      <Plus size={15} />

                      Record another
                      interaction
                    </button>
                  </section>
                </div>

                {/* Recent Meetings */}
                <section className="mt-5 glass-card overflow-hidden">
                  <div className="flex flex-col justify-between gap-3 border-b border-white/[0.06] p-5 sm:flex-row sm:items-center">
                    <div>
                      <div className="text-[10px] font-semibold uppercase tracking-[0.18em] text-indigo-300">
                        RECENT INTERACTIONS
                      </div>

                      <h2 className="mt-1 text-sm font-semibold text-white">
                        Meeting history
                      </h2>
                    </div>

                    <div className="relative">
                      <Search
                        size={14}
                        className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600"
                      />

                      <input
                        value={search}
                        onChange={(
                          event
                        ) =>
                          setSearch(
                            event.target
                              .value
                          )
                        }
                        placeholder="Search meetings..."
                        className="search-input pl-8"
                      />
                    </div>
                  </div>

                  <div className="divide-y divide-white/[0.05]">
                    {visibleMeetings
                      .slice(0, 8)
                      .map(
                        (
                          meeting,
                          index
                        ) => (
                          <div
                            key={
                              meeting.id ||
                              `${meeting.date}-${index}`
                            }
                            className="flex flex-col gap-4 p-5 transition hover:bg-white/[0.02] sm:flex-row sm:items-center"
                          >
                            <div className="meeting-icon">
                              <FileText
                                size={17}
                              />
                            </div>

                            <div className="min-w-0 flex-1">
                              <div className="flex flex-wrap items-center gap-2">
                                <h3 className="text-sm font-medium text-slate-200">
                                  {meeting.title ||
                                    "Client Meeting"}
                                </h3>

                                <span className="rounded-full border border-white/[0.06] px-2 py-0.5 text-[9px] uppercase tracking-wider text-slate-600">
                                  {
                                    meeting.client
                                  }
                                </span>
                              </div>

                              <p className="mt-1 line-clamp-2 text-xs leading-5 text-slate-500">
                                {cleanText(
                                  meeting.meeting_notes ||
                                    meeting.summary
                                )}
                              </p>
                            </div>

                            <div className="shrink-0 text-right">
                              <div className="text-xs text-slate-400">
                                {formatDate(
                                  meeting.date
                                )}
                              </div>

                              <div className="mt-1 text-[10px] text-slate-600">
                                {meeting
                                  .commitments
                                  ?.length ||
                                  0}{" "}
                                commitments
                              </div>
                            </div>
                          </div>
                        )
                      )}

                    {visibleMeetings.length ===
                      0 && (
                      <div className="p-8 text-center text-sm text-slate-600">
                        No matching
                        meetings found.
                      </div>
                    )}
                  </div>
                </section>
              </>
            )}
          </div>
        </main>
      </div>

      {/* Record Meeting Modal */}
      {showMeetingModal && (
        <div className="fixed inset-0 z-[90] flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm">
          <div className="max-h-[92vh] w-full max-w-3xl overflow-y-auto rounded-2xl border border-white/[0.08] bg-[#0b1120] shadow-2xl">
            <div className="sticky top-0 z-10 flex items-center justify-between border-b border-white/[0.06] bg-[#0b1120]/95 p-5 backdrop-blur">
              <div>
                <div className="eyebrow">
                  <Database size={12} />

                  Add to memory
                </div>

                <h2 className="mt-1 text-lg font-semibold text-white">
                  Record Client Meeting
                </h2>

                <p className="mt-1 text-xs text-slate-500">
                  Capture the interaction so
                  RecallMeet can use it in
                  future preparation.
                </p>
              </div>

              <button
                onClick={() =>
                  setShowMeetingModal(
                    false
                  )
                }
                className="rounded-lg p-2 text-slate-500 transition hover:bg-white/[0.05] hover:text-white"
              >
                <X size={18} />
              </button>
            </div>

            <form
              onSubmit={
                handleRecordMeeting
              }
              className="space-y-5 p-5"
            >
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-xs font-medium text-slate-400">
                    Client *
                  </label>

                  <input
                    value={
                      meetingForm.client
                    }
                    onChange={(
                      event
                    ) =>
                      updateMeetingForm(
                        "client",
                        event.target
                          .value
                      )
                    }
                    className="input"
                    placeholder="Acme Corp"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-xs font-medium text-slate-400">
                    Contact
                  </label>

                  <input
                    value={
                      meetingForm.contact
                    }
                    onChange={(
                      event
                    ) =>
                      updateMeetingForm(
                        "contact",
                        event.target
                          .value
                      )
                    }
                    className="input"
                    placeholder="Sarah Chen, CTO"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-xs font-medium text-slate-400">
                    Meeting Date
                  </label>

                  <input
                    type="date"
                    value={
                      meetingForm.date
                    }
                    onChange={(
                      event
                    ) =>
                      updateMeetingForm(
                        "date",
                        event.target
                          .value
                      )
                    }
                    className="input"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-xs font-medium text-slate-400">
                    Meeting Title *
                  </label>

                  <input
                    value={
                      meetingForm.title
                    }
                    onChange={(
                      event
                    ) =>
                      updateMeetingForm(
                        "title",
                        event.target
                          .value
                      )
                    }
                    className="input"
                    placeholder="Security Architecture Review"
                  />
                </div>
              </div>

              <div>
                <label className="mb-2 block text-xs font-medium text-slate-400">
                  Meeting Notes *
                </label>

                <textarea
                  value={
                    meetingForm.meeting_notes
                  }
                  onChange={(
                    event
                  ) =>
                    updateMeetingForm(
                      "meeting_notes",
                      event.target
                        .value
                    )
                  }
                  className="input min-h-[120px] resize-y py-3"
                  placeholder="Describe what was discussed, important context, concerns, and decisions..."
                />
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <TextAreaField
                  label="Decisions"
                  value={
                    meetingForm.decisions
                  }
                  onChange={(
                    value
                  ) =>
                    updateMeetingForm(
                      "decisions",
                      value
                    )
                  }
                  placeholder={
                    "AWS selected\nRBAC required"
                  }
                />

                <TextAreaField
                  label="Concerns"
                  value={
                    meetingForm.concerns
                  }
                  onChange={(
                    value
                  ) =>
                    updateMeetingForm(
                      "concerns",
                      value
                    )
                  }
                  placeholder={
                    "Security review pending\nTimeline risk"
                  }
                />

                <TextAreaField
                  label="Commitments"
                  value={
                    meetingForm.commitments
                  }
                  onChange={(
                    value
                  ) =>
                    updateMeetingForm(
                      "commitments",
                      value
                    )
                  }
                  placeholder={
                    "Prepare architecture proposal\nShare security plan"
                  }
                />

                <TextAreaField
                  label="Follow-ups"
                  value={
                    meetingForm.follow_ups
                  }
                  onChange={(
                    value
                  ) =>
                    updateMeetingForm(
                      "follow_ups",
                      value
                    )
                  }
                  placeholder={
                    "Schedule technical discussion\nComplete security review"
                  }
                />
              </div>

              <div className="flex flex-col-reverse justify-end gap-3 border-t border-white/[0.06] pt-5 sm:flex-row">
                <button
                  type="button"
                  onClick={() =>
                    setShowMeetingModal(
                      false
                    )
                  }
                  className="secondary-button justify-center"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  disabled={recording}
                  className="primary-button justify-center"
                >
                  {recording ? (
                    <>
                      <RefreshCw
                        size={15}
                        className="animate-spin"
                      />

                      Saving...
                    </>
                  ) : (
                    <>
                      <Database
                        size={15}
                      />

                      Save to Client
                      Memory
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

/* =========================================================
   TEXT AREA FIELD
   ========================================================= */

function TextAreaField({
  label,
  value,
  onChange,
  placeholder,
}) {
  return (
    <div>
      <label className="mb-2 block text-xs font-medium text-slate-400">
        {label}
      </label>

      <textarea
        value={value}
        onChange={(event) =>
          onChange(
            event.target.value
          )
        }
        className="input min-h-[105px] resize-y py-3"
        placeholder={`${placeholder}\n(one item per line)`}
      />
    </div>
  );
}

export default App;