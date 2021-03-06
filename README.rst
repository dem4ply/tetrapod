================
how to run tests
================

to run the test you can use the `make` command

.. code-block:: shell

	# run all unit test
	make test
	# for run pep8 and flake
	make style_test
	# or you can use
	make pep8; make flakes

to open the coverage report you can use

.. code-block:: shell

	make open_report_firefox
	# or
	firefox .coverage_html_report/index.html


=============
configuration
=============

***
BGC
***

.. code-block:: python

	from tetrapod.bgc import connections
	connections.configure(
		default={
			'host': (
					'https://direct2m.backgroundchecks.com/'
					'integration/bgcdirectpost.aspx' ),
			'user': os.environ[ 'BGC__DEFAULT__USER' ],
			'password': os.environ[ 'BGC__DEFAULT__PASSWORD' ],
			'account': os.environ[ 'BGC__DEFAULT__ACCOUNT' ],
		 },
		another={
			'host': (
					'https://direct2m.backgroundchecks.com/'
					'integration/bgcdirectpost.aspx' ),
			'user': os.environ[ 'BGC__ANOTHER__USER' ],
			'password': os.environ[ 'BGC__ANOTHER__PASSWORD' ],
			'account': os.environ[ 'BGC__ANOTHER__ACCOUNT' ],
		},
		with_proxy={
			'host': (
					'https://direct2m.backgroundchecks.com/'
					'integration/bgcdirectpost.aspx' ),
			'user': os.environ[ 'BGC__WITH_PROXY__USER' ],
			'password': os.environ[ 'BGC__WITH_PROXY__PASSWORD' ],
			'account': os.environ[ 'BGC__WITH_PROXY__ACCOUNT' ],
			'proxy': {
				'http': os.environ[ 'BGC__WITH_PROXY__PROXY__HTTP' ],
				'https': os.environ[ 'BGC__WITH_PROXY__PROXY__HTTPS' ],
			},
		},
	)


==========
how to use
==========

***
bgc
***

us_one_validate
===============

.. code-block:: python

	from tetrapod.bgc import bgc
	result = bgc.us_one_validate( ssn='899999914' )

the result is a dict and have the next structure

.. code-block:: python

	{'order_id': '6421064b-0c45-4fb4-ad52-1bd9edfbf034', 'order': {'ssn': 'XXXXX9914'}, 'is_deceased': True, 'is_valid': True, 'state_issued': None, 'text_response': 'This SSN may have been issued as part of the Social Security Administration (SSA) Randomization Program that limits our ability to provide the issuance state and dates.  Please direct the subject to the SSA to validate authenticity.', 'year_issued': None}

us_one_trace
============

.. code-block:: python

	from tetrapod.bgc import bgc
	result = bgc.us_one_trace(
		ssn='999999999', first_name='jonh', last_name='doe' )

the result is a dict with the next structure

.. code-block:: python

	{'order_id': '559be3d7-4019-4af7-9714-723077890856', 'order': {'ssn': 'XXXXX9999', 'last_name': 'doe', 'first_name': 'jonh'}, 'records': [{'street': {'number': '123', 'pre_direction': None, 'name': 'Qa St', 'post_direction': None, 'suffix': 'QA'}, 'first_name': 'jonh', 'middle_name': None, 'last_name': 'doe', 'city': None, 'state': None, 'county': None, 'postal_code': None, 'postal_code4': None, 'date_first_seen__raw': {'year': '2009', 'month': '1'}, 'date_first_seen': datetime.date(2009, 1, 1), 'date_last_seen__raw': {'year': '2012', 'month': '12'}, 'date_last_seen': datetime.date(2012, 12, 1), 'verified': False, 'phone_info': None}]}
