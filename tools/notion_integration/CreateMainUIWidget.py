import unreal

widget_name = "WBP_MainUI"
widget_path = "/Game/UI/" + widget_name

if unreal.EditorAssetLibrary.does_asset_exist(widget_path):
    print(f"{widget_name} 已存在: {widget_path}")
    widget = unreal.EditorAssetLibrary.load_asset(widget_path)
else:
    # 创建Widget蓝图并设置父类
    widget_factory = unreal.WidgetBlueprintFactory()
    widget_factory.set_editor_property("ParentClass", unreal.UserWidget)
    widget = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name=widget_name,
        package_path="/Game/UI",
        asset_class=unreal.WidgetBlueprint,
        factory=widget_factory
    )
    print(f"已创建Widget蓝图: {widget_path}")

# 可选：提示用户后续在编辑器内自行添加控件和布局
print("主界面Widget蓝图已创建。请在编辑器中打开并添加UI控件（如血条、技能栏等）进行布局和美化。")