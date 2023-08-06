# variousconnector
handy tools to connect the various data sources

## What are the Key Features?
1. Support PostgreSQL with SSH functionality.
2. Support Snowflake
	
## How to Install?

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install variousconnector
```

## How to Use?

### PostgreSQL

```python

from variousconnector import postgresql_connector

postgresql_credential = {
        "host":"your_db_server_url",
        "port":5432,
        "user":"your_user_name",
        "pwd":"your_password",
        "ssh_enable":True, # require SSH if using VPN
        "ssh_host":"your_ssh_host", # not require if ssh_enable is False
        "ssh_user":"your_ssh_user", # not require if ssh_enable is False
        "ssh_pwd":"your_ssh_password" # not require if ssh_enable is False
        }

pg = postgresql_connector(credential = postgresql_credential)

query = '''
    select *
    from table_name
    '''

query_result = pg_nossh.query(db='your_db_name',
                              query=query
                              )
```

### Snowflake

```python

from variousconnector import snowflake_connector

snowflake_credential = {
        'account':'XXXX',
        'user':'XXXX',
        'pwd':'XXXX',
        'warehouse':'XXXX'
    }

sw = snowflake_connector(credential = snowflake_credential)

query = '''
    select *
    from table_name
    '''

query_result = sw.query(db='your_db_name',
                        query=query
                        )

'''
how to know my snowflake account?
if your URL is "https://abc.snowflakecomputing.com/", then your Snowflake account name is "abc". 
If you are in any other region (such as AWS US-EAST), then if your URL is "https://xyz.us-east-1.snowflakecomputing.com/", then your account name is "xyz"
'''

```
