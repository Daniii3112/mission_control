import os
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """Provider-agnostic interface for LLM text generation."""

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str: ...


class OpenAILLMClient(BaseLLMClient):
    """OpenAI implementation. Reads OPENAI_API_KEY from environment."""

    def __init__(self, model: str = "gpt-4.1-mini"):
        import openai
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content


class AnthropicLLMClient(BaseLLMClient):
    """Anthropic Claude implementation. Reads ANTHROPIC_API_KEY from environment."""

    def __init__(self, model: str = "claude-sonnet-4-6"):
        import anthropic
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text


class StubLLMClient(BaseLLMClient):
    """Returns hardcoded JSON responses for local testing without any API calls."""

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        # Dispatch by agent persona (unique per agent file), then by method within Director.
        sp = system_prompt.lower()

        if "creative director" in sp:
            return (
                '{"concept_title": "No sabes qué es, pero lo sientes",'
                ' "core_idea": "Un teaser corto que presenta Pymmys como una presencia sugerente, estética e incierta, sin explicarla del todo.",'
                ' "emotional_tone": "misterioso, premium, íntimo",'
                ' "visual_style": "minimalista, cálido, cinematográfico",'
                ' "atmosphere": "silencio, tensión suave, curiosidad",'
                ' "pacing": "lento al inicio, intenso al final",'
                ' "suggested_duration": "10-12 segundos",'
                ' "closing_feeling": "quiero saber más"}'
            )

        if "product lead" in sp:
            return (
                '{"options": ['
                '{"id": "option_1", "name": "Guía Digital de Estilo Pymmys",'
                ' "description": "PDF premium con metodología de diseño personal aplicada al estilo",'
                ' "target_audience": "Mujeres 25-35 interesadas en estilo consciente",'
                ' "price_range": "25-45€", "time_to_market": "3-4 semanas",'
                ' "key_differentiator": "Framework visual propio de Pymmys"},'
                '{"id": "option_2", "name": "Kit de Inicio Físico",'
                ' "description": "Caja curada con 3-5 objetos de diseño seleccionados por Pymmys",'
                ' "target_audience": "Amantes del diseño con poder adquisitivo medio-alto",'
                ' "price_range": "60-90€", "time_to_market": "8-10 semanas",'
                ' "key_differentiator": "Experiencia unboxing premium con curaduría experta"},'
                '{"id": "option_3", "name": "Workshop Online en Vivo",'
                ' "description": "Sesión grupal de diseño personal con metodología Pymmys",'
                ' "target_audience": "Profesionales que quieren reinventarse a través del estilo",'
                ' "price_range": "75-120€", "time_to_market": "2-3 semanas",'
                ' "key_differentiator": "Acceso directo al método y comunidad en tiempo real"}]}'
            )

        if "brand lead" in sp and "video teaser pymmys" in user_prompt.lower():
            return (
                '{"evaluations": ['
                '{"option_id": "video_teaser_1",'
                ' "brand_fit_score": 9,'
                ' "strengths": ["Construye identidad desde la atmósfera", "Refuerza percepción premium"],'
                ' "risks": ["Puede ser demasiado abstracto", "Necesita un gesto visual memorable"],'
                ' "verdict": "potencia_marca",'
                ' "recommendation": "Mantener el misterio, pero fijar memoria con una imagen o texto final claro"}]}'
            )

        if "brand lead" in sp:
            return (
                '{"evaluations": ['
                '{"option_id": "option_1", "brand_fit_score": 7, "strengths": ["Posiciona expertise",'
                ' "Bajo riesgo de marca"], "risks": ["Puede parecer genérico", "Difícil de diferenciar visualmente"],'
                ' "verdict": "neutro", "recommendation": "Viable solo si la producción visual es impecable"},'
                '{"option_id": "option_2", "brand_fit_score": 9, "strengths": ["Experiencia tangible premium",'
                ' "Alto potencial de difusión orgánica"], "risks": ["Mayor inversión inicial", "Logística compleja"],'
                ' "verdict": "potencia_marca", "recommendation": "Opción más alineada con la identidad aspiracional"},'
                '{"option_id": "option_3", "brand_fit_score": 8, "strengths": ["Genera comunidad inmediata",'
                ' "Prueba de valor del método"], "risks": ["Escalabilidad limitada", "Depende de energía del fundador"],'
                ' "verdict": "potencia_marca", "recommendation": "Excelente para validar propuesta de valor con bajo riesgo"}]}'
            )

        if "marketing lead" in sp and "video teaser pymmys" in user_prompt.lower():
            return (
                '{"angles": ['
                '{"option_id": "video_teaser_1",'
                ' "hook": "No todo lo importante se entiende al instante.",'
                ' "main_message": "Pymmys llega como una sensación antes que como una explicación.",'
                ' "target_channels": ["Instagram Reels", "TikTok"],'
                ' "campaign_concept": "Teaser corto de intriga y estética premium",'
                ' "communication_risk": "Puede quedar demasiado abstracto si no hay un ancla visual clara"}]}'
            )

        if "marketing lead" in sp:
            return (
                '{"angles": ['
                '{"option_id": "option_1", "hook": "El método para vestir con intención, no por impulso",'
                ' "main_message": "Diseña tu estilo como diseñas tu vida", "target_channels": ["Instagram", "Newsletter", "Pinterest"],'
                ' "campaign_concept": "5 días de contenido teaser + reveal del método", "communication_risk": "Saturación de contenido de moda digital"},'
                '{"option_id": "option_2", "hook": "Tu primera caja Pymmys. Curada para quién quieres ser.",'
                ' "main_message": "No es lo que compras. Es lo que dice de ti.", "target_channels": ["Instagram Stories", "Influencer gifting", "Waitlist email"],'
                ' "campaign_concept": "Preventa con lista de espera exclusiva de 48h", "communication_risk": "El unboxing real debe cumplir la promesa visual"},'
                '{"option_id": "option_3", "hook": "¿Y si rediseñas tu imagen en una tarde?",'
                ' "main_message": "El workshop que cambia cómo te ven — y cómo te ves", "target_channels": ["Instagram Lives", "LinkedIn", "Email"],'
                ' "campaign_concept": "Lanzamiento con sesión gratuita para los primeros 5 inscritos", "communication_risk": "Competencia alta en espacio de workshops online"}]}'
            )

        if "operations lead" in sp:
            return (
                '{"assessments": ['
                '{"option_id": "option_1", "complexity_score": 3, "resources_needed": ["Diseñador gráfico", "Redactor", "Plataforma de venta digital"],'
                ' "bottlenecks": ["Calidad de producción visual"], "estimated_time": "3-4 semanas", "verdict": "viable",'
                ' "notes": "La opción más rápida de lanzar con inversión mínima"},'
                '{"option_id": "option_2", "complexity_score": 8, "resources_needed": ["Proveedor de producto", "Packaging personalizado", "Gestión de stock", "Logística de envíos"],'
                ' "bottlenecks": ["Tiempo de fabricación de packaging", "Capital inicial para stock"], "estimated_time": "8-12 semanas", "verdict": "viable_con_condiciones",'
                ' "notes": "Viable solo con inversión inicial validada y proveedor confirmado"},'
                '{"option_id": "option_3", "complexity_score": 4, "resources_needed": ["Plataforma de videoconferencia", "Landing page", "Sistema de pagos"],'
                ' "bottlenecks": ["Disponibilidad del fundador", "Límite de participantes por sesión"], "estimated_time": "2-3 semanas", "verdict": "viable",'
                ' "notes": "Opción más rápida para validar modelo con riesgo financiero mínimo"}]}'
            )

        if "critical reviewer" in sp and "creative_concept" in user_prompt.lower():
            return (
                '{"weak_assumptions": ["Asumir que la audiencia conectará con la atmósfera sin entender el contexto"],'
                ' "hidden_risks": ["Que el teaser sea bonito pero no memorable", "Que no haya ningún elemento distintivo de Pymmys"],'
                ' "uncomfortable_questions": ["¿Qué recordará la gente exactamente al terminar el vídeo?",'
                ' "¿Hay un ancla visual o verbal suficientemente fuerte?"],'
                ' "overall_verdict": "prometedor",'
                ' "summary": "La idea funciona si el misterio no sacrifica recordación."}'
            )

        if "critical reviewer" in sp:
            return (
                '{"weak_assumptions": ["Asumir que el mercado ya conoce Pymmys y confía en la marca",'
                ' "Creer que el precio premium es aceptable sin proof of concept previo",'
                ' "Asumir que la identidad de marca está clara para la audiencia objetivo"],'
                ' "hidden_risks": ["Sin audiencia existente, el lanzamiento puede caer en el vacío",'
                ' "El kit físico requiere capital que puede perderse sin validación previa",'
                ' "Los workshops escalan poco si dependen exclusivamente del fundador"],'
                ' "uncomfortable_questions": ["¿Tienes audiencia existente o estás construyendo desde cero?",'
                ' "¿Cuántos clientes necesitas en el mes 1 para considerar esto validado?",'
                ' "¿Estás listo operativamente para gestionar devoluciones, envíos e incidencias?"],'
                ' "per_option_verdict": {"option_1": "Riesgo bajo pero impacto potencial también moderado",'
                ' "option_2": "Alto potencial pero necesita capital y tiempo que pueden no estar disponibles ahora",'
                ' "option_3": "Mejor opción para validar con riesgo financiero mínimo"},'
                ' "overall_verdict": "fragil",'
                ' "summary": "El plan tiene buenas ideas pero está construido sobre supuestos no validados."}'
            )

        # Director is called twice: define_mission (no prior outputs in prompt) and make_decision (has full outputs).
 
        if "director final" in sp and "video_plan" in user_prompt.lower():
            return (
                '{"title": "Teaser 01 — Pymmys",'
                ' "objective": "presentar Pymmys con intriga y estética premium",'
                ' "recommended_duration": "10-12 segundos",'
                ' "scenes": ['
                '{"scene": 1, "time": "0-3s", "visual": "pantalla oscura, luz cálida apareciendo lentamente", "text": "algo está cambiando"},'
                '{"scene": 2, "time": "3-6s", "visual": "detalle de mesa minimalista, sombras suaves, objeto insinuado", "text": "no sabes qué es"},'
                '{"scene": 3, "time": "6-9s", "visual": "movimiento sutil, atmósfera íntima, enfoque corto", "text": "pero lo sientes"},'
                '{"scene": 4, "time": "9-12s", "visual": "pantalla limpia con logo o palabra PYMMYS", "text": "PYMMYS · coming soon"}'
                '],'
                ' "visual_prompts": ['
                '"cinematic warm lighting, premium minimalism, mysterious atmosphere, shallow depth of field",'
                '"clean luxury teaser, soft shadows, emotional brand reveal, short form video aesthetic"'
                '],'
                ' "music_direction": "ambient minimal, soft tension, cinematic pulse",'
                ' "final_note": "menos explicación, más sensación"}'
            )        

        if "director" in sp and "vídeo teaser corto para pymmys" in user_prompt.lower():
            return (
                '{"mission": "Crear un teaser corto de presentación de marca para Pymmys",'
                ' "real_decision": "¿Cómo generar intriga, identidad y hype en 10-12 segundos sin explicar demasiado?",'
                ' "key_tension": "Misterio e impacto visual vs claridad mínima de marca",'
                ' "success_criteria": ["Se siente premium", "Genera curiosidad", "Deja una imagen recordable", "Funciona en formato corto"]}'
            )

        if "recommended_option_id" in user_prompt:
            return (
                '{"recommended_option_id": "option_3", "recommended_option_name": "Workshop Online en Vivo",'
                ' "synthesis": "Tras analizar las tres opciones, el Workshop Online es el primer movimiento más'
                ' inteligente para Pymmys: valida la propuesta de valor antes de invertir en producto físico,'
                ' genera comunidad real y permite iterar el mensaje rápidamente.",'
                ' "rationale": ["Menor riesgo financiero y operativo de los tres", "Valida propuesta de valor antes de comprometer capital",'
                ' "Genera primeros clientes y comunidad desde el día 1", "Permite iterar el mensaje con feedback directo"],'
                ' "what_not_to_ignore": ["Sin audiencia previa el lanzamiento necesita apoyo de distribución externa",'
                ' "El workshop debe tener producción visual impecable para transmitir la identidad de marca"],'
                ' "next_moves": ["Definir fecha y tema del primer workshop en los próximos 7 días",'
                ' "Crear landing page con preventa en 5 días",'
                ' "Activar lista de espera con contenido teaser en Instagram",'
                ' "Usar el workshop como caso de estudio para el siguiente producto"],'
                ' "confidence": "alta"}'
            )

        # define_mission fallback
        return (
            '{"mission": "Elegir y lanzar el primer producto de Pymmys con el mayor impacto de marca posible",'
            ' "real_decision": "¿Digital, físico o servicio como primer movimiento?",'
            ' "key_tension": "Velocidad de lanzamiento vs coherencia de marca",'
            ' "success_criteria": ["Encaje con identidad de marca", "Viable en 60 días", "Precio entre 20-80 euros"]}'
        )


def get_default_client() -> BaseLLMClient:
    """Auto-detect available API key and return the appropriate client."""
    from dotenv import load_dotenv

    load_dotenv()

    if os.getenv("ANTHROPIC_API_KEY"):
        return AnthropicLLMClient()
    if os.getenv("OPENAI_API_KEY"):
        return OpenAILLMClient()

    print("[WARN] No API key found — using StubLLMClient (modo local sin API)")
    return StubLLMClient()
