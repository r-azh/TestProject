__author__ = 'R.Azh'


class Connection:
    def description(self):
        return "Generic"


class SecureMySqlConnection(Connection):
    def description(self):
        return "MySQL secure"


class SecureOracleConnection(Connection):
    def description(self):
        return "Oracle secure"


class SecureSqlServerConnection(Connection):
    def description(self):
        return "SQL Server secure"


class ConnectionFactory:
    def create_connection(self, type):
        raise NotImplementedError


class SecureFactory(ConnectionFactory):
    def create_connection(self, type):
        if type == "Oracle":
            return SecureOracleConnection()
        elif type == "SQL Server":
            return SecureSqlServerConnection
        else:
            return SecureMySqlConnection()

# usage
factory = SecureFactory()
connection = factory.create_connection("Oracle")
print("You're connecting with " +
      connection.description())
