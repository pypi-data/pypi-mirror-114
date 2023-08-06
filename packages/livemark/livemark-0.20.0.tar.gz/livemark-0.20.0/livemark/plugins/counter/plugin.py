from ...plugin import Plugin


class CounterPlugin(Plugin):
    profile = {
        "type": "object",
        "required": ["type", "code"],
        "properties": {
            "type": {"type": "string"},
            "code": {"type": "string"},
        },
    }

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Prepare context
        type = markup.plugin_config.get("type")
        code = markup.plugin_config.get("code")

        # Update markup
        if type == "google":
            markup.add_markup(
                "markup.html",
                target="head",
                code=code,
            )
