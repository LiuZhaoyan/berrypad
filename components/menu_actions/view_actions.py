from core.component_basic import MenuActionComponent


class ToggleRenderModeAction(MenuActionComponent):
    def execute(self):
        """切换渲染模式"""
        self.manager.publish("view.toggle_render_mode")