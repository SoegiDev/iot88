from waitress import serve
import test_auth
serve(test_auth.app, host='0.0.0.0', port=8080)