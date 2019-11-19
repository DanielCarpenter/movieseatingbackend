from modules import app, db
from flask import url_for, redirect, request, abort
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from modules.movies import Movie, Genre, Actor
from modules.accounts import User, Role


from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import helpers as admin_helpers

#Flask Admin
admin = Admin(app, name='movielog', base_template='my_master.html', template_mode='bootstrap3')

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

#custom modelview for Flask-Security
class AppModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
        )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


#admin views
secure = True #use to switch between secure view and unsecure view if developing

if (secure):
    admin.add_view(AppModelView(Movie, db.session))
    admin.add_view(AppModelView(Genre, db.session))
    admin.add_view(AppModelView(Actor, db.session))
    admin.add_view(AppModelView(User, db.session))
    admin.add_view(AppModelView(Role, db.session))
else:
    admin.add_view(ModelView(Movie, db.session))
    admin.add_view(ModelView(Genre, db.session))
    admin.add_view(ModelView(Actor, db.session))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Role, db.session))