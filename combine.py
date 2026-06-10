#!/usr/bin/env python3
#  pygone - A Python Chess Engine
#  Copyright (C) 2026 scs-ben
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
import sys

source = open(sys.argv[1], 'rb').read().replace(b'\r\n', b'\n')
if len(sys.argv) > 2:
    open(sys.argv[2], 'wb').write(source)
else:
    sys.stdout.buffer.write(source)

