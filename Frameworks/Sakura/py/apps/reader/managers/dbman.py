# coding: utf8
# dataman.py
# 11/7/2012 sshakeel
#
# Always use long for unixtimestamp, as after year 2038 int32 will overflow.

from sakurakit.skclass import Q_Q, staticproperty, memoized, memoizedproperty
import os, string, re
import rc
import sqlite3
from sakurakit.skdebug import dprint, dwarn, derror

class DbManager(object):
  def __init__(self):
    dprint('enter DbManager')
    
    self.TERMS_TABLE = 'terms'    
    self.dbfile = rc.xml_path('syncdb')
    
    self.initializeDb = False
    if not os.path.exists(self.dbfile):
      self.initializeDb = True
    
    self.testConnection()
  
  def testConnection(self):
    self.conn = sqlite3.connect(self.dbfile)
    
    if self.initializeDb:
      dwarn("pass: sync database not found, %s" % self.dbfile)
      self.createTables()
      
      # Test Insertion
      rowId = self.insertTerm()
      dprint('Inserted Row into syncdb with id: %d' % (rowId))
      self.initializeDb = False
    
    self.conn.close();
    
  def insertTerm(self):
    sql = """INSERT INTO `{tn}` 
            (`special`, `gameId`, `pattern`, `text`)
            VALUES 
            ({special}, {gameId}, '{pattern}', '{text}')""" \
          .format(tn=self.TERMS_TABLE, special=1, gameId=55333, pattern='数馬', text='かすま')
    cursor = self.conn.cursor()
    cursor.execute(sql)
    self.conn.commit()
    return cursor.lastrowid
  
  def createTables(self):
    self.conn.cursor().execute(self.termsTableSql())
    self.conn.commit()
  
  def termsTableSql(self):
    """
    @return  sql to create terms table in database
    """
    return 'CREATE TABLE `{tn}` ( ' + \
          '`Id`       INTEGER PRIMARY KEY AUTOINCREMENT,' + \
          '`gameId`   INTEGER,' + \
          '`pattern`  TEXT NOT NULL,' + \
          '`text`     TEXT,' + \
          '`special`  INTEGER NOT NULL' + \
          ')'.format(tn=self.TERMS_TABLE)
  
@memoized
def manager(): return DbManager()

# EOF