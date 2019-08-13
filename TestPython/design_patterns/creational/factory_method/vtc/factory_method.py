__author__ = 'R.Azh'


class Connection:
    def description(self):
        return "Generic"


class MySqlConnection(Connection):
    def description(self):
        return "MySQL"


class OracleConnection(Connection):
    def description(self):
        return "Oracle"


class SqlServerConnection(Connection):
    def description(self):
        return "SQL Server"


class FirstFactory:
    type = None

    def __init__(self, type):
        self.type = type

    def create_connection(self):
        if self.type == "Oracle":
            return OracleConnection()
        elif self.type == "SQL Server":
            return SqlServerConnection
        else:
            return MySqlConnection()

# usage
factory = FirstFactory("Oracle")
connection = factory.create_connection()
print("You're connecting with " +
      connection.description())
