"""
Contains :py:class:`Apathy`.

- Run & Combine everything
"""

import multiprocessing
import json
from .specific import Alliances, Cities, Nations, Trades, Wars
from.boredom import Boredom


class Apathy:
    """Made to make running and combining different categories easy."""

    def __init__(self, types=(Alliances, Cities, Nations, Trades, Wars), fs="filespace"):
        self.filespace = fs
        self.types = types
        self.create()

    def create(self):
        self.processes = []
        self.things = []
        for T in self.types:
            thing = T(fs=self.filespace)
            self.things.append(thing)
            self.processes.append(
                multiprocessing.Process(
                    target=thing.run,
                    daemon=True,
                    name=T.__name__)
            )

    def run(self):
        """..py:function:: run(self: :py:class:`Apathy`) -> None
        
        - Runs :py:meth:`Apathy.collect` and :py:meth:`Apathy.combine`:.


        """
        self.collect()
        self.combine()

    def collect(self):
        """..py:function:: collect(self: :py:class:`Apathy`) -> None
        
        - Runs all collection classes.

        """
        try:
            for process in self.processes:
                process.start()
            for process in self.processes:
                process.join()
        except KeyboardInterrupt:
            for process in self.processes:
                process.terminate()
            raise

    def combine(self):
        """..py:function:: combine(self: :py:class:`Apathy`) -> None
        
        - Combines all collected data into a single ``final.json``.


        """
        data = []

        for thing in self.things:
            with open(thing.file) as f:
                data.append(json.load(f)["timeline"])

        days = set()
        for dat in data:
            keys = set(dat.keys())
            days = days and keys

        final = {}
        for day in days:
            val = []
            str_ver = Boredom.date_conv(None, float(day))
            errors = []
            for i in range(len(data)):
                dat = data[i]
                try:
                    val += list(dat[day].items())
                except KeyError:
                    errors.append(things[i].__name__)
            if len(errors):
                print(f"{str_ver} skipped due to missing data.")
                print(errors)
            else:
                final[day] = dict(val)
                print(f"{str_ver} done!")

        with open(f"{self.filespace}/final.json", "w") as f:
            json.dump(final, f)
