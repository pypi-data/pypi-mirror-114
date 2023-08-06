#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A undo update, which removes the most recent step from
the sheet. 
"""

from copy import copy


UNDO_EVENT = 'undo'
UNDO_PARAMS = []

def execute_undo_update(steps_manager):
    """
    The function responsible for updating the widget state container
    by removing the most recent step.

    If there is no most recent step, does nothing.
    """

    if len(steps_manager.steps) == 1:
        return 

    # Pop off the last element
    new_steps = copy(steps_manager.steps)
    new_steps.pop()

    steps_manager.execute_and_update_steps(new_steps)


"""
This object wraps all the information
that is needed for a undo step!
"""
UNDO_UPDATE = {
    'event_type': UNDO_EVENT,
    'params': UNDO_PARAMS,
    'execute': execute_undo_update
}





