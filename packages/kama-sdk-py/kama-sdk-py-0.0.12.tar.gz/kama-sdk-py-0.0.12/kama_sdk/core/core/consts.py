static_server_ktea = 'server'
managed_server_ktea = 'managed_server'
local_exec_ktea = 'local_executable'
virtual_ktea = 'virtual_ktea'

ASSETS_PREFIX = "assets"
SUPPLIER_PREFIX = "get"

pos = 'positive'
neg = 'negative'
skp = 'skipped'
rng = 'running'
brk = 'broken'
err = 'error'
idl = 'idle'

app_space = 'app'

app_statuses = [
  pos, neg, rng, brk, idl
]

TARGET_STANDARD = 'standard'
TARGET_INLIN = 'inline'
TARGET_STATE = 'state'
TARGET_PREFS = 'prefs'

TARGET_TYPES = [TARGET_STANDARD, TARGET_INLIN, TARGET_STATE, TARGET_PREFS]
DEFAULT_TARGET = TARGET_STANDARD

MAIN_WORKER = 'default'
TELEM_WORKER = 'telem'


statuses = [pos, neg, rng, idl]
