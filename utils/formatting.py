from typing import Any, Dict, List


def format_case_output(case: Dict[str, Any]) -> str:
    """Format a complete case result for human-readable terminal display."""
    lines: List[str] = []
    sep = "=" * 62
    thin = "-" * 62

    lines += [f"\n{sep}", "  PYMMYS MISSION CONTROL — RESULTADO", sep]

    mission = case.get("mission")
    if mission:
        lines += [
            f"\nMISIÓN        {mission.get('mission', '')}",
            f"DECISIÓN REAL {mission.get('real_decision', '')}",
            f"TENSIÓN       {mission.get('key_tension', '')}",
        ]
        criteria = mission.get("success_criteria", [])
        if criteria:
            lines.append("CRITERIOS     " + " / ".join(criteria))

    options = case.get("product_options", [])
    brand_map = {e["option_id"]: e for e in case.get("brand_evaluations", [])}
    mkt_map = {a["option_id"]: a for a in case.get("marketing_angles", [])}
    ops_map = {a["option_id"]: a for a in case.get("feasibility_assessments", [])}

    if options:
        lines += [f"\n{thin}", "  OPCIONES DE PRODUCTO", thin]
        for opt in options:
            oid = opt["id"]
            lines += [
                f"\n  [{oid}] {opt['name'].upper()}",
                f"  {opt['description']}",
                f"  Audiencia  {opt['target_audience']}",
                f"  Precio     {opt['price_range']}   |   Tiempo  {opt['time_to_market']}",
                f"  Diferenciador  {opt['key_differentiator']}",
            ]
            if oid in brand_map:
                ev = brand_map[oid]
                lines.append(
                    f"  Marca      score={ev['brand_fit_score']}/10  "
                    f"veredicto={ev['verdict']}  →  {ev['recommendation']}"
                )
            if oid in mkt_map:
                ang = mkt_map[oid]
                lines.append(f"  Hook       \"{ang['hook']}\"")
                lines.append(f"  Canales    {', '.join(ang['target_channels'])}")
            if oid in ops_map:
                fas = ops_map[oid]
                lines.append(
                    f"  Ops        complejidad={fas['complexity_score']}/10  "
                    f"tiempo={fas['estimated_time']}  veredicto={fas['verdict']}"
                )

    review = case.get("critical_review")
    if review:
        lines += [f"\n{thin}", "  REVISIÓN CRÍTICA", thin]
        lines.append(f"  Veredicto global: {review.get('overall_verdict', '').upper()}")
        lines.append(f"  {review.get('summary', '')}")
        for assumption in review.get("weak_assumptions", []):
            lines.append(f"  ⚠ Supuesto débil: {assumption}")
        for risk in review.get("hidden_risks", []):
            lines.append(f"  ⚠ Riesgo oculto: {risk}")
        for q in review.get("uncomfortable_questions", []):
            lines.append(f"  ? {q}")

    decision = case.get("final_decision")
    if decision:
        lines += [f"\n{sep}", "  DECISIÓN FINAL", sep]
        lines += [
            f"  OPCIÓN  {decision.get('recommended_option_name', '')} "
            f"({decision.get('recommended_option_id', '')})",
            f"  CONFIANZA  {decision.get('confidence', '').upper()}",
            f"\n  SÍNTESIS\n  {decision.get('synthesis', '')}",
        ]
        for r in decision.get("rationale", []):
            lines.append(f"  • {r}")
        not_ignore = decision.get("what_not_to_ignore", [])
        if not_ignore:
            lines.append("\n  QUÉ NO IGNORAR")
            for n in not_ignore:
                lines.append(f"  ⚠ {n}")
        moves = decision.get("next_moves", [])
        if moves:
            lines.append("\n  NEXT MOVES")
            for i, move in enumerate(moves, 1):
                lines.append(f"  {i}. {move}")

    lines.append(f"\n{sep}")
    return "\n".join(lines)

def format_video_plan(case: dict) -> str:
    vp = case["video_plan"]

    lines = []
    lines.append("\n" + "=" * 70)
    lines.append("VIDEO PLAN — PYMMYS")
    lines.append("=" * 70)

    lines.append(f"\nTítulo: {vp['title']}")
    lines.append(f"Objetivo: {vp['objective']}")
    lines.append(f"Duración recomendada: {vp['recommended_duration']}")

    lines.append("\nESCENAS")
    for scene in vp["scenes"]:
        lines.append(f"\n  Escena {scene['scene']} · {scene['time']}")
        lines.append(f"  Visual: {scene['visual']}")
        lines.append(f"  Texto: {scene['text']}")

    lines.append("\nPROMPTS VISUALES")
    for prompt in vp["visual_prompts"]:
        lines.append(f"  - {prompt}")

    lines.append(f"\nMúsica: {vp['music_direction']}")
    lines.append(f"Nota final: {vp['final_note']}")
    lines.append("=" * 70)

    return "\n".join(lines)
