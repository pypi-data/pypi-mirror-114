# encoding: utf-8
"""
K-lity class used to process each test.
"""

import os

import yaml

from klity.database.postgresql import *


class VarDict(dict):
    """
    This enhanced dictionary is used to store variables into klity.
    You can access sub values (like in a dict or attributes of an object).
    """
    def __init__(self):
        self._dict = {}

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        try:
            return self.get(key).decode("utf-8")
        except:
            return str(self.get(key))

    def __repr__(self):
        return str(self._dict)

    def get(self, key, obj=None):
        key = key.strip()
        if obj is None:
            obj = self._dict
        if "." in key:
            try:
                return self.get(".".join(key.split(".")[1:]), obj[key.split(".")[0]])
            except TypeError:
                return self.get(".".join(key.split(".")[1:]), getattr(obj, key.split(".")[0]))
        else:
            try:
                try:
                    return obj[int(key)]
                except ValueError:
                    return obj[key]
            except TypeError:
                return getattr(obj, key)


class TestException(AssertionError):
    """Base class for exceptions in this module."""
    def __init__(self, context=None, traces=None):
        self.context = context
        self.traces = traces

    def __str__(self):
        stacktrace = "\n========== Errors detected ==========\n"
        if self.context is not None:
            for trace in self.context.klity.traces:
                stacktrace += f"{trace}\n"
        elif self.traces is not None:
            for trace in self.traces:
                stacktrace += f"{trace}\n"
        stacktrace += "\n"
        return stacktrace


class DatabaseException(TestException):
    pass


class Klity:
    def __init__(self, args=None):
        # Default configuration
        self.configuration = {
            "behave": {
                "lang": "fr",
            },
            "databases": [],
            "variables": [],
            "timeout": 10,
        }
        # Specific configuration
        try:
            with open(os.path.join(os.getcwd(), "configuration.yml")) as f:
                self.configuration.update(yaml.load(f, Loader=yaml.SafeLoader))
        except FileNotFoundError:
            # No specific configuration
            pass

        # Session variables
        self.variables = VarDict()
        # Requests
        self.connections = {}
        self.requests = {}
        # Traces
        self.traces = []
        # Error
        self.error = False

    def trace(self, message):
        self.traces.append(message)

    def before_feature(self, context, feature):
        # Loading available requests for this specific feature
        self.load_requests(feature.filename)

    def after_feature(self, context, feature):
        # Cleaning connections after feature, if necessary
        for connection in self.connections:
            if self.connections[connection]["type"].lower() == "postgresql":
                return postgresql_close(self.connections[connection])

    def before_scenario(self, context, scenario):
        # Before each scenario, session is cleaned
        self.session = {}
        # And traces too
        self.traces = []
        # Loading global variables
        self.variables = VarDict()
        for variable in self.configuration["variables"]:
            self.variables[variable] = self.configuration["variables"][variable]

    def after_scenario(self, context, scenario):
        # After each scenario, session, variables and error are cleaned
        self.session = {}
        self.variables = VarDict()
        self.error = False

    def before_step(self, context, step):
        self.traces = []

    def load_requests(self, feature_file):
        self.requests = {}
        # Loading requests
        feature_path = os.path.join(
            os.getcwd(), os.path.dirname(feature_file).replace("/", os.path.sep)
        )
        feature_name = os.path.basename(feature_file)
        if feature_name.endswith(".setup.feature"):
            size = 14
        elif feature_name.endswith(".teardown.feature"):
            size = 17
        else:
            size = 8
        request_file = os.path.join(feature_path, feature_name[:-size] + ".sql")
        if not os.path.exists(request_file):
            return
        with open(request_file) as f:
            requests = yaml.load(f, Loader=yaml.SafeLoader)
        for request in requests["requests"]:
            if isinstance(request, str):
                request_object = requests["requests"][request]
                self.requests[request] = request_object
            else:
                key = str(len(self.requests))
                self.requests[key] = request
        # Connecting to database if necessary
        for request in self.requests:
            self.connect(self.requests[request]["config"])

    def connect(self, connection):
        if connection not in self.configuration["databases"]:
            self.trace(f"Connection {connection} unknown, check your configuration.")
            raise DatabaseException(traces=self.traces)
        if connection not in self.connections:
            configuration = self.configuration["databases"][connection]
            if configuration["type"].lower() == "postgresql":
                try:
                    self.connections[connection] = postgresql_connect(configuration)
                except Exception as exception:
                    self.trace(f"Error while connecting to {configuration['host']}")
                    self.trace(exception)
                    raise DatabaseException(traces=self.traces)

    def execute(self, request, parameters=None):
        self.trace(f"Request '{request}' / {parameters}")
        if request not in self.requests:
            self.trace(f"Request '{request}' unknown.")
            raise DatabaseException(traces=self.traces)
        if "config" not in self.requests[request]:
            self.trace(f"Request '{request}' has no configuration set.")
            raise DatabaseException(traces=self.traces)
        if self.requests[request]["config"] not in self.connections:
            self.trace(f"Request '{request}' has no connection set.")
            raise DatabaseException(traces=self.traces)
        connection_name = self.requests[request]["config"]
        connection = self.connections[connection_name]
        if connection["type"].lower() == "postgresql":
            try:
                # Postgresql parameters are "%s" and not "?"
                query = self.requests[request]['request'].replace("?", "%s")
                result = postgresql_execute(connection, query, parameters)
                self.variables[request] = result
                return result
            except Exception as exception:
                self.trace(f"Error while executing request {request}")
                self.trace(exception)
                raise DatabaseException(traces=self.traces)
        else:
            self.trace(f"Connection '{connection_name}' not implemented.")
            raise DatabaseException(traces=self.traces)
