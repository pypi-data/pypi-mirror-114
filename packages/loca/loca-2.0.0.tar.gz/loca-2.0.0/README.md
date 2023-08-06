# Local locations for Python

> It's mi vida loca.

Loca is a highly opinionated redesign of [appdirs].  It relies on [pathlib],
[dataclasses] and `@property` to replace most of the parameters in
the original library to create a more intuitive API.

## Usage

```python
from loca import Loca

loca = Loca()
assert loca == loca.user.data == loca.data.user
assert loca.state() == loca.user.state()
assert loca.config == loca.user.config
assert loca.cache() == loca.cache.user()

shared = loca.shared
assert shared == loca.shared.data == loca.data.shared
foobar_shared_config = shared.config() / 'foobar'
```

## Contributing

Patches must pass the checks run by `tox` and should be sent to
[~cnx/misc@lists.sr.ht] using [`git send-email`][git-send-email],
with the following configurations:

    git config sendemail.to '~cnx/misc@lists.sr.ht'
    git config format.subjectPrefix 'PATCH python-loca'

## Copying

![LGPLv3](https://www.gnu.org/graphics/lgplv3-147x51.png)

Loca is free software: you can redistribute it and/or modify it
under the terms of the GNU [Lesser General Public License][lgplv3] as
published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

[appdirs]: https://pypi.org/project/appdirs
[pathlib]: https://docs.python.org/3/library/pathlib.html
[dataclasses]: https://docs.python.org/3/library/dataclasses.html
[~cnx/misc@lists.sr.ht]: https://lists.sr.ht/~cnx/misc
[git-send-email]: https://git-send-email.io
[lgplv3]: https://www.gnu.org/licenses/lgpl-3.0.html
