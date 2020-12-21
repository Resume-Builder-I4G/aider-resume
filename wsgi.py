from app import create_app
from config import Config

app = application = create_app(Config)

@application.route('/api/vi/')
def home():
    return ''

if __name__ == "__main__":
    application.run()
