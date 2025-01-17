from typing import List
from rich.table import Table
from rich.console import Console

from datetime import datetime
import openai
import typer
import time

app = typer.Typer()
console = Console()


# Sample response data
def generate_file_table(files: List[openai.File]) -> Table:
    table = Table(
        title="OpenAI Files",
    )
    table.add_column("File ID", style="dim")
    table.add_column("Size (bytes)", justify="right")
    table.add_column("Creation Time")
    table.add_column("Filename")
    table.add_column("Purpose")

    for file in files:
        table.add_row(
            file["id"],
            str(file["bytes"]),
            str(datetime.fromtimestamp(file["created_at"])),
            file["filename"],
            file["purpose"],
        )

    return table


def get_files(limit: int = 5) -> List[openai.File]:
    files = openai.File.list(limit=limit)["data"]  # type: ignore
    files = sorted(files, key=lambda x: x["created_at"], reverse=True)
    return files[:limit]


def get_file_status(file_id: str) -> str:
    response = openai.File.retrieve(file_id)
    return response["status"]


@app.command(
    help="Upload a file to OpenAI's servers, will monitor the upload status until it is processed",
)
def upload(
    filepath: str = typer.Argument(..., help="Path to the file to upload"),
    purpose: str = typer.Option("fine-tune", help="Purpose of the file"),
    poll: int = typer.Option(5, help="Polling interval in seconds"),
):
    with open(filepath, "rb") as file:
        response = openai.File.create(file=file, purpose=purpose)
    file_id = response["id"]
    with console.status(f"Monitoring upload: {file_id}...") as status:
        status.spinner_style = "dots"
        while True:
            file_status = get_file_status(file_id)
            if file_status == "processed":
                console.log(f"[bold green]File {file_id} uploaded successfully!")
                break
            time.sleep(poll)


@app.command(
    help="Download a file from OpenAI's servers",
)
def download(
    file_id: str = typer.Argument(..., help="ID of the file to download"),
    output: str = typer.Argument(..., help="Output path for the downloaded file"),
):
    with console.status(f"[bold green]Downloading file {file_id}...", spinner="dots"):
        content = openai.File.download(file_id)
        with open(output, "wb") as file:
            file.write(content)
        console.log(f"[bold green]File {file_id} downloaded successfully!")


@app.command(
    help="Delete a file from OpenAI's servers",
)
def delete(file_id: str = typer.Argument(..., help="ID of the file to delete")):
    with console.status(f"[bold red]Deleting file {file_id}...", spinner="dots"):
        try:
            openai.File.delete(file_id)
            console.log(f"[bold red]File {file_id} deleted successfully!")
        except Exception as e:
            console.log(f"[bold red]Error deleting file {file_id}: {e}")
            return


@app.command(
    help="Monitor the status of a file on OpenAI's servers",
)
def status(
    file_id: str = typer.Argument(..., help="ID of the file to check the status of")
):
    with console.status(f"Monitoring status of file {file_id}...") as status:
        while True:
            file_status = get_file_status(file_id)
            status.update(f"File status: {file_status}")
            if file_status in ["pending", "processed"]:
                break
            time.sleep(5)


@app.command(
    help="List the files on OpenAI's servers",
)
def list(limit: int = typer.Option(5, help="Limit the number of files to list")):
    files = get_files(limit=limit)
    console.log(generate_file_table(files))
