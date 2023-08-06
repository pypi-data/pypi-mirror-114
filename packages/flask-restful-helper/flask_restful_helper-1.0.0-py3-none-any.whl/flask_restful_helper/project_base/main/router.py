
def registry_router(app):
    """
    新增一個app的時候要手動加入該app的blueprint

       Example:     
            from apps.account.router import blueprint as account_blueprint
            app.register_blueprint(account_blueprint)

    """
