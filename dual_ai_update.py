# Update your dual AI call to support PowerPoint creation

def _ai_presentation(self, topic="", create_ppt=False):
    try:
        from engine.voice_advanced_ai import voice_advanced_ai
        if not topic:
            topic = "ai assistant"
        return voice_advanced_ai.ai_presentation_maker(topic, create_ppt)
    except Exception as e:
        return f"Error with AI presentation: {str(e)}"

# Usage examples:
# _ai_presentation("machine learning")           # Text outline only
# _ai_presentation("AI", create_ppt=True)        # Creates actual PowerPoint file