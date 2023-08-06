Dataset loader for specific data
=================================

Project discription:
~~~~~~~~~~~~~~~~~~~~

This project contains a loader of a special data set, as well as a connection to the database using pymssql.

Get start:
~~~~~~~~~~~~~~~~~~~~
First you need to import the package: ::

    import pack_dataset

Now create an instance of the connection class, specifying the login and password for connecting to the database: ::

    datasets_loader = pack_dataset.create_connect(username, password)

And the data for connecting to the database is contained in the permanent environment, then they are automatically initialized. Then you just want to get a data set indicating how many rows you need to get (0 if you need to get everything): ::
    
    dataset = datasets_loader.get_data_weather(row=15)

Manual connection to the database:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If, when creating a class, a message is displayed stating that it was not possible to get connection data to the database, you must specify them manually: ::

    datasets_loader.connect_data['server'] = server:port
    datasets_loader.connect_data['database'] = database_name
    datasets_loader.connect_data['schema'] = shema_name
    datasets_loader.connect_data['table'] = table_name
    datasets_loader.connect_to_db()

Next, you can get a dataset: ::

    dataset = datasets_loader.get_data_weather(row=15)

