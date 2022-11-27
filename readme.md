to host database at your local disc type in terminal:
>>> from app import app, db
> 
>>> app.app_context().push()
> 
>>> db.create_all()
