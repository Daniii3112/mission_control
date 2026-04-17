import logging
import sys

from dotenv import load_dotenv

from core.llm_client import StubLLMClient
from core.memory import CaseMemory
from core.orchestrator import MissionControl
from utils.formatting import format_case_output, format_video_plan

load_dotenv()
logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s — %(message)s")

BANNER = """\
╔══════════════════════════════════════════════════════════════╗
║           PYMMYS MISSION CONTROL  —  V2                     ║
╚══════════════════════════════════════════════════════════════╝"""

DEFAULT_CASE = (
    "Quiero decidir cuál debería ser el primer producto de Pymmys. "
    "Tengo dudas entre lanzar algo digital rápido, un kit físico premium "
    "o un workshop en vivo. Necesito saber qué mover primero."
)


def run_new_case(mc: MissionControl) -> None:
    print("\nDescribe el caso (Enter para usar el caso de ejemplo):")
    case_input = input("  > ").strip()

    if not case_input:
        case_input = DEFAULT_CASE
        print(f"\n  [Ejemplo] {case_input}\n")

    print()
    try:
        case = mc.run_case(case_input)
        print(format_case_output(case))
        print(f"\n  Caso guardado  ID: {case['id']}\n")
    except ValueError as e:
        print(f"\n[ERROR] {e}\n")
        sys.exit(1)


def list_cases(memory: CaseMemory) -> None:
    cases = memory.list_cases()
    if not cases:
        print("\n  No hay casos guardados aún.\n")
        return
    print(f"\n  {'ID':<16}  {'Fecha':<20}  Caso")
    print(f"  {'─'*16}  {'─'*20}  {'─'*40}")
    for c in cases:
        print(f"  {c['id']:<16}  {c['created_at'][:19]:<20}  {c['preview']}")
    print()


def main() -> None:
    print(BANNER)

    use_stub = "--stub" in sys.argv or (
        input("\n¿Ejecutar en modo stub (sin API, ideal para test)? [s/N]: ").strip().lower() == "s"
    )

    llm = StubLLMClient() if use_stub else None
    mc = MissionControl(llm=llm)

    if use_stub:
        print("  [Modo STUB activado — no se realizan llamadas a la API]\n")

    while True:
        print("  [1] Nuevo caso estratégico   [2] Ver historial   [3] Crear teaser de vídeo   [0] Salir")
        choice = input("  > ").strip()

        if choice == "1":
            run_new_case(mc)
        elif choice == "2":
            list_cases(mc.memory)
        elif choice == "3":
            print("\nDescribe el vídeo teaser que quieres (Enter para usar ejemplo):")
            case_input = input("  > ").strip()

            if not case_input:
                case_input = (
                    "Quiero un vídeo mazo corto para presentar Pymmys, con mucha intriga, "
                    "incertidumbre, estética premium y hype."
                )
                print(f"\n  [Ejemplo] {case_input}\n")

            try:
                case = mc.run_video_case(case_input)
                print(format_video_plan(case))
                print(f"\n  Caso guardado  ID: {case['id']}\n")
            except ValueError as e:
                print(f"\n[ERROR] {e}\n")
        elif choice == "0":
            print("  Hasta luego.\n")
            break
        else:
            print("  Opción no válida.\n")


if __name__ == "__main__":
    main()
