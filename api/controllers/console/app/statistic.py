from datetime import datetime
from decimal import Decimal

import pytz
from flask import jsonify
from flask import current_app, jsonify
from flask_restful import Resource, reqparse
from extensions.ext_database import db
from libs.helper import DatetimeString
from datetime import datetime
import pytz
import traceback
from flask_login import current_user
from flask_restful import Resource, reqparse

from controllers.console import api
from controllers.console.app.wraps import get_app_model
from controllers.console.setup import setup_required
from controllers.console.wraps import account_initialization_required
from extensions.ext_database import db
from libs.helper import DatetimeString
from libs.login import login_required
from models.model import AppMode


class DailyMessageStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    DATE(DATE_TRUNC('day', created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    COUNT(*) AS message_count
FROM
    messages
WHERE
    app_id = :app_id"""
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append({"date": str(i.date), "message_count": i.message_count})

        return jsonify({"data": response_data})


class DailyConversationStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    DATE(DATE_TRUNC('day', created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    COUNT(DISTINCT messages.conversation_id) AS conversation_count
FROM
    messages
WHERE
    app_id = :app_id"""
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append({"date": str(i.date), "conversation_count": i.conversation_count})

        return jsonify({"data": response_data})


class DailyTerminalsStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    DATE(DATE_TRUNC('day', created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    COUNT(DISTINCT messages.from_end_user_id) AS terminal_count
FROM
    messages
WHERE
    app_id = :app_id"""
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append({"date": str(i.date), "terminal_count": i.terminal_count})

        return jsonify({"data": response_data})


class DailyTokenCostStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    DATE(DATE_TRUNC('day', created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    (SUM(messages.message_tokens) + SUM(messages.answer_tokens)) AS token_count,
    SUM(total_price) AS total_price
FROM
    messages
WHERE
    app_id = :app_id"""
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append(
                    {"date": str(i.date), "token_count": i.token_count, "total_price": i.total_price, "currency": "USD"}
                )

        return jsonify({"data": response_data})


class AverageSessionInteractionStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model(mode=[AppMode.CHAT, AppMode.AGENT_CHAT, AppMode.ADVANCED_CHAT])
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    DATE(DATE_TRUNC('day', c.created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    AVG(subquery.message_count) AS interactions
FROM
    (
        SELECT
            m.conversation_id,
            COUNT(m.id) AS message_count
        FROM
            conversations c
        JOIN
            messages m
            ON c.id = m.conversation_id
        WHERE
            c.override_model_configs IS NULL
            AND c.app_id = :app_id"""
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND c.created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND c.created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += """
        GROUP BY m.conversation_id
    ) subquery
LEFT JOIN
    conversations c
    ON c.id = subquery.conversation_id
GROUP BY
    date
ORDER BY
    date"""

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append(
                    {"date": str(i.date), "interactions": float(i.interactions.quantize(Decimal("0.01")))}
                )

        return jsonify({"data": response_data})


class UserSatisfactionRateStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    DATE(DATE_TRUNC('day', m.created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    COUNT(m.id) AS message_count,
    COUNT(mf.id) AS feedback_count
FROM
    messages m
LEFT JOIN
    message_feedbacks mf
    ON mf.message_id=m.id AND mf.rating='like'
WHERE
    m.app_id = :app_id"""
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append(
                    {
                        "date": str(i.date),
                        "rate": round((i.feedback_count * 1000 / i.message_count) if i.message_count > 0 else 0, 2),
                    }
                )

        return jsonify({"data": response_data})


class AverageResponseTimeStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model(mode=AppMode.COMPLETION)
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    DATE(DATE_TRUNC('day', created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    AVG(provider_response_latency) AS latency
FROM
    messages
WHERE
    app_id = :app_id"""
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append({"date": str(i.date), "latency": round(i.latency * 1000, 4)})

        return jsonify({"data": response_data})


class TokensPerSecondStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @get_app_model
    def get(self, app_model):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    DATE(DATE_TRUNC('day', created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    CASE
        WHEN SUM(provider_response_latency) = 0 THEN 0
        ELSE (SUM(answer_tokens) / SUM(provider_response_latency))
    END as tokens_per_second
FROM
    messages
WHERE
    app_id = :app_id"""
        arg_dict = {"tz": account.timezone, "app_id": app_model.id}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY date ORDER BY date"

        response_data = []

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for i in rs:
                response_data.append({"date": str(i.date), "tps": round(i.tokens_per_second, 4)})

        return jsonify({"data": response_data})

class AllAppsDailyMessageStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def get(self):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    a.id AS app_id,
    a.name AS app_name,
    DATE(DATE_TRUNC('day', m.created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    COUNT(*) AS message_count
FROM
    apps a
LEFT JOIN
    messages m ON a.id = m.app_id
WHERE 1=1"""
        arg_dict = {"tz": account.timezone}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY a.id, a.name, date ORDER BY a.id, date"

        response_data = {}

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for row in rs:
                app_id = str(row.app_id)
                if app_id not in response_data:
                    response_data[app_id] = {
                        "app_name": row.app_name,
                        "daily_messages": []
                    }
                response_data[app_id]["daily_messages"].append({
                    "date": str(row.date),
                    "message_count": row.message_count
                })

        return jsonify({"data": response_data})

class AllAppsDailyConversationStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def get(self):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    a.id AS app_id,
    a.name AS app_name,
    DATE(DATE_TRUNC('day', m.created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    COUNT(DISTINCT m.conversation_id) AS conversation_count
FROM
    apps a
LEFT JOIN
    messages m ON a.id = m.app_id
WHERE 1=1"""
        arg_dict = {"tz": account.timezone}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY a.id, a.name, date ORDER BY a.id, date"

        response_data = {}

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for row in rs:
                app_id = str(row.app_id)
                if app_id not in response_data:
                    response_data[app_id] = {
                        "app_name": row.app_name,
                        "daily_conversations": []
                    }
                response_data[app_id]["daily_conversations"].append({
                    "date": str(row.date),
                    "conversation_count": row.conversation_count
                })

        return jsonify({"data": response_data})

class AllAppsDailyTerminalsStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def get(self):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    a.id AS app_id,
    a.name AS app_name,
    DATE(DATE_TRUNC('day', m.created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    COUNT(DISTINCT m.from_end_user_id) AS terminal_count
FROM
    apps a
LEFT JOIN
    messages m ON a.id = m.app_id
WHERE 1=1"""
        arg_dict = {"tz": account.timezone}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY a.id, a.name, date ORDER BY a.id, date"

        response_data = {}

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for row in rs:
                app_id = str(row.app_id)
                if app_id not in response_data:
                    response_data[app_id] = {
                        "app_name": row.app_name,
                        "daily_terminals": []
                    }
                response_data[app_id]["daily_terminals"].append({
                    "date": str(row.date),
                    "terminal_count": row.terminal_count
                })

        return jsonify({"data": response_data})

class AllAppsDailyTokenCostStatistic(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def get(self):
        account = current_user

        parser = reqparse.RequestParser()
        parser.add_argument("start", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        parser.add_argument("end", type=DatetimeString("%Y-%m-%d %H:%M"), location="args")
        args = parser.parse_args()

        sql_query = """SELECT
    a.id AS app_id,
    a.name AS app_name,
    DATE(DATE_TRUNC('day', m.created_at AT TIME ZONE 'UTC' AT TIME ZONE :tz )) AS date,
    SUM(m.message_tokens + m.answer_tokens) AS token_count,
    SUM(m.total_price) AS total_price
FROM
    apps a
LEFT JOIN
    messages m ON a.id = m.app_id
WHERE 1=1"""
        arg_dict = {"tz": account.timezone}

        timezone = pytz.timezone(account.timezone)
        utc_timezone = pytz.utc

        if args["start"]:
            start_datetime = datetime.strptime(args["start"], "%Y-%m-%d %H:%M")
            start_datetime = start_datetime.replace(second=0)

            start_datetime_timezone = timezone.localize(start_datetime)
            start_datetime_utc = start_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at >= :start"
            arg_dict["start"] = start_datetime_utc

        if args["end"]:
            end_datetime = datetime.strptime(args["end"], "%Y-%m-%d %H:%M")
            end_datetime = end_datetime.replace(second=0)

            end_datetime_timezone = timezone.localize(end_datetime)
            end_datetime_utc = end_datetime_timezone.astimezone(utc_timezone)

            sql_query += " AND m.created_at < :end"
            arg_dict["end"] = end_datetime_utc

        sql_query += " GROUP BY a.id, a.name, date ORDER BY a.id, date"

        response_data = {}

        with db.engine.begin() as conn:
            rs = conn.execute(db.text(sql_query), arg_dict)
            for row in rs:
                app_id = str(row.app_id)
                if app_id not in response_data:
                    response_data[app_id] = {
                        "app_name": row.app_name,
                        "daily_token_costs": []
                    }
                response_data[app_id]["daily_token_costs"].append({
                    "date": str(row.date),
                    "token_count": row.token_count,
                    "total_price": float(row.total_price),
                    "currency": "USD"
                })

        return jsonify({"data": response_data})

api.add_resource(AllAppsDailyTokenCostStatistic, "/apps/statistics/all-apps/all-daily-token-costs", endpoint='all_apps_daily_token_costs')
api.add_resource(AllAppsDailyTerminalsStatistic, "/apps/statistics/all-apps/all-daily-end-users", endpoint='all_apps_daily_end_users')
api.add_resource(AllAppsDailyConversationStatistic, "/apps/statistics/all-apps/all-daily-conversations", endpoint='all_apps_daily_conversations')
api.add_resource(AllAppsDailyMessageStatistic, "/apps/statistics/all-apps/all-daily-messages", endpoint='all_apps_daily_messages')

api.add_resource(DailyMessageStatistic, "/apps/<uuid:app_id>/statistics/daily-messages", endpoint='daily_messages')
api.add_resource(DailyConversationStatistic, "/apps/<uuid:app_id>/statistics/daily-conversations", endpoint='daily_conversations')
api.add_resource(DailyTerminalsStatistic, "/apps/<uuid:app_id>/statistics/daily-end-users", endpoint='daily_end_users')
api.add_resource(DailyTokenCostStatistic, "/apps/<uuid:app_id>/statistics/token-costs", endpoint='token_costs')
api.add_resource(AverageSessionInteractionStatistic, "/apps/<uuid:app_id>/statistics/average-session-interactions", endpoint='average_session_interactions')
api.add_resource(UserSatisfactionRateStatistic, "/apps/<uuid:app_id>/statistics/user-satisfaction-rate", endpoint='user_satisfaction_rate')
api.add_resource(AverageResponseTimeStatistic, "/apps/<uuid:app_id>/statistics/average-response-time", endpoint='average_response_time')
api.add_resource(TokensPerSecondStatistic, "/apps/<uuid:app_id>/statistics/tokens-per-second", endpoint='tokens_per_second')