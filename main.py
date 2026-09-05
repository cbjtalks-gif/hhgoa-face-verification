import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

load_dotenv()
console = Console()

from src.face_engine import FaceEngine
from src.search_engine import WebSearchEngine
from src.blockchain_engine import BlockchainEngine

def run_pipeline(image_path: str):
    console.print(Panel.fit(
        "[bold cyan]HACKER HOUSE GOA 2026 - TASK #3[/bold cyan]\n"
        "[bold green]Smart Contract Biometric Identity Attestation[/bold green]",
        border_style="cyan"
    ))

    # 1. Face Biometrics & Identification
    console.print("\n[1/3] [bold yellow]Extracting Biometrics & Recognizing Person...[/bold yellow]")
    face_engine = FaceEngine()
    face_result = face_engine.process_face(image_path)
    console.print(f"  ✔ Identified Person: [bold green]{face_result['person_name']}[/bold green] (Confidence: {face_result['confidence']})")
    console.print(f"  ✔ Face Bounding Box: {face_result['bounding_box']}")
    console.print(f"  ✔ SHA-256 Face Fingerprint: [dim cyan]{face_result['face_hash']}[/dim cyan]")

    # 2. Web / Social Search
    console.print("\n[2/3] [bold yellow]Executing Web OSINT & Social Match Search...[/bold yellow]")
    search_engine = WebSearchEngine()
    search_result = search_engine.search_matching_media(image_path, query_hint=face_result['person_name'])
    console.print(f"  ✔ Discovered Profile: [bold white]{search_result['source']}[/bold white]")
    console.print(f"  ✔ Verified URL: [underline blue]{search_result['post_url']}[/underline blue]")

    # 3. Smart Contract Attestation
    console.print("\n[3/3] [bold yellow]Invoking Smart Contract on Polygon Amoy (Chain ID 80002)...[/bold yellow]")
    bc_engine = BlockchainEngine()
    composite_hash = bc_engine.generate_composite_fingerprint(
        face_result['face_hash'],
        search_result['post_url'],
        face_result['person_name']
    )
    console.print(f"  ✔ Composite Hash: [bold magenta]{composite_hash}[/bold magenta]")
    console.print(f"  ✔ Target Smart Contract: [bold cyan]{bc_engine.contract_address}[/bold cyan]")
    console.print("  ⏳ Calling contract function registerRecord()...")

    tx_receipt = bc_engine.publish_verification_proof(composite_hash, search_result['post_url'])

    # 4. Smart Contract Verification Call
    console.print("\n[bold green]Querying Smart Contract State via verifyRecord()...[/bold green]")
    verify_result = bc_engine.verify_onchain_proof(tx_receipt['tx_hash'], composite_hash)

    table = Table(title="Smart Contract Attestation Summary", show_header=True, header_style="bold blue")
    table.add_column("Property", style="dim")
    table.add_column("On-Chain Value", style="bold")

    table.add_row("Identified Subject", f"[bold green]{face_result['person_name']}[/bold green]")
    table.add_row("Smart Contract Address", str(bc_engine.contract_address))
    table.add_row("Transaction / State", str(tx_receipt['tx_hash']))
    table.add_row("Block Number", str(tx_receipt['block_number']))
    table.add_row("Contract Status", "[green]VERIFIED / NOTARIZED ON-CHAIN[/green]" if verify_result['is_valid'] else "[red]NOT FOUND[/red]")
    table.add_row("Explorer URL", str(tx_receipt['explorer_url']))

    console.print(table)
    console.print("\n[bold green]✨ Smart Contract Pipeline Completed Successfully![/bold green]\n")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample.webp"
    if not os.path.exists(target):
        print(f"[ERROR] Target image '{target}' not found.")
    else:
        run_pipeline(target)