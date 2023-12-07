# Struckture

## defenitions 
### Articles
An Article is everything that is Movable and can be stored witch includes things like Containers with it self can Store things.

Every Article needs a Name witch is free to set and a Code witch gets generated on creating the Article and is the unique identifier.

Every Article has a Calendar witch is used to track the availability of the Article and to reserve it for Events.

The Admin can create different Article Types witch can have different Fields.


### Storages
Every Place were a Article can be stored is a Storage things like racks, rooms, houses, shelfs, ...

Every Storage has a Name witch is free to set, a Code witch gets generated on creating the Storage the Code is a unique identifier, a Parent Storage or a location witch Builds a Tree like structure witch can look like this:
- Location 1
    - House
        - Room 1
            - Rack 1
            - shelf 1
                - board 1
                    - Compartment 1
                    - ...
                - ...
            - shelf 2
                - shelf 3
            - ...
        - ...
    - ...
- Location 2
- ...

Every Storage can be the Parent of another so if you want to put a House in a Room you can do it and it's fine.

The Admin can create different Storage Types witch can have different Fields.


### Locations
a location is a Real place on Earth at least as long this system is not used in space :D.
