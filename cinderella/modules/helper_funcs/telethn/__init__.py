from cinderella import (DEV_USERS, SUDO_USERS, telethn)

IMMUNE_USERS = SUDO_USERS + DEV_USERS

IMMUNE_USERS = list(SUDO_USERS) + list(DEV_USERS)
