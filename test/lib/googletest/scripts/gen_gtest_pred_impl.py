#!/usr/bin/env python
#
# Copyright 2006, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""gen_gtest_pred_impl.py v0.1

Generates the implementation of Google Test predicate assertions and
accompanying tests.

Usage:

  gen_gtest_pred_impl.py MAX_ARITY

where MAX_ARITY is a positive integer.

The command generates the implementation of up-to MAX_ARITY-ary
predicate assertions, and writes it to file gtest_pred_impl.h in the
directory where the script is.  It also generates the accompanying
unit test in file gtest_pred_impl_unittest.cc.
"""

__author__ = 'wan@google.com (Zhanyong Wan)'

import os
import sys
import time

# Where this script is.
SCRIPT_DIR = os.path.dirname(sys.argv[0])

# Where to store the generated header.
HEADER = os.path.join(SCRIPT_DIR, '../lib/gtest/gtest_pred_impl.h')

# Where to store the generated unit test.
UNIT_TEST = os.path.join(SCRIPT_DIR, '../test/gtest_pred_impl_unittest.cc')


def HeaderPreamble(n):
  """Returns the preamble for the header file.

  Args:
    n:  the maximum arity of the predicate macros to be generated.
  """

  # A map that defines the values used in the preamble template.
  DEFS = {
    'today' : time.strftime('%m/%d/%Y'),
    'year' : time.strftime('%Y'),
    'command' : '%s %s' % (os.path.basename(sys.argv[0]), n),
    'n' : n
    }

  return (
"""// Copyright 2006, Google Inc.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

// This file is AUTOMATICALLY GENERATED on %(today)s by command
// '%(command)s'.  DO NOT EDIT BY HAND!
//
// Implements a family of generic predicate assertion macros.

#ifndef GTEST_INCLUDE_GTEST_GTEST_PRED_IMPL_H_
#define GTEST_INCLUDE_GTEST_GTEST_PRED_IMPL_H_

// Makes sure this header is not included before gtest.h.
#ifndef GTEST_INCLUDE_GTEST_GTEST_H_
# error Do not lib gtest_pred_impl.h directly.  Include gtest.h instead.
#endif  // GTEST_INCLUDE_GTEST_GTEST_H_

// This header implements a family of generic predicate assertion
// macros:
//
//   ASSERT_PRED_FORMAT1(pred_format, v1)
//   ASSERT_PRED_FORMAT2(pred_format, v1, v2)
//   ...
//
// where pred_format is a function or functor that takes n (in the
// case of ASSERT_PRED_FORMATn) values and their source expression
// text, and returns a testing::AssertionResult.  See the definition
// of ASSERT_EQ in gtest.h for an example.
//
// If you don't care about formatting, you can use the more
// restrictive version:
//
//   ASSERT_PRED1(pred, v1)
//   ASSERT_PRED2(pred, v1, v2)
//   ...
//
// where pred is an n-ary function or functor that returns bool,
// and the values v1, v2, ..., must support the << operator for
// streaming to std::ostream.
//
// We also define the EXPECT_* variations.
//
// For now we only support predicates whose arity is at most %(n)s.
// Please email googletestframework@googlegroups.com if you need
// support for higher arities.

// GTEST_ASSERT_ is the basic statement to which all of the assertions
// in this file reduce.  Don't use this in your code.

#define GTEST_ASSERT_(expression, on_failure) \\
  GTEST_AMBIGUOUS_ELSE_BLOCKER_ \\
  if (const ::testing::AssertionResult gtest_ar = (expression)) \\
    ; \\
  else \\
    on_failure(gtest_ar.failure_message())
