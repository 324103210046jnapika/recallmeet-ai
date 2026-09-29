from typing import Optional

from ..schemas.prepare import (
    MeetingPrepareRequest,
    MeetingPrepareResponse
)

from ..schemas.memory import MemoryOperationInfo

from ..services.hindsight_service import (
    hindsight_service
)

from ..services.llm_service import (
    llm_service
)

from ..utils.logger import logger


class MeetingPrepService:

    async def prepare_meeting(
        self,
        request: MeetingPrepareRequest
    ) -> MeetingPrepareResponse:

        """
        Prepare a meeting using accumulated
        Hindsight memory.

        Flow:

        1. Check Hindsight connection
        2. RECALL relevant memories
        3. REFLECT on accumulated client knowledge
        4. Pass memory context to LLM
        5. Generate meeting preparation brief
        """

        logger.info(
            f"Preparing meeting for "
            f"'{request.client}'. "
            f"Memory Enabled: "
            f"{request.memory_enabled}. "
            f"Context: "
            f"{request.upcoming_context}"
        )

        # --------------------------------------------------------------
        # INITIAL STATE
        # --------------------------------------------------------------

        memories = []

        reflection_text = None

        # --------------------------------------------------------------
        # CHECK HINDSIGHT
        # --------------------------------------------------------------

        hindsight_status = (
            await hindsight_service.check_connection()
        )

        hindsight_connected = (
            hindsight_status.get(
                "connected",
                False
            )
        )

        # --------------------------------------------------------------
        # MEMORY BANK
        # --------------------------------------------------------------

        if (
            hasattr(request, "bank_id")
            and getattr(
                request,
                "bank_id",
                None
            )
        ):

            bank_id = request.bank_id

        else:

            bank_id = (
                hindsight_service.bank_id
            )

        # --------------------------------------------------------------
        # MEMORY ENABLED
        # --------------------------------------------------------------

        if request.memory_enabled:

            # ----------------------------------------------------------
            # BUILD RECALL QUERY
            # ----------------------------------------------------------

            recall_query = (
                f"{request.upcoming_context} "
                f"{request.user_question or ''}"
            ).strip()

            # ----------------------------------------------------------
            # HINDSIGHT RECALL
            # ----------------------------------------------------------

            (
                memories,
                provider_name,
                op_info
            ) = await hindsight_service.recall_memories(
                client=request.client,
                query=recall_query,
                bank_id=bank_id
            )

            # ----------------------------------------------------------
            # HINDSIGHT REFLECT
            # ----------------------------------------------------------

            if hindsight_connected:

                reflection_text = (
                    await hindsight_service.reflect_on_client(
                        client=request.client,
                        query=(
                            "Provide strategic briefing "
                            f"for meeting: "
                            f"{request.upcoming_context}"
                        ),
                        bank_id=bank_id
                    )
                )

                if (
                    reflection_text
                    and "reflect"
                    not in op_info.operations
                ):

                    op_info.operations.append(
                        "reflect"
                    )

        # --------------------------------------------------------------
        # MEMORY DISABLED
        # --------------------------------------------------------------

        else:

            provider_name = "none"

            op_info = MemoryOperationInfo(
                provider="none",
                operations=[],
                bank_id=bank_id,
                memory_count=0,
                connected=hindsight_connected,
                message=(
                    "Memory disabled "
                    "(Hackathon baseline "
                    "comparison mode)"
                )
            )

        # --------------------------------------------------------------
        # GENERATE MEETING PREPARATION
        # --------------------------------------------------------------

        return llm_service.generate_meeting_prep(
            client=request.client,
            upcoming_context=request.upcoming_context,
            user_question=request.user_question,
            memories=memories,
            memory_enabled=request.memory_enabled,
            hindsight_connected=hindsight_connected,
            reflection_text=reflection_text,
            memory_provider=provider_name,
            memory_info=op_info
        )


# ----------------------------------------------------------------------
# GLOBAL SERVICE INSTANCE
# ----------------------------------------------------------------------

prep_service = MeetingPrepService()