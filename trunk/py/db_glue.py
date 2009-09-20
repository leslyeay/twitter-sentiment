import psycopg

connect_string = ('dbname=cycling user=cycling password= host=')

def new():
   '''Return a DB object which is not in use by any other requests. FIXME:
      Currently, this may be too inefficient; should use some kind of
      connection pooling.'''
   return DB()

def req_db_release(req):
   '''Release the given request's DB object.'''
   if (req.db is not None):
      req.db.rollback()
      req.db = None
   

class DB(object):

   __slots__ = ('conn',
                'curs')

   def __init__(self):
      self.conn = psycopg.connect(connect_string, serialize=0)
      self.conn.autocommit(0)
      self.curs = self.conn.cursor()

   def commit(self):
      # FIXME: Do something smart if commit fails.
      self.conn.commit()

   def quoted(self, s):
      if (s is None):
         return "''"
      return str(psycopg.QuotedString(s))

   def rollback(self):
      self.conn.rollback()

   def rowcount(self):
      return self.curs.rowcount
      
   def sql(self, sql, parms=None):
      # Skip this -- we can turn it on in Postgres if needed
      #g.log.debug(sql)
      start_time = util.nowfloat()
      self.curs.execute(sql, parms)

      # Avoid clogging the log now that some operations take hundreds or
      # or thousands of queries.
      #g.log.debug('Database execute() took %fs'
      #            % (util.nowfloat() - start_time))

      if (self.curs.description is None):
         return None
      else:
         return self.pack_result(self.curs.description, self.curs.fetchall())

   def table_columns(self, tablename):
      'Return the column names of the given table as a set of strings.'
      rows = self.sql("""
SELECT attname FROM pg_attribute
WHERE
   attnum > 0
   AND NOT attisdropped
   AND attrelid = (SELECT oid FROM pg_class WHERE relname = '%s')"""
                      % (tablename))
      return set([row['attname'] for row in rows])

   def transaction_begin(self):
      # Apparently this is not necessary
      #self.sql("BEGIN TRANSACTION");
      self.sql('SET CONSTRAINTS ALL DEFERRED')
      self.sql('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE')
