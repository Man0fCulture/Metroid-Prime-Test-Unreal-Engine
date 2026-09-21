import unreal


def safe(obj, prop):
    try:
        return obj.get_editor_property(prop)
    except Exception as exc:
        return f"<ERROR {type(exc).__name__}: {exc}>"


asset_path = "/Game/Widget/WBP_MainMenu.WBP_MainMenu"
asset = unreal.load_asset(asset_path)
print("CODEX_ASSET", asset, asset.get_class().get_name() if asset else None)

if asset:
    print("CODEX_ASSET_DIR", [name for name in dir(asset) if any(term in name.lower() for term in ("anim", "widget", "graph", "generat", "class"))])
    print("CODEX_BP_LIB_DIR", [name for name in dir(unreal.BlueprintEditorLibrary) if any(term in name.lower() for term in ("graph", "node", "blueprint"))])
    print("CODEX_CLASS_DIR", [name for name in dir(asset.get_class()) if any(term in name.lower() for term in ("prop", "field", "function", "class"))])
    try:
        generated_class = asset.generated_class()
        print("CODEX_GENERATED_CLASS_METHOD", generated_class)
        cdo = unreal.get_default_object(generated_class)
        print("CODEX_CDO", cdo)
        print("CODEX_CDO_DIR", [name for name in dir(cdo) if any(term in name.lower() for term in ("anim", "selector", "border"))])
    except Exception as exc:
        print("CODEX_GENERATED_CLASS_ERROR", type(exc).__name__, exc)

    for prop in ("animations", "widget_tree", "ubergraph_pages", "function_graphs", "generated_class"):
        value = safe(asset, prop)
        print("CODEX_PROPERTY", prop, value)

    animations = safe(asset, "animations")
    if isinstance(animations, (list, tuple)):
        print("CODEX_ANIMATION_COUNT", len(animations))
        for animation in animations:
            print("CODEX_ANIMATION", animation.get_name(), animation.get_path_name())
            movie_scene = safe(animation, "movie_scene")
            print("CODEX_MOVIE_SCENE", movie_scene)
            try:
                bindings = unreal.MovieSceneSequenceExtensions.get_bindings(animation)
                print("CODEX_BINDING_COUNT", len(bindings))
                for binding in bindings:
                    print("CODEX_BINDING", binding.get_display_name(), binding.get_id())
                    for track in binding.get_tracks():
                        print("CODEX_TRACK", track.get_name(), track.get_class().get_name(), safe(track, "display_name"))
                        for section in track.get_sections():
                            print("CODEX_SECTION", section.get_name(), section.get_class().get_name())
                            try:
                                for channel in section.get_channels():
                                    print("CODEX_CHANNEL", channel.get_name(), channel.get_class().get_name(), len(channel.get_keys()))
                            except Exception as exc:
                                print("CODEX_CHANNEL_ERROR", exc)
            except Exception as exc:
                print("CODEX_BINDING_ERROR", type(exc).__name__, exc)

    tree = safe(asset, "widget_tree")
    if not isinstance(tree, str):
        try:
            widgets = tree.get_all_widgets()
            print("CODEX_WIDGET_COUNT", len(widgets))
            for widget in widgets:
                if "Selector" in widget.get_name() or "Border" in widget.get_name():
                    print(
                        "CODEX_WIDGET",
                        widget.get_name(),
                        widget.get_class().get_name(),
                        "visibility=", safe(widget, "visibility"),
                        "render_opacity=", safe(widget, "render_opacity"),
                    )
        except Exception as exc:
            print("CODEX_WIDGET_ERROR", type(exc).__name__, exc)

    graphs = safe(asset, "ubergraph_pages")
    if isinstance(graphs, (list, tuple)):
        for graph in graphs:
            print("CODEX_GRAPH", graph.get_name())
            nodes = safe(graph, "nodes")
            if isinstance(nodes, (list, tuple)):
                for node in nodes:
                    label = ""
                    try:
                        label = node.get_node_title(unreal.NodeTitleType.LIST_VIEW)
                    except Exception:
                        pass
                    node_text = f"{node.get_name()} {node.get_class().get_name()} {label}"
                    if any(term.lower() in node_text.lower() for term in ("animation", "construct", "selector", "play")):
                        print("CODEX_NODE", node_text)

print("CODEX_DONE")
