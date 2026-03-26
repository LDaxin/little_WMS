# Struckture

## Defenitions 
### Articles
- An article is everything that is movable and can be stored. This includes things like containers, which themselves can be a storage for other things.
- An article needs a name and a [UUID](https://de.wikipedia.org/wiki/Universally_Unique_Identifier)-code. The UUID gets automatically generated while creating an article and acts as the unique identifier.
- Every article has a calendar which is used to track the availability of the article and to reserve it for events.
- The Admin can create different types of articlesles which can have different data fields.


### Storages
- Everything where an article can be stored is a storage (think about things like racks, rooms, houses, shelfs ...)
- Every Storage has a name and a UUID that gets automatically generated during the creation of the storage
- Any storage can have a parent storage that it is located in. Also, any storage can be the parent storage to another storage. This builds a tree-like structure of storages which can look like this:
```
- Location 1
    - Blue House
        - Kitchen
            - Rack 1
            - shelf 1
                - board 1
                    - Compartment 1
                    - ...
                - ...
            - shelf 2
                - shelf 3
            - ...
        - Living room
        - ...
    - Red House
    - ...
- Location 2
- ...
```
- The admin can create different storage types which can have different data fields.


### Locations
- A location is a real place on earth (at least as long this system is not used in space)