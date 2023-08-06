import rlogging
from rocshelf.compile import meta, params, routes, tracebacks, utils, controller

logger = rlogging.get_logger('mainLogger')


@tracebacks.stage_run
def run():
    """ Полная компиляция исходников опираясь на конфигурацию приложения """

    logger.info('Запуск компиляции')

    utils.statistics.start_point()

    utils.backuping_last_compilation()
    utils.delete_dist()

    routes.run()
    meta.run()

    utils.statistics.end_point()
    utils.statistics.print()