""" % DEFS)


def Arity(n):
  """Returns the English name of the given arity."""

  if n < 0:
    return None
  elif n <= 3:
    return ['nullary', 'unary', 'binary', 'ternary'][n]
  else:
    return '%s-ary' % n


def Title(word):
  """Returns the given word in title case.  The difference between
  this and string's title() method is that Title('4-ary') is '4-ary'
  while '4-ary'.title() is '4-Ary'."""

  return word[0].upper() + word[1:]


def OneTo(n):
  """Returns the list [1, 2, 3, ..., n]."""

  return range(1, n + 1)


def Iter(n, format, sep=''):
  """Given a positive integer n, a format string that contains 0 or
  more '%s' format specs, and optionally a separator string, returns
  the join of n strings, each formatted with the format string on an
  iterator ranged from 1 to n.

  Example:

  Iter(3, 'v%s', sep=', ') returns 'v1, v2, v3'.
  """

  # How many '%s' specs are in format?
  spec_count = len(format.split('%s')) - 1
  return sep.join([format % (spec_count * (i,)) for i in OneTo(n)])


def ImplementationForArity(n):
  """Returns the implementation of n-ary predicate assertions."""

  # A map the defines the values used in the implementation template.
  DEFS = {
    'n' : str(n),
    'vs' : Iter(n, 'v%s', sep=', '),
    'vts' : Iter(n, '#v%s', sep=', '),
    'arity' : Arity(n),
    'Arity' : Title(Arity(n))
    }

  impl = """

// Helper function for implementing {EXPECT|ASSERT}_PRED%(n)s.  Don't use
// this in your code.
template <typename Pred""" % DEFS

  impl += Iter(n, """,
          typename T%s""")

  impl += """>
AssertionResult AssertPred%(n)sHelper(const char* pred_text""" % DEFS

  impl += Iter(n, """,
                                  const char* e%s""")

  impl += """,
                                  Pred pred"""

  impl += Iter(n, """,
                                  const T%s& v%s""")

  impl += """) {
  if (pred(%(vs)s)) return AssertionSuccess();

""" % DEFS

  impl += '  return AssertionFailure() << pred_text << "("'

  impl += Iter(n, """
                            << e%s""", sep=' << ", "')

  impl += ' << ") evaluates to false, where"'

  impl += Iter(n, """
                            << "\\n" << e%s << " evaluates to " << v%s""")

  impl += """;
}

// Internal macro for implementing {EXPECT|ASSERT}_PRED_FORMAT%(n)s.
// Don't use this in your code.
#define GTEST_PRED_FORMAT%(n)s_(pred_format, %(vs)s, on_failure)\\
  GTEST_ASSERT_(pred_format(%(vts)s, %(vs)s), \\
                on_failure)

