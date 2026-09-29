import os
import json
import uuid
import tempfile
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..config import settings
from ..utils.logger import logger
from ..schemas.meeting import MeetingCreate, MeetingResponse
from ..schemas.client import ClientSummary, ClientDetail
from .hindsight_service import hindsight_service


class MeetingService:

    def __init__(self):
        # Project-level data directory.
        # When the backend is started from D:\recallmeet-ai,
        # this becomes D:\recallmeet-ai\data
        self.data_dir = os.path.join(
            os.getcwd(),
            settings.DATA_DIR
        )

        os.makedirs(
            self.data_dir,
            exist_ok=True
        )

        self.file_path = os.path.join(
            self.data_dir,
            "meetings.json"
        )

        self._meetings: Dict[str, dict] = {}

        self._load()

    # ------------------------------------------------------------------
    # JSON-SAFE CONVERSION
    # ------------------------------------------------------------------

    def _make_json_safe(self, value: Any) -> Any:
        """
        Convert values into structures that can always be serialized
        safely as JSON.

        This protects the local store if Hindsight returns an object
        that is not directly JSON serializable.
        """

        if value is None:
            return None

        if isinstance(value, (str, int, float, bool)):
            return value

        if isinstance(value, dict):
            return {
                str(key): self._make_json_safe(item)
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple, set)):
            return [
                self._make_json_safe(item)
                for item in value
            ]

        # Pydantic v2 models
        if hasattr(value, "model_dump"):
            try:
                return self._make_json_safe(
                    value.model_dump()
                )
            except Exception:
                pass

        # Pydantic v1 models / other model-like objects
        if hasattr(value, "dict"):
            try:
                return self._make_json_safe(
                    value.dict()
                )
            except Exception:
                pass

        # Last-resort conversion.
        return str(value)

    # ------------------------------------------------------------------
    # LOAD MEETINGS
    # ------------------------------------------------------------------

    def _load(self):
        """
        Load meetings from the local JSON store.

        If the file is empty/corrupted, start with an empty
        in-memory store instead of crashing the application.
        """

        if not os.path.exists(self.file_path):
            self._meetings = {}
            logger.info(
                "No meetings file found. Starting with empty local store."
            )
            return

        try:
            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as f:

                raw = f.read().strip()

                if not raw:
                    self._meetings = {}
                    logger.info(
                        "Meetings file was empty. Starting with empty store."
                    )
                    return

                data = json.loads(raw)

                if not isinstance(data, list):
                    raise ValueError(
                        "meetings.json must contain a JSON array."
                    )

                self._meetings = {
                    m["id"]: m
                    for m in data
                    if isinstance(m, dict) and m.get("id")
                }

            logger.info(
                f"Loaded {len(self._meetings)} meetings "
                "from local store."
            )

        except Exception as e:
            logger.error(
                f"Error loading meetings from "
                f"{self.file_path}: {e}"
            )

            # Do not allow a corrupted local file to stop
            # the entire application.
            self._meetings = {}

    # ------------------------------------------------------------------
    # SAVE MEETINGS
    # ------------------------------------------------------------------

    def _save(self):
        """
        Safely persist meetings to disk.

        Uses:
        1. JSON-safe conversion
        2. Temporary file
        3. Flush + fsync
        4. Atomic os.replace()

        This prevents meetings.json from being left partially written
        if serialization fails or the process is interrupted.
        """

        safe_data = self._make_json_safe(
            list(self._meetings.values())
        )

        temp_path = None

        try:
            # Create temporary file in the same directory.
            # Keeping it in the same directory makes os.replace()
            # reliable on Windows.
            fd, temp_path = tempfile.mkstemp(
                prefix="meetings_",
                suffix=".tmp",
                dir=self.data_dir
            )

            with os.fdopen(
                fd,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    safe_data,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

                f.flush()
                os.fsync(f.fileno())

            # Replace the old file only after the complete JSON
            # document has been successfully written.
            os.replace(
                temp_path,
                self.file_path
            )

            temp_path = None

            logger.info(
                f"Saved {len(self._meetings)} meetings "
                f"to {self.file_path}"
            )

        except Exception as e:

            logger.error(
                f"Error saving meetings to "
                f"{self.file_path}: {e}"
            )

            # Remove failed temporary file if it exists.
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

            # Raise the error so the API knows that persistence failed.
            raise

    # ------------------------------------------------------------------
    # CREATE MEETING
    # ------------------------------------------------------------------

    async def create_meeting(
        self,
        meeting: MeetingCreate,
        custom_id: Optional[str] = None
    ) -> MeetingResponse:

        """
        Create a meeting, attempt to retain it in Hindsight,
        persist it locally, and return the complete meeting record.
        """

        meeting_id = (
            custom_id
            or str(uuid.uuid4())[:8]
        )

        now_str = datetime.now().isoformat()

        # --------------------------------------------------------------
        # RETAIN INTO HINDSIGHT
        # --------------------------------------------------------------

        retain_result = await hindsight_service.retain_meeting(
            meeting=meeting,
            meeting_id=meeting_id
        )

        if not isinstance(retain_result, dict):
            retain_result = {}

        hindsight_status = (
            "retained_in_hindsight"
            if retain_result.get("hindsight_connected")
            else "retained_resilient_store"
        )

        retained_memory_id = retain_result.get(
            "operation_id"
        )

        if not retained_memory_id:
            retained_memory_id = retain_result.get(
                "memory_id"
            )

        memory_provider = retain_result.get(
            "memory_provider",
            "local_fallback"
        )

        memory_info = retain_result.get(
            "memory_info"
        )

        # Make the Hindsight result JSON-safe before putting it
        # into the meeting record.
        memory_info = self._make_json_safe(
            memory_info
        )

        # --------------------------------------------------------------
        # LOCAL MEETING RECORD
        # --------------------------------------------------------------

        meeting_record = {
            "id": meeting_id,
            "client": meeting.client,
            "contact": meeting.contact,
            "date": meeting.date,
            "title": meeting.title,
            "meeting_notes": meeting.meeting_notes,
            "decisions": meeting.decisions or [],
            "concerns": meeting.concerns or [],
            "commitments": meeting.commitments or [],
            "follow_ups": meeting.follow_ups or [],
            "retained_memory_id": retained_memory_id,
            "hindsight_status": hindsight_status,
            "memory_provider": memory_provider,
            "memory_info": memory_info,
            "created_at": now_str
        }

        # --------------------------------------------------------------
        # LOCAL PERSISTENCE
        # --------------------------------------------------------------

        self._meetings[meeting_id] = meeting_record

        # Atomic save.
        self._save()

        logger.info(
            f"Meeting {meeting_id} saved for client "
            f"'{meeting.client}'. "
            f"Provider: {memory_provider}"
        )

        return MeetingResponse(
            **meeting_record
        )

    # ------------------------------------------------------------------
    # GET ALL MEETINGS
    # ------------------------------------------------------------------

    def get_meetings(
        self,
        client: Optional[str] = None
    ) -> List[MeetingResponse]:

        """
        List meetings, optionally filtered by client name.
        """

        records = list(
            self._meetings.values()
        )

        if client:
            records = [
                meeting
                for meeting in records
                if client.lower()
                in meeting.get(
                    "client",
                    ""
                ).lower()
            ]

        # Sort chronologically.
        records.sort(
            key=lambda meeting: meeting.get(
                "date",
                ""
            ),
            reverse=False
        )

        for meeting in records:

            if "memory_provider" not in meeting:

                meeting["memory_provider"] = (
                    "hindsight"
                    if meeting.get(
                        "hindsight_status"
                    ) == "retained_in_hindsight"
                    else "local_fallback"
                )

        return [
            MeetingResponse(**meeting)
            for meeting in records
        ]

    # ------------------------------------------------------------------
    # GET SINGLE MEETING
    # ------------------------------------------------------------------

    def get_meeting(
        self,
        meeting_id: str
    ) -> Optional[MeetingResponse]:

        """
        Retrieve one meeting by ID.
        """

        record = self._meetings.get(
            meeting_id
        )

        if record:

            if "memory_provider" not in record:

                record["memory_provider"] = (
                    "hindsight"
                    if record.get(
                        "hindsight_status"
                    ) == "retained_in_hindsight"
                    else "local_fallback"
                )

            return MeetingResponse(
                **record
            )

        return None

    # ------------------------------------------------------------------
    # GET CLIENTS
    # ------------------------------------------------------------------

    def get_clients(
        self
    ) -> List[ClientSummary]:

        """
        Aggregate all distinct clients
        and summary metrics.
        """

        client_map: Dict[str, dict] = {}

        for meeting in self._meetings.values():

            client_name = meeting.get(
                "client",
                "Unknown"
            )

            if client_name not in client_map:

                client_map[client_name] = {
                    "name": client_name,
                    "contacts": set(),
                    "total_meetings": 0,
                    "last_interaction": meeting.get(
                        "date",
                        ""
                    )
                }

            client_map[
                client_name
            ][
                "total_meetings"
            ] += 1

            if meeting.get("contact"):

                client_map[
                    client_name
                ][
                    "contacts"
                ].add(
                    meeting.get("contact")
                )

            if (
                meeting.get("date", "")
                >
                client_map[
                    client_name
                ][
                    "last_interaction"
                ]
            ):

                client_map[
                    client_name
                ][
                    "last_interaction"
                ] = meeting.get(
                    "date",
                    ""
                )

        summaries = []

        for client_name, data in client_map.items():

            primary_contact = (
                next(
                    iter(data["contacts"]),
                    "Unknown"
                )
                if data["contacts"]
                else None
            )

            summaries.append(
                ClientSummary(
                    name=client_name,
                    primary_contact=primary_contact,
                    total_meetings=data[
                        "total_meetings"
                    ],
                    last_interaction=data[
                        "last_interaction"
                    ]
                )
            )

        summaries.sort(
            key=lambda summary:
            summary.total_meetings,
            reverse=True
        )

        return summaries

    # ------------------------------------------------------------------
    # GET CLIENT DETAIL
    # ------------------------------------------------------------------

    def get_client_detail(
        self,
        client_name: str
    ) -> Optional[ClientDetail]:

        """
        Retrieve a rich profile for a client.
        """

        client_meetings = [
            meeting
            for meeting in self._meetings.values()
            if client_name.lower()
            in meeting.get(
                "client",
                ""
            ).lower()
        ]

        if not client_meetings:
            return None

        client_meetings.sort(
            key=lambda meeting:
            meeting.get(
                "date",
                ""
            )
        )

        first_date = client_meetings[0].get(
            "date"
        )

        last_date = client_meetings[-1].get(
            "date"
        )

        contacts = list({
            meeting.get("contact")
            for meeting in client_meetings
            if meeting.get("contact")
        })

        priorities = set()
        tags = set()

        for meeting in client_meetings:

            for decision in meeting.get(
                "decisions",
                []
            ):
                priorities.add(
                    decision
                )

            notes = meeting.get(
                "meeting_notes",
                ""
            ).lower()

            if "aws" in notes:
                tags.add("AWS")

            if (
                "security" in notes
                or meeting.get("concerns")
            ):
                tags.add(
                    "Security-Focused"
                )

            if "rbac" in notes:
                tags.add(
                    "RBAC-Required"
                )

        return ClientDetail(
            name=client_meetings[0].get(
                "client",
                client_name
            ),

            primary_contact=(
                contacts[0]
                if contacts
                else None
            ),

            total_meetings=len(
                client_meetings
            ),

            first_interaction=first_date,

            last_interaction=last_date,

            known_priorities=list(
                priorities
            )[:5],

            contacts=contacts,

            tags=list(tags)
        )


# ----------------------------------------------------------------------
# GLOBAL SERVICE INSTANCE
# ----------------------------------------------------------------------

meeting_service = MeetingService()