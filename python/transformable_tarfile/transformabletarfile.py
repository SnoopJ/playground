"""
  Based on a question in freenode #python on Oct 19, 2018
"""
import tarfile
import copy
import re
import shutil

for fn in ('foo', 'bar', 'baz', 'taco', 'foofile.txt', 'barfile.txt'):
    if shutil.os.path.isdir(fn):
        shutil.rmtree(fn)
    else:
        try:
            shutil.os.remove(fn)
        except OSError:
            pass

class TransformableTarFile(tarfile.TarFile):
    """
    A subclass to support arbitrary transformations on the structure of the output,
    akin to the --transform argument to GNU tar
    """
    def extract(self, member, path="", set_attrs=True, *, numeric_owner=False, transform=None):
      """
      Adapted from the original method. If a callable `transform` is specified, 
      apply it to member before performing the extraction with the return value.
      """
      if callable(transform):
          member = transform(member)

      if not member: return

      super().extract(member=member, path=path, set_attrs=set_attrs, numeric_owner=numeric_owner)

def regex_transform(pattern, repl):
    """ Factory for a function that applies a regex substitution to a TarInfo instance's name """
    def transform(tarinfo):
      tarinfo = copy.copy(tarinfo) # we should probably avoid mutating the parent TarFile as much as we can. deepcopy() might even make sense here, but I don't know the tarfile library
      tarinfo.name = re.sub(pattern, repl, tarinfo.name) 
      return tarinfo

    transform.pattern = pattern
    transform.repl = repl
    return transform

def explicit_transform(tarinfo):
    """ Reject files with 'bar' anywhere in their path """
    if 'bar' in tarinfo.name:
        return False
    else:
        return tarinfo

f = TransformableTarFile('foo.tar')
f.extractall()

tr1 = regex_transform('foo|bar', 'taco')  # mm tacos
tr2 = regex_transform('(foo|bar)/', '')  # flatten
tr3 = explicit_transform

print(f'Before extraction, state of file is:\n{list(f)}\n')

# this looping business is NOT how this should really be done in production!
# the most proper thing is to also overload extractfile() and extractall() to
# also accept the `transform` keyword and pass it along to extract()
# but there's lots of helper logic in those methods in the original class, and I
# didn't want to bother.

# try changing this transformation or writing your own!
tr = tr1
if tr in (tr1, tr2):
  print(f'Using the transformation s/{re.escape(tr.pattern)}/{re.escape(tr.repl)}/\n-----')
elif tr == tr3:
  print("Avoiding all files with 'bar' anywhere in their name")

for child in list(f):
  print(f'{child.name} → {tr(child).name}')
  f.extract(child, transform=tr)

print(f'After extraction, state of file is:\n{list(f)}\n')
