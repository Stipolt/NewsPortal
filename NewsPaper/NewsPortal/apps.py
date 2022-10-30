from django.apps import AppConfig


class NewsportalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NewsPortal'

    def ready(self):
        import NewsPortal.signals

        # # from .tasks import def ...
        # from .scheduler import post_scheduler
        #
        # post_scheduler.add_job(
        #     id='post_bla_bla',
        #     func=...,
        #     trigger='interval',
        #     week=1,
        # )
        # post_scheduler.start()

