### cs107-FinalProject
## GROUP #4

#Team Member
- ShangShang Wang
- Max Urbany
- Meghna Banerjee
- Mingcheng(Jason) Liu

[![codecov](https://codecov.io/gh/cs107-fantastic4/cs107-FinalProject/branch/main/graph/badge.svg?token=8L1HTFH7DC)](https://codecov.io/gh/cs107-fantastic4/cs107-FinalProject)

[![Build Status](https://app.travis-ci.com/cs107-fantastic4/cs107-FinalProject.svg?token=hCPptEMssAc5ih8ePZmo&branch=main)](https://app.travis-ci.com/cs107-fantastic4/cs107-FinalProject)

The current coverage for the dual.py and ad.py is above 90%. We will need to use the runtests.sh bash script to run the test. We have the following result:
![test result](https://github.com/cs107-fantastic4/cs107-FinalProject/blob/Final-markdown/docs/images/tests_result.jpeg?raw=true)



We use the following way to run our tests:
- Step 1
	Download the test code from github
	The test web link: https://github.com/cs107-fantastic4/cs107-FinalProject/tree/main/src/tests
	
        git clone https://github.com/cs107-fantastic4/cs107-FinalProject.git

- Step 2

	cd src

- Step 3

    -pip install pytest-cov


    -bash run_tests.sh pytest --cov-report term-missing --cov=. tests/


	This will run the pytests and return the number of tests that we passed. We can also use the following command to see the actual coverage:
		
	-bash run_tests.sh pytest --cov-report term-missing --cov=.tests/

### Broader Impact and Inclusivity Statement

	As a team, we believe in building libraries and products that help others equitably 
    and equip them
    with tools to solve complex problems. The goal of software engineering tools 
    is to improve human productivity and wrap complex problems in a usable, black box.

	We hope that our package takes away the complexity of having a deep understanding of implementing and extracting derivatives, 
    and the user can just directly call our functions to get computed values. Since python is a user-friendly language, we hope that those who are taking introductory 
    courses in either programming or calculus will be able to use it to solve complex problems much more efficiently. 
    The first step we have taken to make our product more inclusive is to publish it in PyPi so anyone who installs our library can use it.

	Our team comprises people from different backgrounds, different cultures, different countries and different genders. 
    This is why inclusivity and usability of our product by a wide range of people from different walks of life is important to us.

	However, our package does expect a certain depth of familiarity with introductory programming in Python and multivariable calculus. 
    It also assumes familiarity with the English language as the user goes through our documentation. To combat these challenges,
    the next steps would be to: (1) build some form of UI interface for our product (mobile app, web app), (2) write documentation in different languages 
    (including support for text-to-speech for users struggling with vision processing), (3) links to introductory python tutorials, 
    (4) links to introductory Calculus tutorials and (5) provide support in different programming languages.

	We hope that our package will be used to solve different problems in computer science, mathematics, engineering, chemistry and physics. 