import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RoomOutputOptions,
    WorkerOptions,
    WorkerType,
    cli,
)
from livekit.plugins import bithuman, openai, silero

logger = logging.getLogger("bithuman-livekit-agent")
logger.setLevel(logging.INFO)

load_dotenv()

IMX_MODEL_ROOT = os.getenv("IMX_MODEL_ROOT", "/persistent-storage/imx-models")


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    valid_models = sorted(Path(IMX_MODEL_ROOT).glob("*.imx"))
    if len(valid_models) == 0:
        raise ValueError("No valid models found")

    # example: read model path from participant identity
    remote_participant = await ctx.wait_for_participant()
    if remote_participant.identity in valid_models:
        model_path = valid_models[remote_participant.identity]
        logger.info(f"using model {model_path} from participant identity")
    else:
        model_path = valid_models[0]
        logger.info(f"using default model {model_path}")

    logger.info("starting bithuman runtime")
    bithuman_avatar = bithuman.AvatarSession(
        model_path=str(model_path),
        api_secret=os.getenv("BITHUMAN_API_SECRET"),
        api_token=os.getenv("BITHUMAN_API_TOKEN"),
    )

    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
           voice="coral",
           model="gpt-4o-mini-realtime-preview",
        ),
        vad=silero.VAD.load()
    )

    await bithuman_avatar.start(
        session, 
        room=ctx.room
    )

    await session.start(
        agent=Agent(
            instructions=(
                "Your are helpful assistant, talk to me! Response shortly and concisely."
            )
        ),
        room=ctx.room,
        # audio is forwarded to the avatar, so we disable room audio output
        room_output_options=RoomOutputOptions(audio_enabled=False),
    )

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            worker_type=WorkerType.ROOM,
            job_memory_warn_mb=1500,
            num_idle_processes=1,
            initialize_process_timeout=120,
        )
    )
