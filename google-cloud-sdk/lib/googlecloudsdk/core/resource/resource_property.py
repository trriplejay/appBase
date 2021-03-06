# Copyright 2015 Google Inc. All Rights Reserved.

"""Resource property Get."""


def Get(resource, key, default=None):
  """Gets the value referenced by key in the object resource.

  Since it is common for resource instances to be sparse it is not an error if
  a key is not present in a particular resource instance, or if an index does
  not match the resource type.

  Args:
    resource: The resource object possibly containing a value for key.
    key: Ordered list of key names/indices, applied left to right. Each
      element in the list may be one of:
        str - A resource property name. This could be a class attribute name or
          a dict index.
        int - A list index. Selects one member is the list. Negative indices
          count from the end of the list, starting with -1 for the last element
          in the list. An out of bounds index is not an error; it produces the
          value None.
        None - A list slice. Selects all members of a list or dict like object.
          A slice of an empty dict or list is an empty dict or list.
    default: Get() returns this value if key is not in resource.

  Returns:
    The value, None if any of the given keys are not found. This is
      intentionally not an error. In this context a value can be any data
      object: dict, list, tuple, class, str, int, float, ...
  """
  for i, index in enumerate(key):

    if resource is None:
      # None is different than an empty dict or list.
      return default

    elif isinstance(index, str) and hasattr(resource, index):
      # class-like -- done here to catch collections
      resource = getattr(resource, index, default)

    elif hasattr(resource, 'iteritems'):
      # dict-like
      if index is None:
        if i + 1 < len(key):
          # Inner slice: *.[].*
          return [Get(resource, [k] + key[i + 1:], default) for k in resource]
        else:
          # Trailing slice: *.[]
          return resource
      elif index in resource:
        resource = resource[index]
      else:
        return default

    elif hasattr(resource, '__iter__') or isinstance(resource, str):
      # list-like
      if index is None:
        if i + 1 < len(key):
          # Inner slice: *.[].*
          return [Get(resource, [k] + key[i + 1:], default)
                  for k in range(len(resource))]
        else:
          # Trailing slice: *.[]
          return resource
      elif not isinstance(index, (int, long)):
        # Index mismatch.
        return default
      elif index in xrange(-len(resource), len(resource)):
        resource = resource[index]
      else:
        return default

    else:
      # Resource or index mismatch.
      return default

  return resource