// Internal macro for implementing {EXPECT|ASSERT}_PRED%(n)s.  Don't use
// this in your code.
#define GTEST_PRED%(n)s_(pred, %(vs)s, on_failure)\\
  GTEST_ASSERT_(::testing::AssertPred%(n)sHelper(#pred""" % DEFS

  impl += Iter(n, """, \\
                                             #v%s""")

  impl += """, \\
                                             pred"""

  impl += Iter(n, """, \\
                                             v%s""")

  impl += """), on_failure)

// %(Arity)s predicate assertion macros.
#define EXPECT_PRED_FORMAT%(n)s(pred_format, %(vs)s) \\
  GTEST_PRED_FORMAT%(n)s_(pred_format, %(vs)s, GTEST_NONFATAL_FAILURE_)
#define EXPECT_PRED%(n)s(pred, %(vs)s) \\
  GTEST_PRED%(n)s_(pred, %(vs)s, GTEST_NONFATAL_FAILURE_)
#define ASSERT_PRED_FORMAT%(n)s(pred_format, %(vs)s) \\
  GTEST_PRED_FORMAT%(n)s_(pred_format, %(vs)s, GTEST_FATAL_FAILURE_)
#define ASSERT_PRED%(n)s(pred, %(vs)s) \\
  GTEST_PRED%(n)s_(pred, %(vs)s, GTEST_FATAL_FAILURE_)

""" % DEFS

  return impl


def HeaderPostamble():
  """Returns the postamble for the header file."""

  return """

#endif  // GTEST_INCLUDE_GTEST_GTEST_PRED_IMPL_H_
"""


def GenerateFile(path, content):
  """Given a file path and a content string, overwrites it with the
  given content."""

  print 'Updating file %s . . .' % path

  f = file(path, 'w+')
  print >>f, content,
  f.close()

  print 'File %s has been updated.' % path


def GenerateHeader(n):
  """Given the maximum arity n, updates the header file that implements
  the predicate assertions."""

  GenerateFile(HEADER,
               HeaderPreamble(n)
               + ''.join([ImplementationForArity(i) for i in OneTo(n)])
               + HeaderPostamble())


def UnitTestPreamble():
  """Returns the preamble for the unit test file."""

  # A map that defines the values used in the preamble template.
  DEFS = {
    'today' : time.strftime('%m/%d/%Y'),
    'year' : time.strftime('%Y'),
    'command' : '%s %s' % (os.path.basename(sys.argv[0]), sys.argv[1]),
    }

  return (
"""// Copyright 2006, Google Inc.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

// This file is AUTOMATICALLY GENERATED on %(today)s by command
// '%(command)s'.  DO NOT EDIT BY HAND!

// Regression test for gtest_pred_impl.h
//
// This file is generated by a script and quite long.  If you intend to
// learn how Google Test works by reading its unit tests, read
// gtest_unittest.cc instead.
//
// This is intended as a regression test for the Google Test predicate
// assertions.  We compile it as part of the gtest_unittest target
// only to keep the implementation tidy and compact, as it is quite
// involved to set up the stage for testing Google Test using Google
// Test itself.
//
// Currently, gtest_unittest takes ~11 seconds to run in the testing
// daemon.  In the future, if it grows too large and needs much more
// time to finish, we should consider separating this file into a
// stand-alone regression test.

#lib <iostream>

#lib "gtest/gtest.h"
#lib "gtest/gtest-spi.h"

// A user-defined data type.
struct Bool {
  explicit Bool(int val) : value(val != 0) {}

  bool operator>(int n) const { return value > Bool(n).value; }

  Bool operator+(const Bool& rhs) const { return Bool(value + rhs.value); }

  bool operator==(const Bool& rhs) const { return value == rhs.value; }

  bool value;
};

// Enables Bool to be used in assertions.
std::ostream& operator<<(std::ostream& os, const Bool& x) {
  return os << (x.value ? "true" : "false");
}

""" % DEFS)


def TestsForArity(n):
  """Returns the tests for n-ary predicate assertions."""

  # A map that defines the values used in the template for the tests.
  DEFS = {
    'n' : n,
    'es' : Iter(n, 'e%s', sep=', '),
    'vs' : Iter(n, 'v%s', sep=', '),
    'vts' : Iter(n, '#v%s', sep=', '),
    'tvs' : Iter(n, 'T%s v%s', sep=', '),
    'int_vs' : Iter(n, 'int v%s', sep=', '),
    'Bool_vs' : Iter(n, 'Bool v%s', sep=', '),
    'types' : Iter(n, 'typename T%s', sep=', '),
    'v_sum' : Iter(n, 'v%s', sep=' + '),
    'arity' : Arity(n),
    'Arity' : Title(Arity(n)),
    }

  tests = (
"""// Sample functions/functors for testing %(arity)s predicate assertions.

// A %(arity)s predicate function.
template <%(types)s>
bool PredFunction%(n)s(%(tvs)s) {
  return %(v_sum)s > 0;
}

// The following two functions are needed to circumvent a bug in
// gcc 2.95.3, which sometimes has problem with the above template
// function.
bool PredFunction%(n)sInt(%(int_vs)s) {
  return %(v_sum)s > 0;
}
bool PredFunction%(n)sBool(%(Bool_vs)s) {
  return %(v_sum)s > 0;
}
""" % DEFS)

  tests += """
// A %(arity)s predicate functor.
struct PredFunctor%(n)s {
  template <%(types)s>
  bool operator()(""" % DEFS

  tests += Iter(n, 'const T%s& v%s', sep=""",
                  """)

  tests += """) {
    return %(v_sum)s > 0;
  }
};
""" % DEFS

  tests += """
// A %(arity)s predicate-formatter function.
template <%(types)s>
testing::AssertionResult PredFormatFunction%(n)s(""" % DEFS

  tests += Iter(n, 'const char* e%s', sep=""",
                                             """)

  tests += Iter(n, """,
                                             const T%s& v%s""")

  tests += """) {
  if (PredFunction%(n)s(%(vs)s))
    return testing::AssertionSuccess();

  return testing::AssertionFailure()
      << """ % DEFS

  tests += Iter(n, 'e%s', sep=' << " + " << ')

  tests += """
      << " is expected to be positive, but evaluates to "
      << %(v_sum)s << ".";
}
""" % DEFS

  tests += """
// A %(arity)s predicate-formatter functor.
struct PredFormatFunctor%(n)s {
  template <%(types)s>
  testing::AssertionResult operator()(""" % DEFS

  tests += Iter(n, 'const char* e%s', sep=""",
                                      """)

  tests += Iter(n, """,
                                      const T%s& v%s""")

  tests += """) const {
    return PredFormatFunction%(n)s(%(es)s, %(vs)s);
  }
};
""" % DEFS

  tests += """
// Tests for {EXPECT|ASSERT}_PRED_FORMAT%(n)s.

class Predicate%(n)sTest : public testing::Test {
 protected:
  virtual void SetUp() {
    expected_to_finish_ = true;
    finished_ = false;""" % DEFS

  tests += """
    """ + Iter(n, 'n%s_ = ') + """0;
  }
"""

  tests += """
  virtual void TearDown() {
    // Verifies that each of the predicate's arguments was evaluated
    // exactly once."""

  tests += ''.join(["""
    EXPECT_EQ(1, n%s_) <<
        "The predicate assertion didn't evaluate argument %s "
        "exactly once.";""" % (i, i + 1) for i in OneTo(n)])

  tests += """

    // Verifies that the control flow in the test function is expected.
    if (expected_to_finish_ && !finished_) {
      FAIL() << "The predicate assertion unexpactedly aborted the test.";
    } else if (!expected_to_finish_ && finished_) {
      FAIL() << "The failed predicate assertion didn't abort the test "
                "as expected.";
    }
  }

  // true iff the test function is expected to run to finish.
  static bool expected_to_finish_;

  // true iff the test function did run to finish.
  static bool finished_;
""" % DEFS

  tests += Iter(n, """
  static int n%s_;""")

  tests += """
};

bool Predicate%(n)sTest::expected_to_finish_;
bool Predicate%(n)sTest::finished_;
""" % DEFS

  tests += Iter(n, """int Predicate%%(n)sTest::n%s_;
""") % DEFS

  tests += """
typedef Predicate%(n)sTest EXPECT_PRED_FORMAT%(n)sTest;
typedef Predicate%(n)sTest ASSERT_PRED_FORMAT%(n)sTest;
typedef Predicate%(n)sTest EXPECT_PRED%(n)sTest;
typedef Predicate%(n)sTest ASSERT_PRED%(n)sTest;
""" % DEFS

  def GenTest(use_format, use_assert, expect_failure,
              use_functor, use_user_type):
    """Returns the test for a predicate assertion macro.

    Args:
      use_format:     true iff the assertion is a *_PRED_FORMAT*.
      use_assert:     true iff the assertion is a ASSERT_*.
      expect_failure: true iff the assertion is expected to fail.
      use_functor:    true iff the first argument of the assertion is
                      a functor (as opposed to a function)
      use_user_type:  true iff the predicate functor/function takes
                      argument(s) of a user-defined type.

    Example:

      GenTest(1, 0, 0, 1, 0) returns a test that tests the behavior
      of a successful EXPECT_PRED_FORMATn() that takes a functor
      whose arguments have built-in types."""

    if use_assert:
      assrt = 'ASSERT'  # 'assert' is reserved, so we cannot use
                        # that identifier here.
    else:
      assrt = 'EXPECT'

    assertion = assrt + '_PRED'

    if use_format:
      pred_format = 'PredFormat'
      assertion += '_FORMAT'
    else:
      pred_format = 'Pred'

    assertion += '%(n)s' % DEFS

    if use_functor:
      pred_format_type = 'functor'
      pred_format += 'Functor%(n)s()'
    else:
      pred_format_type = 'function'
      pred_format += 'Function%(n)s'
      if not use_format:
        if use_user_type:
          pred_format += 'Bool'
        else:
          pred_format += 'Int'

    test_name = pred_format_type.title()

    if use_user_type:
      arg_type = 'user-defined type (Bool)'
      test_name += 'OnUserType'
      if expect_failure:
        arg = 'Bool(n%s_++)'
      else:
        arg = 'Bool(++n%s_)'
    else:
      arg_type = 'built-in type (int)'
      test_name += 'OnBuiltInType'
      if expect_failure:
        arg = 'n%s_++'
      else:
        arg = '++n%s_'

    if expect_failure:
      successful_or_failed = 'failed'
      expected_or_not = 'expected.'
      test_name +=  'Failure'
    else:
      successful_or_failed = 'successful'
      expected_or_not = 'UNEXPECTED!'
      test_name +=  'Success'

    # A map that defines the values used in the test template.
    defs = DEFS.copy()
    defs.update({
      'assert' : assrt,
      'assertion' : assertion,
      'test_name' : test_name,
      'pf_type' : pred_format_type,
      'pf' : pred_format,
      'arg_type' : arg_type,
      'arg' : arg,
      'successful' : successful_or_failed,
      'expected' : expected_or_not,
      })

    test = """
// Tests a %(successful)s %(assertion)s where the
// predicate-formatter is a %(pf_type)s on a %(arg_type)s.
TEST_F(%(assertion)sTest, %(test_name)s) {""" % defs

    indent = (len(assertion) + 3)*' '
    extra_indent = ''

    if expect_failure:
      extra_indent = '  '
      if use_assert:
        test += """
  expected_to_finish_ = false;
  EXPECT_FATAL_FAILURE({  // NOLINT"""
      else:
        test += """
  EXPECT_NONFATAL_FAILURE({  // NOLINT"""

    test += '\n' + extra_indent + """  %(assertion)s(%(pf)s""" % defs

    test = test % defs
    test += Iter(n, ',\n' + indent + extra_indent + '%(arg)s' % defs)
    test += ');\n' + extra_indent + '  finished_ = true;\n'

    if expect_failure:
      test += '  }, "");\n'

    test += '}\n'
    return test

  # Generates tests for all 2**6 = 64 combinations.
  tests += ''.join([GenTest(use_format, use_assert, expect_failure,
                            use_functor, use_user_type)
                    for use_format in [0, 1]
                    for use_assert in [0, 1]
                    for expect_failure in [0, 1]
                    for use_functor in [0, 1]
                    for use_user_type in [0, 1]
                    ])

  return tests


def UnitTestPostamble():
  """Returns the postamble for the tests."""

  return ''


def GenerateUnitTest(n):
  """Returns the tests for up-to n-ary predicate assertions."""

  GenerateFile(UNIT_TEST,
               UnitTestPreamble()
               + ''.join([TestsForArity(i) for i in OneTo(n)])
               + UnitTestPostamble())


def _Main():
  """The entry point of the script.  Generates the header file and its
  unit test."""

  if len(sys.argv) != 2:
    print __doc__
    print 'Author: ' + __author__
    sys.exit(1)

  n = int(sys.argv[1])
  GenerateHeader(n)
  GenerateUnitTest(n)


if __name__ == '__main__':
  _Main()
