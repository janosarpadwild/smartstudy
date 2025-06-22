from django.core.management.commands.runserver import Command as RunserverCommand
from werkzeug.serving import run_simple
from werkzeug.middleware.proxy_fix import ProxyFix
from django.core.wsgi import get_wsgi_application

class Command(RunserverCommand):
    help = 'Run the development server with Werkzeug and keep-alive settings'

    def handle(self, *args, **options):
        application = ProxyFix(get_wsgi_application())
        
        # Set default values for missing options
        use_reloader = options.get('use_reloader', False)
        use_debugger = options.get('use_debugger', False)
        port = options.get('port', 8000)
        self.keep_alive_timeout = 10
        
        run_simple(
            hostname='localhost',
            port=int(port),
            application=application,
            use_reloader=use_reloader,
            use_debugger=use_debugger,
            ssl_context=('certificate/localhost.crt', 'certificate/localhost.key'),
            threaded=True  # Enables threading for multiple concurrent connections
        )
