"""Tests of selected stdlib functions."""


from pytype.tests import test_inference


class StdlibTests(test_inference.InferenceTest):
  """Tests for files in typeshed/stdlib."""

  def testAST(self):
    with self.Infer("""
      import ast
      def f():
        return ast.parse("True")
    """, deep=True, solve_unknowns=True) as ty:
      self.assertTypesMatchPytd(ty, """
        ast = ...  # type: module
        def f() -> _ast.AST
      """)

  def testUrllib(self):
    with self.Infer("""
      import urllib
    """, deep=True, solve_unknowns=True) as ty:
      self.assertTypesMatchPytd(ty, """
        urllib = ...  # type: module
      """)

  def testTraceBack(self):
    with self.Infer("""
      import traceback
      def f(exc):
        return traceback.format_exception(*exc)
    """, deep=True, solve_unknowns=True) as ty:
      self.assertTypesMatchPytd(ty, """
        traceback = ...  # type: module
        def f(exc) -> str
      """)

  def testOsWalk(self):
    with self.Infer("""
      import os
      x = list(os.walk("/tmp"))
    """, deep=False, extract_locals=True) as ty:
      self.assertTypesMatchPytd(ty, """
        os = ...  # type: module
        x = ...  # type: List[Tuple[Union[str, unicode, List[Union[str, unicode]]], ...]]
      """)

  def testStruct(self):
    with self.Infer("""
      import struct
      x = struct.Struct("b")
    """, deep=False) as ty:
      self.assertTypesMatchPytd(ty, """
        struct = ...  # type: module
        x = ...  # type: struct.Struct
      """)

  def testWarning(self):
    with self.Infer("""
      import warnings
    """, deep=False) as ty:
      self.assertTypesMatchPytd(ty, """
        warnings = ...  # type: module
      """)


if __name__ == "__main__":
  test_inference.main()