## TODOS

<!-- - error handling -->
<!-- - check passing parameters for OCRing, specicially language -->
<!-- - test with language for sync endpoint !! -->
<!-- - autoformatter -->
<!-- - info endpoint respond with languages available -->
<!-- - update README!!!! -->
<!-- - why still docker_volumes has xml dir ? -->
<!-- - test with a wider variety of PDFs -->
<!-- - be able to use external Redis -->
<!-- - `upload` route is returning `task registered` which is NOT true, should be something like `upload accepted` -->
<!-- - README code does not include import RedisSMQ -->
<!-- - setup production environment with auto restart ? -->
<!-- - make sure logs work -->

- cleanup (delete) downloaded PDF files?
- change the PORT number default in order to be able to be installed along-side our other services in the same machine. Should we have a pattern for future services?
- make sure tests use config for testing redis container
- make sure works on mac
- setup_venv needs to stop on error to avoid insalling local packages
- Nice to have: allow upping the service without redis if you only want to use the sync method
