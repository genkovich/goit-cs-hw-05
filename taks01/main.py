import argparse
import asyncio
import logging

from aiopath import AsyncPath
from aioshutil import copyfile


async def read_folder(path: AsyncPath) -> None:
    try:
        async for element in path.iterdir():
            if await element.is_dir():
                logging.info(f"Reading folder {element}")
                await read_folder(element)
            else:
                logging.info(f"Copying {element}")
                await copy_file(element)

    except Exception as e:
        logging.error(f"Read error: {e}")


async def copy_file(file: AsyncPath) -> None:
    extension_name = file.suffix[1:]
    extension_folder = output / extension_name
    try:
        await extension_folder.mkdir(exist_ok=True, parents=True)
        await copyfile(file, extension_folder / file.name)
    except Exception as e:
        logging.error(f"Copy error: {e}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(threadName)s %(message)s"
    )

    parser = argparse.ArgumentParser(
        description="Copy files from source to dist"
    )

    parser.add_argument(
        "--source",
        help="Source directory",
        required=True,
        type=AsyncPath
    )

    parser.add_argument(
        "--output",
        help="Destination directory",
        default=AsyncPath("dist"),
        type=AsyncPath
    )

    args = parser.parse_args()

    source = AsyncPath(args.source)
    output = AsyncPath(args.output)

    asyncio.run(read_folder(source))
