import logging

from sqlalchemy import event
from sqlalchemy.orm import Session

logger = logging.getLogger("SQLAlchemyLogging")


def before_request_log(model, user_id, method, raw_id):
    logger.info(
        f"User with id={user_id} has started {method} model {model} (raw ID={raw_id})"
    )


def after_request_log(model, user_id, method, raw_id):
    logger.info(
        f"User with id={user_id} has finished {method} model {model} (raw ID={raw_id})"
    )


def before_rollback_log(model, user_id, method, raw_id):
    logger.info(
        f"Before rollback user with id={user_id} has started {method} model {model} (raw ID={raw_id})"
    )


def check_owner(instance):
    try:
        owner_id = instance.add_by_user
    except:
        owner_id = None
    return owner_id


def get_session_info(session):
    sessions_info = {}
    session_instances = []
    methods = []
    counter = 0
    for instance in session.new:
        methods.append("creating")
        session_instances.append(instance)
        counter += 1
    for instance in session.deleted:
        methods.append("deleting")
        session_instances.append(instance)
        counter += 1
    for instance in session.dirty:
        methods.append("updating")
        session_instances.append(instance)
        counter += 1
    instance_method = list(zip(session_instances, methods))
    for i, instance in enumerate(instance_method):
        session_info = {}
        owner_id = check_owner(instance[0])
        session_info["user_id"] = owner_id
        session_info["method"] = instance[1]
        session_info["model"] = instance[0].__tablename__
        session_info["raw_id"] = instance[0].id
        sessions_info[i] = session_info
    return sessions_info


class Logger:
    def session_before_flush(self, session, flush_context, instanses):
        session_info = get_session_info(session)
        for instance in session_info.values():
            before_request_log(
                instance["model"],
                instance["user_id"],
                instance["method"],
                instance["raw_id"],
            )

    def listen_before_flush(self):
        event.listen(Session, "before_flush", self.session_before_flush)

    def session_after_flush(self, session, flush_context):
        session_info = get_session_info(session)
        for instance in session_info.values():
            after_request_log(
                instance["model"],
                instance["user_id"],
                instance["method"],
                instance["raw_id"],
            )

    def listen_after_flush(self):
        event.listen(Session, "after_flush", self.session_after_flush)

    def session_after_rollback(self, session):
        session_info = get_session_info(session)
        for instance in session_info.values():
            before_rollback_log(
                instance["model"],
                instance["user_id"],
                instance["method"],
                instance["raw_id"],
            )

    def listen_after_rollback(self):
        event.listen(Session, "after_rollback", self.session_after_rollback)
