from app.routes.utils import *
from app.routes.interactive import *
from app.routes.account import *
from app.routes.wiki import *


@app.route('/')
def index():
    return render_template('index.html')
