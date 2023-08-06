from __future__ import absolute_import, print_function, unicode_literals

from le_utils.constants import format_presets

from madrassati.core.content import hooks as content_hooks
from madrassati.plugins import MadrassatiPluginBase
from madrassati.plugins.hooks import register_hook


class ExercisePerseusRenderPlugin(MadrassatiPluginBase):
    pass


@register_hook
class ExercisePerseusRenderAsset(content_hooks.ContentRendererHook):
    bundle_id = "main"
    presets = (format_presets.EXERCISE,)
