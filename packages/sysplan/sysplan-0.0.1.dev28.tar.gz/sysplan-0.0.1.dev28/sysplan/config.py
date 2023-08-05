import importlib_metadata
import os
import yaml


SYSPLAN_ROOT = os.getenv('SYSPLAN_ROOT', '/')
SYSPLAN_D = os.getenv('SYSPLAN_D', '/etc/sysplan.d')


class Config(dict):
    plugins = {
        ep.name: ep
        for ep in importlib_metadata.entry_points(group='sysplan_plans')
    }

    @classmethod
    def factory(cls, root):
        for root, dirs, files in os.walk(root):
            for filename in files:
                if not filename.endswith('.yaml'):
                    continue
                target_file = os.path.join(root, filename)
                with open(target_file, 'r') as f:
                    content = f.read()
                    for document in content.split('---'):
                        yield cls(yaml.safe_load(document))

    def plans(self, root, *names):
        for plugin_name, plans in self.items():
            plugin = None
            if plugin_name in self.plugins:
                plugin = self.plugins[plugin_name].load()
            elif plugin_name.endswith('.sh'):
                path = os.path.join(SYSPLAN_D, plugin_name)
                if os.path.exists(path):
                    from sysplan.bash import BashPlan
                    plugin = type(
                        plugin_name.capitalize(),
                        (BashPlan,),
                        dict(path=path),
                    )

            if not plugin:
                if not os.getenv('CI'):
                    print('Skipping ' + plugin_name)
                continue

            plugin_config = self.get(plugin_name, {})
            if not plugin_config:
                continue

            for name, data in plugin_config.items():
                if names and name not in names:
                    continue
                yield from plugin(root, self, name, data or {}).plans()
