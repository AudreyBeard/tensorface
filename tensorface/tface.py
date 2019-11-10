""" tface.py
    Tensorboard interface to make it easier to do fast data processing with
    tensorboard events
"""
import os

from tensorboard.backend.event_processing.event_multiplexer import EventMultiplexer

__all__ = ['TensorFace']


def realpath(path):
    """ Does real path names
    """
    path = os.path.realpath(os.path.expandvars(os.path.expanduser(
        path
    )))
    return path


def ls_r(directory):
    """ Recursive list directory, maintaining full paths
    """
    all_files = []
    for root, _, fns in os.walk(directory):
        all_files.extend([os.path.join(root, fn) for fn in fns])
    return all_files


class TensorFace(object):
    def __init__(self, dpath=None, do_load_now=False):
        """ Don't do anything by default because we may want to set the load
            path later, and loading takes a while
        """
        self.dpath = dpath
        self._emux = None
        self.run_names = None
        self.scalar_names = None

        # Loading takes a while, so don't do it by default
        if self._dpath is not None and do_load_now:
            self.load()

    def load(self, dpath=None):
        """ Load up all events and set interface variables
        """

        # Set dpath
        if dpath is not None:
            self.dpath = dpath
        event_map = self._get_events()
        self.run_names = list(event_map.keys())
        self._emux = EventMultiplexer(event_map)

        # This takes a while - several seconds on my machine
        self._emux.Reload()

        self.scalar_names = list({
            scalar_name
            for run_name in self.run_names
            for scalar_name in self._scalar_names_for(run_name)
        })

    def all_runs(self):
        """ Grabs all scalar values for all runs
        """
        assert self._emux is not None
        all_runs = {
            run_name: self.scalars_for(run_name) for run_name in self.run_names}
        return all_runs

    def all_scalars(self):
        """ Grabs all runs for all scalar names
        """
        assert self._emux is not None
        all_scalars = {
            scalar_name: self.runs_with_scalar(scalar_name)
            for scalar_name in self.scalar_names
        }
        return all_scalars

    def runs_with_scalar(self, scalar_name):
        """ Grabs all runs with their scalars for a given scalar name
            (also nice)
        """
        assert self._emux is not None
        runs = {
            run_name: self.get_events_dict(run_name, scalar_name)
            for run_name in self.run_names
            if scalar_name in self._scalar_names_for(run_name)
        }
        return runs

    def scalars_for(self, run_name):
        """ Gets all scalar values for a run name in a dict
            NOTE this is what I use most
            keys: scalar names (loss_val, acc_train, etc.)
            values: dict
                keys: 'wall_time', 'step', 'value'
                values: lists of wall_time, step, and value
        """
        # Don't try this if the EventMultiplexer hasn't loaded yet
        assert self._emux is not None

        # Get scalar events for this run
        scalar_names = self._scalar_names_for(run_name)
        scalar_events = {
            k: self._emux.Scalars(run_name, k)
            for k in scalar_names
        }

        # Convert scalar events to a simple dictionary
        events_dict = {
            k: self._eventslist_to_dict(v)
            for k, v in scalar_events.items()
        }
        return events_dict

    def get_events_dict(self, run_name, scalar_name):
        assert self._emux is not None
        events_dict = self._eventslist_to_dict(self._emux.Scalars(
            run_name,
            scalar_name
        ))
        return events_dict

    def _get_events(self):
        """ Get events fpaths from dpath and map them to run names
        """
        fpaths = [
            fp for fp in ls_r(self.dpath)
            if os.path.split(fp)[-1].startswith('events.out.tfevents')
        ]

        # Map from run name to full filepath
        event_map = {
            os.path.split(dpath)[-1]: fpaths[i]
            for i, (dpath, fpath) in enumerate(map(os.path.split, fpaths))
        }
        return event_map

    def _scalar_names_for(self, run_name):
        """ Scalar names for a given run
        """
        assert self._emux is not None
        return self._emux.Runs()[run_name]['scalars']

    def _eventslist_to_dict(self, eventslist):
        """ Converts a list of tensorboard ScalarEvents to a dictionary
        """
        d = {'wall_time': [],
             'step': [],
             'value': []}

        for i, event in enumerate(eventslist):
            d['wall_time'].append(event.wall_time)
            d['step'].append(event.step)
            d['value'].append(event.value)

        return d

    @property
    def dpath(self):
        return self._dpath

    @dpath.setter
    def dpath(self, dpath):
        self._dpath = realpath(dpath)

    def __repr__(self):
        s = self.__class__.__name__
        s += ': '
        s += self.dpath if self.dpath is not None else '*Uninitialized*'
        return s
