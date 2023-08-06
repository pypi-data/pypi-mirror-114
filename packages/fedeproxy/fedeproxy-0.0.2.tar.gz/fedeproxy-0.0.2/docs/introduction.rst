Introduction
============

Fedeproxy

Hacking
=======

* direnv allow .
* pip install pipenv
* pipenv install --dev
* pre-commit install
* tests/setup-gitlab.sh

Release management
==================

* Prepare the release notes

* Prepare a new version

.. code:: sh

 $ version=1.3.0
 $ perl -pi -e "s/^version.*/version = $version/" setup.cfg
 $ for i in 1 2 ; do
       python setup.py sdist
       amend=$(git log -1 --oneline | grep --quiet "version $version" && echo --amend)
       git commit $amend -m "version $version" ChangeLog setup.cfg
       git tag -a -f -m "version $version" $version
   done
 $ git push ; git push --tags
 $ twine upload -s --username fedeproxy --password "$FEDEPROXY_PYPI_PASSWORD" dist/fedeproxy-$version.tar.gz
