#!/bin/bash
#
# Script that makes changes in preparation of a new release, such as updating
# the version and documentation.

EXIT_FAILURE=1;
EXIT_SUCCESS=0;

VERSION=`date -u +"%Y%m%d"`
DPKG_DATE=`date -R`

# Update the Python module version.
sed "s/__version__ = '[0-9]*'/__version__ = '${VERSION}'/" -i dfwinreg/__init__.py

# Update the version in the dpkg configuration files.
cat > config/dpkg/changelog << EOT
dfwinreg (${VERSION}-1) unstable; urgency=low

  * Auto-generated

 -- Log2Timeline maintainers <log2timeline-maintainers@googlegroups.com>  ${DPKG_DATE}
EOT

# Regenerate the API documentation.
tox -edocs

exit ${EXIT_SUCCESS};

