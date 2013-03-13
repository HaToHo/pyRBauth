===========
Declarative authorization with pyRBauth
===========
Declarative authorization to protect resources with string representations.

A string representation can be an URL, but do not have to be.

The declarations is perform in a JSON structure and is contained in a file.

How to use
---------------------------
    First get a new instance of the class with the singleton pattern.

    dAuth = DeclarativeAuth.getInstance("./myFileName.json")

    You may also create a instance without using the singleton pattern if you like it better:
    dAuth =  DeclarativeAuth("./myFileName.json")

    The singleton pattern is prefered since you do not have read the configuration file every time
    you need a new instance.

    You can verify if a user is in a specific role:
    dAuth.userInRole("user1", {"rolename3": ["*"]})

    You can verify is a user is allowed access to a resource:
    dAuth.userMatchRule("/exact","user1")


Description of JSON file
---------------------------
You may use any name for the JSON file, but should use the file ending .json.


This is an example of the JSON file:
{
   "roles":
            [
                {"rolename1":["subrole1","subrole2"]},
                {"rolename2":["subrole1","subrole2"]},
                {"rolename3":[]}
            ],
    "userroles":
            [
                {"user1":[{"rolename1":["*"]},{"rolename2":["*"]},{"rolename3":["*"]}]},
                {"user2":[{"rolename2":["subrole1"]},{"rolename3":["*"]}]},
            ],
    "matchrules":
        [
            {".*":[{"rolename3":["*"]}]},
            {"/somestring.*":[{"rolename1":["*"]}]},
            {"/startstring/.*/endstring":[{"rolename1":["*"]},{"rolename2":["subrole1"]}]},
            {"/exact":[{"rolename1":["*"]},{"rolename2":["*"]}]}
        ]
}

The keys "roles", "userroles" and "matchrules" are mandatory. If you want to change them the constants
 CONST_ROLES, CONST_USERROLES and CONST_MATCRULES must be changes.

The roles are given arbitrary names and subrole names. Each role consists of main role and its subroles.
Each role should have a unique name, since the code only searches for the first role match.
Non unique role names can give a non consistent behaviour.
The subroles should be unique within the same list, but can be non unique between lists.

Users are the keys in userroles and each user have a list of roles.
Each user should be unique, since the code only searches for the first match.
Non unique users can give a non consistent behaviour.

The roles for a user may not be an exact match with the roles give in the roles dictionary.

For example a user can have all the given subroles for a role, instead of adding all roles use the * symbol.
{"rolename1":["*"]} is equal to {"rolename1":["subrole1","subrole2"]}

A user may also only have only some of the subroles. In this case the user is not authorized to use any
resorces protected by rolname2 and subrole2.
{"rolename2":["subrole1"]}

In the case of rolename3 that do not contains any subroles, should be added to the user as:
{"rolename3":["*"]}

Roles are the connected to rules in the matchrule dictionary.
The key in the dictionary is the rule to be matched. The rule is an regual expression that will match
the string to be protected with re.match.

In the example above the .* is used to represent any characters.

The rule {".*":[{"user":["*"]}]} says that the user must have the role rolename3 to access any resource.

The rule {"/somestring.*":[{"rolename1":["*"]}]}, says that the user must have the role rolename1
with at least one subrole to access the resource that starts with /somstring.

The rule {"/startstring/.*/endstring":[{"rolename1":["*"]},{"rolename2":["subrole1"]}]},
says that the user must have the role rolename1 with at least one subrole or
 have the role rolename2 with the subrole1 to access the resource that starts with /startstring/
 and ends with /endstring.

The rule {"/exact":[{"rolename1":["*"]},{"rolename2":["*"]}]}, says that the user must have the role rolename1
with at least one subrole or rolename2 with at least one subrole to access the resource /exact.

All matched rules must be true for the user to access the resource.

So if a user may access /somestring.* but the user do not have access to .*, then the access to /somestring.*
will be denied since both rules apply.

Example
---------------------------
You can se an example of how the authorization is used in the test folder.

