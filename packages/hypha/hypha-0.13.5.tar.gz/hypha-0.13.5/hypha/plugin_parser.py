"""ImJoy plugin parser module."""
import json
import uuid

import yaml
from lxml import etree

from hypha.utils import dotdict

tag_types = ["config", "script", "link", "window", "style", "docs", "attachment"]

CONFIGURABLE_FIELDS = [
    "env",
    "requirements",
    "dependencies",
    "icon",
    "ui",
    "type",
    "flags",
    "labels",
    "cover",
    "base_frame",
    "base_worker",
    "passive",
]


def parse_imjoy_plugin(source, overwrite_config=None):
    """Parse ImJoy plugin file and return a dict with all the fields."""
    root = etree.HTML("<html>" + source + "</html>")
    plugin_comp = dotdict()
    for tag_type in tag_types:
        elms = root.xpath(f".//{tag_type}")
        values = []
        for elm in elms:
            values.append(
                dotdict(
                    attrs=dotdict(elm.attrib),
                    content=elm.text,
                )
            )
        plugin_comp[tag_type] = values
    if plugin_comp.config[0].attrs.lang == "yaml":
        config = yaml.safe_load(plugin_comp.config[0].content)
    elif plugin_comp.config[0].attrs.lang == "json":
        config = json.loads(plugin_comp.config[0].content)
    else:
        raise Exception(
            "Unsupported config language: " + plugin_comp.config[0].attrs.lang
        )

    overwrite_config = overwrite_config or {}
    config["tag"] = overwrite_config.get("tag") or (
        config.get("tags") and config.get("tags")[0]
    )
    config["hot_reloading"] = overwrite_config.get("hot_reloading")
    config["scripts"] = []
    # try to match the script with current tag
    for elm in plugin_comp.script:
        if elm.attrs.tag == config["tag"]:
            config["script"] = elm.content
        # exclude script with mismatched tag
        if not elm.attrs.tag or elm.attrs.tag == config["tag"]:
            config["scripts"].append(elm)
    if not config.get("script") and len(plugin_comp.script) > 0:
        config["script"] = plugin_comp.script[0].content
        config["lang"] = plugin_comp.script[0].attrs.lang
    config["links"] = plugin_comp.link or None
    config["windows"] = plugin_comp.window or None
    config["styles"] = plugin_comp.style or None
    config["docs"] = plugin_comp.docs[0] if plugin_comp.docs else config.get("docs")
    config["attachments"] = plugin_comp.attachment or None

    config["_id"] = overwrite_config.get("_id") or config.get("name").replace(" ", "_")
    config["uri"] = overwrite_config.get("uri")
    config["origin"] = overwrite_config.get("origin")
    config["namespace"] = overwrite_config.get("namespace")
    config["code"] = source
    config["id"] = (
        config.get("name").strip().replace(" ", "_") + "_" + str(uuid.uuid4())
    )
    config["runnable"] = config.get("runnable", True)
    config["requirements"] = config.get("requirements") or []

    for field in CONFIGURABLE_FIELDS:
        obj = config.get(field)
        if obj and isinstance(obj, dict) and not isinstance(obj, list):
            if config.get("tag"):
                config[field] = obj.get(config.get("tag"))
                if not obj.get(config.get("tag")):
                    print(
                        "WARNING: "
                        + field
                        + " do not contain a tag named: "
                        + config.get("tag")
                    )
            else:
                raise Exception("You must use 'tags' with configurable fields.")
    config["lang"] = config.get("lang") or "javascript"
    return config
