from typing import Any
from typing import Dict

import dict_tools.update


async def unlock(hub, profiles: Dict[str, Dict[str, Any]], backend_key: str = None):
    """
    Read the raw profiles and search for externally defined profiles.
    """
    # Allow custom specification of a backend key per acct_file
    if backend_key is None:
        backend_key = profiles.get("backend_key", hub.acct.BACKEND_KEY)

    ret = {}
    for backend, backend_profile_data in profiles.get(backend_key, {}).items():
        if backend not in hub.acct.backend:
            hub.log.error(f"acct backend '{backend}' is not available")
            continue
        # The keys are irrelevant for backend profiles
        for ctx in backend_profile_data.values():
            try:
                hub.log.info(f"Reading acct backend profiles from '{backend}'")
                backend_profiles = hub.acct.backend[backend].unlock(**ctx)
                backend_profiles = await hub.pop.loop.unwrap(backend_profiles)

                # If an acct-backend specifies other backends, then recursively load them onto the same space
                if backend_key in backend_profiles:
                    dict_tools.update.update(
                        ret, await hub.acct.backend.init.unlock(backend_profiles)
                    )
                else:
                    ret[backend] = backend_profiles
            except Exception as e:
                hub.log.error(f"{e.__class__}: {e}")

    return ret
