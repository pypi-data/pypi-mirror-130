#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.generic.entity.model import Entity
from labstep.service.helpers import getTime
from labstep.constants import UNSPECIFIED


class Collection(Entity):
    """
    Represents a Collection on Labstep.

    To see all attributes of a collection run
    ::
        print(my_collection)

    Specific attributes can be accessed via dot notation like so...
    ::
        print(my_collection.name)
        print(my_collection.id)
    """

    __entityName__ = "folder"
    __hasParentGroup__ = True

    def edit(self, name=UNSPECIFIED, extraParams={}):
        """
        Edit the name of an existing Collection.

        Parameters
        ----------
        name (str)
            The new name of the Collection.

        Returns
        -------
        :class:`~labstep.entities.collection.model.Collection`
            An object representing the edited Collection.

        Example
        -------
        ::

            # Get all collections, since there is no function
            # to get one collection.
            collections = user.getCollections()

            # Select the collection by using python index.
            collections[1].edit(name='A New Collection Name')
        """
        import labstep.entities.collection.repository as collectionRepository

        return collectionRepository.editCollection(self, name, extraParams=extraParams)

    def delete(self):
        """
        Delete an existing collection.

        Parameters
        ----------
        collection (obj)
            The collection to delete.

        Returns
        -------
        collection
            An object representing the collection to delete.
        """
        return self.edit(extraParams={"deleted_at": getTime()})
