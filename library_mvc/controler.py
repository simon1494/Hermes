import template
import model

if input("aber: ") == "ok":
    model.create_db()
    template.app()
