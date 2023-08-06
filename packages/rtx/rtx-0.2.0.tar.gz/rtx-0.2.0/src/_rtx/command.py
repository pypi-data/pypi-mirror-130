"""
Apache-2.0

Copyright 2021 VincentRPS
   
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import asyncio
from discord.commands import SlashCommand, MessageCommand, UserCommand

class Command(SlashCommand):
    """Support For Slash Commands"""
    pass
class Message(MessageCommand):
    """Message Command Support"""
    pass

class User(UserCommand):
    """User Command Support"""
    pass

class App:
    """Support For Application Commands"""
    def __init__(self):
        pass

    @callable
    def command() -> Command:
        """Slash Command Decorating"""
        pass

    @callable
    def message() -> Message:
        """Message Command Decorating"""
        pass

    @callable
    def user() -> User:
        """User Command Decorating"""
        pass