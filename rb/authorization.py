__author__ = 'Hans Hoerberg'
import json
import re

class DeclarativeAuth:
    """
        The class handles declarative authorizations on strings.

        The class takes a JSON file that must have a specific structure. Read more in README.txt.


    """
    #Contains the singleton
    _instance = None

    #Dictionary key in the JSON file for all roles.
    CONST_ROLES = "roles"
    #Dictionary key in the JSON file for the roles a user posses.
    CONST_USERROLES = "userroles"
    #Dictionary key in the JSON file for all the rules."
    CONST_MATCHRULES = "matchrules"
    CONST_ALL = "*"

    def __init__(self, authSetupFile=None):
        """
        Will initialize the declarative authorization from a json file.
        :param authSetupFile:
        """
        self.authSetup = None
        if authSetupFile is not None:
            with open(authSetupFile) as fileData:
                try:
                    self.authSetup = json.load(fileData)
                except:
                    print "Not a correct JSON syntax!"
                print self.authSetup



    @staticmethod
    def getInstance(authSetupFile=None):
        """
        Get the instance for the class.
        It should only exist one instance for the authorization.


        :rtype : DeclartiveAuth object
        :return:
        """
        if not DeclarativeAuth._instance:
            DeclarativeAuth._instance = DeclarativeAuth(authSetupFile)
        return DeclarativeAuth._instance

    def classId(self):
        """
        Will return the id for the class.

        :rtype : integer
        :return: The id for the class.
        """
        return id(self)

    @staticmethod
    def findKeyInList(list, key):
        """
        Help class that searches for a key in a list with dictionaries.
        If the key exists in one dictionary the methods returns true, otherwise false.
        :rtype : bool
        :param list: A list with dictionaries.
        :param key: A string key.
        :return: True if the key exists, otherwise false.
        """
        return DeclarativeAuth.findItemInList(list, key) is not None

    @staticmethod
    def findItemInList(list, key):
        """
        Help class that searches for a key in a list with dictionaries.
        If the key exists in one dictionary the methods returns the dictionary that contains the key, otherwise none.

        :rtype : dict
        :param list: A list with dictionaries.
        :param key: A string key.
        :return: The first dict that contains the key, otherwise None.
        """
        for item in list:
            if key in item:
                return item
        return None


    @staticmethod
    def matchRoles(roleMaster, roleMatch):
        """
        Matches two roles with each other.

        :rtype: bool
        :param roleMaster: The role to be match.
        :param roleMatch: The role to match.
        :return: True if the two roles match eachother, otherwise false.
        """
        try:
            masterKey = roleMaster.keys()[0]
            roleKey = roleMatch.keys()[0]
            if masterKey != roleKey:
                return False
            masterSubRules = roleMaster[masterKey]
            roleSubRules = roleMatch[masterKey]
            if len(roleSubRules) == 1 and roleSubRules[0] == DeclarativeAuth.CONST_ALL:
                return True
            if len(masterSubRules) == 1 and masterSubRules[0] == DeclarativeAuth.CONST_ALL:
                return True
            for subRule in roleSubRules:
                if subRule not in masterSubRules:
                    return False
            return True
        except:
            return False

    def userExists(self, user):
        """
        Verifies if a user exists.

        :rtype : bool
        :param user: A unique user.
        :return: True if the user exists, otherwise false.
        """
        if self.authSetup is None:
            return False
        try:
            return self.findKeyInList(self.authSetup[self.CONST_USERROLES], user)
        except KeyError:
            pass
        return False

    def roleExists(self, role):
        """
        Verifies if a role exists.

        :rtype : bool
        :param role: A unique role.
        :return: True if the role exists, otherwise false.
        """
        if self.authSetup is None:
            return False
        try:
            if self.findKeyInList(self.authSetup[DeclarativeAuth.CONST_ROLES], role.keys()[0]):
                return self.matchRoles(
                    self.findItemInList(self.authSetup[self.CONST_ROLES], role.keys()[0]),
                    role)
        except KeyError:
            pass
        return False

    def ruleExists(self, rule):
        """
        Verifies if a rule exists.

        :rtype : bool
        :param role: A unique rule.
        :return: True if the rule exists, otherwise false.
        """
        if self.authSetup is None:
            return False
        try:
            return self.findKeyInList(self.authSetup[self.CONST_MATCHRULES], rule)
        except KeyError:
            pass
        return False

    def userInRole(self, user, role):
        """
        Verifies if a user is in specific role.

        :rtype: bool
        :param user: The user
        :param role: The role
        :return: True if the user have the given role.
        """
        if self.userExists(user):
            if self.roleExists(role):
                userRoles = self.findItemInList(self.authSetup[self.CONST_USERROLES], user)[user]
                for userRole in userRoles:
                    if self.matchRoles(role, userRole):
                        return True
        return False

    def userMatchRule(self, rule, user):
        """


        :rtype : bool
        :param rule:
        :param user:
        :return:
        """
        ruleOK = True
        for tmprule in self.authSetup[self.CONST_MATCHRULES]:
            ruleKey = tmprule.keys()[0]
            if re.match(ruleKey,rule): #.replace("*",".*")
                ruleOK = False
                if self.ruleExists(ruleKey):
                    ruleRoles = self.findItemInList(self.authSetup[self.CONST_MATCHRULES], ruleKey)
                    if len(ruleRoles) == 0:
                        ruleOK = True
                    else:
                        userRoles = self.findItemInList(self.authSetup[self.CONST_USERROLES], user)[user]
                        for ruleRole in ruleRoles[ruleKey]:
                            for userRole in userRoles:
                                if self.matchRoles(ruleRole, userRole):
                                    ruleOK = True
            if ruleOK == False:
                return False
        return ruleOK