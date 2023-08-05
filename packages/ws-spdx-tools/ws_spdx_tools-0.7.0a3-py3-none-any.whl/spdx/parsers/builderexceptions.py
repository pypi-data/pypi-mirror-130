# Copyright (c) 2014 Ahmed H. Ismail
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class BuilderException(Exception):
    """Builder exception base class."""

    pass


class CardinalityError(BuilderException):
    def __init__(self, msg):
        self.msg = msg


class SPDXValueError(BuilderException):
    def __init__(self, msg):
        self.msg = msg


class OrderError(BuilderException):
    def __init__(self, msg):
        self.msg = msg

class FileTypeError(BuilderException):
    def __init__(self,msg):
        self.msg = msg
