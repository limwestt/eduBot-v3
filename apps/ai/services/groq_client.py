import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def grade_mission(instruction: str, user_answer: str) -> dict:
    """
    Retourne un dict :
    {
        "score": 0-100,
        "passed": true|false,
        "feedback": "...",
        "improvements": ["...", "..."]
    }
    """
    system_prompt = """Tu es un correcteur pédagogique bienveillant mais rigoureux.
Tu évalues la réponse d'un apprenant à un exercice de programmation.
Réponds UNIQUEMENT en JSON valide, sans texte autour, avec exactement ces clés :
{
  "score": <nombre entier entre 0 et 100>,
  "passed": <true si score >= 60, sinon false>,
  "feedback": "<commentaire global en français, 1-2 phrases>",
  "improvements": ["<conseil 1>", "<conseil 2>"]
}"""

    user_prompt = f"""Consigne de l'exercice :
{instruction}

Réponse de l'apprenant :
{user_answer}"""

    try:
        res = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=500,
        )
        content = res.choices[0].message.content
        return json.loads(content)

    except json.JSONDecodeError:
        return {
            "score": 0,
            "passed": False,
            "feedback": "L'IA n'a pas pu analyser ta réponse. Réessaie.",
            "improvements": []
        }
    except Exception as e:
        return {
            "score": 0,
            "passed": False,
            "feedback": f"Erreur IA : {str(e)}",
            "improvements": []
        }
