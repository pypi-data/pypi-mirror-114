from extras.plugins import PluginConfig

class UNMSConfig(PluginConfig):
    name = 'netbox_plugin_unms'
    verbose_name = 'Netbox Plugin UNMS'
    description = 'UNMS Data importer'
    version = '0.1'
    author = 'Schylar Utley'
    author_email = 'schylarutley@hotmail.com'
    base_url = 'unms'
    required_settings = []
    default_settings = {
        'loud': False
    }

config = UNMSConfig
