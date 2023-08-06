from typing import Dict


class TaggedContentCollection(dict):
    """
        A Container for tagged content that supports the appending we need
    """
    def add(self, tag:str, content:str):
        """
            Add content to the collection
        """
        if tag not in self:
            self[tag] = f"{content}\n"
            return
        self[tag] += f"\n{content}\n"

    def merge(self, other: 'TaggedContentCollection'):
        """
            Merge this collection with another
        """
        for tag, content in other.items():
            if tag not in self:
                self[tag] = f"{content}"
            else:
                self[tag] += f"\n{content}"
