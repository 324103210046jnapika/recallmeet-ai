from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import os
import json
import time

from hindsight_client import Hindsight
from hindsight_client_api.exceptions import ApiException

from ..config import settings
from ..utils.logger import logger
from ..schemas.memory import MemoryItem, MemoryOperationInfo
from ..schemas.meeting import MeetingCreate


class HindsightService:
    """
    Service layer for RecallMeet AI's Hindsight memory system.

    Hindsight operations:
        RETAIN  -> store meeting intelligence
        RECALL  -> retrieve relevant memories
        REFLECT -> synthesize accumulated client intelligence

    The service also contains a local development fallback so the
    application remains usable when Hindsight Cloud is temporarily
    unavailable during development.
    """

    def __init__(self):
        self.base_url = settings.HINDSIGHT_BASE_URL
        self.api_key = (
            settings.HINDSIGHT_API_KEY
            if settings.HINDSIGHT_API_KEY
            else None
        )
        self.bank_id = settings.HINDSIGHT_BANK_ID

        self._client: Optional[Hindsight] = None
        self._connected: Optional[bool] = None
        self._last_check_time: float = 0.0
        self._cached_status: Optional[Dict[str, Any]] = None

        # Development-only fallback memory.
        self._local_fallback_memories: List[Dict[str, Any]] = []

        self.last_operation_status: Dict[str, Any] = {
            "operation": "initialization",
            "timestamp": datetime.now().isoformat(),
            "provider": "none",
            "status": "idle",
            "details": "Service initialized",
        }

        self._init_client()

    # ------------------------------------------------------------------
    # CLIENT INITIALIZATION
    # ------------------------------------------------------------------

    def _init_client(self):
        """Initialize the official Hindsight client."""
        try:
            self._client = Hindsight(
                base_url=self.base_url,
                api_key=self.api_key,
                timeout=float(settings.HINDSIGHT_TIMEOUT),
            )

            logger.info(
                f"Hindsight client initialized pointing to {self.base_url}"
            )

        except Exception as e:
            logger.warning(
                f"Failed to instantiate Hindsight client: {e}"
            )
            self._client = None

    def close(self):
        """Cleanly close Hindsight client sessions."""
        if self._client:
            try:
                self._client.close()
            except Exception as e:
                logger.debug(
                    f"Hindsight client close notice: {e}"
                )

    # ------------------------------------------------------------------
    # CONNECTION CHECK
    # ------------------------------------------------------------------

    async def check_connection(
        self,
        force: bool = False,
    ) -> Dict[str, Any]:
        """
        Check whether Hindsight Cloud is reachable.

        Uses the asynchronous Hindsight SDK because this service
        runs inside FastAPI's async event loop.
        """

        now = time.time()

        # Use cached result for 10 seconds unless forced.
        if (
            not force
            and self._cached_status
            and (now - self._last_check_time) < 10.0
        ):
            return self._cached_status

        configured = bool(self.base_url)

        if not self._client:
            self._cached_status = {
                "configured": configured,
                "connected": False,
                "base_url": self.base_url,
                "version": None,
                "bank_id": self.bank_id,
                "error": "Client not initialized",
            }

            self._last_check_time = now

            return self._cached_status

        try:
            # IMPORTANT:
            # Use async SDK method inside FastAPI.
            version_resp = await self._client.aget_version()

            version_str = getattr(
                version_resp,
                "version",
                str(version_resp),
            )

            self._connected = True

            self._cached_status = {
                "configured": configured,
                "connected": True,
                "base_url": self.base_url,
                "version": version_str,
                "bank_id": self.bank_id,
                "error": None,
            }

        except Exception as e:
            self._connected = False

            self._cached_status = {
                "configured": configured,
                "connected": False,
                "base_url": self.base_url,
                "version": None,
                "bank_id": self.bank_id,
                "error": str(e),
            }

        self._last_check_time = now

        return self._cached_status

    # ------------------------------------------------------------------
    # MEMORY BANK
    # ------------------------------------------------------------------

    async def ensure_bank(
        self,
        bank_id: Optional[str] = None,
    ) -> bool:
        """
        Ensure the target Hindsight memory bank exists.
        """

        target_bank = bank_id or self.bank_id

        if not self._client:
            return False

        try:
            await self._client.acreate_bank(
                bank_id=target_bank,
                name=f"RecallMeet Intelligence Bank ({target_bank})",
                mission=(
                    "Track client meeting intelligence, technical "
                    "constraints, security concerns, delivery timelines, "
                    "and commitments over time."
                ),
                retain_mission=(
                    "Extract client technical preferences, unresolved "
                    "objections, promised deliverables, and timeline "
                    "milestones from meeting discussions."
                ),
                reflect_mission=(
                    "Synthesize comprehensive client intelligence briefs, "
                    "identify pending commitments and unresolved risks."
                ),
                enable_observations=True,
                enable_text_search=True,
                enable_temporal_retrieval=True,
                enable_graph_retrieval=True,
                enable_reranking=True,
            )

            logger.info(
                f"Hindsight memory bank '{target_bank}' "
                "created/verified."
            )

            return True

        except Exception as e:
            # Creating an already-existing bank can return an error.
            # That does not necessarily mean the bank is unusable.
            logger.debug(
                f"Bank verification notice for "
                f"'{target_bank}': {e}"
            )

            return True

    # ------------------------------------------------------------------
    # MEETING FORMATTING
    # ------------------------------------------------------------------

    def format_meeting_memory(
        self,
        meeting: MeetingCreate,
    ) -> str:
        """
        Convert meeting information into structured text for
        Hindsight RETAIN.
        """

        lines = [
            f"Client: {meeting.client}",
            f"Contact: {meeting.contact}",
            f"Meeting Date: {meeting.date}",
            f"Meeting Title: {meeting.title}",
            "",
            "Meeting Notes & Discussion:",
            meeting.meeting_notes.strip(),
        ]

        if meeting.decisions:
            lines.append("\nKey Decisions:")

            for decision in meeting.decisions:
                lines.append(
                    f"- {decision}"
                )

        if meeting.concerns:
            lines.append(
                "\nConcerns & Unresolved Objections:"
            )

            for concern in meeting.concerns:
                lines.append(
                    f"- {concern}"
                )

        if meeting.commitments:
            lines.append(
                "\nCommitments & Promises Made to Client:"
            )

            for commitment in meeting.commitments:
                lines.append(
                    f"- {commitment}"
                )

        if meeting.follow_ups:
            lines.append(
                "\nAction Items & Next Steps:"
            )

            for follow_up in meeting.follow_ups:
                lines.append(
                    f"- {follow_up}"
                )

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # RETAIN
    # ------------------------------------------------------------------

    async def retain_meeting(
        self,
        meeting: MeetingCreate,
        meeting_id: str,
        bank_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Store a meeting in Hindsight using RETAIN.

        Flow:

            FastAPI
                ↓
            retain_meeting()
                ↓
            check_connection()
                ↓
            ensure_bank()
                ↓
            Hindsight.aretain()
        """

        target_bank = bank_id or self.bank_id

        formatted_content = self.format_meeting_memory(
            meeting
        )

        # Try to convert meeting date into datetime.
        parsed_dt = None

        for fmt in (
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d",
        ):
            try:
                parsed_dt = datetime.strptime(
                    meeting.date[:10],
                    fmt,
                )
                break

            except Exception:
                pass

        tag_client = (
            meeting.client
            .lower()
            .replace(" ", "_")
        )

        tags = [
            tag_client,
            "meeting",
            "recallmeet",
        ]

        context_str = (
            f"Client meeting for {meeting.client} "
            f"with {meeting.contact} "
            f"on {meeting.date}: "
            f"{meeting.title}"
        )

        metadata = {
            "client": meeting.client,
            "contact": meeting.contact,
            "date": meeting.date,
            "title": meeting.title,
            "meeting_id": meeting_id,
            "has_concerns": str(
                bool(meeting.concerns)
            ).lower(),
            "has_commitments": str(
                bool(meeting.commitments)
            ).lower(),
        }

        # --------------------------------------------------------------
        # CHECK HINDSIGHT CONNECTION
        # --------------------------------------------------------------

        status_info = await self.check_connection()

        # --------------------------------------------------------------
        # REAL HINDSIGHT
        # --------------------------------------------------------------

        if (
            status_info["connected"]
            and self._client
        ):
            try:
                await self.ensure_bank(
                    target_bank
                )

                logger.info(
                    f"Retaining meeting {meeting_id} "
                    f"using real Hindsight SDK in "
                    f"bank '{target_bank}'..."
                )

                # IMPORTANT:
                # Use async RETAIN operation.
                retain_resp = await self._client.aretain(
                    bank_id=target_bank,
                    content=formatted_content,
                    timestamp=parsed_dt,
                    context=context_str,
                    document_id=f"meet_{meeting_id}",
                    metadata=metadata,
                    tags=tags,
                )

                operation_id = (
                    getattr(
                        retain_resp,
                        "operation_id",
                        None,
                    )
                    or f"op_{meeting_id}"
                )

                self.last_operation_status = {
                    "operation": "retain",
                    "timestamp": datetime.now().isoformat(),
                    "provider": "hindsight",
                    "status": "success",
                    "details": (
                        f"Retained meeting {meeting_id} "
                        f"in Hindsight bank "
                        f"'{target_bank}'"
                    ),
                }

                return {
                    "retained": True,
                    "memory_provider": "hindsight",
                    "hindsight_connected": True,
                    "operation_id": operation_id,
                    "bank_id": target_bank,
                    "content": formatted_content,
                    "metadata": metadata,
                    "memory_info": MemoryOperationInfo(
                        provider="hindsight",
                        operations=["retain"],
                        bank_id=target_bank,
                        memory_count=1,
                        connected=True,
                        message=(
                            f"Retained in Hindsight bank "
                            f"'{target_bank}' "
                            f"(Op: {operation_id})"
                        ),
                    ),
                }

            except Exception as e:
                logger.error(
                    f"Hindsight retain call error: {e}. "
                    "Falling back to resilient dev memory."
                )

        # --------------------------------------------------------------
        # PRODUCTION SAFETY
        # --------------------------------------------------------------

        if settings.ENVIRONMENT == "production":
            raise RuntimeError(
                "Hindsight memory engine unreachable "
                f"at {self.base_url}: "
                f"{status_info.get('error')}"
            )

        # --------------------------------------------------------------
        # LOCAL DEVELOPMENT FALLBACK
        # --------------------------------------------------------------

        fallback_record = {
            "id": f"mem_fb_{meeting_id}",
            "bank_id": target_bank,
            "client": meeting.client,
            "content": formatted_content,
            "metadata": metadata,
            "tags": tags,
            "date": meeting.date,
            "created_at": datetime.now().isoformat(),
        }

        self._local_fallback_memories.append(
            fallback_record
        )

        self.last_operation_status = {
            "operation": "retain",
            "timestamp": datetime.now().isoformat(),
            "provider": "local_fallback",
            "status": "notice",
            "details": (
                f"Retained meeting {meeting_id} "
                "in local development fallback"
            ),
        }

        return {
            "retained": True,
            "memory_provider": "local_fallback",
            "hindsight_connected": False,
            "operation_id": (
                f"fallback_{meeting_id}"
            ),
            "bank_id": target_bank,
            "content": formatted_content,
            "metadata": metadata,
            "memory_info": MemoryOperationInfo(
                provider="local_fallback",
                operations=["retain"],
                bank_id=target_bank,
                memory_count=1,
                connected=False,
                message=(
                    "Retained in development "
                    "fallback layer "
                    "(Hindsight server offline)"
                ),
            ),
        }

    # ------------------------------------------------------------------
    # RECALL
    # ------------------------------------------------------------------

    async def recall_memories(
        self,
        client: str,
        query: str,
        bank_id: Optional[str] = None,
        max_tokens: int = 4096,
    ) -> Tuple[
        List[MemoryItem],
        str,
        MemoryOperationInfo,
    ]:
        """
        Retrieve relevant memories using Hindsight RECALL.
        """

        target_bank = bank_id or self.bank_id

        tag_client = (
            client
            .lower()
            .replace(" ", "_")
        )

        status_info = await self.check_connection()

        # --------------------------------------------------------------
        # REAL HINDSIGHT RECALL
        # --------------------------------------------------------------

        if (
            status_info["connected"]
            and self._client
        ):
            try:
                logger.info(
                    f"Recalling memories using real "
                    f"Hindsight SDK in bank "
                    f"'{target_bank}' for '{client}'"
                )

                # IMPORTANT:
                # Async RECALL operation.
                recall_resp = await self._client.arecall(
                    bank_id=target_bank,
                    query=(
                        f"Client: {client}. {query}"
                    ),
                    tags=[tag_client],
                    tags_match="any",
                    max_tokens=max_tokens,
                )

                memories: List[MemoryItem] = []

                for item in getattr(
                    recall_resp,
                    "results",
                    [],
                ):
                    score_val = None

                    if (
                        hasattr(item, "scores")
                        and item.scores
                    ):
                        if isinstance(
                            item.scores,
                            dict,
                        ):
                            score_val = next(
                                iter(
                                    item.scores.values()
                                ),
                                None,
                            )

                        elif isinstance(
                            item.scores,
                            (list, tuple),
                        ):
                            if item.scores:
                                score_val = (
                                    item.scores[0]
                                )

                    elif hasattr(
                        item,
                        "score",
                    ):
                        score_val = item.score

                    metadata = (
                        getattr(
                            item,
                            "metadata",
                            {},
                        )
                        or {}
                    )

                    memories.append(
                        MemoryItem(
                            id=getattr(
                                item,
                                "id",
                                None,
                            ),
                            content=getattr(
                                item,
                                "text",
                                str(item),
                            ),
                            score=(
                                float(score_val)
                                if score_val
                                is not None
                                else None
                            ),
                            metadata=(
                                metadata
                                if isinstance(
                                    metadata,
                                    dict,
                                )
                                else {}
                            ),
                            network=getattr(
                                item,
                                "type",
                                None,
                            ),
                            timestamp=str(
                                getattr(
                                    item,
                                    "occurred_start",
                                    None,
                                )
                                or getattr(
                                    item,
                                    "mentioned_at",
                                    None,
                                )
                                or ""
                            ),
                            provider="hindsight",
                        )
                    )

                logger.info(
                    f"Hindsight recalled "
                    f"{len(memories)} memory items."
                )

                self.last_operation_status = {
                    "operation": "recall",
                    "timestamp": (
                        datetime.now().isoformat()
                    ),
                    "provider": "hindsight",
                    "status": "success",
                    "details": (
                        f"Recalled {len(memories)} "
                        f"items from Hindsight "
                        f"bank '{target_bank}'"
                    ),
                }

                operation_info = (
                    MemoryOperationInfo(
                        provider="hindsight",
                        operations=["recall"],
                        bank_id=target_bank,
                        memory_count=len(memories),
                        connected=True,
                        message=(
                            f"Recalled {len(memories)} "
                            "items directly from "
                            "Hindsight memory engine"
                        ),
                    )
                )

                return (
                    memories,
                    "hindsight",
                    operation_info,
                )

            except Exception as e:
                logger.error(
                    f"Hindsight recall error: {e}. "
                    "Falling back to resilient "
                    "dev memory."
                )

        # --------------------------------------------------------------
        # PRODUCTION SAFETY
        # --------------------------------------------------------------

        if settings.ENVIRONMENT == "production":
            raise RuntimeError(
                "Hindsight memory engine "
                "unreachable for recall: "
                f"{status_info.get('error')}"
            )

        # --------------------------------------------------------------
        # LOCAL FALLBACK RECALL
        # --------------------------------------------------------------

        fallback_memories = (
            self._fallback_recall(
                client,
                query,
            )
        )

        self.last_operation_status = {
            "operation": "recall",
            "timestamp": datetime.now().isoformat(),
            "provider": "local_fallback",
            "status": "notice",
            "details": (
                f"Recalled "
                f"{len(fallback_memories)} "
                "items from local "
                "development fallback"
            ),
        }

        operation_info = (
            MemoryOperationInfo(
                provider="local_fallback",
                operations=["recall"],
                bank_id=target_bank,
                memory_count=(
                    len(fallback_memories)
                ),
                connected=False,
                message=(
                    "Retrieved from development "
                    "fallback memory "
                    "(Hindsight server offline)"
                ),
            )
        )

        return (
            fallback_memories,
            "local_fallback",
            operation_info,
        )

    # ------------------------------------------------------------------
    # FALLBACK MEMORY LOADING
    # ------------------------------------------------------------------

    def _ensure_fallback_loaded(self):
        """
        Populate local fallback memory from persisted
        meetings when the server restarts.
        """

        if self._local_fallback_memories:
            return

        data_file = os.path.join(
            os.getcwd(),
            settings.DATA_DIR,
            "meetings.json",
        )

        if not os.path.exists(data_file):
            return

        try:
            with open(
                data_file,
                "r",
                encoding="utf-8",
            ) as file:
                meetings = json.load(file)

            for meeting_data in meetings:
                meeting = MeetingCreate(
                    client=meeting_data.get(
                        "client",
                        "",
                    ),
                    contact=meeting_data.get(
                        "contact",
                        "",
                    ),
                    date=meeting_data.get(
                        "date",
                        "",
                    ),
                    title=meeting_data.get(
                        "title",
                        "",
                    ),
                    meeting_notes=meeting_data.get(
                        "meeting_notes",
                        "",
                    ),
                    decisions=meeting_data.get(
                        "decisions",
                        [],
                    ),
                    concerns=meeting_data.get(
                        "concerns",
                        [],
                    ),
                    commitments=meeting_data.get(
                        "commitments",
                        [],
                    ),
                    follow_ups=meeting_data.get(
                        "follow_ups",
                        [],
                    ),
                )

                formatted = (
                    self.format_meeting_memory(
                        meeting
                    )
                )

                client_name = meeting_data.get(
                    "client",
                    "",
                )

                self._local_fallback_memories.append(
                    {
                        "id": (
                            f"mem_fb_"
                            f"{meeting_data.get('id', '')}"
                        ),
                        "bank_id": self.bank_id,
                        "client": client_name,
                        "content": formatted,
                        "metadata": {
                            "client": client_name,
                            "contact": meeting_data.get(
                                "contact",
                                "",
                            ),
                            "date": meeting_data.get(
                                "date",
                                "",
                            ),
                            "title": meeting_data.get(
                                "title",
                                "",
                            ),
                            "meeting_id": meeting_data.get(
                                "id",
                                "",
                            ),
                        },
                        "tags": [
                            client_name
                            .lower()
                            .replace(
                                " ",
                                "_",
                            ),
                            "meeting",
                            "recallmeet",
                        ],
                        "date": meeting_data.get(
                            "date",
                            "",
                        ),
                        "created_at": meeting_data.get(
                            "created_at",
                            "",
                        ),
                    }
                )

        except Exception as e:
            logger.debug(
                f"Could not load fallback meetings: {e}"
            )

    # ------------------------------------------------------------------
    # FALLBACK RECALL
    # ------------------------------------------------------------------

    def _fallback_recall(
        self,
        client: str,
        query: str,
    ) -> List[MemoryItem]:
        """
        Simple keyword/client relevance matching
        for development fallback memory.
        """

        self._ensure_fallback_loaded()

        query_terms = [
            term.lower()
            for term in query.split()
            if len(term) > 2
        ]

        matched: List[MemoryItem] = []

        for record in (
            self._local_fallback_memories
        ):
            record_client = record.get(
                "client",
                "",
            )

            if (
                client.lower()
                not in record_client.lower()
                and record_client.lower()
                not in client.lower()
            ):
                continue

            content = record.get(
                "content",
                "",
            )

            content_lower = content.lower()

            matches = sum(
                1
                for term in query_terms
                if term in content_lower
            )

            score = (
                0.5
                + (
                    0.5
                    * (
                        matches
                        / max(
                            len(query_terms),
                            1,
                        )
                    )
                )
            )

            matched.append(
                MemoryItem(
                    id=record.get("id"),
                    content=content,
                    score=round(
                        score,
                        2,
                    ),
                    metadata=record.get(
                        "metadata",
                        {},
                    ),
                    network="experience",
                    timestamp=record.get(
                        "date"
                    ),
                    provider="local_fallback",
                )
            )

        matched.sort(
            key=lambda memory: (
                memory.score or 0.0
            ),
            reverse=True,
        )

        return matched

    # ------------------------------------------------------------------
    # REFLECT
    # ------------------------------------------------------------------

    async def reflect_on_client(
        self,
        client: str,
        query: str,
        bank_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Invoke Hindsight REFLECT to synthesize
        accumulated client intelligence.
        """

        target_bank = bank_id or self.bank_id

        tag_client = (
            client
            .lower()
            .replace(" ", "_")
        )

        status_info = await self.check_connection()

        # --------------------------------------------------------------
        # REAL HINDSIGHT REFLECT
        # --------------------------------------------------------------

        if (
            status_info["connected"]
            and self._client
        ):
            try:
                logger.info(
                    f"Executing Hindsight REFLECT "
                    f"for client '{client}' "
                    f"query: '{query}'"
                )

                # IMPORTANT:
                # Async REFLECT operation.
                reflect_resp = await self._client.areflect(
                    bank_id=target_bank,
                    query=(
                        f"Analyze client {client}: "
                        f"{query}"
                    ),
                    tags=[tag_client],
                    tags_match="any",
                )

                self.last_operation_status = {
                    "operation": "reflect",
                    "timestamp": (
                        datetime.now().isoformat()
                    ),
                    "provider": "hindsight",
                    "status": "success",
                    "details": (
                        f"Reflected on client "
                        f"'{client}' in Hindsight"
                    ),
                }

                if hasattr(
                    reflect_resp,
                    "text",
                ):
                    return reflect_resp.text

                return str(reflect_resp)

            except Exception as e:
                logger.warning(
                    f"Hindsight reflect error: {e}"
                )

                return None

        return None


# ----------------------------------------------------------------------
# GLOBAL SINGLETON
# ----------------------------------------------------------------------

hindsight_service = HindsightService()