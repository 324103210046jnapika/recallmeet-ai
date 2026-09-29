from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from .config import settings
from .utils.logger import logger
from .routes import health, meetings, memory, clients, insights
from .services.hindsight_service import hindsight_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle startup and shutdown handler.

    On startup:
    - Checks Hindsight connectivity
    - Initializes the Hindsight memory bank when available

    On shutdown:
    - Closes the Hindsight client
    """

    logger.info(
        f"Starting {settings.PROJECT_NAME} v{settings.VERSION}..."
    )

    # ------------------------------------------------------------
    # HINDSIGHT STARTUP CHECK
    # ------------------------------------------------------------

    try:
        # Hindsight SDK uses asynchronous operations.
        conn = await hindsight_service.check_connection()

        if conn.get("connected"):

            logger.info(
                f"Connected to Hindsight server at "
                f"{settings.HINDSIGHT_BASE_URL} "
                f"(v{conn.get('version')})"
            )

            # Ensure the configured memory bank exists.
            await hindsight_service.ensure_bank()

        else:

            logger.warning(
                f"Hindsight server at "
                f"{settings.HINDSIGHT_BASE_URL} "
                f"not reachable "
                f"({conn.get('error')}). "
                "RecallMeet AI is running in resilient mode."
            )

    except Exception as e:

        logger.warning(
            f"Notice during Hindsight bank startup check: {e}"
        )

    # ------------------------------------------------------------
    # APPLICATION RUNNING
    # ------------------------------------------------------------

    yield

    # ------------------------------------------------------------
    # SHUTDOWN
    # ------------------------------------------------------------

    logger.info(
        f"Shutting down {settings.PROJECT_NAME}..."
    )

    hindsight_service.close()


# ================================================================
# FASTAPI APPLICATION
# ================================================================

app = FastAPI(
    title="RecallMeet AI API",

    description=(
        "Portfolio-grade AI Meeting Intelligence Agent that remembers "
        "previous interactions with clients using Hindsight persistent "
        "memory to prepare the user for future meetings."
    ),

    version=settings.VERSION,

    lifespan=lifespan,

    docs_url="/docs",
    redoc_url="/redoc"
)


# ================================================================
# CORS CONFIGURATION
# ================================================================

# Allows the React/Vite frontend to communicate with the FastAPI backend.
app.add_middleware(
    CORSMiddleware,

    allow_origins=settings.CORS_ORIGINS,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ================================================================
# REGISTER API ROUTES
# ================================================================

app.include_router(health.router)
app.include_router(meetings.router)
app.include_router(memory.router)
app.include_router(clients.router)
app.include_router(insights.router)


# ================================================================
# ROOT ROUTE
# ================================================================

@app.get(
    "/",
    include_in_schema=False
)
def root():
    """
    Redirect the root URL to the interactive API documentation.
    """
    return RedirectResponse(url="/docs")


# ================================================================
# DIRECT EXECUTION
# ================================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )