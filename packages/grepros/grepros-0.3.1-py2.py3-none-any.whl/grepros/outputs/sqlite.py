# -*- coding: utf-8 -*-
"""
SQLite output for search results.

------------------------------------------------------------------------------
This file is part of grepros - grep for ROS bag files and live topics.
Released under the BSD License.

@author      Erki Suurjaak
@created     03.12.2021
@modified    05.12.2021
------------------------------------------------------------------------------
"""
## @namespace grepros.outputs.sqlite
import atexit
import collections
import json
import os
import re
import sqlite3

from .. common import ConsolePrinter, format_bytes, plural, quote
from .. import rosapi
from . base import SinkBase, TextSinkMixin


class SqliteSink(SinkBase, TextSinkMixin):
    """
    Writes messages to an SQLite database.

    Output will have:
    - table "messages", with all messages as YAML and serialized binary
    - table "types", with message definitions
    - table "topics", with topic information

    plus:
    - table "pkg/MsgType" for each message type, with detailed fields,
      and array fields to linking to subtypes
    - view "/topic/full/name" for each topic,
      selecting from the message type table

    """

    ## Auto-detection file extensions
    FILE_EXTENSIONS = (".sqlite", ".sqlite3")

    ## SQL statements for populating database base schema
    BASE_SCHEMA = """
    CREATE TABLE IF NOT EXISTS messages (
      id           INTEGER   PRIMARY KEY,
      dt           TIMESTAMP NOT NULL,
      topic        TEXT      NOT NULL,
      type         TEXT      NOT NULL,
      yaml         TEXT      NOT NULL,
      data         BLOB      NOT NULL,
      topic_id     INTEGER   NOT NULL,
      timestamp    INTEGER   NOT NULL
    );

    CREATE TABLE IF NOT EXISTS types (
      id         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      type       TEXT    NOT NULL,
      definition TEXT    NOT NULL,
      subtypes   JSON
    );

    CREATE TABLE IF NOT EXISTS topics (
      id                   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      name                 TEXT    NOT NULL,
      type                 TEXT    NOT NULL,
      count                INTEGER NOT NULL DEFAULT 0,
      dt_first             TIMESTAMP,
      dt_last              TIMESTAMP,
      timestamp_first      INTEGER,
      timestamp_last       INTEGER,
      serialization_format TEXT DEFAULT "cdr",
      offered_qos_profiles TEXT DEFAULT ""
    );
    """

    ## SQL statement for inserting messages
    INSERT_MESSAGE = """
    INSERT INTO messages (dt, topic, type, yaml, data, topic_id, timestamp)
    VALUES (:dt, :topic, :type, :yaml, :data, :topic_id, :timestamp)
    """

    ## SQL statement for inserting topics
    INSERT_TOPIC = "INSERT INTO topics (name, type) VALUES (:name, :type)"

    ## SQL statement for updating topics with latest message
    UPDATE_TOPIC = """
    UPDATE topics SET count = count + 1,
    dt_first = MIN(COALESCE(dt_first, :dt), :dt),
    dt_last  = MAX(COALESCE(dt_last,  :dt), :dt),
    timestamp_first = MIN(COALESCE(timestamp_first, :timestamp), :timestamp),
    timestamp_last  = MAX(COALESCE(timestamp_last,  :timestamp), :timestamp)
    WHERE name = :name AND type = :type
    """

    ## SQL statement for inserting types
    INSERT_TYPE = """
    INSERT INTO types (type, definition, subtypes)
    VALUES (:type, :definition, :subtypes)
    """

    ## SQL statement for creating a view for topic
    CREATE_TOPIC_VIEW = """
    CREATE VIEW %(name)s AS
    SELECT %(cols)s
    FROM %(type)s
    WHERE _topic = %(topic)s
    """

    ## SQL statement template for inserting message types
    INSERT_MESSAGE_TYPE = """
    INSERT INTO %(type)s (_topic, _dt, _timestamp, _parent_type, _parent_id%(cols)s)
    VALUES (:_topic, :_dt, :_timestamp, :_parent_type, :_parent_id%(vals)s)
    """

    ## Default columns for pkg/MsgType tables
    MESSAGE_TYPE_BASECOLS = [("_topic",       "TEXT"),
                             ("_dt",          "TIMESTAMP"),
                             ("_timestamp",   "INTEGER"),
                             ("_id",          "INTEGER NOT NULL "
                                              "PRIMARY KEY AUTOINCREMENT"),
                             ("_parent_type", "TEXT"),
                             ("_parent_id",   "INTEGER"), ]


    def __init__(self, args):
        """
        @param   args               arguments object like argparse.Namespace
        @param   args.META          whether to print metainfo
        @param   args.DUMP_TARGET   name of SQLite file to write,
                                    will be appended to if exists
        @param   args.WRAP_WIDTH    character width to wrap message YAML output at
        @param   args.VERBOSE       whether to print debug information
        """
        args = TextSinkMixin.make_full_yaml_args(args)

        super(SqliteSink, self).__init__(args)
        TextSinkMixin.__init__(self, args)

        self._filename      = args.DUMP_TARGET
        self._db            = None   # sqlite3.Connection
        self._close_printed = False

        self._topics = {}  # {(topic, typename): {topics-row}}
        self._types  = {}  # {typename: {types-row}}
        # {"view": {topic: {typename: True}}, "table": {typename: {cols}}}
        self._schema = collections.defaultdict(dict)

        self._format_repls.update({k: "" for k in self._format_repls})
        atexit.register(self.close)


    def emit(self, topic, index, stamp, msg, match):
        """Writes message to output file."""
        if not self._db:
            self._init_db()
        typename = rosapi.get_message_type(msg)
        self._process_topic(topic, typename, msg)
        self._process_message(topic, typename, msg, stamp)
        super(SqliteSink, self).emit(topic, index, stamp, msg, match)


    def close(self):
        """Closes output file, if any."""
        if self._db:
            self._db.close()
            self._db = None
        if not self._close_printed and self._counts:
            self._close_printed = True
            ConsolePrinter.debug("Wrote %s in %s to %s (%s).",
                                 plural("message", sum(self._counts.values())),
                                 plural("topic", len(self._counts)), self._filename,
                                 format_bytes(os.path.getsize(self._filename)))



    def _init_db(self):
        """Opens the database file and populates schema if not already existing."""
        for t in (dict, list, tuple): sqlite3.register_adapter(t, json.dumps)
        if self._args.VERBOSE:
            sz = os.path.exists(self._filename) and os.path.getsize(self._filename)
            ConsolePrinter.debug("%s %s%s.", "Adding to" if sz else "Creating", self._filename,
                                 (" (%s)" % format_bytes(sz)) if sz else "")
        self._db = sqlite3.connect(self._filename, isolation_level=None, check_same_thread=False)
        self._db.row_factory = lambda cursor, row: dict(sqlite3.Row(cursor, row))
        self._db.executescript(self.BASE_SCHEMA)
        for row in self._db.execute("SELECT * FROM topics"):
            topickey = (row["name"], row["type"])
            self._topics[topickey] = row
        for row in self._db.execute("SELECT * FROM types"):
            self._types[row["type"]] = row
        for row in self._db.execute("SELECT name FROM sqlite_master "
                                    "WHERE type = 'table' AND name LIKE '%/%'"):
            cols = self._db.execute("PRAGMA table_info(%s)" % quote(row["name"])).fetchall()
            cols = [c for c in cols if not c["name"].startswith("_")]
            self._schema["table"][row["name"]] = {c["name"]: c for c in cols}
        for row in self._db.execute("SELECT sql FROM sqlite_master "
                                    "WHERE type = 'view' AND name LIKE '%/%'"):
            try:
                topic = re.search(r'WHERE _topic = "([^"]+)"', row["sql"]).group(1)
                typename = re.search(r'FROM "([^"]+)"', row["sql"]).group(1)
                self._schema["view"].setdefault(topic, {})[typename] = True
            except Exception as e:
                ConsolePrinter.error("Error parsing view %s: %s.", row, e)


    def _process_topic(self, topic, typename, msg):
        """Inserts topic and message rows and tables and views if not already existing."""
        topickey = (topic, typename)
        if topickey not in self._topics:
            targs = dict(name=topic, type=typename)
            targs["id"] = self._db.execute(self.INSERT_TOPIC, targs).lastrowid
            self._topics[topickey] = targs

        self._process_type(typename, msg)

        if topic not in self._schema["view"] or typename not in self._schema["view"][topic]:
            cols = list(self._schema["table"][typename]) + ["_dt", "_id"]
            fargs = dict(topic=quote(topic), cols=", ".join(map(quote, cols)), type=quote(typename))
            suffix = " (%s)" % typename if topic in self._schema["view"] else ""
            fargs["name"] = quote(topic + suffix)
            sql = self.CREATE_TOPIC_VIEW % fargs
            if self._args.VERBOSE:
                ConsolePrinter.debug("Adding topic %s.", topic)
            self._db.execute(sql)
            self._schema["view"].setdefault(topic, {})[typename] = True


    def _process_type(self, typename, msg):
        """Inserts type rows and creates pkg/MsgType tables if not already existing."""
        if typename not in self._types:
            msgdef = self.source.get_message_definition(typename)
            targs = dict(type=typename, definition=msgdef, subtypes={})
            self._types[typename] = targs
            for path, submsgs, subtype in self._iter_fields(msg, messages_only=True):
                subtype = rosapi.scalar(subtype)
                targs["subtypes"][".".join(path)] = subtype

                if not isinstance(submsgs, (list, tuple)): submsgs = [submsgs]
                elif not submsgs: submsgs = [rosapi.get_message_class(subtype)()]
                for submsg in submsgs:
                    submsg = submsg or self.source.get_message_class(subtype)()  # List may be empty
                    self._process_type(subtype, submsg)

            targs["id"] = self._db.execute(self.INSERT_TYPE, targs).lastrowid

        if typename not in self._schema["table"]:
            cols = []
            for path, value, subtype in self._iter_fields(msg):
                suffix = "[]" if isinstance(value, (list, tuple)) else ""
                cols += [(".".join(path), quote(rosapi.scalar(subtype) + suffix))]
            coldefs = ["%s %s" % (quote(n), t) for n, t in cols + self.MESSAGE_TYPE_BASECOLS]
            sql = "CREATE TABLE %s (%s)" % (quote(typename), ", ".join(coldefs))
            self._schema["table"][typename] = collections.OrderedDict(cols)
            self._db.execute(sql)


    def _process_message(self, topic, typename, msg, stamp):
        """Inserts message to messages-table, and to pkg/MsgType tables."""
        topic_id = self._topics[(topic, typename)]["id"]
        margs = dict(dt=rosapi.to_datetime(stamp), timestamp=rosapi.to_nsec(stamp),
                     topic=topic, name=topic, topic_id=topic_id, type=typename,
                     yaml=self.format_message(msg), data=rosapi.get_message_data(msg))
        self._db.execute(self.INSERT_MESSAGE, margs)
        self._db.execute(self.UPDATE_TOPIC,   margs)
        self._populate_type(topic, typename, msg, stamp)


    def _populate_type(self, topic, typename, msg, stamp, parent_type=None, parent_id=None):
        """
        Inserts pkg/MsgType row for this message, and sub-rows for subtypes in message.

        Returns inserted ID.
        """
        args = dict(_topic=topic, _dt=rosapi.to_datetime(stamp),
                    _timestamp=rosapi.to_nsec(stamp),
                    _parent_type=parent_type, _parent_id=parent_id)
        cols, vals = [], []
        for p, v, t in self._iter_fields(msg):
            if isinstance(v, (list, tuple)) and rosapi.scalar(t) not in rosapi.ROS_BUILTIN_TYPES:
                continue  # for p, v, t
            cols += [".".join(p)]
            vals += [re.sub(r"\W", "_", cols[-1])]
            args[vals[-1]] = v
        inter = ", " if cols else ""
        fargs = dict(type=quote(typename), cols=inter + ", ".join(map(quote, cols)),
                     vals=inter + ", ".join(":" + c for c in vals))
        sql = self.INSERT_MESSAGE_TYPE % fargs
        myid = args["_id"] = self._db.execute(sql, args).lastrowid

        subids = {}  # {path: [ids]}
        for subpath, submsgs, subtype in self._iter_fields(msg, messages_only=True):
            subtype = rosapi.scalar(subtype)
            if isinstance(submsgs, (list, tuple)):
                subids[subpath] = []
            for submsg in submsgs if isinstance(submsgs, (list, tuple)) else [submsgs]:
                subid = self._populate_type(topic, subtype, submsg, stamp, typename, myid)
                if isinstance(submsgs, (list, tuple)):
                    subids[subpath].append(subid)
        if subids:
            sql = "UPDATE %s SET " % quote(typename)
            for i, (path, subids) in enumerate(subids.items()):
                sql += "%s%s = :%s" % (", " if i else "", quote(".".join(path)), "_".join(path))
                args["_".join(path)] = subids
            sql += " WHERE _id = :_id"
            self._db.execute(sql, args)
        return myid


    def _iter_fields(self, msg, messages_only=False, top=()):
        """
        Yields ((nested, path), value, typename) from ROS message.

        @param  messages_only  whether to yield only values that are ROS messages themselves
                               or lists of ROS messages, else will yield scalar and list values
        """
        fieldmap = rosapi.get_message_fields(msg)
        for k, t in fieldmap.items() if fieldmap != msg else ():
            v, path = rosapi.get_message_value(msg, k, t), top + (k, )
            is_true_msg, is_msg_or_time = (rosapi.is_ros_message(v, ignore_time=x) for x in (1, 0))
            is_sublist = isinstance(v, (list, tuple)) and \
                         rosapi.scalar(t) not in rosapi.ROS_COMMON_TYPES
            if (is_true_msg or is_sublist) if messages_only else not is_msg_or_time:
                yield path, v, t
            if is_msg_or_time:
                for p2, v2, t2 in self._iter_fields(v, messages_only, top=path):
                    yield p2, v2, t2
