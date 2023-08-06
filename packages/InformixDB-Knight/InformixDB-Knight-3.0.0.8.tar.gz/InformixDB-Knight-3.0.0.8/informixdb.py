########################################################################
#                 Copyright (c) 1997 by IV DocEye AB
#              Copyright (c) 1999 by Stephen J. Turner
#                Copyright (c) 2005 by Carsten Haese
#  
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#  
# Permission to use, copy, modify, and distribute this software and its
# associated documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appears in all
# copies, and that both that copyright notice and this permission notice
# appear in supporting documentation, and that the name of the author
# not be used in advertising or publicity pertaining to distribution of
# the software without specific, written prior permission.
#  
# THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.  IN
# NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
# USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
########################################################################

# $Id$
# informixdb.py
#
# This is a trivial python wrapper around the C core _informixdb.so
#

"""\
 DB-API 2.0 compliant interface for IBM Informix databases.

Here's a small example to get you started:

>>> import informixdb
>>> conn = informixdb.connect('mydatabase')
>>> cursor = conn.cursor()
>>> cursor.execute('SELECT * FROM names')
>>> cursor.fetchall()
[('donald', 'duck', 34), ('mickey', 'mouse', 23)]

For more information on DB-API 2.0, see
http://www.python.org/peps/pep-0249.html
"""

version = "2.5"

class Row(object):
  """Helper class for cursors whose row format is ROW_AS_OBJECT."""
  def __init__(self, d): self.__dict__.update(d)
  def __repr__(self): return repr(self.__dict__)
  def __str__(self): return str(self.__dict__)
  def __getitem__(self,k): return self.__dict__[k]

class IntervalYearToMonth(object):
  """\
This class is used for input and output binding of
INTERVAL columns whose precision is a subset of
YEAR TO MONTH.

Intervals can be added to dates, datetimes, and other Intervals
that have compatible precision. Intervals can also be multiplied
and divided by scalar factors.
"""
  def __init__(self, years=0, months=0):
    self._months = 12*years+months
    self.years, self.months = divmod(self._months,12)
  def __repr__(self):
    return "%s(%d, %d)"%(self.__class__.__name__,self.years,self.months)
  def __str__(self):
    """Returns the interval in Informix's format for input binding."""
    if self._months < 0:
      return "-%d-%02d" % divmod(-self._months,12)
    else:
      return "%d-%02d" % divmod(self._months,12)
  def __add__(self, other):
      if isinstance(other, IntervalYearToMonth):
        return self.__class__(0, int(self._months+other._months))
      elif isinstance(other, (datetime.datetime, datetime.date)):
        # extract the date from the other operand
        y,m,d = other.timetuple()[0:3]
        otherdate = datetime.date(y,m,d)
        # shift the date by the desired number of months
        y2,m2 = divmod(m-1+self._months,12)
        try:
          date2 = datetime.date(y+y2,m2+1,d)
        except ValueError:
          raise ValueError("month arithmetic yielded an invalid date.")
        # apply the resulting timedelta to the operand
        return other + (date2 - otherdate)
      else: return NotImplemented
  def __neg__(self): return self.__class__(0, -self._months)
  def __sub__(self, other): return self + -other
  def __rsub__(self, other): return -self + other
  def __abs__(self):
      if self._months < 0: return -self
      else: return self
  def __mul__(self, other):
      #if isinstance(other, (int,long,float)):
      if isinstance(other, (int,float)):
        return self.__class__(0, int(self._months*other))
      else: return NotImplemented
  def __div__(self, other):
      #if isinstance(other, (int,long,float)):
      if isinstance(other, (int,float)):
        return self.__class__(0, int(self._months/other))
      else: return NotImplemented
  __radd__ = __add__
  __rmul__ = __mul__
  __floordiv__ = __div__
  def __cmp__(self, other):
      """Implements comparisons between intervals."""
      if isinstance(other, IntervalYearToMonth):
        return self._months - other._months
      else: return NotImplemented

# Define IntervalDayToFraction for symmetry. All the heavy lifting is done
# by datetime.timedelta, from which this class is derived.
import datetime
class IntervalDayToFraction(datetime.timedelta):
  """\
This class is used for input and output binding of
INTERVAL columns whose precision is a subset of
DAY TO FRACTION.

Intervals can be added to dates, datetimes, and other Intervals
that have compatible precision. Intervals can also be multiplied
and divided by scalar factors.
"""
  def __init__(self,days=0,seconds=0,microseconds=0):
    datetime.timedelta.__init__(self, days, seconds, microseconds)
  def __str__(self):
    """Returns the interval in Informix's format for input binding."""
    if self.days<0:
      neg = IntervalDayToFraction(-self.days, -self.seconds, -self.microseconds)
      return '-'+str(neg)
    else:
      minutes, seconds = divmod(self.seconds, 60)
      hours, minutes = divmod(minutes, 60)
      return "%d %02d:%02d:%02d.%05d" % (self.days, hours,minutes,seconds,
                                         self.microseconds/10)

# The module initialization of _informixdb references the Interval classes
# above, so don't put this import before the interval class definitions.
from _informixdb import *

# promote the class definitions of _informixdb.Cursor and
# _informixdb.Connection into this namespace so that help(informixdb)
# sees their doc strings. Also make it impossible for the user to try
# to instantiate these classes directly.
from _informixdb import Cursor as _Cursor, Connection as _Connection
class Cursor(_Cursor):
  __doc__ = _Cursor.__doc__
  def __new__(self, *args, **kwargs):
    raise InterfaceError("Use Connection.cursor() to instantiate a cursor.")
del _Cursor
class Connection(_Connection):
  __doc__ = _Connection.__doc__
  def __new__(self, *args, **kwargs):
    raise InterfaceError("Use connect() to instantiate a connection.")
del _Connection
try:
  # Same for Sblobs if we have support for them in _informixdb
  from _informixdb import Sblob as _Sblob
  class Sblob(_Sblob):
    __doc__ = _Sblob.__doc__
    def __new__(self, *args, **kwargs):
      raise InterfaceError("Use Connection.Sblob() to instantiate an Sblob.")
  del _Sblob
except: pass
