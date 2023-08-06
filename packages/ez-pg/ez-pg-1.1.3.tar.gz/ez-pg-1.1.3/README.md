# easypg
Query builder based on psycopg2 to make querying databases in python more accessible for every day use

The goal of *easypg* is to allow others to easily use psycopg in a programmatic way and simplify creating scalable database queries within your python scripts. 

## Connecting to a Database:

Currently it is only possible to use simple connections via usernames and passwords to connect to local databases.

Essentially you just need to call dbActions('dbname', 'username')
<sub>*if there is a password you can enter it, but if not, the default is None so it is not required*</sub>

### Changing the Cursor

By default easypg will use Psycopg's built-in dictionary cursor ('RealDictCursor') meaning that the output will be in a dictionary structure rather than the default output of psycopg. If you would like to change this you can simply pass the cursor_factory argument in the initialization of the database connection.

Possible values are:
- ez_pg.extras.NamedTupleCursor
- ez_pg.extras.DictCursor
- ez_pg.extras.RealDictCursor (default)
- None (uses the default psycopg cursor)

## The basic query syntax is as follows:

*operation('table', columns, arguments)*

Here the columns part is either a list (for selects) or a dictionary of {columns:values} for inserts and updates. 

The last argument allows users to pass any number of SQL key words as long as they are in the correct order for a normal SQL query and any spaces are replaced by an underscore. 

Example:

The query "select column1, max(column2) from table where argument=value and arg2='test' group by column1" would look like:

dbActions.select('table', ['column1', 'max(column2)'], where='argument=value', and='arg2=test', group_by='column1')
note: for SELECT actions only, the default value for columns is all so if no value is passed the result will be a 'select * ' statement. 

### Deleting from a table:

The *delete* function has a slightly different syntax as specifying columns is not necessary. Still it follow a similar syntax to the other basic queries:
*delete('table', arguments)*

Example:

To delete all elements of a table (test_table) where column2 is 'test' you would use delete("test_table", where="column2='test'")

## CTE:

Using common table expressions is very different from other queries as **each** one must first be assembled via the CTE function. They can then be included in the optional cte argument of the *select* function in order to be executed. For example, a cte, 'test' of "Select * from table1" must first be passed as cte('table1') style function. The CTE is extremely similar to a basic query in that the syntax of arguments is all the same, however the result is actually a preassembled SQL string that can be use in the final select query. 

If the above example was set as a variable of "cte", it can then be used in a select function like so:
select('table', cte={'test':cte}, limit=100)

The outcome of this would be the same as using the following query:

WITH 'test' as(
	SELECT
	*
	FROM table1)
SELECT
 *
FROM table
LIMIT 100

## Creating Tables/Database:

Each element has a separate function with their own set of necessary arguments. For a database, only the name is required, but any extra that meet pg standards should be allowed in the same manner as other queries. Creating tables is different (hence the separate function) where you are required to include the name of the table and a dictionary with the names of the columns and a nested dictionary with a required 'type' element. You can also include a 'contraint' element in this dictionary if necessary. 

**Example:**
create_table('test', {'column1':{'type':'int', 'constraint':'unique'}, 'column2':{'type':'text'}})

Any of the pre-table name elements listed in the PG documentation can be included as \*args elements after the columns dictionary.

## Dropping Element:

As with basic query syntax, there is only a single function for dropping elements. This requires the 'obj' (ie TABLE/DATABASE etc) to be specified along with the name. Any other options can then be included as keyword arguments just as with basic query syntax.